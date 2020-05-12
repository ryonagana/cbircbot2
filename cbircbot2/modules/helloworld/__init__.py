from cbircbot2.core.module_base import IrcModuleInterface

class helloworld(IrcModuleInterface):
    def __init__(self, irc=None):
        super().__init__(self, irc)

        self.MODULE_NAME ="helloworld"
        self.AUTHOR = "ryonagana"
        self.DESCRIPTION = "Default Hello World!"

    def start(self):
        print("hello world 1")
