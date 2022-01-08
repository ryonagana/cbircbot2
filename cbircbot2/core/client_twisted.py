from copy import Error
from multiprocessing import Pool, managers
from multiprocessing.queues import JoinableQueue
from queue import Empty
import sys
import os
import multiprocessing
import re
import traceback
from types import NoneType


from twisted.words.protocols import irc
from twisted.internet import protocol, reactor

from cbircbot2.core.config import Config
from cbircbot2.core.modules import IrcModules
from typing import Any, Optional
from cbircbot2.core.params import EnvironmentParams

class IRCClientTwisted(irc.IRCClient):    

    command_regex = None

    def __init__(self, config:Optional[Config] = None) -> None:
        self.params = None
        self.config = None
        self.nickname = config.get("NICK","nickname")
        self.modules = None
        self.command_regex =  re.compile(r"^([?|!]\s)(.+[aA-zZ0-9]\s)(.+[aA-zZ0-9])$", re.IGNORECASE)
        super().__init__()

    def connectionMade(self):
        irc.IRC.connectionMade(self)
        return super().connectionMade()

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        return super().connectionLost(reason)

    def signedOn(self):
        self.join(self.factory.channel)
        return super().signedOn()

    def privmsg(self, user, channel, message):
        #print(f"{user}-{channel}:{message}")
        #self.queue.put((self, user, channel, message,))

        data = {
            'client': self,
            'sender': user,  # sender's nickname
            'ident':  None,  # ident
            'receiver': channel,  # channel or receiver's nickname
            'message':  message,  # message
        }

        self._parse_private_message(**data)
        print(f"<{user}@<{channel}>:{message}")
        return super().privmsg(user, channel, message)


    def _parse_private_message(self,**kwargs):
        command_data = None
        msg_data = None
        module_instance = None
        
        try:
            msg_data = kwargs['message']
            
            if not msg_data:
                return
            

            valid_cmd = self.command_regex.match(msg_data)

            print(valid_cmd)

            if not valid_cmd:
                print (f"{msg_data} not valid cmd")
                return

            command_data = {
                    'prefix':  valid_cmd.groups()[0].strip().lower(),
                    'module':  valid_cmd.groups()[1].strip().lower(),
                    'command': valid_cmd.groups()[2].strip().lower()
            }


   
        except AttributeError as attribute_error:
            print(f"malformed command Exception: {attribute_error}")
            traceback.print_exc()
        except IndexError as index_error:
            print(f"command internals not found Exception {index_error} ")
            traceback.print_exc()



        """
        try:
            for m in self.modules.module_instances_list:
                module_instance = self.modules.get_module_instance(m)

                if not module_instance:
                    print("Module {m} not loaded!")
                    continue

                for cmd in module_instance.registered_commands:
                    module_instance.registered_commands[cmd].run(module_instance, full_command=command_data, client=self, data=kwargs)
        except Exception as e:
            print(f"Invalid Module - Exception: {e}")
            traceback.print_exc()
        """

    def msg_to_channel(self, sender, msg):
        self.msg_to_channel(sender, msg)
        return
    
    def msg_to(self, sender, msg):
        self.msg(sender, msg)
    

class BotFactory(protocol.ClientFactory):


    protocol = IRCClientTwisted

    def __init__(self, config:Optional[Config] = None) -> None:
        self.hostname = config.get("SERVER",'hostname')
        self.port = int(config.get("SERVER",'port'))
        self.nick = config.get("NICK",'nickname')
        self.name = config.get("NICK",'identd')
        self.channel  = config.get("CHANNEL",'channel')
        self.passwd = config.get("NICK","password")
        self.config = config
        self.irc = self.protocol(self.config)
        super().__init__()

    def buildProtocol(self, addr=None):
        self.irc.factory = self
        self.irc.params = EnvironmentParams()
        self.irc.config = self.config
        self.irc.config.load()
        self.irc.params.load_from_config(self.irc.config)
        self.irc.modules = IrcModules(client=self.irc)

        self.irc.modules.irc_client = self.irc
        return  self.irc

    def clientConnectionLost(self, connector, reason):
        connector.connect()
        return super().clientConnectionLost(connector, reason)

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()
        print(f"Connector Stopped {reason}")

        return super().clientConnectionFailed(connector, reason)


