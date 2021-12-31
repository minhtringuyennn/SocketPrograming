# Import Python library
import os, sys, socket, threading, logging, asyncio, json
import datetime
from datetime import datetime

# Import Pyqt library
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets, QtCore
from qtpy.QtCore import QObject, Signal, QThread

# Import custom module
from ServerDatabase import Db
from GUI.uiServer import Ui_GoldPriceServer

# Constanst
NUM_CONN = 8
BUFFER = 1024

# Class handle console logging to pyqt
logger = logging.getLogger(__name__)

class ConsoleWindowLogHandler(logging.Handler, QObject):
    sigLog = Signal(str)
    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)

    def emit(self, logRecord):
        message = str(logRecord.getMessage())
        self.sigLog.emit(message)

# Handle server
class ServerSide(QtWidgets.QDialog):
    # Init server
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Init GUI
        self.ui = Ui_GoldPriceServer()
        self.ui.setupUi(self)

        self.setWindowIcon(QtGui.QIcon('./GUI/icon/logo.png'))
        self.setWindowFlags(
            QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint |
            QtCore.Qt.WindowCloseButtonHint
           )

        self.HOST = "0.0.0.0"
        self.PORT = 12345
        self.Data = Db()
        self.loadFunction()
        self.ChangeState()
        self.show()

        # Bind console to pyqt
        consoleHandler = ConsoleWindowLogHandler()
        consoleHandler.sigLog.connect(self.ui.serverLogsTable.append)
        logger.addHandler(consoleHandler)

    # Connect button to function
    def loadFunction(self):
        self.ui.startButton.clicked.connect(self.run)
        self.ui.startButton.setIcon(QtGui.QIcon('./GUI/icon/start.png'))
        self.ui.startButton.setIconSize(QtCore.QSize(15, 15))

        self.ui.restartButton.clicked.connect(self.restart)
        self.ui.restartButton.setIcon(QtGui.QIcon('./GUI/icon/restart.png'))
        self.ui.restartButton.setIconSize(QtCore.QSize(12, 12))

    # Starting the server thread
    def run(self):
        self.thread = threading.Thread(target = self.start_server)
        self.ui.startButton.setEnabled(False)
        self.ChangeState(1)
        self.thread.start()

    # Handle restart server
    def restart(self):
        reply = QtWidgets.QMessageBox.question(None, "Thông báo", "Bạn có chắc khởi động lại server chứ?")
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                os.execv(sys.executable, ['python3'] + sys.argv)
            except:
                QtWidgets.QMessageBox.critical(None, "Lỗi", "Không thể khởi động lại máy chủ! Bạn nên để server tại ổ C!")
                pass
        else:
            pass

    # Run server async
    def start_server(self):
        asyncio.run(self.run_server())

    # Print server logs (UI)
    def printlogs(self, msg):
        msg = str(msg)
        print(msg)
        logger.error(msg)

    # Show status
    def ChangeState(self, netstate = 0):
        # Havent run
        if (netstate==0):
            self.ui.statusLabel.setText(str("Trạng thái: Chưa khởi chạy"))
            return

        # Running server
        if (netstate==1):
            self.ui.statusLabel.setText(str("Trạng thái: Server sẵn sàng tại " + str(socket.gethostbyname(socket.gethostname())) + ":" + str(self.PORT)))
            return

    # Handle client reponse
    async def handle_client(self, client, addr):
        # Create loop to get event
        loop = asyncio.get_event_loop()
        request = None 

        while True:
            try:
                # Waiting for connection
                request = await asyncio.wait_for((loop.sock_recv(client, 4)), timeout = 6000) # Timeout after 6000s (100 minutes)
                
                # Get data size
                size = int.from_bytes(request, "big")

                # Recieve data from client
                data = ""
                while size > 0:
                    recv = (await loop.sock_recv(client, min(BUFFER, size))).decode('utf8')
                    data += recv
                    if (size > len(recv)):
                        size -= len(recv)
                    else:
                        size = 0

                # Try loading data
                try:
                    request = json.loads(data)
                    self.printlogs(f"Client Requested: {data}")
                except:
                    pass

                # If client request to close or close unexpected
                if (request["event"] == 'close' or not request):
                    self.printlogs(f"Client Disconnected at: " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + ".")
                    break

                # Send back the reponse to client
                response = json.dumps(self.process_request(request), separators=(',', ':'))
                await loop.sock_sendall(client, len(response.encode('utf-8')).to_bytes(4, 'big'))
                await loop.sock_sendall(client, response.encode('utf-8'))
                self.printlogs(f"Server response send sucessfully.")

            # Notify when client close unxpected
            except socket.error as msg:
                self.printlogs(f"Client Close Unexpected.")
                break

            # If connection time-out
            except asyncio.TimeoutError as te:
                response = 'Request Timeout'
                await loop.sock_sendall(client, response.encode('utf8'))
                self.printlogs(f"Client Connection Timeout.")
                break

            # Notify client when server can't handle request
            except Exception as Error:
                response = 'Request Error'
                await loop.sock_sendall(client, response.encode('utf8'))
                self.printlogs(Error)
                pass

        client.close()

    # Process client request
    def process_request(self, request):
        # Get database

        # Handle user login
        if (request["event"] == "login"):
            self.printlogs(f"Client requested login at: " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + ".")
            res = self.Data.Login(request["username"], request["password"])
            self.printlogs(res)
            return res

        # Handle user register
        if (request["event"] == "register"):
            self.printlogs(f"Client requested register at: " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + ".")
            res = self.Data.Register(request["username"], request["password"])
            self.printlogs(res)
            return res

        # Handle user logout
        if (request["event"] == "logout"):
            self.printlogs(f"Client requested logout at: " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + ".")
            res = self.Data.Logout(request["user_id"])
            self.printlogs(res)
            return res

        # Handle user get gold type
        if (request["event"] == "GetType"):
            res = self.Data.GetType(request["type"], request["date"])
            # self.printlogs(res)
            return res
            
        # Return None
        return {}

    # Run server
    async def run_server(self):
        # Establish socket connection
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.server.bind((self.HOST, self.PORT))
                break
            except socket.error as err:
                self.printlogs("Port " + str(self.PORT) + " on used, try on port " + str(self.PORT + 1))
                self.PORT += 1
                pass

        # Success run server
        self.server.listen(NUM_CONN)
        self.server.setblocking(False)
        loop = asyncio.get_event_loop()
        self.printlogs("Server Ready on " + str(socket.gethostbyname(socket.gethostname())) + ":" + str(self.PORT) + "!")
        
        # Connect client
        while True:
            client, addr = await loop.sock_accept(self.server)
            self.printlogs(str("Client " + str(addr[0]) + ":" + str(addr[1]) + " Connected at: " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "."))

            # Handle client
            try:
                loop.create_task(self.handle_client(client, addr))
            except:
                pass