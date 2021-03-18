from cbircbot2.core.module_base import IrcModuleInterface

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
        self.register_cmd("hello", self.hello_callback, self.CMD_PUBLIC, "Just a Test!")

    def end(self):
        pass

    def hello_callback(self,*args, **kwargs):
        irc = None
        if "client" in kwargs:
            irc = kwargs["client"]

        print(dir(irc))
        irc.msg_to_channel(irc.params.CHANNEL, "Hello World!")