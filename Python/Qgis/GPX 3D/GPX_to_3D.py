# A little App to get elevation from a Track grom a GPX or KML track.
# Uses information of Instituto Geografico Nacional de España trough WCS service.
# Is make with QGis libraries
# KML and GPX are generate in a rudimentary but effetive way, and with full control

import os,time


from qgis.core import QgsProject,QgsApplication,QgsVectorLayer,QgsRasterLayer,QgsRaster,QgsFeature,QgsDistanceArea,QgsLayerTreeModel,QgsSymbolLayerRegistry,QgsSymbol,QgsSingleSymbolRenderer
from qgis.gui import QgsLayerTreeMapCanvasBridge,QgsLayerTreeView,QgsMapToolPan,QgsMapToolZoom,QgsMapCanvas

from qgis.PyQt.QtCore import (Qt,QRect,QDateTime)
from qgis.PyQt.QtWidgets import(QApplication,QDialog,QVBoxLayout,QHBoxLayout,QPushButton,QSplitter,QWidget,QFileDialog,QTextEdit,QLabel,QComboBox)
from qgis.PyQt.QtGui import (QIcon,QPixmap,QFont,QPixmap,QColor)

class gpx_to_3d(QDialog):

    # Open Qgis Aplication, for using his function
    # I think there is a better way to start, but by the moment I don't know how    
    QgsApplication.setPrefixPath('/usr', True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    
    # Initialize window and create Graphic User Interface
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("GPX TO 3D")
        
        # File to show in map
        self.Output_KML_File='C:/Roberto/Visual_Studio_Code/Sharing_Little_Things/Python/Qgis/GPX 3D/2019_E6_V8.gpx'
        self.Output_KML_File='C:/Roberto/Visual_Studio_Code/Sharing_Little_Things/Python/Qgis/GPX 3D/2019_E6_V8_3D.kml'
        #self.Output_KML_File=None
        self.initGui()
        
    def select_file(self):
        # User select the file to converter and start convertion
        filename,_ = QFileDialog.getOpenFileName(self, 'Select GPX File / Selecciona Fichero GPX',os.path.dirname(__file__) , 'TRACK (*.gpx *.kml)')
        if filename:
            # Start convertion
            self.convert_track(filename) 
            
            # Create a Profile
            self.profile()
            
            # Open Map
            map=see_map(self.Output_KML_File)
            map.exec_()
            self.info('Finished / Finalizado')
    
    def convert_track(self,filename):
        self.file_name=filename
        if self.file_name[-3:]=='gpx':
            # Set parameters to load file like a layer. Get track like a points, not a line
            uri = self.file_name+"|layername=track_points"
            # Load Layer with points of track gpx o line KML
            self.points = QgsVectorLayer(uri, "Original Points", "ogr")
            # Check if load is correct
            if not self.points.isValid():
                self.info("Track failed to load! /n"+filename)
            else:
                self.info("Track Load Correct! "+filename)
                
        elif self.file_name[-3:]=='kml':
            uri = self.file_name
            # Set parameters to load file like a layer. Get track like a line
            # Load Layer with points of track gpx o line KML
            lines = QgsVectorLayer(uri, "Original Line", "ogr")
            # Check if load is correct
            if not lines.isValid():
                self.info("Track failed to load! /n"+filename)
            else:
                self.info("Track Load Correct! "+filename)

            # KML is a line convert line in points
            for line in lines.getFeatures():
                # Create a layer for points in memory
                self.points = QgsVectorLayer("Point?crs=epsg:4326&index=yes", "Original Points", "memory")
                features=[]
                for vertex in line.geometry().vertices():
                    feature=QgsFeature()
                    feature.setGeometry(vertex)
                    features.append(feature)
                    
                self.points.dataProvider().addFeatures(features)


        # Set parameters to load the Digital Elevation Model of IGN
        if self.comboBox.currentIndex()==3:
            uri="dpiMode=7&identifier=mdt:Elevacion4258_1000&url=http://www.ign.es/wcs/mdt"
        elif self.comboBox.currentIndex()==2:
            uri="dpiMode=7&identifier=mdt:Elevacion4258_500&url=http://www.ign.es/wcs/mdt"
        elif self.comboBox.currentIndex()==1:
            uri="dpiMode=7&identifier=mdt:Elevacion4258_200&url=http://www.ign.es/wcs/mdt"
        else:
            uri="dpiMode=7&identifier=mdt:Elevacion4258_25&url=http://www.ign.es/wcs/mdt"
        DEM  = QgsRasterLayer(uri, 'my wcs layer', 'wcs')
        if not DEM.isValid():
            self.info("DEM failed to load!")
        else:
            self.info("DEM Load Correct!") 
            
        # For calculate distance between points
        d = QgsDistanceArea()
        d.setEllipsoid('WGS84')
        point_origin=0
            
        # For make profile
        self.all_coord_m=[]
        self.all_coord_z=[]
        self.ymax=0
        
        # Start to create KML file (firts lines of file)
        self.start_creation_kml()
        
        # Start to create GPX file (firts lines of file)
        self.start_creation_gpx()
        
        # For put time in points of track
        self.track_day=QDateTime.currentDateTime()
        
        # For each point in the track, analize information
        for point in self.points.getFeatures():
            # Get Geometry of feature like a point
            geompt = point.geometry().asPoint()
            # Find this point in DEM and return his elevation
            elevation = DEM.dataProvider().identify(geompt, QgsRaster.IdentifyFormatValue).results()
            
            #print (elevation[1],point['ele'])
            # Get Value of original point (y - Latitude, x - Longitude)
            self.coor_x=geompt.x()
            self.coor_y=geompt.y()
            if len(elevation)>0:
                # Set value of elevation like coordinate Z
                self.coor_z=elevation[1]
            else:
                self.info('Point '+str(self.coor_y)+" / "+str(self.coor_x)+" Not Found / No encontrado")
                self.coor_z=0
            
            # Calculate lenght of track
            if not point_origin==0:
                self.distance=d.measureLine(point_origin, geompt)
                self.coor_m+=(self.distance/1000) # Distance in km
                point_origin=geompt
            else:
                self.coor_m=0
                self.distance=0
                point_origin=geompt
            
            # Maxium Hight for profile
            if self.ymax<self.coor_z:
                self.ymax=self.coor_z
            # Acumulate points (distance / Elevation) for make profile
            self.all_coord_m.append(self.coor_m)
            self.all_coord_z.append(self.coor_z)
            
            # Put a time in points    
            if self.file_name[-3:]=='kml':
                self.track_day=self.track_day.addSecs(1)
            else:    
                if point['time']==None:
                    # If track hase no time add 1 second to previous time
                    self.track_day=self.track_day.addSecs(1)
                else:
                    # Get point time from track
                    self.track_day=point['time']

            # Add point in the new kml file
            self.add_points_kml()
            
            # Add point in the new GPX file
            self.add_points_gpx()
        
        # Close and write finish of kml file
        self.finish_kml()
        
        # Close and write finish of gpx file
        self.finish_gpx()

    def start_creation_kml(self):
        # Write head lines of kml file
        self.Output_KML_File=self.file_name[:-4]+'_3D.kml'
        self.file_kml=open(self.Output_KML_File, 'w')
        color_dic={'Rojo':'ff0000ff','Verde':'ff00ff00','Azul':'ffff0000','Morado':'ff800080','Amarillo':'ff00ffff','Rosado':'ffff00ff','Naranja':'ff0080ff','Marrón':'ff336699'}
        color=['ff0000ff','ff00ff00','ffff0000','ff800080','ff00ffff','ffff00ff','ff0080ff','ff336699']
        self.file_kml.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        self.file_kml.write("<kml xmlns='http://www.opengis.net/kml/2.2' xmlns:gx='http://www.google.com/kml/ext/2.2' xmlns:kml='http://www.opengis.net/kml/2.2' xmlns:atom='http://www.w3.org/2005/Atom'>\n")
        self.file_kml.write("<Document>\n")
        self.file_kml.write("   <name>" + self.Output_KML_File +"</name>\n")
        self.file_kml.write("   <Placemark>\n")
        self.file_kml.write("       <name>" + os.path.basename(self.Output_KML_File) + "</name>\n")
        self.file_kml.write("       <description>" + os.path.basename(self.Output_KML_File) + "</description>\n")
        self.file_kml.write("	<Style>\n")
        self.file_kml.write("		<LineStyle>\n")
        self.file_kml.write("			<color>"+color[0]+"</color>\n")
        self.file_kml.write("			<width>4</width>\n")
        self.file_kml.write("		</LineStyle>\n")
        self.file_kml.write("	</Style>\n")
        self.file_kml.write("       <LineString>\n")
        self.file_kml.write("           <coordinates>")

    def add_points_kml(self):
        self.file_kml.write(str(self.coor_x)+","+str(self.coor_y)+","+str(self.coor_z)+" ")     
    
    def finish_kml(self):
        # Write foot lines, write and close kml file
        self.file_kml.write("           </coordinates>\n")
        self.file_kml.write("       </LineString>\n")
        self.file_kml.write("   </Placemark>\n")
        self.file_kml.write("</Document>\n")
        self.file_kml.write("</kml>\n")
        self.file_kml.close()
        self.info(self.Output_KML_File)
            
    def start_creation_gpx(self):
        # Write head lines of gpx file
        self.Output_GPX_File=self.file_name[:-4]+'_3D.gpx'
        self.file_gpx=open(self.Output_GPX_File, 'w')

        self.file_gpx.write('''<?xml version="1.0"?>\n''')
        self.file_gpx.write('''<gpx version="1.1" creator="GDAL 3.0.4" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n''')
        self.file_gpx.write("  <trk>\n")
        self.file_gpx.write("    <name>"+os.path.basename(self.Output_GPX_File)+"</name>\n")
        self.file_gpx.write("    <trkseg>\n")
        
    def add_points_gpx(self):
        # Add points in the GPX file
        self.file_gpx.write('      <trkpt lat="'+str(self.coor_y)+'" lon="'+str(self.coor_x)+'">\n')
        self.file_gpx.write("        <ele>"+str(self.coor_z)+"</ele>\n")
        self.file_gpx.write("      <time>"+self.track_day.toString('yyyy-MM-ddTHH:mm:ssZ')+"</time>\n")
        self.file_gpx.write("      </trkpt>\n")
 
    def finish_gpx(self):
        # Write foot lines, write and close kml file
        self.file_gpx.write("    </trkseg>\n")
        self.file_gpx.write("  </trk>\n")
        self.file_gpx.write("</gpx>\n")
        self.file_gpx.close()
        self.info(self.Output_GPX_File) 
 
    def profile(self):
        import matplotlib.pyplot as plt
        
        # Create Profile
        plt.xlim(right=self.coor_m) #xmax is your value
        plt.xlim(left=0) #xmin is your value
        plt.ylim(top=self.ymax*1.2) #ymax is your value
        plt.ylim(bottom=0) #ymin is your value
        plt.plot(self.all_coord_m,self.all_coord_z)
        plt.fill_between(self.all_coord_m, self.all_coord_z, facecolor='red', color='#539ecd')
        #pylab.fill_between(x, y, color='#539ecd')
        file_profile=self.file_name[:-3]+"jpg"
        plt.savefig(file_profile)
        plt.clf()  
        pixmap = QPixmap(file_profile)
        self.profile_jpg.setPixmap(pixmap)
        self.profile_jpg.setScaledContents(True)
        self.info(file_profile)      
        
    def info(self,message):
        # Show Information message in the screen and print in console
        print(message)
        self.message_box.append(message)

    def initGui(self):
        # Create Graphical User Interface
        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.dirname(__file__)+"/icon.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowFlags(Qt.Window
                    | Qt.WindowSystemMenuHint
                    | Qt.WindowMinimizeButtonHint
                    | Qt.WindowMaximizeButtonHint
                    | Qt.WindowCloseButtonHint)

        self.resize(520, 520)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(10, 20, 500, 20))
        font = QFont()
        font.setPointSize(14)
        font.setUnderline(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(10, 70, 500, 16))
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QRect(10, 90, 500, 16))
        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QRect(10, 110, 500, 16))
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QRect(50, 150, 121, 24))
        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(QRect(240, 150, 121, 24))
        self.comboBox.addItem("Paso Malla 25m")
        self.comboBox.addItem("Paso Malla 200m")
        self.comboBox.addItem("Paso Malla 500m")
        self.comboBox.addItem("Paso Malla 1.000m")
        self.bt_view_map = QPushButton(self)
        self.bt_view_map.setGeometry(QRect(370, 150, 121, 24))
        self.profile_jpg = QLabel(self)
        self.profile_jpg.setGeometry(QRect(20, 200, 480, 180))

        self.message_box = QTextEdit(self)
        self.message_box.setGeometry(QRect(10, 400, 500, 111))
        self.label.setText("KML / GPX TO 3D")
        self.label_2.setText("Convert a GPX file without elevation, in a GPX and KML with elevation. It's only for Spain.")
        self.label_3.setText("Convierte un GPX sin elevación, en un GPX y KML con elevación.")
        self.label_4.setText("Es solo para España ya que utiliza el servicio WCS del Instituto Geografico Nacional")
        self.pushButton.setText("File / Fichero")
        self.bt_view_map.setText("Map / Mapa")

        self.pushButton.clicked.connect(self.select_file)
        self.bt_view_map.clicked.connect(lambda: see_map(self.Output_KML_File).exec_())
        
