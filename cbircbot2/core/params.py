import os
import traceback

from cbircbot2.core.config import  Config
class EnvironmentParams:

    NICKNAME = "creekman"
    USERNAME = "creeka"
    IDENTD = "lame guy"
    CHANNEL = "#lamechannel"
    MODULES = "*"
    HOSTNAME = "irc.freenode.net"
    PORT = "6667"
    NICKSERV_IDENTIFY = False
    SSL_ENABLED = False
    ZEO_ADDRESS = "localhost"
    ZEO_PORT    = 9100
    

    def __init__(self):
        
        print(os.environ)

        if not self.check_environ_exists('CB_NICKNAME'):
            print("Error: username not found using default: "  + self.NICKNAME)
        else:
            self.NICKNAME = self.check_environ_exists('CB_NICKNAME')

        if not self.check_environ_exists('CB_USERNAME'):
            print("Error: username not found using default " + self.USERNAME)
        else:
            self.USERNAME = self.check_environ_exists('CB_USERNAME')

        if not self.check_environ_exists('CB_IDENTD'):
            print("Error: identd environment var not found")
        else:
            self.IDENTD = self.check_environ_exists('CB_IDENTD')

        if not self.check_environ_exists('CB_CHANNEL'):
            print("Error: channel environment var not found")
        else:
            self.CHANNEL= self.check_environ_exists('CB_CHANNEL')

        if not self.check_environ_exists('CB_MODULES'):
            print("Error: modules environment var not found")
        else:
            self.MODULES= self.check_environ_exists('CB_MODULES')

        if not self.check_environ_exists('CB_HOST') or not self.check_environ_exists('CB_HOSTNAME'):
            print("Warning: hostname environment var not found -  using default: " + self.HOSTNAME)
        else:
            self.HOSTNAME= self.check_environ_exists('CB_HOST')

        if not self.check_environ_exists('CB_PORT'):
            print("Warning: port environment var not found - using default: " + self.PORT)
        else:
            self.PORT = self.check_environ_exists('CB_PORT')

        if not self.check_environ_exists('CB_SSL'):
            print("Initializing without SSL connection!")
        elif int(os.environ['CB_SSL']) != int(0):
            self.SSL_ENABLED = True

        if not self.check_environ_exists('ZEO_ADDRESS'):
            print("ZEO Address default localhost")
        else:
            self.ZEO_ADDRESS = self.check_environ_exists('ZEO_ADDRESS')

        if not self.check_environ_exists('ZEO_PORT'):
            print('ZEO default port 9100')
        else:
            self.ZEO_PORT = self.check_environ_exists('ZEO_PORT')


    def check_environ_exists(self, key):
        try:
            return os.environ[key]
        except KeyError as key:
            print(key)
            return False

    def load_from_config(self, cfg):
        
        if type(cfg) is not Config:
            raise Exception("Config type is not a Valid Class!")
        
        if  not cfg.check_config_exists():
           cfg.write_conf()
           cfg.load()
        else:
           cfg.load()
           
        
        self.NICKNAME = cfg.get('NICK', 'nickname')
        self.IDENTD = cfg.get('NICK', 'identd')
        self.USERNAME = self.NICKNAME
        self.CHANNEL = cfg.get('CHANNEL', 'channel')
        self.HOSTNAME = cfg.get('SERVER', 'hostname')
        self.PORT = int(cfg.get('SERVER', 'port'))
        self.SSL_ENABLED = bool(cfg.get('SERVER', 'enable_ssl'))
        self.NICKSERV_IDENTIFY = bool(cfg.get('SERVER', 'enable_nickserv_identify'))
        
        #self.ZEO_ADDRESS = cfg.get('ZEO', 'host')
        #self.ZEO_PORT = cfg.get('ZEO', 'port')
        
        
        return
    