# Import Python Libary
from PySide2.QtUiTools import QUiLoader
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui

# Import pyqt GUI
from GUI.uiRegister import Ui_RegisterFormUI

# Handle Register dialog
class RegUi(QtWidgets.QDialog):
    # Init dialog
    def __init__(self, Net, parent=None):
        super(RegUi, self).__init__(parent=parent)
        self.ui = Ui_RegisterFormUI()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.net = Net
        self.LoadFunction()

    # Load button function
    def LoadFunction(self):
        self.ui.registerButton.clicked.connect(self.RegisterProcess)
    
    # Hadle Register process
    def RegisterProcess(self):
        # Get field text
        username = self.ui.usernameField.text()
        password = self.ui.passwordField.text()
        repassword = self.ui.repasswordField.text()

        # Check password
        if (password != repassword):
            # Notify user
            self.ui.statusLabel.setText("Mật khẩu nhập không chính xác!")
            return

        # Register user
        try:
            # Send query over socket connection
            query = {
                "event" : "register",
                "username" : username,
                "password" : password,
            }

            self.net.send_query(query)
            
            # Get server respones
            login = self.net.Data
            
            # Get nothing -> keep trying
            if (login == []): return

            # Can't login
            if (login["avai"] == False and login["success"] == False):
                self.ui.statusLabel.setText(str("Không thể đăng kí! Vui lòng thử lại sau"))
            elif (not login["avai"]): 
                # Username is used before
                self.ui.statusLabel.setText(str("Tên tài khoản đã được sử dụng"))
            else:
                self.ui.statusLabel.setText(str("Tài khoản: " + username + " được tạo thành công!"))
        except:
            # Notify unexpected error
            self.ui.statusLabel.setText("Lỗi không xác định!")