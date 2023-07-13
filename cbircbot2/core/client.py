import multiprocessing
import os
import sys

import cbircbot2.core.module_handler.irc_plugin_manager
from cbircbot2.core.auth import AuthClient
from cbircbot2.core.modules import IrcModules
import time
import logging
import re
from cbircbot2.core.module_handler import irc_plugin_manager
from dataclasses import dataclass
from typing import Any

logging.basicConfig(filename="log.txt")


@dataclass
class IrcMessageData:
    irc:object
    sender:str
    receiver:str
    identd:str
    message:str

class IrcClient(object):
    
    MAX_PROCESS: int = 4
    MAX_TASKS: int = 10
    MAX_JOIN_TRIES: int = 10
    
    def __init__(self, sock=None, params=None, *args, **kwargs):
        self.sock = sock
        self.params = params
        self.is_auth = False
        self.is_connected = False
        self.end_motd_detect = False
        self.is_joined = False
        self.auth_user = AuthClient(self)
        #self.modules: IrcModules = IrcModules(client=self)
        self.modules2: irc_plugin_manager.IRCPluginManager = irc_plugin_manager.IRCPluginManager(self)
        self.modules2.load()

        #self.modules.irc_client = self
        
        self.regex_list = {}
        self.compile_regexes()
    
    def compile_regexes(self):
        self.regex_list['privmsg'] = re.compile(r"^:(.+[aA-zZ0-9])!(.*) PRIVMSG (.+?) :(.+[aA-zZ0-9\\+\\-])$")
       #self.regex_list['valid_command'] = re.compile(f"^([?|!]\s)(.+[aA-zZ0-9]\s)(.+[aA-zZ0-9])$", re.IGNORECASE)
        self.regex_list['valid_command'] = re.compile(r"^([?|!]\s)(.+)$", re.IGNORECASE)

        
    def get_regex(self, name):
        if name not in self.regex_list:
            return None
        
        return self.regex_list[name]
    
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
    def write_error(message, *args, **kwargs):
        sys.stderr.write(f"ERROR: {message}\n")
        return
    @staticmethod
    def write_out(message):
        sys.stdout.write(f"OUT: {message}\n")
        return
    @staticmethod
    def sanitize_string(msg:str):
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
        #message = msg.decode(encoding="UTF-8", errors="strict")
        return msg
    

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
        data = msg #IrcClient.sanitize_string(msg)
        if data and data.find("PING") != -1 or data.startswith("PING") != -1:
            pong = data.split(':')[1]
            msg = f'PONG :{pong}'
            self.send(msg)
            print(msg)

    def detect_motd(self, msg):
        """detect if motd is found, end of the motd to start auto join and modules thread"""
        data = IrcClient.sanitize_string(msg)


        if data.find(':End of /MOTD') != -1 or data.find('/MOTD') != -1 and not self.end_motd_detect:
            self.end_motd_detect = True
            return True

        return False

    def output_data(self, msg):
        print(f"SERVER: {msg}", file=sys.stdout)
        
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
            while not self.is_joined and tries <= self.MAX_JOIN_TRIES:
                if tries == self.MAX_JOIN_TRIES:
                    print("Bot Exceeded Max Tries")
                    sys.exit(-1)
                self.join_channel(self.params.CHANNEL)
                print(f"tried {tries} times to join {self.params.CHANNEL}")
                time.sleep(2)
                tries += 1
        
        self.output_data(data)

    
    @classmethod
    def parse_messages(cls, client : Any, message: Any):
        
        msg = IrcClient.sanitize_string(message)
        
        if msg.find("PRIVMSG") == -1:
            return
       
        privmsg_regex = client.get_regex("privmsg")
        valid_msg = privmsg_regex.search(msg)
        
        if not valid_msg:
            return
        
        data = IrcMessageData(
            irc=client,
            sender=valid_msg.groups()[0],
            identd=valid_msg.groups()[1],
            receiver=valid_msg.groups()[2],
            message=valid_msg.groups()[3]
        )
        
        is_valid_command: Any = client.get_regex("valid_command")
        valid_cmd = is_valid_command.search(data.message)
        
        if not valid_cmd:
            IrcClient.write_out(f"{data.message} is Invalid Command!")
            return
        
        
        
        prefix = valid_cmd.groups()[0]
        cmd = valid_cmd.groups()[1].split(' ')
    
        cmd_dict = {
            'prefix': prefix,
            #'module': valid_cmd.group()[1],
            'command': cmd[0],
            'params' : cmd[1:],
            'client': client
        }
        
        if not cmd_dict.get("prefix") or not cmd_dict.get("command"):
            sys.stderr.write(f"{data.message} -> Malformed Command")
            return
        c : cbircbot2.core.module_handler.irc_plugin_manager.IRCPluginManager = client.irc.modules2
        #client.modules2.issue_command(**cmd_dict)
        c.issue_command(**cmd_dict)
        
        
        return

    @classmethod
    def process_private_message(cls, irc, msg):

        msg = IrcClient.sanitize_string(msg)
        
        if msg.find('PRIVMSG') != -1:
    
            is_message = re.search(r"^:(.+[aA-zZ0-9])!(.*) PRIVMSG (.+?) :(.+[aA-zZ0-9\\+\\-])$", msg)
            if not is_message:
                return
            
            data = {
                'client': irc,
                'sender': is_message.groups()[0],  # sender's nickname
                'ident': is_message.groups()[1],  # ident
                'receiver': is_message.groups()[2],  # channel or receiver's nickname
                'message': is_message.groups()[3],  # message
            }
            
            #broadcast all messages before tests
            irc.modules.broadcast_message_all_modules(**data)
            if not data['message'].startswith("?"):
                return

            command_regex = re.compile(r"^([?|!|@]\s)(.+[aA-zZ0-9]\s)(.+[aA-zZ0-9])$", re.IGNORECASE)
            is_valid_command = command_regex.search(data['message'])
            print(is_valid_command.groups())
            
            if not is_valid_command:
                return

            msg = {
                'prefix': is_valid_command.groups()[0].strip(),
                'module': is_valid_command.groups()[1].strip(),
                'command': is_valid_command.groups()[2].strip()
            }
            
            print(f"Command Issued: {msg}")
   
            try:
                module = msg['module'].lower()
                command = msg['command'].lower()
            except IndexError as index_error:
                print(f"invalid or malformed command {index_error}")
                return
    
            module_instance = None
            
            try:
                if not irc.modules:
                    return
                
                if module in irc.modules.module_instances_list:
                    module_instance = irc.modules.get_module_instance(module)
                
                if not module_instance:
                    print(f"{module} cannot be loaded")
                    return

                if command in module_instance.registered_commands:
                    module_instance.registered_commands[command].run(module_instance, full_command=msg, client=irc, data=data)
            except Exception as ex:
                print(f"Error: {ex}")
                return
    # MULTIPROCESSING CALLBACK ALERT
    
    @classmethod
    def process_modules_worker(cls, queue: multiprocessing.JoinableQueue) -> None:
        
        while True:
            if queue.empty():
                continue
                
            q = queue.get_nowait()
            irc: IrcClient = q[0]
            message:str = q[1]
            sys.stdout.write(f"QUEUE: {q}")
            
            if not message:
                continue
                
            #irc.process_private_message(irc, message)
            irc.parse_messages(irc, message)
            queue.task_done()
