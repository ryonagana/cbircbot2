import os
import socket
import time


class Socket:
    def __init__(self, host,port):
        self.host = host
        self.port = port
        self.socket_handler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket_handler.connect_ex((self.host, int(self.port)))
        except Exception as error:
            print(error.__str__())
            return False

        return True

    def recv(self, size):
        if type(size) == int:
            return self.socket_handler.recv(size)

        return None

    def send(self, data):
        self.socket_handler.send(str.encode(data))

    def close(self):
        self.socket_handler.shutdown(socket.SHUT_RDWR)
        self.socket_handler.close()

    def exit_gracefully(self):
        time.sleep(1)
        self.close()