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
        self.cert_file = ssl.get_default_verify_paths().cafile

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print("socket failed - Exception:" + str(e))
            sys.exit(1)

        if has_ssl:
            self.ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
            self.ssl_context.options &= ~ssl.OP_NO_SSLv3
            self.ssl_context.load_verify_locations(cafile=self.cert_path)
            self.socket_handler = self.ssl_context.wrap_socket(self.sock)
        else:
            self.socket_handler = self.sock
            self.sock.setblocking(False)
            self.sock.settimeout(2)

    def get_sock(self):
        return self.socket_handler

    def connect(self):
        try:
            self.socket_handler.connect((self.host, int(self.port)))
            self.socket_handler.setblocking(False)
            self.socket_handler.settimeout(10)
            self.socket_connected = True
            pass
        except Exception as error:
            print(str(error))
            return False

        return True

    def recv(self, sock):
        return sock.recv(4096)


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
        sys.exit(0)