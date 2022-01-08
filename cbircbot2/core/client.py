import multiprocessing
import os
import sys
from cbircbot2.core.auth import AuthClient
from cbircbot2.core.modules import IrcModules
import time
import logging
import re
logging.basicConfig(filename="log.txt")


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
        self.modules: IrcModules = IrcModules(client=self)

        self.modules.irc_client = self
 

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
        data = IrcClient.sanitize_string(msg)
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

            command_regex = re.compile(r"^([?|!]\s)(.+[aA-zZ0-9]\s)(.+[aA-zZ0-9])$", re.IGNORECASE)
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

            print(f"{os.getpid()}")
            q = queue.get_nowait()
            
            irc: IrcClient = q[0]
            message:str = q[1]
            
            if not message:
                continue
                
            irc.process_private_message(irc, message)
            queue.task_done()
