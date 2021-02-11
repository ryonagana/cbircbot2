import os
import socket
import time
import ssl
import sys

class Socket:
    def __init__(self, host, port, has_ssl=False):
        self.host = host
        self.port = port
        self.sock = None
        self.socket_handler = None
        self.ssl_context = None

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print("socket failed")
            sys.exit(1)

        if has_ssl:
            self.ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
            self.socket_handler = self.ssl_context.wrap_socket(self.sock)
        else:
            self.socket_handler = self.sock

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