# Import Python Libary
from PySide2.QtUiTools import QUiLoader
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui

# Import pyqt GUI
from GUI.uiAbout import Ui_About

# Handle Register dialog
class AbtUI(QtWidgets.QDialog):
    # Init dialog
    def __init__(self, parent = None):
        super(AbtUI, self).__init__(parent = parent)
        self.ui = Ui_About()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)