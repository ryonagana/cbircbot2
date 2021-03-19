import multiprocessing as mp
import re
from cbircbot2.core.auth import AuthClient
import time
import selectors
from cbircbot2.core.colors import *
import traceback
from cbircbot2.core.modules import IrcModules

class IrcClient:
    def __init__(self, sock=None, params=None, *args, **kwargs):
        self.sock = sock
        self.params = params
        self.selector = selectors.DefaultSelector()

        self.is_auth = False
        self.is_connected = False
        self.end_motd_detect = False
        self.is_joined = False
        self.modules = None
        self.auth_user = AuthClient(self)
        self.modules_process = None
        self.modules_queue = mp.SimpleQueue()

    def get_socket(self):
        return self.sock.get_sock()

    def send(self, message):
        if not self.sock.socket_connected:
            return
        self.sock.send(IrcClient.format_msg(message))
        time.sleep(1.0)

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
        if data and data.find("PING") != -1 or data.startswith("PING") != -1:
            msg = 'PONG :{pong}'.format(pong=data.split(':')[1])
            self.send(msg)
            print(msg)

    def detect_motd(self, msg):

        data = IrcClient.convert_utf8(msg)

        if data.find(':End of /MOTD') != -1 or data.find('/MOTD') != -1 and not self.end_motd_detect:
            self.end_motd_detect = True

            try:
                self.modules_process = mp.Process(target=self.process_modules_worker, args=(self.modules_queue, self,))
                #self.modules_process.daemon = True
                self.modules_process.start()
                #self.modules_process.join()
            except Exception as e:
                print(COLOR_RED +  "main daemon failed!" + COLOR_RESET)
                print(COLOR_RED + "exception: {0}".format(str(e)) + COLOR_RESET)
                print()
                self.sock.exit_gracefully()
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
                is_message = re.search("^:(.+[aA-zZ0-9])!(.*) PRIVMSG (.+?) :(.+[aA-zZ0-9])$", msg)

                if is_message:

                    data = {

                        'sender': is_message.groups()[0],  # sender's nickname
                        'ident': is_message.groups()[1],  # ident
                        'receiver': is_message.groups()[2],  # channel or receiver's nickname
                        'message': is_message.groups()[3],  # message
                    }

                    irc.modules.broadcast_message_all_modules(data['message'])

                    if not data['message'].strip("").startswith("?"):
                        #self.privmsg_event(data['message'])
                        continue



                    msg = data['message'].strip("").split(" ")

                    prefix = msg[0]
                    module = msg[1]
                    command = msg[2]
                    params = data['message'].split(" ")[3:]

                    module_instance = None

                    try:
                        module_instance = irc.modules.get_module_instance(module)
                        if not module_instance:
                            continue

                        if command in module_instance.registered_commands:

                            try:
                                module_instance.registered_commands[command].run(module_instance, full_command=msg, client=irc, data=data)
                            except Exception as e:
                                print("Command: {0} not Found".format(command))
                                print("Exception: {ex}".format(ex=str(e)))
                                print(traceback.print_exc())
                                continue

                        else:
                            print("Command: {0} not Found".format(command))
                            continue

                    except Exception as e:
                        print("Module Not Found!")
                        print(BG_RED + COLOR_BLACK + "Exception: {ex}".format(ex=str(e)) + BG_RESET + COLOR_RESET )
                        continue


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

    def list_users(self):
        self.send("NAMES {0}".format(self.params.CHANNEL))