class see_map(QDialog):
    #app2 = QgsApplication([], True)
    #app2.initQgis()
    def __init__(self,file_name):
        super().__init__()

        # Creación del Lienzo / Canvas
        self.canvas=QgsMapCanvas(self)
        self.setWindowTitle("Map of Track  /  Mapa del Recorrido")
        self.canvas.setCanvasColor(Qt.white)
         
        self.initGui()

        if not file_name==None:
            vlayer=QgsVectorLayer(file_name, "Track Converted", "ogr")
            #vlayer.updateExtents()
            self.project.instance().addMapLayer(vlayer) 
            vlayer.renderer().symbol().setWidth(2)
            vlayer.renderer().symbol().setColor(QColor.fromRgb(250,0,0))
            self.view.refreshLayerSymbology(vlayer.id())

            uri='crs=EPSG:4326&dpiMode=7&format=image/jpeg&layers=IGNBaseTodo&styles=default&tileMatrixSet=EPSG:4326&url=http://www.ign.es/wmts/ign-base'
            map_spain=QgsRasterLayer(uri, "Spain", "wms")
            self.root.insertLayer(1,map_spain) 
            self.project.instance().addMapLayer(map_spain) 
            if not map_spain.isValid():
                print("Track failed to load! /n"+file_name)
            else:
                print("Track Load Correct! "+file_name)
            
        else:
            uri='crs=EPSG:4326&dpiMode=7&format=image/jpeg&layers=IGNBaseTodo&styles=default&tileMatrixSet=EPSG:4326&url=http://www.ign.es/wmts/ign-base'
            map_spain=QgsRasterLayer(uri, "Spain", "wms")
            self.project.instance().addMapLayer(map_spain) 

            if not map_spain.isValid():
                print("Track failed to load! /n"+file_name)
            else:
                print("Track Load Correct! "+file_name)

           
    def zoomIn(self):
        self.canvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
        self.canvas.setMapTool(self.toolZoomOut)

    def pan(self):
        self.canvas.setMapTool(self.toolPan)

    def file(self):
        filename,_ = QFileDialog.getOpenFileName(self, 'Selecciona Fichero GPX','c:/', 'QGis (*.qgz)')
        if filename:
            self.project.read(filename)       

    def initGui(self):
        icon = QIcon()
        icon.addPixmap(QPixmap("C:/Roberto/Visual_Studio_Code/GisBike/programa/IMG/Qgis.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowFlags(Qt.Window
                    | Qt.WindowSystemMenuHint
                    | Qt.WindowMinimizeButtonHint
                    | Qt.WindowMaximizeButtonHint
                    | Qt.WindowCloseButtonHint)

        self.resize(1200,600)

        self.verticalLayout_2= QVBoxLayout(self)
        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Horizontal)

        self.actionZoomIn=QPushButton("Zoom in",self.splitter )
        self.actionZoomOut=QPushButton("Zoom out",self.splitter )
        self.actionPan=QPushButton("Pan",self.splitter )
        self.actionFile=QPushButton("File",self.splitter )
        
        self.project = QgsProject.instance() 
        self.project.read('C:/Users/Fcc/Desktop/QGis/pruebas2.qgz')   
        self.root = QgsProject.instance().layerTreeRoot()
        self.bridge = QgsLayerTreeMapCanvasBridge(self.root, self.canvas)
        
        self.bridge.setCanvasLayers()
        self.bridge.setAutoSetupOnFirstLayer(True)
        
        #https://gis.stackexchange.com/questions/141516/adding-legend-to-canvas-in-standalone-pyqgis-application
        self.model = QgsLayerTreeModel(self.root)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.model.setFlag(QgsLayerTreeModel.ShowLegend)
        self.view = QgsLayerTreeView(self.splitter)
        self.view.setModel(self.model)
        self.view.setFixedWidth(150)
        #self.view.resize(150,600)

        self.widget = QWidget(self.splitter)
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.actionZoomIn)
        self.horizontalLayout.addWidget(self.actionZoomOut)
        self.horizontalLayout.addWidget(self.actionPan)
        self.horizontalLayout.addWidget(self.actionFile)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout_2.addWidget(self.splitter)
   
        self.actionZoomIn.clicked.connect(self.zoomIn)
        self.actionZoomOut.clicked.connect(self.zoomOut)
        self.actionPan.clicked.connect(self.pan)
        self.actionFile.clicked.connect(self.file)

        # create the map tools
        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False) # false = in
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = out
 
if __name__ == "__main__":
    import sys
    # Start QT Aplicacition
    app = QApplication(sys.argv)
    
    # Set style of QT
    app.setStyle('Fusion')
    
    # Create Screen and Function Class
    window = gpx_to_3d()
    
    # Show Create Window
    window.show()
    
    # Loop program
    sys.exit(app.exec_())