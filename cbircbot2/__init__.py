from  cbircbot2.core.sockets import  Socket
from cbircbot2.core.params import  EnvironmentParams
from cbircbot2.core.client import IrcClient
from cbircbot2.core.modules import IrcModules
import multiprocessing

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

    while 1:
        try:
            data = sock.recv(2048)
            irc.bot_loop(data)
            irc.parse(data)
        except sock.socket_handler.error:
            print("bot interrupted by signal (CTRL+C)")
            break


def main():
    params = EnvironmentParams()
    sock = Socket(params.HOSTNAME, params.PORT)
    irc = IrcClient(sock, params)
    modules = IrcModules({'modules': params.MODULES, 'client': irc })

    process = multiprocessing.Process(target=mainloop, kwargs={'sock': sock,
                                                               'params': params,
                                                               'irc': irc,
                                                               'modules': modules
                                                               }
                                     )
    #process.daemon = True
    process.start()


    while process.is_alive():
        if not process.is_alive():
            break
    process.join()
    sock.exit_gracefully()
