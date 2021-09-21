import os
import traceback

from cbircbot2.core.config import Config


class EnvironmentParams:
    NICKNAME: str = "creekman"
    USERNAME: str = "creeka"
    IDENTD: str = "lame guy"
    CHANNEL: str = "#lamechannel"
    CHANNEL_PASSWD: str = ""
    MODULES : str = "*"
    HOSTNAME : str = "irc.freenode.net"
    PORT : int = 6667
    NICKSERV_IDENTIFY : bool = False
    SSL_ENABLED : bool = False
    ZEO_ADDRESS : str = "localhost"
    ZEO_HOST : str = "localhost"
    ZEO_PORT : str = 9100
    ZEO_DB : str = "d"
    OPENWEATHER_API=""
    
    def __init__(self) -> None:
        
        if not self.check_environ_exists('CB_NICKNAME'):
            print(f"Error: username not found using default: {self.NICKNAME}")
        else:
            self.NICKNAME = self.check_environ_exists('CB_NICKNAME')
        
        if not self.check_environ_exists('CB_USERNAME'):
            print(f"Error: username not found using default {self.USERNAME}")
        else:
            self.USERNAME = self.check_environ_exists('CB_USERNAME')
        
        if not self.check_environ_exists('CB_IDENTD'):
            print("Error: identd environment var not found")
        else:
            self.IDENTD = self.check_environ_exists('CB_IDENTD')
        
        if not self.check_environ_exists('CB_CHANNEL'):
            print("Error: channel environment var not found")
        else:
            self.CHANNEL = self.check_environ_exists('CB_CHANNEL')
        
        if not self.check_environ_exists('CB_CHANNEL_PASSWD'):
            print("Error: channel environment var not found")
        else:
            self.CHANNEL_PASSWD = self.check_environ_exists('CB_CHANNEL_PASSWD')
        
        if not self.check_environ_exists('CB_MODULES'):
            print("Error: modules environment var not found")
        else:
            self.MODULES = self.check_environ_exists('CB_MODULES')
        
        if not self.check_environ_exists('CB_HOST') or not self.check_environ_exists('CB_HOSTNAME'):
            print(f"Warning: hostname environment var not found -  using default: {self.HOSTNAME}")
        else:
            self.HOSTNAME = self.check_environ_exists('CB_HOST')
        
        if not self.check_environ_exists('CB_PORT'):
            print(f"Warning: port environment var not found - using default: {self.PORT}")
        else:
            self.PORT = int(self.check_environ_exists('CB_PORT'))
        
        if not self.check_environ_exists('CB_SSL'):
            print("Initializing without SSL connection!")
        elif int(os.environ['CB_SSL']) != int(0):
            self.SSL_ENABLED = True
        
        if not self.check_environ_exists('ZEO_HOST'):
            print("ZEO hostname default localhost")
        else:
            self.ZEO_HOST = self.check_environ_exists('ZEO_ADDRESS')
        
        if not self.check_environ_exists('ZEO_PORT'):
            print('ZEO default port 9100')
        else:
            self.ZEO_PORT = self.check_environ_exists('ZEO_PORT')
    
    def check_environ_exists(self, key: str):
        try:
            return os.environ[key]
        except KeyError as key:
            print(f"Environ variable {key} doesnt exists!")
            return ""
    
    def load_from_config(self, cfg: Config) -> None:
        """
        :type cfg: object
        """
        if type(cfg) is not Config:
            raise Exception("Config type is not a Valid Class!")
        
        if not cfg.check_config_exists():
            cfg.write_conf()
            cfg.load()
        else:
            cfg.load()
        
        self.NICKNAME = str(cfg.get('NICK', 'nickname'))
        self.IDENTD = str(cfg.get('NICK', 'identd'))
        self.USERNAME = self.NICKNAME
        self.CHANNEL = str(cfg.get('CHANNEL', 'channel'))
        self.CHANNEL_PASSWD = str(cfg.get('CHANNEL', 'passwd'))
        self.HOSTNAME = str(cfg.get('SERVER', 'hostname'))
        self.PORT = int(cfg.get('SERVER', 'port'))
        self.SSL_ENABLED = cfg.get_bool('SERVER', 'enable_ssl')
        self.NICKSERV_IDENTIFY = cfg.get_bool('NICK', 'enable_nickserv_identify')
        self.ZEO_DB = str(cfg.get('ZEO', 'db'))
        self.ZEO_HOST = str(cfg.get('ZEO', 'host'))
        self.ZEO_PORT = int(cfg.get('ZEO', 'port'))
        self.OPENWEATHER_API = str(cfg.get('MODULE_OPTS', 'openweather_api'))
        return
