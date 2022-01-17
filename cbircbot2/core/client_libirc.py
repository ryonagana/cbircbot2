import os
import sys
import irc.bot
import irc.strings

from cbircbot2.core.config import Config
from cbircbot2.core.modules import IRCModules
from typings import Optional, Any

class IRCClientProtocol(irc.bot.SingleServerIrcBot):
    def __init__(self, config:Optional[Config] = None):
        self.hostname = config.get("SERVER","hostname")
        self.port = int(config.get("SERVER","port"))
        self.nick = config.get("NICK","nickname")
        self.identd = config.get("NICK","identd")
        self.name = self.identd
        self.channel = config.get("CHANNEL", "channel")
        self.passwd - config.get("NICK", "password")
        self.config = config
        self()__init__((self.hostname,self.port),self.nick,self.name)

            self()__init__((self.hostname,self.port),self.nick,self.name)
            
        def msg_to_channel(self,sender, msg):
            pass

        def msg_to(self, sender, msg):
            pass
    

        

    
    
        

            

                
