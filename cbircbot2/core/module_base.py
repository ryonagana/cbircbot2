from cbircbot2.core.command import Command
import re
from enum import Enum, auto


class IrcCommandType(Enum):
    """Command types"""
    CMD_NONE = auto()
    CMD_PUBLIC = auto()
    CMD_PRIVATE = auto()
    CMD_BOTH =  auto()

class IrcModuletype(Enum):
    """type of modules"""
    MODULE_PUBLIC = auto()
    MODULE_INTERNAL = auto()
    MODULE_THREAD = auto()

class IrcModuleInterface(object):
    ID: int = 0  # must be unique default bot ID 0-1000  please use 1000+
    AUTHOR: str = "Author Foo"
    PERMISSION: int = 0
    MODULE_NAME: str = "ModuleFoo"
    DESCRIPTION: str = None
    MODULE_TYPE = IrcModuletype.MODULE_PUBLIC
    registered_commands = {}
    irc = None
    message = ""

    def command_exists(self, command):
        for k,_ in self.registered_commands.items():
            if command.find(k) != -1:
                return True
        return False
    
    @staticmethod
    def get_args(*args, **kwargs):
        irc = None
        if "client" in kwargs:
            irc = kwargs["client"]

        message = kwargs['data']['message']
        receiver = kwargs['data']['receiver']
        sender = kwargs['data']['sender']
        params = message.split(" ", 3)
        count = len(params) - 3
        t = (irc, message, sender, receiver,params, count)
        return t



    def get_command(self, name=None):

        if not name:
            return self.registered_commands

        try:
            return self.registered_commands[name]
        except IndexError as e:
            print('command not found')
            return None

    def start(self, client):
        self.irc = client
        self.cmd_help_generator()
        assert self.irc is not None
        print("{mod_name} Started".format(mod_name=self.MODULE_NAME))
        pass

    def end(self, *args, **kwargs):
        pass

    def help_func(self, *args, **kwargs):

        if not "message" in kwargs:
            return

    def get_params(self, data):
        if "message_data" not in data:
            return False

        msg = data['message_data']
        msg = msg.split(" ", 2)

        return {'cmd': msg, 'params_count': len(msg)}

    def cmd_help_generator(self):
        self.register_cmd("!help", self.help_func,  IrcCommandType.CMD_PRIVATE, "Default help for {0}".format(self.MODULE_NAME))


    @staticmethod
    def remove_spaces(str):
        string = re.sub('\s{2,}', ' ', str)
        return string

    @classmethod
    def register_cmd(cls, command: str, callback: object, access: IrcCommandType = IrcCommandType.CMD_PRIVATE, description: str = ""):

        if command and callback:
            prefix = '?'  # command[0]
            cmd = command

            data = {
                "prefix": prefix,
                "cmd": cmd,
                "access": access,
                "description": description,
                "callback": callback
            }

            cls.registered_commands[cmd] = Command.register(**data)
            pass
        pass

    def on_message(self, *args, **kwargs):
        pass

    def get_message(self):
        return self.message

    def invoke_cmd(self, name, *args, **kwargs):

        if name not in self.registered_commands:
            print("The command: {name} is not in registered commands - cannot be invoked".format(name=name))
            return

        self.registered_commands[name].run(**kwargs)
        return
