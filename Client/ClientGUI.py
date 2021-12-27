# Import Python library
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from datetime import date, datetime
import re, time

# Import custom modules
from ClientLogin import LoginUi
from ClientRegister import RegUi
from ClientHandle import ClientSide

# Import pyqt GUI
from GUI.uiClient import Ui_GoldPriceCilent
from GUI.uiLogin import Ui_Login

# Handle Client UI
class ClientUI(QtWidgets.QDialog):
    # Initalize UI
    def __init__(self):
        super(ClientUI, self).__init__()
        
        self.ui = Ui_GoldPriceCilent()
        self.ui.setupUi(self)
        
        self.setWindowFlags(
            QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint |
            QtCore.Qt.WindowCloseButtonHint
           )

        self.LoadFunction()
        self.net = ClientSide()
        self.LoginWidget = LoginUi(self.net)
        self.RegWidget = RegUi(self.net)

        self.count = 0
        self.ChangeIP = False
        self.net.Connected = False

        self.show()

    # Load UI function
    def LoadFunction(self):
        self.ui.Login.clicked.connect(self.showLogin)
        self.ui.Register.clicked.connect(self.showRegister)
        self.ui.Connect.clicked.connect(self.getconnect)
        self.ui.Search.clicked.connect(self.QueryType)

        now = str(date.today()).split("-")
        self.ui.GetDate.setDateTime(QtCore.QDateTime(QtCore.QDate(int(now[0]), int(now[1]), int(now[2])), QtCore.QTime(0, 0, 0)))
    
    # Connect
    def getconnect(self):
        # Get IP field input
        self.ip = str(self.ui.IP.text())
        
        # Check IP is valid or not
        if (not re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', self.ip)):  
            QtWidgets.QMessageBox.about(None, "Error", "IP nhập vào không hợp lệ!")
            return

        # Show network connection status
        self.ChangeState(0)

        if (self.net.create_connection(self.ip)):
            self.ChangeState(1)
        else:
            self.ChangeState(-1)

    # Show status
    def ChangeState(self, netstate = 0):
        # Connecting
        if (netstate==0):
            self.ui.Netstate.setText(str("Connecting to " + str(self.ip)))
            return
        # Connected
        if (netstate==1):
            self.ui.Netstate.setText(str("Connected to " + str(self.net.HOST) + ":" + str(self.net.PORT)))
            return
        # Server not found
        if (netstate==-1):
            self.ui.Netstate.setText("Connect to " + str(self.net.HOST) + " Error! Server is unavailable!")
            return

    # Show Login Dialog
    def showLogin(self):
        self.LoginWidget.exec_()

    # Show Register Dialog
    def showRegister(self):
        self.RegWidget.exec_()
    
    def UpdateTable(self):
        # print(self.net.Data)
        
        row = len(self.net.Data) - 1
        self.ui.DataTable.setRowCount(row + 1)

        row = 0
        for data in self.net.Data:
            # print(data)
            item = QtWidgets.QTableWidgetItem(str(data['type']))
            self.ui.DataTable.setItem(row, 0, item)
            item = QtWidgets.QTableWidgetItem(str(data['brand']))
            self.ui.DataTable.setItem(row, 1, item)
            item = QtWidgets.QTableWidgetItem(str(data['buy']))
            self.ui.DataTable.setItem(row, 2, item)
            item = QtWidgets.QTableWidgetItem(str(data['sell']))
            self.ui.DataTable.setItem(row, 3, item)
            item = QtWidgets.QTableWidgetItem(str(data['update']))
            self.ui.DataTable.setItem(row, 4, item)
            row += 1
            #column += 1

    def QueryType(self):
        date = "NOW"
        type = self.ui.SearchType.text()
        date = str(self.ui.GetDate.date().toPyDate()).replace("-", "")
        
        if type == "":
            query = {
                "event" : "GetTotal",
                "date"  : date
            }
        else:
            query = {
                "event" : "GetType",
                "type"  : type,
                "date"  : date
            }

        # print(query)

        # time.sleep(0.005)
        self.net.send_query(query)

        if (self.net.Data != []):
            self.UpdateTable()
        else:
            QtWidgets.QMessageBox.about(None, "Error", "Không có dữ liệu!")

    # Close UI
    def CloseUI(self):
        pass