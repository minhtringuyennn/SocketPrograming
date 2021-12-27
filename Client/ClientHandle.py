# Import Python library
import socket, json, time
from PyQt5.QtWidgets import QMessageBox

# Handle client process
class ClientSide():
    # Init client connection
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Default HOST and PORT
        self.HOST = '127.0.0.1'
        self.PORT = 12345
        self.Connected = False
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Create network connection
    def create_connection(self, IP):
        # Get HOST and PORT
        self.HOST = IP
        PORT = self.PORT
        
        # Try connect server
        try:
            server_address = (self.HOST, PORT)
            self.server =  socket.create_connection(server_address, timeout = 1)
            self.Connected = True
            return True
        except:
            return False

    # Send close connection query
    def close_connection(self):
        query = {
            "event" : "close"
        }
        self.Connected = True
        self.send_query(query)
        self.Connected = False

    # Handle send query over socket
    def send_query(self,query):
        # Notify user when client haven't connect server
        if (self.Connected == False):
            QMessageBox.about(None, "Error", "Kết nối chưa được thiết lập.")
            self.Data = []
            return

        # Send query over socket
        try:
            # Parse raw information
            squery = json.dumps(query, separators=(',', ':'))
            
            # Send query
            self.server.send(len(squery.encode('utf8')).to_bytes(4, 'big'))
            self.server.send(squery.encode('utf8'))
            
            # Get server respone
            data = self.server.recv(4)
            size = int.from_bytes(data, "big")
            data = ''

            # Get data chunk
            while size > 0:
                recv = self.server.recv(min(1024, size)).decode('utf8')
                data += recv

                if (size > len(recv)):
                    size -= len(recv)
                else:
                    size = 0

            # Import data
            try:
                self.Data = json.loads(data)
            except:
                self.Data = []

        # Handle unexpected error
        except socket.error:
            self.Connected = False
            self.Data = []
            pass
