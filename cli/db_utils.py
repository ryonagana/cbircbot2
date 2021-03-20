import os
import sys

sys.path.insert(0, '..' )

import traceback
import zlib
import datetime
from cbircbot2.modules.Users.db.db import UserDB
from cbircbot2.core.sockets import  Socket
from cbircbot2.core.params import  EnvironmentParams
from cbircbot2.core.client import IrcClient
from cbircbot2.core.modules import IrcModules
from cbircbot2.core.input import InputText

from cbircbot2.modules.Users.db.models.AdminModel import AdminModel, UserModel
from cbircbot2.modules.Users.db.models.PiadaModel import PiadaModel

import json

#laziest way to achieve this
ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))[:-4]
BACKUP_FOLDER = os.path.join(ROOT, 'cli')
DB_PATH = os.path.join(ROOT, 'd')

print(BACKUP_FOLDER)
def create_fresh_db():
    try:
        db = UserDB(DB_PATH)
        db.close()
    except Exception as e:
        print(traceback.print_exc())
        pass

def menu_options_str():
    print ("1 - Create a Fresh Database")
    print ("2 - Backup Database (WIP)")
    print ("3 - Restore Database (WIP)")
    print ("4 - Exit")

def backup_db():

    try:
        db = UserDB(DB_PATH)

        file = {}

        for user in db.users.items():
            name = user[0]
            obj = user[1]

            user_register = { name: {
                                'nickname': name,
                                'karma': obj.karma
                            }
            }

        file = {'users': user_register}

        admin_register = None
        if db.admin:
            for admin in db.admin:
                admin_register = {admin: {
                                    'nickname': admin
                                 }}
        else:
            print("no admin was found.. ignoring")

        file['admin'] = admin_register


        piada_register = None
        if db.piadas:
            for piada in db.piadas:
                piada_register = {piada: {
                                    'owner' : piada[1].owner,
                                    'piada' : piada[1].piada
                                  }}





        file['piadas'] = piada_register


        js = json.dumps(file, ensure_ascii=False).encode('utf-8')


        compressed = zlib.compress(js)


        dt = datetime.date.today().strftime("%Y-%m-%d-%H%M%S")
        name = "backup-" + dt + ".bkp"
        with open(name,"wb+") as fp:
                fp.write(compressed)

        print ("file written {f}".format(f=name))

    except Exception as e:
        print(e, traceback.print_exc())
        pass
    finally:
        db.close()


def load_db_select_file():
    files = [f for f in os.listdir(BACKUP_FOLDER) if os.path.isfile(f) ]

    result = []
    for file in files:
        filename, ext = os.path.splitext(file)
        if not ext == ".bkp": continue
        result.append(filename + ext)

    return result


def load_db():

    while True:
        backup_files = load_db_select_file()

        print("Select your File:")
        for index,bf in enumerate(backup_files, start=1):
            print("{i} - {file}".format(i=index, file=bf))


        print("{i} - Exit".format(i=index + 1))

        select = input(">>> ")


        if int(select) == index + 1:
            break


def import_db(list):
    pass

def option_parse(opt):

    if opt == 1:
        create_fresh_db()
        pass

    if opt == 2:
        backup_db()
        pass

    if opt == 3:
        load_db()
        pass

    return opt

def menu():
    opt = None
    while True:

        try:
            menu_options_str()

            opt = input(">>> ")
            selected = option_parse(int(opt))


            if(selected == 4):
                sys.exit(0)
        except Exception as ex:
            print("{opt} Is An Invalid Option".format(opt=opt))
            pass


def main():
    menu()
    pass

if __name__ == "__main__":
    main()
    pass
