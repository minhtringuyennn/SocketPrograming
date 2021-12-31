# Import Python library
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from datetime import date, datetime
import re

# Import custom modules
from ClientLogin import LoginUi
from ClientRegister import RegUi
from ClientAbout import AbtUI
from ClientHandle import ClientSide

# Import pyqt GUI
from GUI.uiClient import Ui_GoldPriceCilent

# Handle Client UI
class ClientUI(QtWidgets.QDialog):
    # Initalize UI
    def __init__(self):
        super(ClientUI, self).__init__()
        
        self.ui = Ui_GoldPriceCilent()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./GUI/icon/logo.png'))
        self.setWindowFlags(
            QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint |
            QtCore.Qt.WindowCloseButtonHint
           )

        self.LoadFunction()
        self.net = ClientSide()

        self.LoginWidget = LoginUi(self.net, self.ui)
        self.RegWidget = RegUi(self.net)
        self.AboutWidget = AbtUI()
        
        self.ChangeIP = False
        self.net.Connected = False

        self.show()

    # Load UI function
    def LoadFunction(self):
        self.ui.loginButton.clicked.connect(self.showLogin)
        self.ui.loginButton.setIcon(QtGui.QIcon('./GUI/icon/login.png'))
        self.ui.loginButton.setIconSize(QtCore.QSize(12, 12))
        
        self.ui.registerButton.clicked.connect(self.showRegister)
        self.ui.registerButton.setIcon(QtGui.QIcon('./GUI/icon/register.png'))
        self.ui.registerButton.setIconSize(QtCore.QSize(14, 14))
        
        self.ui.aboutButton.clicked.connect(self.showAbout)
        self.ui.aboutButton.setIcon(QtGui.QIcon('./GUI/icon/info.png'))
        self.ui.aboutButton.setIconSize(QtCore.QSize(12, 12))
        
        self.ui.connectButton.clicked.connect(self.getconnect)
        self.ui.connectButton.setIcon(QtGui.QIcon('./GUI/icon/connect.png'))
        self.ui.connectButton.setIconSize(QtCore.QSize(12, 12))
        
        self.ui.disconnectButton.clicked.connect(self.disconnect)
        self.ui.disconnectButton.setIcon(QtGui.QIcon('./GUI/icon/disconnect.png'))
        self.ui.disconnectButton.setIconSize(QtCore.QSize(12, 12))
        self.ui.disconnectButton.setEnabled(False)
        
        self.ui.logoutButton.clicked.connect(self.logout)
        self.ui.logoutButton.setIcon(QtGui.QIcon('./GUI/icon/logout.png'))
        self.ui.logoutButton.setIconSize(QtCore.QSize(12, 12))
        self.ui.logoutButton.setEnabled(False)

        self.ui.searchButton.clicked.connect(self.QueryType)
        self.ui.searchButton.setIcon(QtGui.QIcon('./GUI/icon/search.png'))
        self.ui.searchButton.setIconSize(QtCore.QSize(12, 12))
        
        now = str(date.today()).split("-")
        self.ui.getDateButton.setDateTime(QtCore.QDateTime(QtCore.QDate(int(now[0]), int(now[1]), int(now[2])), QtCore.QTime(0, 0, 0)))
    
    # Connect
    def getconnect(self):
        # Get IP field input
        self.ip = str(self.ui.IPField.text())
        self.port = str(self.ui.PORTField.text())
        
        # Check IP is valid or not
        if (not re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', self.ip)):
            QtWidgets.QMessageBox.critical(None, "Lỗi", "IP nhập vào không hợp lệ!")
            return

        # Check PORT is valid or not
        if (self.port.isnumeric() == False or len(self.port) > 5 or int(self.port) > 65535):
            QtWidgets.QMessageBox.critical(None, "Lỗi", "PORT nhập vào không hợp lệ!")
            return

        # Show network connection status
        self.ChangeState(0)

        if (self.net.create_connection(self.ip, self.port)):
            self.ChangeState(1)
        else:
            self.ChangeState(-2)

    def disconnect(self):
        self.logout()
        self.ChangeState(-1)
        self.net.close_connection();

    def logout(self):
        if self.LoginWidget.isLogin == True:
            self.ui.accountStatus.setText(str("Trạng thái tài khoản: Chưa đăng nhập"))
            self.LoginWidget.isLogin = False
            self.ui.loginButton.setEnabled(True)
            self.ui.logoutButton.setEnabled(False)
            self.net.log_out(self.LoginWidget.UserID)
        else:
            pass

    # Show status
    def ChangeState(self, netstate = 0):
        # Connecting
        if (netstate == 0):
            self.ui.netStatus.setText(str("Đang kết nối đến " + str(self.ip)))
            return
        # Connected
        if (netstate == 1):
            self.ui.netStatus.setText(str("Đã kết nối thành công với server " + str(self.net.HOST) + ":" + str(self.net.PORT)))
            self.ui.connectButton.setEnabled(False)
            self.ui.disconnectButton.setEnabled(True)
            return
        # Server not found
        if (netstate == -1):
            self.ui.netStatus.setText("Trạng thái kết nối: Chưa kết nối")
            self.ui.connectButton.setEnabled(True)
            self.ui.disconnectButton.setEnabled(False)
            return
        # Lost connection
        if (netstate == -2):
            QtWidgets.QMessageBox.critical(None, "Lỗi", "Không thể kết nối đến server!")
            self.ui.netStatus.setText("Trạng thái kết nối: Không thể kết nối đến server")
            self.ui.connectButton.setEnabled(True)
            self.ui.disconnectButton.setEnabled(False)
            return

    # Show Login Dialog
    def showLogin(self):
        self.LoginWidget.ui.usernameField.clear()
        self.LoginWidget.ui.passwordField.clear()
        self.LoginWidget.ui.statusLabel.setText("Trạng thái:")
        self.LoginWidget.exec_()

    # Show Register Dialog
    def showRegister(self):
        self.RegWidget.ui.usernameField.clear()
        self.RegWidget.ui.passwordField.clear()
        self.RegWidget.ui.repasswordField.clear()
        self.RegWidget.ui.statusLabel.setText("Trạng thái:")
        self.RegWidget.exec_()

    def showAbout(self):
        self.AboutWidget.exec_()
    
    def UpdateTable(self):
        if self.net.Data == {}:
            self.ui.dataTable.setRowCount(0)

            if self.net.Connected == False:
                self.ChangeState(-2)
        else:
            row = len(self.net.Data) - 1
            self.ui.dataTable.setRowCount(row + 1)

            row = 0
            for data in self.net.Data:

                item = QtWidgets.QTableWidgetItem(str(data['type']))
                self.ui.dataTable.setItem(row, 0, item)
                
                item = QtWidgets.QTableWidgetItem(str(data['brand']))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.dataTable.setItem(row, 1, item)
                
                item = QtWidgets.QTableWidgetItem(str(data['buy']))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.dataTable.setItem(row, 2, item)
                
                item = QtWidgets.QTableWidgetItem(str(data['sell']))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.dataTable.setItem(row, 3, item)
                
                item = QtWidgets.QTableWidgetItem(str(data['update']))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.dataTable.setItem(row, 4, item)
                
                row += 1
                
    def QueryType(self):
        if self.net.Connected and not self.LoginWidget.isLogin:
            QtWidgets.QMessageBox.critical(None, "Lỗi", "Người dùng chưa đăng nhập!")
            return

        date = "NOW"
        type = self.ui.searchField.text()
        date = str(self.ui.getDateButton.date().toPyDate()).replace("-", "")
        
        query = {
            "event" : "GetType",
            "type"  : type,
            "date"  : date
        }

        self.net.send_query(query)

        if (self.net.Data != []):
            self.UpdateTable()
        else:
            self.ui.dataTable.setRowCount(0)
            if self.net.Connected == False:
                self.ChangeState(-2)

    # Close UI
    def CloseUI(self):
        self.disconnect()