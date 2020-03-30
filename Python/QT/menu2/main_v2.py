### Version with difference Languages 
# and diferents GUI options - Qt, Tkinter, Kivy, ....
#
# I start this sample with the information from
# https://github.com/eyllanesc/stackoverflow/tree/master/questions/53349623
# Thank you Edwin Christian Yllanes Cucho
#
import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets

class Demo_Qt(QtWidgets.QWidget):
    def __init__(self):
        UserInterface=QtWidgets.QApplication(sys.argv)    # Starting Aplication in QT
        super(Demo_Qt, self).__init__() # Inicialize Qwidget with Demo_Qt
        
        self.button = QtWidgets.QPushButton()
        self.label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.message = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.button.clicked.connect(self.push)

        self.combo = QtWidgets.QComboBox(self)
        self.combo.currentIndexChanged.connect(self.change_func)
        
        self._translate = QtCore.QCoreApplication.translate # For transalate Text o Message
        self.trans = QtCore.QTranslator(self)               # For translate Widgets

        self.v_layout = QtWidgets.QVBoxLayout(self)
        self.v_layout.addWidget(self.combo)
        self.v_layout.addWidget(self.button)
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.message)

        options = ([('English', ''), ('français', 'eng-fr' ), ('中文', 'eng-chs'), ('Español', 'eng-es'),])
        
        for i, (text, lang) in enumerate(options):
        	self.combo.addItem(text)
        	self.combo.setItemData(i, lang)
        self.retranslateUi()
        
        self.show()                         # Show the Graphic User Interface
        sys.exit(UserInterface.exec())      # Loop for Aplication and exit when close the window

    @QtCore.pyqtSlot(int)
    def change_func(self, index):           # Change language when select another
        data = self.combo.itemData(index)
        if data:
            dire=os.path.join(os.path.dirname(__file__), data)
            self.trans.load(dire)
            QtWidgets.QApplication.instance().installTranslator(self.trans)
        else:
            QtWidgets.QApplication.instance().removeTranslator(self.trans)
        self.message.setText('')
        
    def push(self):                         # Message when you push the button
        self.message.setText(self._translate('Messages', 'Pushed'))
        
    def changeEvent(self, event):          # When there is a change language call update text widgets
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi()
        super(Demo_Qt, self).changeEvent(event)

    def retranslateUi(self):            # Update text of widgets
        self.button.setText(QtWidgets.QApplication.translate('Demo', 'Start'))
        self.label.setText(QtWidgets.QApplication.translate('Demo', 'Hello, World'))
 
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

GUI_Choice="Qt"  # I want mi GUI with QT

class App(Demo_Qt if GUI_Choice=="Qt" else Demo_Tkinter): 
    """I create a class from QT or Tkinter depending of value of GUI_Choice"""
    def __init__(self):
        super().__init__()

# starting APP
if __name__ == "__main__":
    inicia=App()
