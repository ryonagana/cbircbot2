import os
import configparser
import  traceback

class Config:
    DEFAULT_CONF = {
           'SERVER' : {
                'hostname': 'irc.libera.chat',
                'port' : 6667,
                'enable_ssl' : False,
               
    },
           'CHANNEL' : {
                'channel' : "#defaultchan"
            
    },
           'NICK' : {
            'identd' : 'Its a Me',
            'nickname' : 'pythonbot',
            'password': '',
            'enable_nickserv_identify' : False
    },
            'MODULE_OPTS': {
                'openweather_api' : ''
    },
    'ZEO' : {
            'host' : 'localhost',
            'port' : 9100
        }
}

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config['SERVER'] = self.DEFAULT_CONF['SERVER']
        self.config['CHANNEL'] = self.DEFAULT_CONF['CHANNEL']
        self.config['NICK'] = self.DEFAULT_CONF['NICK']
        self.config['MODULE_OPTS'] = self.DEFAULT_CONF['MODULE_OPTS']
    
    def write_conf(self):
        with open('config.conf',"w") as fp:
            self.config.write(fp)
            
    def load(self):
        if not self.config.read("config.conf"):
            print("config ini not found")
            return
        
        return self.config
        
    def set(self, group, key, value):
        try:
            self.config[group][key] = value
        except KeyError as k:
            traceback.print_exc()
    
    def get(self, group, key):
        try:
            return self.config[group][key]
        except KeyError as k:
            traceback.print_exc()
        return None
    
    def check_config_exists(self):
        found = False
        try:
            with open("config.conf","r") as fp:
                found = True
        except IOError as err:
            pass
        
        return found
