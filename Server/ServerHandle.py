import asyncio, socket
import datetime
from PyQt5 import QtWidgets, QtCore
import requests
from ServerDatabase import Db
import json
import threading
from datetime import datetime
from GUI.uiServer import Ui_GoldpriceServer

# Constanst
NUM_CONN = 8
BUFFER = 1024

class ServerSide(QtWidgets.QDialog):
    # Init server
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_GoldpriceServer()
        self.ui.setupUi(self)

        self.setWindowFlags(
            QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint |
            QtCore.Qt.WindowCloseButtonHint
           )

        self.HOST = "0.0.0.0"
        self.PORT = 12345
        self.Data = Db()
        self.loadFunction()
        self.show()

    # Link button Start server
    def loadFunction(self):
        self.ui.startButton.clicked.connect(self.run)

    # Starting the server thread
    def run(self):
        self.thread = threading.Thread(target=self.start_server)
        self.ui.startButton.setEnabled(False)
        self.thread.start()

    # Calback server
    def start_server(self):
        asyncio.run(self.run_server())

    # Print server logs (UI)
    def printlogs(self, msg):
        msg = str(msg)
        print(msg)
        self.ui.serverLogsTable.appendPlainText(msg)

    # Handle client reponse
    async def handle_client(self, client, addr):
        loop = asyncio.get_event_loop()
        request = None 

        while True:
            try:
                # Waiting for connection
                request = await asyncio.wait_for((loop.sock_recv(client, 4)), timeout=600)
                size = int.from_bytes(request, "big")
                data = ""

                # Recieve data from client
                while size > 0:
                    recv = (await loop.sock_recv(client, min(BUFFER,size))).decode('utf8')
                    data += recv
                    if (size > len(recv)):
                        size -= len(recv)
                    else:
                        size = 0

                # Print log
                try:
                    request = json.loads(data)
                    # self.printlogs(f"Client Requested.")
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
                # self.printlogs(f"Server response send sucessfully.")

            # Notify when client close unxpected
            except socket.error as msg:
                self.printlogs(f"Client Close Unexpected.")
                break

            # If connection time-out
            except asyncio.TimeoutError as te:
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
        if (request["event"] == "GetTotal"):
            # self.printlogs(f"Client requested get total data.")
            return self.Data.GetTotal(request["date"])

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

        # Handle user get gold type
        if (request["event"] == "GetType"):
            # self.printlogs(f"Client requested get gold type.")
            return self.Data.GetType(request["type"], request["date"])
            
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

        self.server.listen(NUM_CONN)
        self.server.setblocking(False)
        loop = asyncio.get_event_loop()
        self.printlogs("Server Ready on " + str(socket.gethostbyname(socket.gethostname())) + ":" + str(self.PORT) + "!")
        
        # Connect client
        while True:
            client, addr = await loop.sock_accept(self.server)
            self.printlogs(str("Client " + str(addr[0]) + ":" + str(addr[1]) + " Connected at: " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "."))

            try:
                loop.create_task(self.handle_client(client, addr))
            except:
                pass