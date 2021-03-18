from  cbircbot2.core.sockets import  Socket
from cbircbot2.core.params import  EnvironmentParams
from cbircbot2.core.client import IrcClient
from cbircbot2.core.modules import IrcModules
from cbircbot2.core.input import InputText
import selectors
import sys
import os
import pathlib
import traceback
target_path = pathlib.Path(os.path.abspath(__file__)).parents[3]
sys.path.append(target_path)


def main():
    params = EnvironmentParams()
    sock = Socket(params.HOSTNAME, params.PORT, params.SSL_ENABLED)
    irc = IrcClient(sock, params)
    modules = IrcModules({'modules': params.MODULES, 'client': irc })
    text = InputText(irc)
    sel = selectors.DefaultSelector()

    sel.register(sock.socket_handler, selectors.EVENT_READ, sock.recv)

    if not sock.connect():
        print("Error Trying to connect on {server}:{port}".format(server=params.HOSTNAME, port=params.PORT))
        sys.exit(0)

    irc.auth(modules=modules)

    try:

        fulldata = None

        while True:

            event = sel.select(0.1)

            if event:
                for key, mask in event:
                    callback = key.data
                    fulldata = callback(key.fileobj)
                if fulldata:
                    irc.bot_loop(fulldata)
                    irc.parse(fulldata)

    except Exception as ex:
        traceback.print_exc()
    finally:
        sock.exit_gracefully()