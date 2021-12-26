import sys 
from PyQt5 import QtWidgets
from ServerHandle import ServerSide

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) 
    window = ServerSide()
    sys.exit(app.exec_())