import os

class EnvironmentParams:

    NICKNAME = "creekman"
    USERNAME = "creeka"
    IDENTD = "lame guy"
    CHANNEL = "#lamechannel"
    MODULES = "*"
    HOSTNAME = "irc.freenode.net"
    PORT = "6667"
    SSL_ENABLED = False

    def __init__(self):

        if not self.check_environ_exists('CB_NICKNAME'):
            print("Error: username not found using default: "  + self.NICKNAME)
        else:
            self.NICKNAME = self.check_environ_exists('CB_NICKNAME')

        if not self.check_environ_exists('CB_USERNAME'):
            print("Error: username not found using default " + self.USERNAME)
        else:
            self.USERNAME = self.check_environ_exists('CB_USERNAME')

        if not self.check_environ_exists('CB_IDENTD'):
            print("Error: identd environment var not found")
        else:
            self.IDENTD = self.check_environ_exists('CB_IDENTD')

        if not self.check_environ_exists('CB_CHANNEL'):
            print("Error: channel environment var not found")
        else:
            self.CHANNEL= self.check_environ_exists('CB_CHANNEL')

        if not self.check_environ_exists('CB_MODULES'):
            print("Error: modules environment var not found")
        else:
            self.MODULES= self.check_environ_exists('CB_MODULES')

        if not self.check_environ_exists('CB_HOSTNAME'):
            print("Warning: hostname environment var not found -  using default: " + self.HOSTNAME)
        else:
            self.HOSTNAME= self.check_environ_exists('CB_MODULES')

        if not self.check_environ_exists('CB_PORT'):
            print("Warning: port environment var not found - using default: " + self.PORT)
        else:
            self.PORT = self.check_environ_exists('CB_PORT')

        if not self.check_environ_exists('CB_SSL') or self.check_environ_exists('CB_SSL') == int(0):
            print("Initializing without SSL connection!")
        else:
            self.SSL_ENABLED = True


    def check_environ_exists(self, key):
        try:
            return os.environ[key]
        except KeyError as key:
            return False
