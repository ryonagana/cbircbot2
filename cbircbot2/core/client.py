from multiprocessing import Queue, Process, Pool

import cbircbot2.core.client
from cbircbot2.core.auth import AuthClient
from cbircbot2.core.modules import IrcModules
import time
import logging
from typing import Any
import threading
import re
from contextlib import suppress
logging.basicConfig(filename="log.txt")


class IrcClient(object):
    
    MAX_PROCESS: int = 4
    MAX_TASKS: int = 10
    
    def __init__(self, sock=None, params=None, *args, **kwargs):
        self.sock = sock
        self.params = params
        self.is_auth = False
        self.is_connected = False
        self.end_motd_detect = False
        self.is_joined = False
        self.modules: IrcModules
        self.auth_user = AuthClient(self)
 

    def set_modules(self, module_class: IrcModules):
        self.modules = module_class
        
    def get_socket(self):
        """ :return: the connected socket from Socket class (built in socket) """

        return self.sock.get_sock()

    def send(self, message) -> None:
        """
        :param message: send a message to the server
        :return: None
        """
        if not self.sock.socket_connected:
            return
        self.sock.send(IrcClient.format_msg(message))
        time.sleep(0.3)

    @staticmethod
    def format_msg(msg):
        if msg.find("\r\n") == -1:
            return "{0}\r\n".format(msg)
        return msg

    @staticmethod
    def sanitize_string(msg):
        """
        :param msg: get the message data
        :return: stripped carriage return from server
        """
        if msg.find('\r\n') != -1 or msg.find('\n'):
            return msg.strip()
        return msg

    @staticmethod
    def convert_utf8(msg):
        """
        
        :param msg: binary string from server
        :return: a decoded utf-8 string
        """
        return msg.decode('utf-8')
    
    def add_queue(self, data:Any = None) -> None:
        """
        adds the message to the queue for posterior processing
        
        :param data: get the data from connected SERVER string only, other types will be ignored
        :return: None
        """
        self.modules_queue.put(data)

    def msg_to(self, receiver, message):
        self.send("PRIVMSG {0} :{1}".format(receiver, message))


    def msg_to_channel(self, channel, message):

        self.send("PRIVMSG {0} :{1}".format(channel, message))

    def join_channel(self, channel):
        self.send("JOIN {0}".format(channel))
        self.is_joined = True

    def auth(self, **kwargs):
        if "modules" in kwargs:
            self.modules = kwargs["modules"]

        self.send("NICK {0}".format(self.params.NICKNAME))
        self.send("USER {0} {1} * :{2}".format(self.params.NICKNAME, self.params.HOSTNAME, self.params.IDENTD))

    def heartbeat(self, msg):
        data = IrcClient.convert_utf8(msg)
        if data and data.find("PING") != -1 or data.startswith("PING") != -1:
            pong = data.split(':')[1]
            msg = f'PONG :{pong}'
            self.send(msg)
            print(msg)

    def detect_motd(self, msg :str):
        """detect if motd is found, end of the motd to start auto join and modules thread"""
        data = IrcClient.convert_utf8(msg)

        if data.find(':End of /MOTD') != -1 or data.find('/MOTD') != -1 and not self.end_motd_detect:
            self.end_motd_detect = True
            return True

        return False

    def output_data(self, msg):
        print(IrcClient.convert_utf8(msg))
        
    def bot_loop(self, data:str = ""):

        
        # do ping pong check
  
        self.heartbeat(data)
        

        if self.detect_motd(data):
            # change flag to connected
            self.is_connected = True
            print("CONNECTED")
            self.auth_user.do_auth()
            time.sleep(1)

            # try to join a channel
            tries: int = 1
            while not self.is_joined and  tries <= 5:
                self.join_channel(self.params.CHANNEL)
                print(f"tried {tries} times to join {self.params.CHANNEL}")
                time.sleep(2)
                tries += 1
        
        
        
        self.output_data(data)

    

    def process_private_message(self, modules, msg: str):
        print("PROCESSA MSG")
        
        msg = IrcClient.sanitize_string(IrcClient.convert_utf8(msg))
        
        if msg.find('PRIVMSG') != -1:
    
            is_message = re.search("^:(.+[aA-zZ0-9])!(.*) PRIVMSG (.+?) :(.+[aA-zZ0-9\\+\\-])$", msg)
            if not is_message:
                return
        
    
            data = {
                'client': self,
                'sender': is_message.groups()[0],  # sender's nickname
                'ident': is_message.groups()[1],  # ident
                'receiver': is_message.groups()[2],  # channel or receiver's nickname
                'message': is_message.groups()[3],  # message
            }

            modules.broadcast_message_all_modules(**data)
            if not data['message'].strip("").startswith("?"):
                return
            
            self.msg_to_channel(self.params.CHANNEL, f"Oi {data['sender']}. Meus Modulos estão desativados, prometo que logo vou consertar, desculpe o transtorno")
            time.sleep(10)
        
                

            
            """
            msg = data['message'].strip("").split(" ")
            module = msg[1]
            command = msg[2]
            module_instance = None
            
            try:
                if not modules:
                    return
                
                module_instance = modules.get_module_instance(module)
                
                if not module_instance:
                    print(f"{module} cannot be loaded")
                    return
            except Exception as ex:
                print(f"Error: {ex}")

            if command in module_instance.registered_commands:
                module_instance.registered_commands[command].run(module_instance, full_command=msg, client=self, data=data)
            """

    # MULTIPROCESSING CALLBACK ALERT

    def process_modules_worker(self, modules, queue: Queue) -> None:
        print("PROCESSA MODULES")
        message = queue.get()
        if message:
            self.process_private_message(modules, message)
            time.sleep(0.3)
"""
        while True:
            msg = queue_in.get()
            
            if not msg:
                continue

            if msg.find('PRIVMSG') != -1:
                is_message = re.search("^:(.+[aA-zZ0-9])!(.*) PRIVMSG (.+?) :(.+[aA-zZ0-9\\+\\-])$", msg)
                
                if is_message:

                    data = {
                        'client': irc,
                        'sender': is_message.groups()[0],  # sender's nickname
                        'ident': is_message.groups()[1],  # ident
                        'receiver': is_message.groups()[2],  # channel or receiver's nickname
                        'message': is_message.groups()[3],  # message
                    }

                    irc.modules.broadcast_message_all_modules(**data)

                    if not data['message'].strip("").startswith("?"):
                        continue

                    msg = data['message'].strip("").split(" ")
                    
                    with suppress(IndexError):
                        prefix = msg[0]
                        module = msg[1]
                        command = msg[2]
                        params = data['message'].split(" ")[3:]
 
                    with suppress(Exception):
                        module_instance = irc.modules.get_module_instance(module)
                        if not module_instance:
                            continue

                        if command in module_instance.registered_commands:
                            module_instance.registered_commands[command].run(module_instance, full_command=msg, client=irc, data=data)
                            
            queue_in.task_done()
            time.sleep(0.1)


    ## END MULTIPROCESSING CALLBACK ALERT

    ##remember to decode to utf8 and strip \r\n from the messages


    def list_users(self):
        self.send("NAMES {0}".format(self.params.CHANNEL))

"""
