import os
import sys
import multiprocessing as mp
import re
from cbircbot2.core.auth import AuthClient
import time

class IrcClient:
    def __init__(self, sock=None, params=None, *args, **kwargs):
        self.sock = sock
        self.params = params

        self.is_auth = False
        self.is_connected = False
        self.end_motd_detect = False
        self.is_joined = False
        self.modules = None
        self.auth_user = AuthClient(self)

        self.modules_queue = mp.Queue()

    def send(self, message):
        if not self.sock:
            return
        self.sock.send(IrcClient.format_msg(message))

    @staticmethod
    def format_msg(msg):
        if msg.find("\r\n") == -1:
            return "{0}\r\n".format(msg)
        return msg

    @staticmethod
    def sanitize_string(msg):
        if msg.find('\r\n') != -1:
            return msg.strip()
        return msg

    @staticmethod
    def convert_utf8(msg):
        return msg.decode('utf-8')

    def msg_to(self, receiver, message):
        self.send("PRIVMSG {0} :{1}".format(receiver, message))

    def msg_to_channel(self, channel, message):

        self.send("PRIVMSG {0} :{1}".format(channel, message))

    def join_channel(self, channel):

        self.send("JOIN {0}".format(channel))

    def auth(self, **kwargs):
        if "modules" in kwargs:
            self.modules = kwargs["modules"]

        self.send("NICK {0}".format(self.params.NICKNAME))
        self.send("USER {0} {1} * :{2}".format(self.params.NICKNAME, self.params.HOSTNAME, self.params.IDENTD))

    def heartbeat(self, msg):
        data = IrcClient.convert_utf8(msg)
        if data.find("PING") != -1 or data.startswith("PING") != -1:
            self.send('PONG {0}'.format(data.split()[1]))

    def detect_motd(self, msg):

        data = IrcClient.convert_utf8(msg)

        if data.find(':End of /MOTD') != -1 or data.find('/MOTD') != -1 and not self.end_motd_detect:
            self.end_motd_detect = True
            self.modules_process = mp.Process(target=self.process_modules_worker, args=((self.modules_queue), self,))
            self.modules_process.daemon = True
            self.modules_process.start()

            return True

        return False

    def output_data(self, msg):
        print(IrcClient.convert_utf8(msg))

    def bot_loop(self, data):

        # do ping pong check
        self.heartbeat(data)

        if self.detect_motd(data):
            # change flag to connected
            self.is_connected = True
            print("CONNECTED")
            self.auth_user.do_auth()
            time.sleep(2)

            # try to join a channel
        if not self.is_joined and self.is_connected:
            self.join_channel(self.params.CHANNEL)
            print("JOINED {0}".format(self.params.CHANNEL))
            self.is_joined = True

        self.output_data(data)

    def parse(self, data):

        msg = IrcClient.sanitize_string(IrcClient.convert_utf8(data))
        self.modules_queue.put(msg)

    # MULTIPROCESSING CALLBACK ALERT
    def process_modules_worker(self, queue, irc):

        while True:
            msg = queue.get()

            if msg and msg.find('PRIVMSG') != -1:
                is_message = re.search("^:(.+[aA-zZ0-0])!(.*) PRIVMSG (.+?) :(.+[aA-zZ0-9])$", msg)

                if is_message:

                    data = {

                        'sender': is_message.groups()[0],  # sender's nickname
                        'ident': is_message.groups()[1],  # ident
                        'receiver': is_message.groups()[2],  # channel or receiver's nickname
                        'message': is_message.groups()[3],  # message
                    }

                    for mod in irc.modules.module_folder_list:
                        m = irc.modules.get_module_instance(mod)

                        if not m:
                            print("Error: Module {0} Not Found".format(mod))
                            continue

                        for command in m.registered_commands:

                            command_obj = m.registered_commands[command]
                            full_cmd = "{0} {1}".format(command_obj.prefix, command_obj.cmd) #command_obj.prefix + command_obj.cmd
                            #print("FULL_CMD:", full_cmd)

                            if data['message'].find(full_cmd) != -1:
                                m.registered_commands[command_obj.cmd].run(m, client=irc, data=data)
                                continue
                            else:
                                print("MSG SENT: {0}".format(data['message']))
                                pass
                            continue

                # print(dir(irc.modules))
                # if is_message:
                #    for module in irc.modules:
                #        for cmd in module:
                #            print("cmd {1} module {0}", module, cmd)
                #            msg.task_done()

    ## END MULTIPROCESSING CALLBACK ALERT

    ##remember to decode to utf8 and strip \r\n from the messages

    def privmsg_event(self, msg):

        if msg and msg.find('PRIVMSG') != -1:
            is_message = re.search("^:(.+[aA-zZ0-0])!(.*) PRIVMSG (.+?) :(.+[aA-zZ0-9])$", msg)
            if is_message:
                self.modules_queue.put({
                    'type': 'private',
                    'sender': is_message.groups()[0],  # sender's nickname
                    'ident': is_message.groups()[1],  # ident
                    'receiver': is_message.groups()[2],  # channel or receiver's nickname
                    'message': is_message.groups()[3],  # message
                })

                return True
        return False
