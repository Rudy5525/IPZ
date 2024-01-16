import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from MRI.main_MRI import MRI
from EEG.main_EEG import EEG

current_dir = os.path.dirname(__file__)
UI_PATH = rf'{current_dir}/UI'


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.loadMainUI()
        self.show()

    def loadMainUI(self):
        uic.loadUi(rf'{UI_PATH}/MainWindow.ui', self)
        self.btn_EEG.clicked.connect(self.runEEG)
        self.btn_MRI.clicked.connect(self.runMRI)

    def runEEG(self):
        EEG()
        print("Uruchomienie EEG")

    def runMRI(self):
        MRI()
        print("Uruchomienie MRI")

app = QApplication(sys.argv)
window = MainWindow()
app.exec_()