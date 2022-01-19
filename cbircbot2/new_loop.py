from cbircbot2.core.client_libirc import IRCClientProtocol
from cbircbot2.core.config import Config
from cbircbot2.core.params import EnvironmentParams 
import traceback

def main():


    cfg = Config()
    cfg.load()
    params = EnvironmentParams()
    params.load_from_config(cfg)

    irc = IRCClientProtocol(cfg, params)
    irc.start()
    pass


"""
from cbircbot2.core.client_twisted import BotFactory
from cbircbot2.core.config import Config
import sys

import traceback
from twisted.internet import reactor
from twisted.python import log

def main():
    config = Config()
    config.load()
    try:
        conn = BotFactory(config)
        
        log.startLogging(sys.stdout)
        reactor.connectTCP(conn.hostname, conn.port, conn)
        reactor.run()
    except Exception as e:
        print(f"Exception: {e}")
        traceback.print_exc()
        reactor.stop()
        
        if conn.irc.processing.is_alive():
            conn.irc.processing.join()
        
        raise SystemExit()
"""
    
