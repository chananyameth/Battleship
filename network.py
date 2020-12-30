import socket
from consts import *


class Network:
    def __init__(self, port: int, ip: str = None):
        self.port = port

        self.socket = None
        self.connection = None
        if ip:
            self.ip = ip
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
        else:
            self.ip = '0.0.0.0'
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.bind((self.ip, self.port))
            self.connection.listen(1)
            self.socket, address = self.connection.accept()
            print('Connected by', address)

    def __del__(self):
        if self.socket:
            self.socket.close()
        if self.connection:
            self.connection.close()

    def send(self, data: bytes):
        if not data:
            return
        self.socket.sendall(data)

    def receive(self) -> bytes:
        return self.socket.recv(MAX_MESSAGE_SIZE_VERSION_1)
