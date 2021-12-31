import sys 
from PyQt5 import QtWidgets
from ClientGUI import ClientUI

if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)
    windows = ClientUI()
    application.aboutToQuit.connect(windows.CloseUI)
    sys.exit(application.exec_())