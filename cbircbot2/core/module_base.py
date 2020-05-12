from cbircbot2.core.command import Command





class IrcModuleInterface(object):
    ID = 0 #must be unique default bot ID 0-100  please use 1000+
    AUTHOR = "Author Foo"
    PERMISSION = 0
    MODULE_NAME = "ModuleFoo"
    DESCRIPTION = None
    MODULE_TYPE = 0

    CMD_NONE = 0
    CMD_PUBLIC = 1
    CMD_PRIVATE = 2
    CMD_BOTH = 3

    def __init__(self, irc=None):
        self.irc = irc
        self.registered_commands = {}
        pass

    def start(self):
        pass

    def end(self):
        pass

    def help_callback(self, *args, **kwargs):

        if not "message" in kwargs:
            return



    def cmd_help(self):
        self.register_cmd("!help", self.help_callback, self.CMD_PRIVATE, "Default help for {0}".format(self.MODULE_NAME))

    @classmethod
    def register_cmd(cls, command, callback, access=0, description=""):

        if not cls.irc:
            return

        if command and callback:
            prefix = command[0]
            cmd = command[1:]

            data = {
                "prefix": prefix,
                "cmd"   : command,
                "access": access,
                "description": description,
                "callback" : callback
            }

            cls.registered_commands[cmd] = Command(**data)
            pass
        pass


