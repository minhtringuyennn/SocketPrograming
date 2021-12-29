# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_Server.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GoldpriceServer(object):
    def setupUi(self, GoldpriceServer):
        GoldpriceServer.setObjectName("GoldpriceServer")
        GoldpriceServer.resize(767, 471)
        self.gridLayout = QtWidgets.QGridLayout(GoldpriceServer)
        self.gridLayout.setObjectName("gridLayout")
        self.serverLogsLabel = QtWidgets.QLabel(GoldpriceServer)
        self.serverLogsLabel.setObjectName("serverLogsLabel")
        self.gridLayout.addWidget(self.serverLogsLabel, 0, 1, 1, 1)
        self.statusLabel = QtWidgets.QLabel(GoldpriceServer)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.statusLabel.setFont(font)
        self.statusLabel.setObjectName("statusLabel")
        self.gridLayout.addWidget(self.statusLabel, 8, 1, 1, 1)
        self.serverLogsTable = QtWidgets.QTextEdit(GoldpriceServer)
        self.serverLogsTable.setReadOnly(True)
        self.serverLogsTable.setObjectName("serverLogsTable")
        self.gridLayout.addWidget(self.serverLogsTable, 4, 1, 1, 5)
        self.restartButton = QtWidgets.QPushButton(GoldpriceServer)
        self.restartButton.setMinimumSize(QtCore.QSize(0, 25))
        self.restartButton.setAutoDefault(False)
        self.restartButton.setObjectName("restartButton")
        self.gridLayout.addWidget(self.restartButton, 8, 5, 1, 1)
        self.startButton = QtWidgets.QPushButton(GoldpriceServer)
        self.startButton.setMinimumSize(QtCore.QSize(0, 25))
        self.startButton.setObjectName("startButton")
        self.gridLayout.addWidget(self.startButton, 8, 4, 1, 1)

        self.retranslateUi(GoldpriceServer)
        QtCore.QMetaObject.connectSlotsByName(GoldpriceServer)

    def retranslateUi(self, GoldpriceServer):
        _translate = QtCore.QCoreApplication.translate
        GoldpriceServer.setWindowTitle(_translate("GoldpriceServer", "Tỷ giá Vàng Việt Nam [SERVER]"))
        self.serverLogsLabel.setText(_translate("GoldpriceServer", "Server Logs"))
        self.statusLabel.setText(_translate("GoldpriceServer", "Trạng thái: Chưa khởi chạy"))
        self.restartButton.setText(_translate("GoldpriceServer", "Restart Server"))
        self.startButton.setText(_translate("GoldpriceServer", "Start Server"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GoldpriceServer = QtWidgets.QDialog()
    ui = Ui_GoldpriceServer()
    ui.setupUi(GoldpriceServer)
    GoldpriceServer.show()
    sys.exit(app.exec_())
