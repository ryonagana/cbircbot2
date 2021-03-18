from cbircbot2.core.module_base import IrcModuleInterface
from cbircbot2.modules.Users.db.db import UserDB

from cbircbot2.modules.Users.db.models.AdminModel import UserModel, AdminModel
from datetime import date
import traceback

class Users(IrcModuleInterface):

    db = None
    MODULE_NAME = "Users"
    AUTHOR = "ryonagana"
    DESCRIPTION = "user module!"

    def __init__(self):
        super().__init__()

        self.db = UserDB('d', "localhost", 9100)


    def start(self,client):
        super().start(client)

        self.register_cmd('karma++', self.user_add_karma, self.CMD_PUBLIC, "Add Karma to User")
        self.register_cmd('add_user', self.add_new_user, self.CMD_PUBLIC, "Add a New User")


    def end(self, *args, **kwargs):
        self.db.close()
        pass


    def is_admin(self, nick):
        if not self.db.admin.get(nick):
            return False
        return True

    def add_new_user(self, *args, **kwargs):
        irc = None
        if "client" in kwargs:
            irc = kwargs["client"]


        message = kwargs['data']['message']
        receiver = kwargs['data']['receiver']
        sender = kwargs['data']['sender']
        params = message.split(" ", 3)
        count_args = len(params) - 3

        if count_args <= 0 and count_args > 1:
            irc.msg_to_channel(irc.params.CHANNEL, "{sender}: Invalid Parameters".format(sender=sender))
            return

        nick = params[3]

        if not self.is_admin(sender):
            irc.msg_to_channel(irc.params.CHANNEL, "{sender}: you're not allowed to do this!".format(sender=nick))
            return

        try:
            dt = date.today().strftime("%Y-%m-%d %H:%M:%S")
            self.db.users[nick] = UserModel(nick, dt)
            self.db.commit()
            irc.msg_to_channel(irc.params.CHANNEL, "{sender}: user {nick} added successfully".format(sender=sender, nick=nick))
        except Exception as ex:
            traceback.print_exc()








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

        if not self.db.admin.get(sender):
            irc.msg_to_channel(irc.params.CHANNEL, "{sender}: you're not allowed to do this!".format(sender=sender))
            return


        try:
            user = self.db.users.get(nick)

            if not user:
                irc.msg_to_channel(irc.params.CHANNEL, "User not Found. Sorry")
                #self.db.users[nick] = UserModel(nick, date.today())
                #self.db.users[nick].add_karma()
            else:
                self.db.users[nick].add_karma()

            self.db.commit()
        except Exception as e:
            traceback.print_exc()

        irc.msg_to_channel(irc.params.CHANNEL,
                           "{nick} karma++  (total: {karma})".format(nick=nick, karma=self.db.users[nick].karma))
        return
