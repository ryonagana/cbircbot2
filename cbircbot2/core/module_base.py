from cbircbot2.core.command import Command

CMD_NONE    = 0x0
CMD_CHANNEL = 0x2
CMD_PRIVATE = 0x4
CMD_BOTH    = 0x8


class IrcModuleInterface:
    ID = 0 #must be unique default bot ID 0-100  please use 1000+
    AUTHOR = "Author Foo"
    PERMISSION = 0
    MODULE_NAME = "ModuleFoo"
    DESCRIPTION = None
    MODULE_TYPE = 0

    def __init__(self, irc=None):
        self.irc = irc
        self.registered_commands = {}
        pass

    def start(self):
        pass

    def end(self):
        pass

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

            cls.registered_commands[cmd] = Command(**data)
            pass



        pass


