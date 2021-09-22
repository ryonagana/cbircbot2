from cbircbot2.core.module_base import IrcModuleInterface, IrcCommandType

class helloworld(IrcModuleInterface):

    irc = None
    MODULE_NAME = "helloworld"
    AUTHOR = "ryonagana"
    DESCRIPTION = "Default Hello World!"

    def __init__(self):
        super().__init__()
        self.irc = None


    def start(self, client):
        print("hello world 1")
        self.register_cmd("hello", self.hello_callback, IrcCommandType.CMD_PUBLIC, "Just a Test!")

    def end(self):
        pass

    def hello_callback(self,*args, **kwargs):
        irc, message, sender, receiver, params, count = IrcModuleInterface.get_args(**kwargs)
        irc.msg_to_channel(receiver, "Hello World!")
        pass
