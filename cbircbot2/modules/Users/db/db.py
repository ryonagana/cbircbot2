from ZODB import FileStorage
import transaction
import ZODB
from .updates import init_db as _init
#from updates import init_db as _init
import os

class UserDB(object):

    DATABASE_FILE="data.db"

    def __init__(self, db_name=None):

        self.model_has_been_created = False

        try:
            if not db_name:
                db_name = self.DATABASE_FILE

            self.storage = ZODB.FileStorage.FileStorage(file_name=db_name, blob_dir='.blob')
            self.db = ZODB.DB(self.storage)
            self.connection = self.db.open()
            self.root = self.connection.root()

            _init(self)

            self.users = self.root['users']
            self.piadas = self.root['piadas']
            self.admin  = self.root['admin']
            pass




        except Exception as e:
            raise Exception("Database Error - " + str(e))



    def close(self):
        self.connection.close()
        self.storage.close()
        self.db.close()


    def commit(self, user = None, note = None):
        trans = transaction.get()
        if user:
            trans.setUser(user)
        if note:
            trans.note(note)

        trans.commit()


    def abort(self):
        tr = transaction.get()
        tr.abort()




if __name__ == "__main__":

    from models.PiadaModel import PiadaModel
    from models.AdminModel import AdminModel
    t = UserDB("d")


    #t.piadas['teste'] = PiadaModel("ryonagana", "AUI")
    #t.piadas['teste1'] = PiadaModel("ryonagana", "Pato")
    #t.piadas['teste3'] = PiadaModel("ryonagana", "Microsoft")
    #t.piadas['teste2'] = PiadaModel("ryonagana", "COCOCO")
    #t.commit()

    t.admin['ryonagana'] = AdminModel('ryonagana')
    t.admin['ryonagana'].set_bot_allowed(True)
    t.commit()


    for key, value in t.piadas.items():
        print(key, value.owner, value.piada)

    t.close()

