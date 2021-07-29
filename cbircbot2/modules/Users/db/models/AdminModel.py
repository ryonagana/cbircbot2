import persistent


class AdminModel(persistent.Persistent):
    nick = ""
    allowed_bot = False

    def __init__(self, nick):
        persistent.Persistent.__init__(self)
        self.nick = nick
        self.allowed_bot = False

    def set_bot_allowed(self, t):
        self.allowed_bot = t

class UserModel(persistent.Persistent):

    nickname = ""
    insert_date = None
    last_seen = None
    karma = 0
    has_admin = False

    def __init__(self, nick, date):
        persistent.Persistent.__init__(self)
        self.nickname = nick
        self.insert_date = date
        self.last_seen = None
        self.karma = 0
        self.has_admin = False


    def change_nickname(self, new_nick):
        self.nickname = new_nick

    def add_karma(self):
        self.karma += 1

    def remove_karma(self):
        self.karma -= 1

    def set_admin(self, val):
        self.has_admin = val

    def __str__(self):
        return "{name}".format(name=self.nickname)

    def __eq__(self, other):
        return self.nickname == other.nickname

    def __hash__(self):
        return hash((self.nickname, self.has_admin))



