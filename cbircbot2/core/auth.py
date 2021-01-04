import  os
import time
class AuthClient:
    def __init__(self, client):
        self.irc = client
        self.isAuth = False
        self.foundEndOfMOTD = False
        self.passwd = None
        self.allowedAuth = None

        if not self.set_auth():
            print("WARN: Server Auth is Not Allowed, CB_USER_PASSWD was not set")

    def set_auth(self):
        if "CB_USER_PASSWD" in os.environ:
            self.passwd = os.environ["CB_USER_PASSWD"]
        if "CB_NICKSERV_AUTH" in os.environ:
            self.allowedAuth = os.environ["CB_NICKSERV_AUTH"]

        if self.passwd and self.allowedAuth:
            return True

        return False

    def do_auth(self):

        if not self.isAuth and self.allowedAuth:

            for tries in range(3):
                #self.irc.msg_to('Nickserv', 'nickserv identify {0}'.format(self.passwd))
                self.irc.send("PRIVMSG NICKSERV :identify {0}".format(self.passwd))
                time.sleep(2)




