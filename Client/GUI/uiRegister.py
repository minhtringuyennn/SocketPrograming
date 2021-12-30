# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_Register.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RegisterFormUI(object):
    def setupUi(self, RegisterFormUI):
        RegisterFormUI.setObjectName("RegisterFormUI")
        RegisterFormUI.setWindowModality(QtCore.Qt.NonModal)
        RegisterFormUI.resize(300, 270)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RegisterFormUI.sizePolicy().hasHeightForWidth())
        RegisterFormUI.setSizePolicy(sizePolicy)
        RegisterFormUI.setMinimumSize(QtCore.QSize(300, 270))
        RegisterFormUI.setMaximumSize(QtCore.QSize(350, 270))
        RegisterFormUI.setBaseSize(QtCore.QSize(0, 0))
        RegisterFormUI.setFocusPolicy(QtCore.Qt.StrongFocus)
        RegisterFormUI.setSizeGripEnabled(False)
        RegisterFormUI.setModal(False)
        self.gridLayout = QtWidgets.QGridLayout(RegisterFormUI)
        self.gridLayout.setObjectName("gridLayout")
        self.userlb = QtWidgets.QLabel(RegisterFormUI)
        self.userlb.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userlb.sizePolicy().hasHeightForWidth())
        self.userlb.setSizePolicy(sizePolicy)
        self.userlb.setMaximumSize(QtCore.QSize(16777215, 20))
        self.userlb.setInputMethodHints(QtCore.Qt.ImhNone)
        self.userlb.setScaledContents(False)
        self.userlb.setObjectName("userlb")
        self.gridLayout.addWidget(self.userlb, 2, 0, 1, 2)
        self.usernameField = QtWidgets.QLineEdit(RegisterFormUI)
        self.usernameField.setMinimumSize(QtCore.QSize(0, 25))
        self.usernameField.setInputMethodHints(QtCore.Qt.ImhNoAutoUppercase)
        self.usernameField.setClearButtonEnabled(False)
        self.usernameField.setObjectName("usernameField")
        self.gridLayout.addWidget(self.usernameField, 3, 0, 1, 3)
        self.statusLabel = QtWidgets.QLabel(RegisterFormUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy)
        self.statusLabel.setMinimumSize(QtCore.QSize(250, 10))
        self.statusLabel.setMaximumSize(QtCore.QSize(500, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.statusLabel.setFont(font)
        self.statusLabel.setObjectName("statusLabel")
        self.gridLayout.addWidget(self.statusLabel, 11, 0, 1, 3)
        self.passwordLabel = QtWidgets.QLabel(RegisterFormUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.passwordLabel.sizePolicy().hasHeightForWidth())
        self.passwordLabel.setSizePolicy(sizePolicy)
        self.passwordLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.passwordLabel.setObjectName("passwordLabel")
        self.gridLayout.addWidget(self.passwordLabel, 5, 0, 1, 2)
        self.registerButton = QtWidgets.QPushButton(RegisterFormUI)
        self.registerButton.setMinimumSize(QtCore.QSize(0, 25))
        self.registerButton.setCheckable(True)
        self.registerButton.setDefault(True)
        self.registerButton.setObjectName("registerButton")
        self.gridLayout.addWidget(self.registerButton, 12, 0, 1, 3)
        self.cancelButton = QtWidgets.QPushButton(RegisterFormUI)
        self.cancelButton.setMinimumSize(QtCore.QSize(0, 25))
        self.cancelButton.setFocusPolicy(QtCore.Qt.TabFocus)
        self.cancelButton.setAutoDefault(False)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 14, 0, 1, 3)
        self.repasswordField = QtWidgets.QLineEdit(RegisterFormUI)
        self.repasswordField.setMinimumSize(QtCore.QSize(0, 25))
        self.repasswordField.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.repasswordField.setObjectName("repasswordField")
        self.gridLayout.addWidget(self.repasswordField, 10, 0, 1, 3)
        self.passwordField = QtWidgets.QLineEdit(RegisterFormUI)
        self.passwordField.setMinimumSize(QtCore.QSize(0, 25))
        self.passwordField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordField.setObjectName("passwordField")
        self.gridLayout.addWidget(self.passwordField, 6, 0, 1, 3)
        self.repasswordLabel = QtWidgets.QLabel(RegisterFormUI)
        self.repasswordLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.repasswordLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.repasswordLabel.setObjectName("repasswordLabel")
        self.gridLayout.addWidget(self.repasswordLabel, 9, 0, 1, 1)

        self.retranslateUi(RegisterFormUI)
        self.cancelButton.clicked.connect(RegisterFormUI.close)
        QtCore.QMetaObject.connectSlotsByName(RegisterFormUI)

    def retranslateUi(self, RegisterFormUI):
        _translate = QtCore.QCoreApplication.translate
        RegisterFormUI.setWindowTitle(_translate("RegisterFormUI", "Đăng kí tài khoản"))
        self.userlb.setText(_translate("RegisterFormUI", "Username"))
        self.usernameField.setPlaceholderText(_translate("RegisterFormUI", "Nhập tài khoản đăng kí"))
        self.statusLabel.setText(_translate("RegisterFormUI", "Trạng thái: Chưa đăng kí"))
        self.passwordLabel.setText(_translate("RegisterFormUI", "Password"))
        self.registerButton.setText(_translate("RegisterFormUI", "Đăng kí"))
        self.cancelButton.setText(_translate("RegisterFormUI", "Huỷ"))
        self.repasswordField.setPlaceholderText(_translate("RegisterFormUI", "Nhập lại mật khẩu người dùng"))
        self.passwordField.setPlaceholderText(_translate("RegisterFormUI", "Nhập mật khẩu người dùng"))
        self.repasswordLabel.setText(_translate("RegisterFormUI", "Retype Password"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RegisterFormUI = QtWidgets.QDialog()
    ui = Ui_RegisterFormUI()
    ui.setupUi(RegisterFormUI)
    RegisterFormUI.show()
    sys.exit(app.exec_())
