from cbircbot2.core.module_base import IrcModuleInterface
from cbircbot2.modules.Users.db.db import UserDB
from cbircbot2.modules.Users.db.models.PiadaModel import PiadaModel
import random
import traceback

class Piadas(IrcModuleInterface):

    ID = 1002
    MODULE_NAME = "Piadas"
    AUTHOR = "ryonagana"
    DESCRIPTION = "user module!"
    def __init__(self):
        super().__init__()


    def is_admin(self, nick):

        db = UserDB('d', "localhost", 9100)
        try:
            if db.admin.has_key(nick):
                return True
        except Exception as ex:
            print(ex)
            print(traceback.print_exc())
        finally:
            db.close()
        return False

    def start(self, client):
        self.irc = client
        self.register_cmd("mostrar", self.mostrar_piada, self.CMD_PUBLIC)
        self.register_cmd("cadastrar", self.cadastrar_piada, self.CMD_PUBLIC)


    def cadastrar_nova_piada(self, nick, piada):
        db = UserDB('d','localhost',9100)

        try:
           if db.piadas:
               size = len(db.piadas)
               db.piadas[size + 1] = PiadaModel(nick, piada[0])

           else:
               db.piadas[0] = PiadaModel(nick, piada[0])

           db.commit()
        except Exception as e:
            pass
        finally:
            db.close()

    def mostrar_piada(self, *args, **kwargs):
        message = kwargs['data']['message']
        receiver = kwargs['data']['receiver']
        sender = kwargs['data']['sender']
        params = message.split(" ", 3)
        count_args = len(params) - 3
        db = UserDB('d', 'localhost', 9100)

        try:

            piadas = [p for p in db.piadas.values() ]

            if not piadas:
                self.irc.msg_to_channel(self.irc.params.CHANNEL, "Nenhuma Piada cadastrada!")
                return


            piada = random.choice(piadas)

            self.irc.msg_to_channel(self.irc.params.CHANNEL,  piada.piada)
            pass
        except Exception as e:
            pass
        finally:
            db.close()


    def cadastrar_piada(self, *args, **kwargs):
        message = kwargs['data']['message']
        receiver = kwargs['data']['receiver']
        sender = kwargs['data']['sender']
        params = message.split(" ", 3)
        count_args = len(params) - 3

        try:
            if not self.is_admin(sender):
                self.irc.msg_to_channel(self.irc.params.CHANNEL, "{sender}: you have no powers here".format(sender=sender))
                return
        except Exception as e:
            print(traceback.print_exc())

        if count_args < 1:
            self.irc.msg_to_channel(self.irc.params.CHANNEL, "{0}: Parâmetros Inválido".format(sender))
            return


        piada = params[3:]

        print("PIADA ", piada)

        try:
            self.cadastrar_nova_piada(sender,piada)
            self.irc.msg_to_channel(self.irc.params.CHANNEL, "Piada cadastrada com sucesso!")
        except Exception as e:
            print(e)
            print(traceback.print_exc())




    def on_message(self, message):
        super().on_message(message)

