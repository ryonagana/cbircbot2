from cbircbot2.core.command import Command

class IrcModuleInterface(object):
    ID = 0  #must be unique default bot ID 0-1000  please use 1000+
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

    def __init__(self, irc=None):
        self.irc = irc

        pass

    def get_command(self, name=None):

        if not name:
            return self.registered_commands

        try:
            return self.registered_commands[name]
        except Exception as e:
            print('command not found')

    def start(self):
        self.cmd_help_generator()
        pass

    def end(self):
        pass

    def help_func(self, *args, **kwargs):

        if not "message" in kwargs:
            return



    def cmd_help_generator(self):
        self.register_cmd("!help", self.help_func, self.CMD_PRIVATE, "Default help for {0}".format(self.MODULE_NAME))

    @classmethod
    def register_cmd(cls, command, callback, access=0, description=""):


        if command and callback:
            prefix = command[0]
            cmd = command[1:]

            data = {
                "prefix": prefix,
                "cmd"   : cmd,
                "access": access,
                "description": description,
                "callback" : callback
            }

            cls.registered_commands[cmd] = Command.register(**data)
            pass
        pass


