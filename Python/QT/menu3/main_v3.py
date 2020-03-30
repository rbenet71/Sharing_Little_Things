### Version with difference Languages 
# and diferents GUI options - Qt, Tkinter, Kivy, ....
# and two options for load GUI from Qt: Load file .UI, or load a Py generate with pyuic5
#
# I start this sample with the information from
# https://github.com/eyllanesc/stackoverflow/tree/master/questions/53349623
# Thank you Edwin Christian Yllanes Cucho
# And this helps also
# https://stackoverflow.com/questions/39734775/python-switch-translations-dynamically-in-a-pyqt4-application
### Version Con Idioma y UI Variables y CARGABLES
import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow

UiClass, QMainWindow= uic.loadUiType('window_qt.ui') # this is very important give the base-class and the ui-class needed for creating a subclass.

class Demo_Qt(QMainWindow, UiClass):
    def __init__(self):
        UserInterface=QtWidgets.QApplication(sys.argv)  # Starting Aplication in QT
        super(Demo_Qt, self).__init__() # Inicialize Qwidget with Demo_Qt

        if os.path.exists('window_qt.py2') and Load_UI=="PY": # If file with GUI exist in format .py load.
            from window_qt import Ui_MainWindow
            self.ui=Ui_MainWindow()
            self.ui.setupUi(self)
            self.ui.retranslateUi(self)
        else:
            self.ui = uic.loadUi('window_qt.ui',self) # If py file don´t exist, load the .ui file
            self.ui.retranslateUi(self)

        # create slot for actions
        self.ui.button.clicked.connect(self.push)
        self.ui.combo.currentIndexChanged.connect(self.change_func)       

        # initialize dictionary
        self._translate = QtCore.QCoreApplication.translate
        self.trans = QtCore.QTranslator(self)

        options = ([('English', ''), ('français', 'eng-fr' ), ('中文', 'eng-chs'), ('Español', 'eng-es')])
        
        for i, (text, lang) in enumerate(options):
        	self.ui.combo.addItem(text)
        	self.ui.combo.setItemData(i, lang)
        #
        
        self.show() # Show the Graphic User Interface
        sys.exit(UserInterface.exec())  # Loop for Aplication and exit when close the window

    @QtCore.pyqtSlot(int)
    def change_func(self, index): # Change language when select another
        data = self.ui.combo.itemData(index)
        if data:
            dire=os.path.join(os.path.dirname(__file__), data)
            self.trans.load(dire)
            QtWidgets.QApplication.instance().installTranslator(self.trans)
        else:
            QtWidgets.QApplication.instance().removeTranslator(self.trans)
        self.ui.retranslateUi(self)
        self.ui.label.setText('')
    def push(self):
        self.ui.label.setText(self._translate('Messages', 'Pushed'))
"""
class Demo_Tkinter():
    #This only works to show how can you see in tkinter. Language changing don`t works
    import tkinter
    import tkinter.ttk
    window = tkinter.Tk()
    window.title("Sample with Tkinter")
    window.geometry('350x200')
    combo = tkinter.ttk.Combobox(window)
    combo['values']= ('English', 'français', '中文', 'Español')
    combo.current(1) #set the selected item
    combo.grid(column=0, row=0)
    window.mainloop() 
"""
GUI_Choice="Qt"  # I want mi GUI with QT
Load_UI="UI" # If i want to use QT GUI loadind a .UI file
Load_UI="PY" # If i want to use QT GUI loadind a .PT file

class App(Demo_Qt if GUI_Choice=="Qt" else Demo_Tkinter): 
    """I create a class from QT or Tkinter depending of value of GUI_Choice"""
    def __init__(self):
        super().__init__()

# starting APP
if __name__ == "__main__":
    inicia=App()
