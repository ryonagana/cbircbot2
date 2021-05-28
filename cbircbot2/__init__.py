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
import  signal
import time
import threading
import logging
import cbircbot2.core.config
import getopt
target_path = pathlib.Path(os.path.abspath(__file__)).parents[3]
sys.path.append(target_path)




console_enable = False
ssl_enable = False

def console_handler(sig, frame):
    global console_enable
    console_enable = not console_enable



def background_console(irc, modules):
    while True:

        try:
            opt = input(">>> ")

            module_name,command_name, params_cmd = opt.split()
            print(opt)
            print(module_name, command_name, params_cmd)
            continue

            if module_name.lower() in  modules.module_instances_list[module_name.lower()]:
                mod = modules.module_instances_list[module_name.lower()]
                dir(mod)
            print("cmd ", opt)
            time.sleep(0.8)



        except Exception as e:
            pass




def main():
    cfg = cbircbot2.core.config.Config()
    global  ssl_enable
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:v", ['ssl'])
    except getopt.GetoptError as ge:
        sys.exit(2)
        
    for opt,a, in opts:
        if opt  in ('-s', '--ssl'):
            ssl_enable = True
            cfg.set('SERVER', 'enable_ssl', ssl_enable)

    params = EnvironmentParams()
    print(params.SSL_ENABLED)
    params.load_from_config(cfg)
    sock = Socket(params.HOSTNAME, params.PORT, False) #force false while im fixing
    irc = IrcClient(sock, params)
    modules = IrcModules(modules=params.MODULES, client=irc)
    text = InputText(irc)

    sel = selectors.DefaultSelector()
    sel.register(sock.socket_handler, selectors.EVENT_READ, sock.recv)

    if not sock.connect():
        print("Error Trying to connect on {server}:{port}".format(server=params.HOSTNAME, port=params.PORT))
        sys.exit(0)

    irc.auth(modules=modules)

    closed = False

    try:

        fulldata = None

        while not closed:

            event = sel.select(0.1)

            if event:
                for key, mask in event:
                    callback = key.data
                    fulldata = callback(key.fileobj)
                if fulldata:
                    irc.bot_loop(fulldata)
                    irc.parse(fulldata)
                else:
                    closed = True

    except KeyboardInterrupt as ex:
        msg = traceback.print_exc()
        logging.critical(msg)

    finally:

        modules.end_all_modules()
        sock.exit_gracefully()

    irc.modules_process.join()