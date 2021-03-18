from ZODB import FileStorage
import transaction
import ZODB
from ZEO import ClientStorage
import ZODB.config

from .updates import init_db as _init
#from updates import init_db as _init
#from updates import init_db as _init
import os

class UserDB(object):

    DATABASE_FILE="data.db"
    host = ""
    port = ""
    is_zeo = False

    def connect(self, host, port):
        self.host = host
        self.port = port
        self.is_zeo = True


    def __init__(self, db_name="d", host = None, port = None):

        self.model_has_been_created = False



        try:

            if not host and not port:
                self.storage = ZODB.FileStorage.FileStorage(file_name=db_name, blob_dir='.blob')
                self.db = ZODB.DB(self.storage)
            else:
                self.db = ZODB.config.databaseFromURL('zeo.conf')

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
    pass