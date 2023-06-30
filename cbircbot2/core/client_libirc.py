import os
import sys
import irc.bot
import irc.strings

from cbircbot2.core.config import Config
from cbircbot2.core.modules import IrcModules
from cbircbot2.core.params import EnvironmentParams 
from typing import Optional, Any
from cbircbot2.core.fancy_module_handler import irc_plugin_manager
class IRCClientProtocol(irc.bot.SingleServerIRCBot):
    def __init__(self, config:Optional[Config] = None, params:Optional[EnvironmentParams] = None ):
        IRCClientProtocol.__init__(self)
        
        self.hostname = config.get("SERVER","hostname")
        self.port = int(config.get("SERVER","port"))
        self.nick = config.get("NICK","nickname")
        self.identd = config.get("NICK","identd")
        self.name = self.identd
        self.channel = config.get("CHANNEL", "channel")
        self.passwd = config.get("NICK", "password")
        self.config = config
        self.modules = IrcModules(client=self)
        self.modules_new = irc_plugin_manager.IRCPluginManager(self)
        self.params = params
        self().__init__((self.hostname,self.port),self.nick,self.name)
            
        def msg_to_channel(self,sender, msg):
            pass

        def msg_to(self, sender, msg):
            pass
    

        

    
    
        

            

                
