import os, os.path, sys

from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

from ui_mainWindow import Ui_MainWindow
#import resources
#from constants import *
#from mapTools import *

"""
class MapExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Landmark Explorer")
        self.resize(800, 400)
def main():
    app = QgsApplication([], True)
    QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX_PATH'], True)
    app.initQgis()
    #app = QApplication(sys.argv)
    window = MapExplorer()
    window.show()
    window.raise_()
    sys.exit(app.exec_())
    app.deleteLater()
    QgsApplication.exitQgis()

if __name__ == "__main__":
    main()

"""

class ForestTrailsWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.actionQuit.triggered.connect(self.quit)
        self.actionZoomIn.triggered.connect(self.zoomIn)
        self.actionZoomOut.triggered.connect(self.zoomOut)
        self.actionPan.triggered.connect(self.setPanMode)
        self.actionEdit.triggered.connect(self.setEditMode)
        self.actionAddTrack.triggered.connect(self.addTrack)
        self.actionEditTrack.triggered.connect(self.editTrack)
        self.actionDeleteTrack.triggered.connect(self.deleteTrack)
        self.actionGetInfo.triggered.connect(self.getInfo)
        self.actionSetStartPoint.triggered.connect(self.setStartingPoint)
        self.actionSetEndPoint.triggered.connect(self.setEndingPoint)
        self.actionFindShortestPath.triggered.connect(self.findShortestPath)

        self.mapCanvas = QgsMapCanvas()
        #self.mapCanvas.useImageToRender(False)
        self.mapCanvas.setCanvasColor(Qt.white)
        self.mapCanvas.show()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.mapCanvas)
        self.centralWidget.setLayout(layout)
    def zoomIn(self):
        self.mapCanvas.zoomIn()
    def zoomOut(self):
        self.mapCanvas.zoomOut()
    def quit(self):
        pass
    def setPanMode(self):
        pass
    def setEditMode(self):
        pass
    def addTrack(self):
        pass
    def editTrack(self):
        pass
    def deleteTrack(self):
        pass
    def getInfo(self):
        pass
    def setStartingPoint(self):
        pass
    def setEndingPoint(self):
        pass
    def findShortestPath(self):
        pass
def main():
    app = QgsApplication([], True)
    QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX_PATH'], True)
    app.initQgis()
    #app = QApplication(sys.argv)

    window = ForestTrailsWindow()
    window.show()
    window.raise_()
    window.setPanMode()
    app.exec_()
    app.deleteLater()
    QgsApplication.exitQgis()
if __name__ == "__main__":
    main()
#"""