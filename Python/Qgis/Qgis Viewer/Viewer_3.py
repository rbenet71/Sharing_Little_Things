
import os, os.path, sys

from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

from Gisbike_Streetview import Gisbike_Streetview

class see_qgis_project(QDialog):
    """ For Seeing QGis Project """
    def __init__(self):
        super().__init__()
 
        # Creación del Lienzo / Canvas
        self.canvas=QgsMapCanvas(self)
        self.setWindowTitle("PyQGIS Visualización Proyectos")
        self.canvas.setCanvasColor(Qt.white)
 
        self.initGui()
        
        """ no hacen nada...
        #canvas.zommToFullExtent()
        self.canvas.freeze(True)
        self.canvas.show()
        self.canvas.refresh()
        self.canvas.freeze(False)
        self.canvas.repaint()
        """
        
    def zoomIn(self):
        self.canvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
        self.canvas.setMapTool(self.toolZoomOut)

    def pan(self):
        self.canvas.setMapTool(self.toolPan)
        
    def streetView (self):
        self.canvas.setMapTool(Gisbike_Streetview(self,self.canvas))
    def file(self):
        filename,_ = QFileDialog.getOpenFileName(self, 'Selecciona Fichero GPX','c:/', 'QGis (*.qgz)')
        if filename:
            self.project.read(filename)       

    def initGui(self):
        #from Gisbike_Functions import Get_Gisbike_DDBB
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
        self.actionStreetView=QPushButton("Street View",self.splitter )
        self.actionFile=QPushButton("File",self.splitter )
        
        self.project = QgsProject.instance() 
        #file_name=Get_Gisbike_DDBB()
        file_name='C:/Roberto/Visual_Studio_Code/GisBike/programa/DDBB/GisBike.gpkg'
        uri=("geopackage:{}?projectName=Mapas_Guia_Tecnica").format(file_name)

        self.project.read(uri)   
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
        self.horizontalLayout.addWidget(self.actionStreetView)
        self.horizontalLayout.addWidget(self.actionFile)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout_2.addWidget(self.splitter)
   
        self.actionZoomIn.clicked.connect(self.zoomIn)
        self.actionZoomOut.clicked.connect(self.zoomOut)
        self.actionPan.clicked.connect(self.pan)
        self.actionStreetView.clicked.connect(self.streetView)
        self.actionFile.clicked.connect(self.file)

        # create the map tools
        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False) # false = in
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = out

if __name__ == "__main__":
    #from Gisbike_Functions import Rob_Dir
    #from Gisbike_Functions import Parameters
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    #app2 = QgsApplication([], True)
    #app2.initQgis()
    #GB.Var_Prog['Program Path']=os.path.dirname(__file__) 
    #Parameters().read()
    window = see_qgis_project()
    window.show()
    sys.exit(app.exec_())