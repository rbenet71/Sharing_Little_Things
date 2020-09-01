
import os, os.path, sys

from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *


class MapViewer(QMainWindow):
    def __init__(self, shapefile):
        QMainWindow.__init__(self)
        self.setWindowTitle("Map Viewer")
        canvas = QgsMapCanvas()
        #canvas.useImageToRender(False)
        canvas.setCanvasColor(Qt.white)
        canvas.show()
        layer = QgsVectorLayer(shapefile, "layer1", "ogr")
        """
        if not layer.isValid():
            raise IOError("Invalid shapefile")
        """
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        canvas.setExtent(layer.extent())
        canvas.setLayerSet([QgsMapCanvasLayer(layer)])
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        contents = QWidget()
        contents.setLayout(layout)
        self.setCentralWidget(contents)


def main():
    app = QgsApplication([], True)
    QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX_PATH'], True)
    app.initQgis()
    #app = QApplication(sys.argv)

    viewer = MapViewer("Data/ne_10m_admin_0_countries.shp")
    viewer.show()
    app.exec_()
    app.deleteLater()
    QgsApplication.exitQgis()
    
if __name__ == "__main__":
    main()
