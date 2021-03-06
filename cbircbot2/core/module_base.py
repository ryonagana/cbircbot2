from cbircbot2.core.command import Command
import re

class IrcModuleInterface(object):
    ID = 0  # must be unique default bot ID 0-1000  please use 1000+
    AUTHOR = "Author Foo"
    PERMISSION = 0
    MODULE_NAME = "ModuleFoo"
    DESCRIPTION = None
    MODULE_TYPE = 0

    CMD_NONE = 0
    CMD_PUBLIC = 1
    CMD_PRIVATE = 2
    CMD_BOTH = 3
    registered_commands = {}
    irc = None

    message = ""

    def __init__(self):

        pass

    def find_command(self, command):

        for k,_ in self.registered_commands.items():
            if command.find(k) != -1:
                return True

        return False


    def  get_args(self, *args, **kwargs):
        if "client" in kwargs:
            irc = kwargs["client"]

        message = kwargs['data']['message']
        receiver = kwargs['data']['receiver']



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
        self.register_cmd("!help", self.help_func, self.CMD_PRIVATE, "Default help for {0}".format(self.MODULE_NAME))


    @staticmethod
    def remove_spaces(str):
        string = re.sub('\s{2,}', ' ', str)
        return string

    @classmethod
    def register_cmd(cls, command, callback, access=0, description=""):

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
