from cbircbot2.core.module_base import IrcModuleInterface
from cbircbot2.modules.Users.db.db import UserDB
from cbircbot2.modules.Users.db.models.PiadaModel import PiadaModel
import random
import traceback
import time
#import sys
#import os

class Piadas(IrcModuleInterface):

    ID = 1002
    MODULE_NAME = "Piadas"
    AUTHOR = "ryonagana"
    DESCRIPTION = "user module!"
    def __init__(self):
        super().__init__()


    def is_admin(self, nick):
    
        db = UserDB(self.irc.params.ZEO_DB, self.irc.params.ZEO_HOST, self.irc.params.ZEO_PORT)
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
        self.register_cmd("mostrar", self._mostrar_piada, self.CMD_PUBLIC)
        self.register_cmd("cadastrar", self._cadastrar_piada, self.CMD_PUBLIC)

        self.register_cmd("listar", self._listar_piadas, self.CMD_PRIVATE)

        self.register_cmd("del", self._del_piadas, self.CMD_PRIVATE)
        self.register_cmd("edit", self._edit_piadas, self.CMD_PRIVATE)


    def _del_piadas(self, *args, **kwargs):
        sender = kwargs['data']['sender']
        self.irc.msg_to_channel(sender, "funcionalidade Não Está Pronta ainda")
        return

    def _edit_piadas(self, *args, **kwargs):
        sender = kwargs['data']['sender']
        message = kwargs['data']['message']
        params = message.split(" ", 3)
        count_args = len(params) - 3

        db = UserDB(self.irc.params.ZEO_DB, self.irc.params.ZEO_HOST, self.irc.params.ZEO_PORT)

        print(params)

        if count_args < 1:
            self.irc.msg_to_channel(sender, "parametros invalidos, o parametro correto é ? piadas edit <num> <texto> para editar")
            return

        other_params = IrcModuleInterface.remove_spaces(params[3]).split(" ", 1)
        other_params = other_params[1].split(" ",1)

        id = int(other_params[0])
        texto = other_params[1]

        if not db.piadas[id] or db.piadas[id].owner != sender:
            self.irc.msg_to_channel(sender, "piada inexistente ou voce nao é o dono dela")
            return

        try:

            if db.piadas[id].owner == sender:
                old = db.piadas[id].piada
                db.piadas[id].piada = texto
                db.commit()
                self.irc.msg_to_channel(sender, "piada \"{old}\" foi trocada por \"{new}\" com sucesso!".format(old=old, new=texto))
        except Exception as e:
            print(e)
            print(traceback.print_exc())
            pass
        finally:
            db.close()


    def _listar_piadas(self, *args, **kwargs):
        sender = kwargs['data']['sender']

        db = UserDB(self.irc.params.ZEO_DB, self.irc.params.ZEO_HOST, self.irc.params.ZEO_PORT)
        self.irc.msg_to_channel(sender,"Lista de Piadas Cadastradas:")
        time.sleep(2)

        piada_list = {}

        for _,p in enumerate(db.piadas.items(), start=1):

            if sender == p[1].owner:
                piada = p[1]
                id = p[0]
                piada_list[id] = piada.piada

        if not piada_list:
            self.irc.msg_to_channel(sender, "Desculpe Voce não cadastrou nenhuma piada")
            return


        for p in piada_list.items():
            print(p)
            msg = " ---- {id} - {piada} ----".format(id=p[0], piada=p[1])
            time.sleep(2)
            self.irc.msg_to_channel(sender, msg)

        self.irc.msg_to_channel(sender, "digite ? piadas del <num> para deletar (não tem volta)")
        time.sleep(1)
        self.irc.msg_to_channel(sender, "digite ? piadas edit <num> <texto> para editar")
        time.sleep(1)

        db.close()
        pass

    def cadastrar_nova_piada(self, nick, piada):
        db = UserDB(self.irc.params.ZEO_DB, self.irc.params.ZEO_HOST, self.irc.params.ZEO_PORT)

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

    def _mostrar_piada(self, *args, **kwargs):
        message = kwargs['data']['message']
        receiver = kwargs['data']['receiver']
        sender = kwargs['data']['sender']
        params = message.split(" ", 3)
        count_args = len(params) - 3
        db = UserDB(self.irc.params.ZEO_DB, self.irc.params.ZEO_HOST, self.irc.params.ZEO_PORT)

        try:

            piadas = [p for p in db.piadas.values() ]

            if not piadas:
                self.irc.msg_to_channel(self.irc.params.CHANNEL, "Nenhuma Piada cadastrada!")
                return

            random.shuffle(piadas)  #random.sample(piadas,len(piadas))
            range  = random.randrange(len(piadas))
            piada = piadas[range]

            if not piada:
                self.irc.msg_to_channel(self.irc.params.CHANNEL, "Piada Não Encontrada")
                return;

            self.irc.msg_to_channel(self.irc.params.CHANNEL,  piada.piada)
            pass
        except Exception as e:
            pass
        finally:
            db.close()


    def _cadastrar_piada(self, *args, **kwargs):
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
