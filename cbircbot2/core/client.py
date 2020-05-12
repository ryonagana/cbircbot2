import os
import sys
import multiprocessing
import re

class IrcClient:
    def __init__(self, sock=None, params = None, *args, **kwargs):
        self.sock = sock
        self.params = params

        self.is_auth = False
        self.is_connected = False
        self.end_motd_detect = False
        self.is_joined = False

        self.modules_process = None
        self.modules_queue = None



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
        self.send("PRIVMSG {0} :{1}", receiver, message)

    def msg_to_channel(self, channel, message):

        self.send("PRIVMSG {0} :{1}".format(channel, message))

    def join_channel(self, channel):

        self.send("JOIN {0}".format(channel))

    def auth(self):

        self.send("NICK {0}".format(self.params.NICKNAME))
        self.send("USER {0} {1} * :{2}".format(self.params.NICKNAME, self.params.HOSTNAME,  self.params.IDENTD))

    def heartbeat(self, msg):
        data = IrcClient.convert_utf8(msg)
        if data.find("PING") != -1 or data.startswith("PING") != -1:
            self.send('PONG {0}'.format(data.split()[1]))

    def detect_motd(self, msg):

        data = IrcClient.convert_utf8(msg)

        if data.find(':End of /MOTD') != -1 or data.find('/MOTD') != -1:
            return True

        return False

    def output_data(self, msg):
        print(IrcClient.convert_utf8(msg))

    def bot_loop(self, data):

        #do ping pong check
        self.heartbeat(data)

        if self.detect_motd(data):
            #change flag to connected
            self.is_connected = True
            print("CONNECTED")

            #try to join a channel
        if not self.is_joined and self.is_connected:
            self.join_channel(self.params.CHANNEL)
            print("JOINED {0}".format(self.params.CHANNEL))
            self.is_joined = True



        self.output_data(data)


    def parse(self, data):

        msg = IrcClient.sanitize_string(IrcClient.convert_utf8(data))
        event = self.privmsg_event(msg)

        if event:
            print(event)



    #remember to decode to utf8 and strip \r\n from the messages
    def privmsg_event(self, msg):

        if msg and msg.find('PRIVMSG') != -1:
            is_message = re.search("^:(.+[aA-zZ0-0])!(.*) PRIVMSG (.+?) :(.+[aA-zZ0-9])$", msg)
            if is_message:

                return  {
                    'sender': is_message.groups()[0],  # sender's nickname
                    'ident': is_message.groups()[1],  # ident
                    'receiver': is_message.groups()[2],  # channel or receiver's nickname
                    'message': is_message.groups()[3],  # message
                }
            return None
        return None








