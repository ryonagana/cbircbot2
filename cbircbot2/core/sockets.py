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
        self.socket_connected = False

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print("socket failed - Exception:" + str(e))
            sys.exit(1)

        if has_ssl:
            self.ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
            self.socket_handler = self.ssl_context.wrap_socket(self.sock, do_handshake_on_connect=True)
        else:
            self.socket_handler = self.sock

    def connect(self):
        try:
            self.socket_handler.connect((self.host, int(self.port)))
            self.socket_connected = True
        except Exception as error:
            print(str(error))
            return False

        return True

    def recv(self, size):
        if type(size) == int:
            return self.socket_handler.recv(size)

        return None

    def send(self, data):
        if not self.sock:
            print("not connected, but tried to send " + data)
            return
        self.socket_handler.send(str.encode(data))

    def close(self):
        self.socket_handler.shutdown(socket.SHUT_RDWR)
        self.socket_handler.close()

    def exit_gracefully(self):
        time.sleep(1)
        self.close()