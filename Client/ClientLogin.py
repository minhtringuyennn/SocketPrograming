# Import Python Library
from PySide2.QtUiTools import QUiLoader
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui

# Import pyqt GUI
from GUI.uiLogin import Ui_LoginUI

# Import Python library
import time

class LoginUi(QtWidgets.QDialog):
    def __init__(self, Net, UI, parent=None):
        super(LoginUi, self).__init__(parent=parent)

        self.ui = Ui_LoginUI()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        
        self.net = Net
        self.clientUI = UI
        self.UserID = -1
        self.isLogin = False
        self.LoadFunction()

    # Connect UI Button
    def LoadFunction(self):
        self.ui.loginButton.clicked.connect(self.LoginProcess)
    
    def ChangeState(self, state = 0, username = ""):
        self.ui.usernameField.clear()
        self.ui.passwordField.clear()

        if (state == 0):
            self.clientUI.accountStatus.setText(str("Trạng thái tài khoản: Chưa đăng nhập"))
            self.clientUI.loginButton.setEnabled(True)
            self.clientUI.logoutButton.setEnabled(False)
            return

        if (state == 1):
            self.clientUI.accountStatus.setText(str(f"Trạng thái tài khoản: Đang đăng nhập với tài khoản '{username}'"))
            self.clientUI.loginButton.setEnabled(False)
            self.clientUI.logoutButton.setEnabled(True)
            return

    # Process Login
    def LoginProcess(self):
        
        # Get text from input field
        username = self.ui.usernameField.text()
        password = self.ui.passwordField.text()
        
        # Handle login
        try:
            if self.isLogin:
                self.ui.statusLabel.setText("Bạn đã đăng nhập! Vui lòng thoát tài khoản!")
                return

            # Send query over socket
            query = {
                "event" : "login",
                "username" : username,
                "password" : password
            }
            
            self.net.send_query(query)
            login = self.net.Data
            
            if (login == []): return
            
            self.isLogin = login["valid_users"]
            
            # If server dont recognize user
            if not self.isLogin:
                self.ChangeState(0, None)
                if login["user_id"] == -1:
                    self.ui.statusLabel.setText("Tài khoản hoặc mật khẩu không chính xác!")
                else:
                    self.ui.statusLabel.setText("Tài khoản của bạn đã đăng nhập tại nơi khác!")
            else:
                # Notify user login successfuly
                self.ChangeState(1, username)
                self.ui.statusLabel.setText(str("Chào mừng bạn, " + username + "!"))
                self.UserID = login["user_id"]

        except:
            self.ui.statusLabel.setText("Lỗi không xác định!")