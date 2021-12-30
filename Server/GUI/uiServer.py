# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_Server.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GoldPriceServer(object):
    def setupUi(self, GoldPriceServer):
        GoldPriceServer.setObjectName("GoldPriceServer")
        GoldPriceServer.resize(800, 450)
        GoldPriceServer.setMinimumSize(QtCore.QSize(800, 450))
        self.gridLayout = QtWidgets.QGridLayout(GoldPriceServer)
        self.gridLayout.setObjectName("gridLayout")
        self.serverLogsLabel = QtWidgets.QLabel(GoldPriceServer)
        self.serverLogsLabel.setObjectName("serverLogsLabel")
        self.gridLayout.addWidget(self.serverLogsLabel, 0, 1, 1, 1)
        self.statusLabel = QtWidgets.QLabel(GoldPriceServer)
        self.statusLabel.setMinimumSize(QtCore.QSize(400, 25))
        self.statusLabel.setMaximumSize(QtCore.QSize(400, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.statusLabel.setFont(font)
        self.statusLabel.setObjectName("statusLabel")
        self.gridLayout.addWidget(self.statusLabel, 8, 1, 1, 1)
        self.serverLogsTable = QtWidgets.QTextEdit(GoldPriceServer)
        self.serverLogsTable.setMinimumSize(QtCore.QSize(0, 0))
        self.serverLogsTable.setMouseTracking(False)
        self.serverLogsTable.setFocusPolicy(QtCore.Qt.NoFocus)
        self.serverLogsTable.setAcceptDrops(False)
        self.serverLogsTable.setReadOnly(True)
        self.serverLogsTable.setObjectName("serverLogsTable")
        self.gridLayout.addWidget(self.serverLogsTable, 4, 1, 1, 5)
        self.restartButton = QtWidgets.QPushButton(GoldPriceServer)
        self.restartButton.setMinimumSize(QtCore.QSize(175, 25))
        self.restartButton.setMaximumSize(QtCore.QSize(175, 25))
        self.restartButton.setAutoDefault(False)
        self.restartButton.setObjectName("restartButton")
        self.gridLayout.addWidget(self.restartButton, 8, 5, 1, 1)
        self.startButton = QtWidgets.QPushButton(GoldPriceServer)
        self.startButton.setMinimumSize(QtCore.QSize(175, 25))
        self.startButton.setMaximumSize(QtCore.QSize(175, 25))
        self.startButton.setObjectName("startButton")
        self.gridLayout.addWidget(self.startButton, 8, 4, 1, 1)

        self.retranslateUi(GoldPriceServer)
        QtCore.QMetaObject.connectSlotsByName(GoldPriceServer)

    def retranslateUi(self, GoldPriceServer):
        _translate = QtCore.QCoreApplication.translate
        GoldPriceServer.setWindowTitle(_translate("GoldPriceServer", "Tỷ giá Vàng Việt Nam [SERVER]"))
        self.serverLogsLabel.setText(_translate("GoldPriceServer", "Server Logs"))
        self.statusLabel.setText(_translate("GoldPriceServer", "Trạng thái: Chưa khởi chạy"))
        self.restartButton.setText(_translate("GoldPriceServer", "Khởi động lại máy chủ"))
        self.startButton.setText(_translate("GoldPriceServer", "Khởi chạy máy chủ"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GoldPriceServer = QtWidgets.QDialog()
    ui = Ui_GoldPriceServer()
    ui.setupUi(GoldPriceServer)
    GoldPriceServer.show()
    sys.exit(app.exec_())
