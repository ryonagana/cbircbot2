from cbircbot2.core.module_base import IrcModuleInterface
from cbircbot2.modules.Users.db import UserDB


class Users(IrcModuleInterface):
    def __init__(self):
        IrcModuleInterface.__init__(self)
        self.MODULE_NAME ="users"
        self.AUTHOR = "ryonagana"
        self.DESCRIPTION = "Modulo de Enviar Piadas"
        self.db = UserDB('d')

        def start():
            pass

        def end():
            pass
