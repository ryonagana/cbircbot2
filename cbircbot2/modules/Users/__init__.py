from cbircbot2.core.module_base import IrcModuleInterface
from cbircbot2.modules.Users.db.db import UserDB

from cbircbot2.modules.Users.db.models.AdminModel import UserModel, AdminModel
from datetime import date
import traceback

class Users(IrcModuleInterface):


    ID = 1001
    MODULE_NAME = "Users"
    AUTHOR = "ryonagana"
    DESCRIPTION = "user module!"

    def __init__(self):
        super().__init__()




    def start(self,client):
        super().start(client)

        self.register_cmd('karma++', self.user_add_karma, self.CMD_PUBLIC, "Add Karma to User")
        self.register_cmd('add_user', self.add_new_user, self.CMD_PUBLIC, "Add a New User")
        self.register_cmd('karma--', self.user_remove_karma, self.CMD_PUBLIC, "Add a New User")


    def end(self, *args, **kwargs):
        super().end(*args, **kwargs)
        pass

    def is_admin(self, nick):

        db = UserDB('d', 'localhost',9100)
        try:
            if db.admin.has_key(nick):
                return True
        except Exception as ex:
            print(ex)
            print(traceback.print_exc())
        finally:
            db.close()
        return False

    def add_new_user(self, *args, **kwargs):


        db = UserDB('d', 'localhost',9100)
        message = kwargs['data']['message']
        receiver = kwargs['data']['receiver']
        sender = kwargs['data']['sender']
        params = message.split(" ", 3)
        count_args = len(params) - 3

        if count_args <= 0 and count_args > 1:
            self.irc.msg_to_channel(self.irc.params.CHANNEL, "{sender}: Invalid Parameters".format(sender=sender))
            return

        nick = params[3]

        if not self.is_admin(sender):
            self.irc.msg_to_channel(self.irc.params.CHANNEL, "{sender}: you're not allowed to do this!".format(sender=nick))
            return

        try:
            dt = date.today().strftime("%Y-%m-%d %H:%M:%S")
            db.users[nick] = UserModel(nick, dt)
            db.commit()
            self.irc.msg_to_channel(self.irc.params.CHANNEL, "{sender}: user {nick} added successfully".format(sender=sender, nick=nick))
        except Exception as ex:
            print(traceback.print_exc())
        finally:
            db.close()


    def user_add_karma(self, *args, **kwargs):
        db = UserDB('d', 'localhost',9100)

        message = kwargs['data']['message']
        receiver = kwargs['data']['receiver']
        sender = kwargs['data']['sender']
        params = message.split(" ", 3)
        count_args = len(params) - 3

        if count_args <= 0:

            self.irc.msg_to_channel(self.irc.params.CHANNEL, "{sender}: Missing parameter".format(sender=sender))
            return

        nick = params[3]
        is_allowed = False

        if not self.is_admin(sender):
            self.irc.msg_to_channel(self.irc.params.CHANNEL, "{sender}: you're not allowed to do this!".format(sender=sender))
            return


        try:
            user = db.users.has_key(nick)

            if not user:
                self.irc.msg_to_channel(self.irc.params.CHANNEL, "User not Found. Sorry")
                #self.db.users[nick] = UserModel(nick, date.today())
                #self.db.users[nick].add_karma()
            else:
                db.users[nick].add_karma()
                db.commit()

        except Exception as e:
            print(traceback.print_exc())
        finally:
            db.close()


        self.irc.msg_to_channel(self.irc.params.CHANNEL,
                           "{nick} karma++  (total: {karma})".format(nick=nick, karma=db.users[nick].karma))
        return


    def user_remove_karma(self, *args, **kwargs):
        db = UserDB('d', 'localhost',9100)

        message = kwargs['data']['message']
        receiver = kwargs['data']['receiver']
        sender = kwargs['data']['sender']
        params = message.split(" ", 3)
        count_args = len(params) - 3

        if count_args <= 0:

            self.irc.msg_to_channel(self.irc.params.CHANNEL, "{sender}: Missing parameter".format(sender=sender))
            return

        nick = params[3]
        is_allowed = False

        if not self.is_admin(sender):
            self.irc.msg_to_channel(self.irc.params.CHANNEL, "{sender}: you're not allowed to do this!".format(sender=sender))
            return


        try:
            user = db.users.has_key(nick)

            if not user:
                self.irc.msg_to_channel(self.irc.params.CHANNEL, "User not Found. Sorry")
            else:
                db.users[nick].remove_karma()
                db.commit()

        except Exception as e:
            print(traceback.print_exc())
        finally:
            db.close()


        msg = ""

        if db.users[nick].karma < 0:
            msg = "(Otário) {nick} karma--  (total: {karma})".format(nick=nick, karma=db.users[nick].karma)
        elif db.users[nick].karma > 10:
            msg = "(Gente Final) {nick} karma--  (total: {karma})".format(nick=nick, karma=db.users[nick].karma)
        elif db.users[nick].karma > 20:
            msg = "(Gente Bonissima) {nick} karma--  (total: {karma})".format(nick=nick, karma=db.users[nick].karma)
        else:
            msg = "{nick} karma--  (total: {karma})".format(nick=nick, karma=db.users[nick].karma)

        self.irc.msg_to_channel(self.irc.params.CHANNEL, msg)
        return


    def show_jokes(self):
        pass


