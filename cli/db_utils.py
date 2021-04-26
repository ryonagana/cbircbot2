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

load_db_with_zeo = False

def get_database():
    if load_db_with_zeo:
        return UserDB('d', 'localhost', 9100)

    return get_database()

def create_fresh_db():
    try:
        db = get_database()
        db.close()
    except Exception as e:
        print(traceback.print_exc())
        pass

def menu_options_str():
    print ("1 - Create a Fresh Database")
    print ("2 - Backup Database (WIP)")
    print ("3 - Restore Database (WIP)")
    print ("4 - Add Admin")
    print ("5 - Add User")
    print ("6 - List all Admins")
    print ("7 - Search Admin By nickname " )
    print ("q - Exit")

def backup_db():

    try:
        db = get_database()

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

def  add_admin_user():
    is_add = True
    while is_add:
        name = input("(Type Name): ")

        try:
            db = get_database()
            db.admin[name] = AdminModel(name)
            db.commit()

            if db.admin.has_key(name):
                print("user: {name} was successfully added!".format(name=name))
            else:
                print("an error was caught when tried to add {nick}".format(nick=name))

        except Exception as e:
            print("a error ocurred while trying to add an user: " + e)
            is_add = False
            pass
        finally:
            db.close()

            while 1:
                new_user = input("Do You Want to Add More Admin (y/n)")
                if new_user == "y" or new_user == "Y":
                    break
                else:
                    is_add  = False
                    break



    pass

def list_all_admins():

    try:
        db = get_database()

        for i, user in enumerate(db.admin.values(), start=1):
            print(i, user.nick)
        out = input("Press Any Key to Continue")
        pass
    except Exception as e:
        print(e)
        pass
    finally:
        db.close()

    pass

def search_user_by_nickname():
    has_user = True
    while has_user:

        try:
            db = get_database()
            name = input("(type admin name: ")

            if not db.admin.has_key(name):
                print("User {0} does not exists".format(name))


            user = db.admin[name]

            print("nick: {0}".format(user.nick))
            print("allowed: {0}".format(user.allowed_bot))
        except Exception as e:
            pass
        finally:
            db.close()

        while 1:
            find = input("wanna to find more admins? (y/n): ")

            if find == "y" or find == "Y":
                break
            else:
                has_user = False
                break

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

    if opt == 4:
        add_admin_user()
        pass
    if opt == 6:
        list_all_admins()
        pass
    if opt == 7:
        search_user_by_nickname()

    return opt

def menu():
    opt = None
    while True:

        try:
            menu_options_str()

            opt = input(">>> ")

            if opt == 'q':
                sys.exit(0)

            selected = option_parse(int(opt))



        except Exception as ex:
            print("{opt} Is An Invalid Option".format(opt=opt))
            pass


def main():
    menu()
    pass

if __name__ == "__main__":

    try:
        if sys.argv[1]:
            if sys.argv[1].startswith('--zeo'):
                load_db_with_zeo = True
                print ("Loading db_utils with ZEO Support")
        else:
            print ("Loading cb_utils without ZEO")
    except IndexError as ie:
        print ("Loading cb_utils without ZEO ")

    main()
    pass
