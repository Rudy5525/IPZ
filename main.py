from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QComboBox
from PyQt5.QtGui import QTextDocument, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtXml import QDomElement
from PyQt5 import uic
import sys
#from MRI.main_MRI import MRI
#from EEG.main_EEG import EEG
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.loadMainUI()
        self.show()

    def loadMainUI(self):
        uic.loadUi("UI/MainWindow.ui", self)
        #self.btn_EEG.clicked.connect(EEG())
        #self.btn_MRI.clicked.connect(MRI())


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()