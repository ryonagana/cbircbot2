from copy import Error
from multiprocessing import Pool, managers
from multiprocessing.queues import JoinableQueue
from queue import Empty, Queue
import sys
import os
import multiprocessing
import re
import traceback


from twisted.words.protocols import irc
from twisted.internet import protocol, reactor

from cbircbot2.core.config import Config
from cbircbot2.core.modules import IrcModules
from typing import Any, Optional
from cbircbot2.core.params import EnvironmentParams

class IRCClientTwisted(irc.IRCClient):

    command_regex = None

    def __init__(self, config:Optional[Config] = None) -> None:
        self.params = EnvironmentParams()
        self.config = config
        self.nickname = config.get("NICK","nickname")
        self.params.load_from_config(config)
        self.modules = IrcModules(client=self)
        self.command_regex =  re.compile(r"^([?|!]\s)(.+[aA-zZ0-9]\s)(.+[aA-zZ0-9])$", re.IGNORECASE)
        
        self.manager = multiprocessing.Manager()
        self.queue = self.manager.Queue()
        self.processing = multiprocessing.Process(target=self.message_worker, args=(self.queue,))
        self.processing.start()
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
        print(f"{user}-{channel}:{message}")
        #self.queue.put((self, user, channel, message,))
        
   
        data = self.manager.dict({
            'sender': user,  # sender's nickname
            'ident':  "",  # ident
            'receiver': channel,  # channel or receiver's nickname
            'message':  message,  # message
        })
        
        self._parse_private_message(data)
        

        #print(f"<{user}@<{channel}>:{message}")
        
        return super().privmsg(user, channel, message)


    def _parse_private_message(self, data_args):

        msg_data = None

        
        try:
            msg_data = data_args['message']
            
            if not msg_data:
                return
            

            valid_cmd = self.command_regex.match(msg_data)

            

            if not valid_cmd:
                print (f"{msg_data} not valid cmd")
                return

            command_data = self.manager.dict({
                'prefix':  valid_cmd.groups()[0].strip().lower(),
                'module':  valid_cmd.groups()[1].strip().lower(),
                'command': valid_cmd.groups()[2].strip().lower(),
                'full_cmd': data_args,
            })
            
            
         
            
            self.queue.put(command_data, block=False)


   
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
        return 
    
    

    def message_worker(self, queue:Optional[Queue] = None):
        
        try:
            while True:
                if queue.empty():
                    continue
                
                data = queue.get()

                
                
                try:
                    for m in self.modules.module_instances_list:
                        mod = self.modules.get_module_instance(m)
                        
                        command_exists = mod.command_exists("hello")
                        print(f"{mod.registered_commands}")
                            
                        
                except Exception as e:
                    print(f"QUEUE Exception: {e}")
                    continue
                
                
        except Exception as e:
            if self.processing.is_alive():
                self.processing.join()
                self.processing.close()
              
                
            print("Restarting Working Service..")
            self.processing.start()
                
    
    
    

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


