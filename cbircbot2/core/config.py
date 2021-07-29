import configparser
import traceback


class Config:
    DEFAULT_CONF = {
           'SERVER': {
                'hostname': 'irc.libera.chat',
                'port': 6667,
                'enable_ssl': False,
               
            },
           'CHANNEL': {
                'channel': "#defaultchan"
            
            },
           'NICK': {
            'identd': 'Its a Me',
            'nickname': 'pythonbot',
            'password': '',
            'enable_nickserv_identify': False
            },
        'MODULE_OPTS': {
                'openweather_api':''
            },
        'ZEO': {
            'db': 'd',
            'host': 'localhost',
            'port': 9100
        }
}

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config['SERVER'] = self.DEFAULT_CONF['SERVER']
        self.config['CHANNEL'] = self.DEFAULT_CONF['CHANNEL']
        self.config['NICK'] = self.DEFAULT_CONF['NICK']
        self.config['MODULE_OPTS'] = self.DEFAULT_CONF['MODULE_OPTS']
        self.config['ZEO'] = self.DEFAULT_CONF['ZEO']
    
    def write_conf(self):
        with open('config.conf',"w") as fp:
            self.config.write(fp)
            
    def load(self) -> object:
        if not self.config.read("config.conf"):
            raise Exception("Config.conf not found!")
        
        return self.config
        
    def set(self, group, key, value) -> bool:
        
        if not self.config.set(group,key,value):
            raise Exception("Config Section: {0} and {1} key not found!".format(group,key))
        return True
    
    def get(self, group: str, key: str) -> str:
        if not self.config.get(group, key):
            raise Exception("Config Section: {0} and {1} key not found!".format(group,key))
        
        val = self.config.get(group, key)
        return val
    
    def get_bool(self, section: str, key: str) -> bool:
        return self.config.getboolean(section, key)
    
    def check_config_exists(self):
        found = False
        try:
            with open("config.conf","r") as fp:
                found = True
        except IOError as err:
            print(err)
        
        return found
    
    def print_cfg(self) -> None:
        
        for section in self.config.sections():
            for keys in self.config[section]:
                print("Section:{0} -> {1} : {2}".format(section, keys, self.config[section][keys]))