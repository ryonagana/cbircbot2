from cbircbot2.core.module_base import IrcModuleInterface
from cbircbot2.modules.Users.db import UserDB

from cbircbot2.modules.Users.db.models.AdminModel import UserModel, AdmModel
from datetime import date


class Users(IrcModuleInterface):
    def __init__(self, irc = None):
        super().__init__(self, irc)
        self.MODULE_NAME = "Users"
        self.AUTHOR = "ryonagana"
        self.DESCRIPTION = "Modulo de Enviar Piadas"
        self.db = UserDB('d')
        self.irc = irc

    def start(self, client):

        self.register_cmd('karma++', self.user_add_karma, self.CMD_PUBLIC, "Add Karma to User")

    def end(self, *args, **kwargs):
        pass

    def user_add_karma(self, *args, **kwargs):
        irc = None

        if "client" in kwargs:
            irc = kwargs["client"]

        message = kwargs['data']['message']
        receiver = kwargs['data']['receiver']
        sender = kwargs['data']['sender']
        params = message.split(" ", 3)
        count_args = len(params) - 3

        if count_args <= 0:
            irc.msg_to_channel(irc.params.CHANNEL, "{sender}: Missing parameter".format(sender=sender))
            return

        nick = params[3]
        is_allowed = False
        """
        for k, _ in self.db.admin.items():
            if k.find(sender) != -1:
                is_allowed = True

        if not is_allowed:
            irc.msg_to_channel(irc.params.CHANNEL, "{sender}: you're not allowed to do this!".format(sender=sender))
            return
        """

        user = self.db.users.get(nick)

        if not user:
            irc.msg_to_channel(irc.params.CHANNEL, "User not Found. Sorry")
            #self.db.users[nick] = UserModel(nick, date.today())
            #self.db.users[nick].add_karma()
        else:
            self.db.users[nick].add_karma()

        self.db.commit()

        irc.msg_to_channel(irc.params.CHANNEL,
                           "{nick} karma++  (total: {karma})".format(nick=nick, karma=self.db.users[nick].karma))
        return
