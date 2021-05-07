from cbircbot2.core.module_base import IrcModuleInterface
from cbircbot2.modules.Users.db.db import UserDB

from cbircbot2.modules.Users.db.models.AdminModel import UserModel, AdminModel
from datetime import date
import traceback
import  re

class Users(IrcModuleInterface):


    ID = 1001
    MODULE_NAME = "Users"
    AUTHOR = "ryonagana"
    DESCRIPTION = "user module!"

    def __init__(self):
        super().__init__()

    def start(self,client):
        super().start(client)
        
        self.db_addr = self.irc.params.ZEO_ADDRESS
        self.db_port = self.irc.params.ZEO_PORT

        self.register_cmd('karma++', self.user_add_karma, self.CMD_PUBLIC, "Add Karma to User")
        self.register_cmd('add', self.add_new_user, self.CMD_PUBLIC, "Add a New User")
        self.register_cmd('karma--', self.user_remove_karma, self.CMD_PUBLIC, "Add a New User")
        self.register_cmd('karma', self.show_karma, self.CMD_PUBLIC, "Shows Karma Number")


    def end(self, *args, **kwargs):
        super().end(*args, **kwargs)
        pass

    def __is_admin(self, nick):

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

    def signup_all_users(self):

        users = []

        self.irc.irc.send("NAMES {0}".format(self.irc.params.CHANNEL))

        pass

    def __add_karma(self, name):
        db = UserDB('d', "localhost", 9100)
        user = db.users.has_key(name)

        if not user:
            self.__register_user(name)
            db.users[name].add_karma()
            db.commit()
            db.close()
            return db.users[name].karma

        db.users[name].add_karma()
        db.commit()
        db.close()
        return db.users[name].karma

    def __remove_karma(self, name):
        db = UserDB('d', "localhost", 9100)
        user = db.users.has_key(name)

        if not user:
            self.__register_user(name)
            db.users[name].remove_karma()
            db.close()
            db.commit()
            return db.users[name].karma

        db.users[name].remove_karma()
        db.commit()
        db.close()
        return db.users[name].karma

    def __register_user(self, name):
        db = UserDB('d', "localhost", 9100)

        user = db.users.has_key(name)

        if not user:
            dt = date.today().strftime("%Y-%m-%d %H:%M:%S")
            new_user = UserModel(name, dt)

            db.users[name] = new_user
            db.commit()
            db.close()


    def show_karma(self, *args, **kwargs):
        db = UserDB('d', "localhost", 9100)
        message = kwargs['data']['message']
        receiver = kwargs['data']['receiver']
        sender = kwargs['data']['sender']
        params = message.split(" ", 3)
        count_args = len(params) - 3

        if count_args == 1:


            nick = params[3]

            user = db.users.has_key(nick)
            if user:
                self.irc.msg_to_channel(self.irc.params.CHANNEL, "{sender}: {nick} has {karma} points".format(sender=sender, nick=nick, karma=db.users[nick].karma))
                return

        try:
            user = db.users.has_key(sender)

            if user:

                karma_count = db.users[sender].karma
                point_m = "point"
                if karma_count > 1:
                    point_m = "points"

                self.irc.msg_to_channel(self.irc.params.CHANNEL, "{sender}: You have {karma} {p}".format(sender=sender,p=point_m,karma=karma_count))
            else:
                self.__register_user(sender)

                point_m = "point"
                if db.users[sender].karma > 1:
                    point_m = "points"

                self.irc.msg_to_channel(self.irc.params.CHANNEL,
                                        "{sender}: You have {karma} {p}".format(sender=sender, p=point_m,
                                                                                karma=db.users[sender].karma))
        except Exception as e:
            pass
        finally:
            db.close()



    def add_new_user(self, *args, **kwargs):


        db = UserDB('d', "localhost", 9100)
        message = kwargs['data']['message']
        receiver = kwargs['data']['receiver']
        sender = kwargs['data']['sender']
        params = message.split(" ", 3)
        count_args = len(params) - 3

        if count_args <= 0 and count_args > 1:
            self.irc.msg_to_channel(self.irc.params.CHANNEL, "{sender}: Invalid Parameters".format(sender=sender))
            return

        nick = params[3]

        if not self.__is_admin(sender):
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
        db = UserDB('d', "localhost", 9100)

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

        #if not self.is_admin(sender):
        #    self.irc.msg_to_channel(self.irc.params.CHANNEL, "{sender}: you're not allowed to do this!".format(sender=sender))
        #    return


        try:
            user = db.users.has_key(nick)

            if not user:
                if self.__is_admin(sender):
                    self.__register_user(nick)
                    self.__add_karma(nick)
                else:
                    self.irc.msg_to_channel(self.irc.params.CHANNEL, "{0} Access Denied!".format(sender))
                    return
            else:
                self.__add_karma(nick)

            self.__karma_message(nick, "karma++")
            self.irc.msg_to_channel(self.irc.params.CHANNEL,
                                    "{nick} karma++  (total: {karma})".format(nick=nick, karma=db.users[nick].karma))

        except Exception as e:
            print(traceback.print_exc())
        finally:
            db.close()
        return


    def __karma_message(self, nick, type):
        db = UserDB('d', "localhost", 9100)
        msg=""
        try:
            karma = db.users[nick].karma

            if karma < -15:
                msg="(Otário) {nick} {tp}   (total: {karma})".format(nick=nick, tp=type,  karma=db.users[nick].karma)
            elif karma >= 0 and karma < 10:
                msg="{nick} {tp} (total: {karma})".format(nick=nick, tp=type, karma=db.users[nick].karma)
            elif karma > 10:
                msg="(Gente Final) {tp} {nick}  (total: {karma})".format(nick=nick, tp=type, karma=db.users[nick].karma)
            elif karma > 20:
                msg="(Gente Bonissima) {tp} {nick} (total: {karma})".format(nick=nick, tp=type, karma=db.users[nick].karma)
            else:
                msg="{tp} {nick}  (total: {karma})".format(nick=nick,tp=type, karma=db.users[nick].karma)

            self.irc.msg_to_channel(self.irc.params.CHANNEL, msg)

        except Exception as e:
            print(traceback.print_exc())
        finally:
            db.close()
        pass

    def user_remove_karma(self, *args, **kwargs):
        db = UserDB('d', "localhost", 9100)

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

        try:
            user = db.users.has_key(nick)

            if not user:
                if self.__is_admin(sender):
                    self.__register_user(nick)
                    self.__remove_karma(nick)
                else:
                    self.irc.msg_to_channel(self.irc.params.CHANNEL, "{0} Access Denied!".format(sender))
                    return
            else:
                self.__remove_karma(nick)

        except Exception as e:
            print(traceback.print_exc())
        finally:
            db.close()

        self.__karma_message(nick,"karma--")
        return


    def show_jokes(self):
        pass


    def __onmessage_karma_points_add(self, *args, **kwargs):
        sender,ident,channel,message = kwargs.values()
        nick = message.split("++")[0].strip()

        if self.__prevent_self_karma(sender,nick):
            self.irc.msg_to_channel(channel, "{nick} access denied", nick=sender)
            return
        try:
            db= UserDB('d', "localhost", 9100)
            user= db.users.has_key(nick)

            if not user:
                if self.__is_admin(sender):
                    self.__register_user(nick)
                    self.__add_karma(nick)

                else:
                    self.irc.msg_to_channel(self.irc.params.CHANNEL, "{s} Access Denied".format(s=sender))
                    return

                self.__karma_message(nick)
                return

            self.__add_karma(nick)
            self.__karma_message(nick, "karma++")
            #self.irc.msg_to_channel(self.irc.params.CHANNEL,
            #                        "{n} has {points} Karma Points".format(n=nick, points=db.users[nick].karma))
        except Exception as e:
            print(e)
            print(traceback.print_exc())
        finally:
            db.close()


    def __onmessage_karma_points_remove(self, *args, **kwargs):
        sender,ident,channel,message = kwargs.values()
        nick = message.split("--")[0].strip()

        if self.__prevent_self_karma(sender,nick):
            self.irc.msg_to_channel(channel, "{nick} access denied".format(nick=sender))
            return

        db=UserDB('d', "localhost", 9100)

        try:
            user=db.users.has_key(nick)

            if not user:
                if self.__is_admin(sender):
                    self.__register_user(nick)
                    self.__remove_karma(nick)

                else:
                    self.irc.msg_to_channel(self.irc.params.CHANNEL, "{s} Access Denied".format(s=sender))
                    return

            self.__remove_karma(nick)
            self.__karma_message(nick, "karma--")

        except Exception as e:
            print(e)
            print(traceback.print_exc())
        finally:
            db.close()


    def __prevent_self_karma(self, sender, nick):
        return sender == nick

    def on_message(self, *args, **kwargs):

        #remove space easiest way the first part is the only thing matter
        nick=kwargs['message'].split(' ')[0] #clean and get the first element
        kwargs['message'] = nick  #inject the new message and discards the rest after space


        if kwargs['message'].startswith(nick) and "++" in kwargs['message']:
            self.__onmessage_karma_points_add(**kwargs)
            return
        if kwargs['message'].startswith(nick) and "--" in kwargs['message']:
            self.__onmessage_karma_points_remove(**kwargs)
            return