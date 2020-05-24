"""
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
"""
# A little App to get elevation from a Track
# Uses information of Instituto Geografico Nacional de España trough WCS service.
# Is make with QGis libraries
# KML and GPX are generate in a rudimentary but effetive way, and with full control

import os,time
from qgis.core import QgsProject,QgsApplication,QgsVectorLayer,QgsRasterLayer,QgsRaster

from qgis.PyQt.QtCore import (Qt,QRect)
from qgis.PyQt.QtWidgets import(QApplication,QDialog,QVBoxLayout,QPushButton,QSplitter,QWidget,QFileDialog,QTextEdit,QLabel)
from qgis.PyQt.QtGui import (QIcon,QPixmap,QFont)


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
        self.initGui()
        
    def select_file(self):
        # User select the file to converter and start convertion
        filename,_ = QFileDialog.getOpenFileName(self, 'Select GPX File / Selecciona Fichero GPX',os.path.dirname(__file__) , 'GPX (*.gpx)')
        if filename:
            # Start convertion
            self.convert_track(filename) 
            self.info('Finished / Finalizado')
    
    def convert_track(self,filename):
        self.filename=filename
        # Set parameters to load file like a layer. Get track like a points, not a line
        uri = self.filename+"|layername=track_points"
        # Load Layer with points of track
        points = QgsVectorLayer(uri, "puntos_gpx_ori", "ogr")
        # Check if load is correct
        if not points.isValid():
            self.info("Track failed to load!")
        else:
            self.info("Track Load Correct!") 

        # Set parameters to load the Digital Elevation Model of IGN
        uri="dpiMode=7&identifier=mdt:Elevacion4258_1000&url=http://www.ign.es/wcs/mdt"
        uri="dpiMode=7&identifier=mdt:Elevacion4258_200&url=http://www.ign.es/wcs/mdt"
        uri="dpiMode=7&identifier=mdt:Elevacion4258_500&url=http://www.ign.es/wcs/mdt"
        uri="dpiMode=7&identifier=mdt:Elevacion4258_25&url=http://www.ign.es/wcs/mdt"
        DEM  = QgsRasterLayer(uri, 'my wcs layer', 'wcs')
        if not DEM.isValid():
            self.info("DEM failed to load!")
        else:
            self.info("DEM Load Correct!") 
        
        # Start to create KML file (firts lines of file)
        self.start_creation_kml()
        
        # Start to create GPX file (firts lines of file)
        self.start_creation_gpx()
        
        # For put time in points of track
        self.track_day=time.time()
        
        # For each point in the track, analize information
        for point in points.getFeatures():
            # Get Geometry of feature like a point
            geompt = point.geometry().asPoint()
            # Find this point in DEM and return his elevation
            elevation = DEM.dataProvider().identify(geompt, QgsRaster.IdentifyFormatValue).results()
            
            #print (elevation[1],point['ele'])
            # Get Value of original point (y - Latitude, x - Longitude)
            self.coor_x=geompt.x()
            self.coor_y=geompt.y()
            # Set value of elevation like coordinate Z
            self.coor_z=elevation[1]
            
            # Put a time in points
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
        self.Output_KML_File=self.filename[:-4]+'_3D.kml'
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
        self.Output_GPX_File=self.filename[:-4]+'_3D.gpx'
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

        self.resize(520, 320)

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
        self.pushButton.setGeometry(QRect(200, 150, 121, 24))
        self.message_box = QTextEdit(self)
        self.message_box.setGeometry(QRect(10, 200, 500, 111))
        self.label.setText("GPX TO 3D")
        self.label_2.setText("Convert a GPX file without elevation, in a GPX and KML with elevation. It's only for Spain.")
        self.label_3.setText("Convierte un GPX sin elevación, en un GPX y KML con elevación.")
        self.label_4.setText("Es solo para España ya que utiliza el servicio WCS del Instituto Geografico Nacional")
        self.pushButton.setText("File / Fichero")

        self.pushButton.clicked.connect(self.select_file)

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