import getopt
import logging
import os
import pathlib
import selectors
import sys
import traceback

import cbircbot2.core.config
from cbircbot2.core.client import IrcClient
from cbircbot2.core.input import InputText
from cbircbot2.core.modules import IrcModules
from cbircbot2.core.params import EnvironmentParams
from cbircbot2.core.sockets import Socket

target_path = pathlib.Path(os.path.abspath(__file__)).parents[3]
sys.path.append(target_path)
ssl_enable = False


def main():
    cfg = cbircbot2.core.config.Config()
    global ssl_enable


    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:v", ['ssl'])
    except getopt.GetoptError as ge:
        sys.exit(2)
    
    for opt, a, in opts:
        if opt in ('-s', '--ssl'):
            ssl_enable = True
            cfg.set('SERVER', 'enable_ssl', ssl_enable)
    
    params = EnvironmentParams()
    params.load_from_config(cfg)
    ssl_enable = params.SSL_ENABLED
    cfg.print_cfg()
    
    print(params.SSL_ENABLED)
    params.load_from_config(cfg)
    sock = Socket(params.HOSTNAME, params.PORT, ssl_enable)  # force false while im fixing
    irc = IrcClient(sock, params)
    modules = IrcModules(modules=params.MODULES, client=irc)
    # text = InputText(irc)
    # print(text)
    sel = selectors.DefaultSelector()
    sel.register(sock.socket_handler, selectors.EVENT_READ, sock.recv)
    
    if not sock.connect():
        print("Error Trying to connect on {server}:{port}".format(server=params.HOSTNAME, port=params.PORT))
        sys.exit(0)
    
    irc.auth(modules=modules)
    
    closed = False
    
    try:
        
        data = None
        
        while not closed:
            
            event = sel.select(0.1)
            
            if event:
                for key, mask in event:
                    callback = key.data
                    data = callback(key.fileobj)
                if data:
                    irc.bot_loop(data)
                    irc.parse(data)
                else:
                    closed = True
    
    except KeyboardInterrupt as ex:
        msg = traceback.print_exc()
        logging.critical(msg)
    
    finally:
        modules.end_all_modules()
        sock.exit_gracefully()
    
    irc.modules_process.join()
