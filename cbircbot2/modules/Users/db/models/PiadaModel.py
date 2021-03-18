import persistent
#from cbircbot2.modules.users.db.models.AdminModel import AdminModel
import ZODB
class PiadaModel(persistent.Persistent):

    owner = ""
    piada = ""

    def __init__(self, owner, piada):
        persistent.Persistent.__init__(self)

        self.owner = owner
        self.piada = piada
