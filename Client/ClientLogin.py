# Import Python Library
from PySide2.QtUiTools import QUiLoader
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui

# Import pyqt GUI
from GUI.uiLogin import Ui_Login
import time

class LoginUi(QtWidgets.QDialog):
    def __init__(self, Net, parent=None):
        super(LoginUi, self).__init__(parent=parent)

        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        
        self.net = Net
        self.LoadFunction()

    # Connect UI Button
    def LoadFunction(self):
        self.ui.loginButton.clicked.connect(self.LoginProcess)
        # self.ui.usernameField.clear()
        # self.ui.passwordField.clear()
    
    # Process Login
    def LoginProcess(self):
        
        # Get text from input field
        username = self.ui.usernameField.text()
        password = self.ui.passwordField.text()
        
        # Handle login
        try:
            # Send query over socket
            query = {
                "event" : "login",
                "username" : username,
                "password" : password
            }
            
            self.net.send_query(query)
            login = self.net.Data
            
            if (login == []): return
            
            # If server dont recognize user
            if (not login["valid_users"]):
                self.ui.errorLabel.setText("Tài khoản hoặc mật khẩu không chính xác!")
            else:
            # Notify user login successfuly
                self.ui.errorLabel.setText(str("Chào mừng bạn, " + username + "!"))
                self.UserID = login["user_id"]

        except:
            self.ui.errorLabel.setText("Tài khoản hoặc mật khẩu không chính xác!")