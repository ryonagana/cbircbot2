from  cbircbot2.core.sockets import  Socket
from cbircbot2.core.params import  EnvironmentParams
from cbircbot2.core.client import IrcClient
from cbircbot2.core.modules import IrcModules
from cbircbot2.core.input import InputText
import multiprocessing
import sys

def mainloop(*args, **kwargs):

    sock = None

    if not 'sock' in kwargs:
        print('error in mainloop invalid socket!')

    if not 'params' in kwargs:
        print('error trying to get parameters')

    if not "modules" in kwargs:
        print('modules loaded incorrectly!')

    params = kwargs['params']
    sock = kwargs['sock']
    irc = kwargs['irc']
    modules = kwargs["modules"]



    if sock.connect():
        print('Connection Success to {0}:{1} !'.format(params.HOSTNAME, params.PORT))

    irc.auth(modules=modules)

    while True:
        data = sock.recv(4096)
        irc.bot_loop(data)
        irc.parse(data)


def main():
    params = EnvironmentParams()
    sock = Socket(params.HOSTNAME, params.PORT, params.SSL_ENABLED)
    irc = IrcClient(sock, params)
    modules = IrcModules({'modules': params.MODULES, 'client': irc })
    text = InputText(irc)

    process = multiprocessing.Process(target=mainloop, kwargs={'sock': sock,
                                                               'params': params,
                                                               'irc': irc,
                                                               'modules': modules
                                                               }
                                     )
    #process.daemon = True
    process.start()
    process.join()

    while process.is_alive():

        #msg = input('>>>')
        #if msg:
        #    text.queue.put(msg)

        if not process.is_alive():
            process.terminate()
            break
    sock.exit_gracefully()