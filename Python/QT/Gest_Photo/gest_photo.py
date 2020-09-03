import sys,os
from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QFileSystemModel, QVBoxLayout,QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QModelIndex,Qt

class FileSystemView(QWidget):
	def __init__(self, dir_path):
		super().__init__()
		appWidth = 800
		appHeight = 300
		self.setWindowTitle('File System Viewer')
		self.setGeometry(300, 300, appWidth, appHeight)
		
		self.model = QFileSystemModel()
		self.model.setRootPath(dir_path)
		self.tree =  QTreeView()
		self.tree.setModel(self.model)
		self.tree.setRootIndex(self.model.index(dirPath))
		self.tree.setColumnWidth(0, 250)
		self.tree.setAlternatingRowColors(True)

		layout = QVBoxLayout()
		self.photo=QLabel('Hola'+chr(10)+'Caracola')
		layout.addWidget(self.tree)
		layout.addWidget(self.photo)
		self.setLayout(layout)
		self.tree.selectionModel().selectionChanged.connect(self.select)
	
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Space or event.key() == Qt.Key_Return:
			index = self.tree.selectedIndexes()[0]
			crawler = index.model().filePath(index)
			print(crawler)
		#self.tree.keyPressEvent(self, event)
	
	def select(self,index1):
		index = self.tree.selectedIndexes()[0]
		file_sel= index.model().filePath(index)
		if os.path.isfile(file_sel) and file_sel[-3:].upper() in 'JPG PNG':
			pixmap = QPixmap(file_sel)
			self.photo.setPixmap(pixmap)
			print(file_sel)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	dirPath = r'c:/'
	demo = FileSystemView(dirPath)
	demo.show()
	sys.exit(app.exec_())
