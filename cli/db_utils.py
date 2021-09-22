import os
import sys
import time

sys.path.insert(0, '..')
import traceback
import zlib
import datetime
from cbircbot2.modules.Users.db.db import UserDB
#from cbircbot2.core.sockets import  Socket
#from cbircbot2.core.params import  EnvironmentParams
#from cbircbot2.core.client import IrcClient
#from cbircbot2.core.modules import IrcModules
#from cbircbot2.core.input import InputText

from cbircbot2.modules.Users.db.models.AdminModel import AdminModel, UserModel
from cbircbot2.modules.Users.db.models.PiadaModel import PiadaModel

import json

os_used = None

if sys.platform.startswith("win32"):
    import msvcrt
    print("MSVCRT Loaded")
    os_used = "windows"
elif sys.platform.startswith("linux"):
    import select
    print("Linux Detected")
    os_used = "linux"
    

#laziest way to achieve this
ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))[:-4]
BACKUP_FOLDER = os.path.join(ROOT, 'cli')
DB_PATH = os.path.join(ROOT, 'd')

print(BACKUP_FOLDER)

load_db_with_zeo = False
use_compression = False

def help():
    print("db_utils.py --zeo - tries to connect at a running ZEO Server / without it just look for \"d\" file")
    print("db_utils.py --compress - all backups are compressed with zlib")

def get_keypress():
    if os_used.startswith("windows"):
        key = msvcrt.kbhit()
        rc = 0
        if not key == 0:
            rc = msvcrt.getch()
            return str(rc)
        return 0
    elif(os_used.startswith('linux')):
        return select.select([sys.stdin], [], [], 0)
    return None

def get_database():
    if load_db_with_zeo:
        return UserDB('d', 'localhost', 9100)

    return UserDB('d')


def th_waitkeypress(break_input):
    while  get_keypress() != 0:
        ch = get_keypress()
        if ch == '\n':
            break_input = True
        
        print(ch)
        

def get_database_version():
    db = None
    try:
        db = get_database()
    except Exception as ex:
        print("Exception: {e}".format(e=ex))
    
    return db.root['version']

def input_multiline(str=""):
    contents = []
    line = ""
    while True:
        try:
            if break_input:
                break
            line = input(str) + "\n"
        except EOFError as eofex:
            print(eofex)
            print(traceback.print_exc())
        contents.append(line)
    return contents

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

def export_backup_db():
    db = get_database()
    try:
        file = {}
        
        user_register = {}
        for name,obj in db.users.items():
            try:
                name = obj.nickname
                karma = obj.karma
                
                user_register[name] = {
                    'nickname': name,
                    'karma': karma
                }
                
            except Exception as e:
                print(e)
        file['users'] = user_register
        
        admin_register = {}
        if db.admin:
            for name,obj in db.admin.items():
                admin_register = {name: {
                                    'nickname': obj.nick,
                                    'allowed_bot': obj.allowed_bot
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
        print(file)
        js = json.dumps(file, ensure_ascii=False).encode('utf-8')
        
        if use_compression:
            compressed = zlib.compress(js)
            dt = datetime.date.today().strftime("%Y-%m-%d-%H%M%S")
            name = "backup-" + dt + ".bkp"
            with open(name,"wb+") as fp:
                fp.write(compressed)
        else:
            dt = datetime.date.today().strftime("%Y-%m-%d-%H%M%S")
            name = "backup-" + dt + ".json"
            with open(name,"w") as fp:
                json.dump(file, fp)

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
        if not ext == ".bkp" or not ext == ".json":
            continue
        result.append(filename + ext)

    return result


def import_db_backup():
    db = get_database()
    
    while True:
        backup_files = load_db_select_file()
        total_indexes = 0
        print("Select your File:")
        for index,bf in enumerate(backup_files, start=1):
            print("{i} - {file}".format(i=index, file=bf))
            total_indexes += 1


        print("{i} - Exit".format(i=index + 1))
    
        select = int(input(">>> "))
        idx = select - 1
        
        if select == idx + 1:
            break
            
        data = None
        try:
            with open(backup_files[index], "rb") as fp:
                data = zlib.decompress(fp.read()) #decompress all bytes to  json (why do i need a compression?)
                data = json.loads(data) #convert back json string to list
            
            
            for u in data['users'].items():
                print(u)
        except Exception as e:
            print(e)
            print(traceback.print_exc())
        

"""
        if not data['users'].items():
            print("ignoring users - empty")
        else:
            for u in data['users'].items():
                #db.root['users'] = UserModel(u['name'])
                print(u)
                
        if not data['admin'].items():
            print('ignoring admin - empty')
            
        if data['piadas'].items():
            print("ignoring jokes - empty")
        
        print(data)
"""

def  add_admin_user():
    is_add = True
    db = get_database()
    while is_add:
        name = input("(Type Name): ")

        try:

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
    db = get_database()
    try:


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
            print(traceback.print_exc())
            print(e)
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

def add_new_user():
    add_user = False
    db = get_database()
    while not add_user:
        name = input("Type Nickname: ")
        
        if len(name) == 0 or name == "":
            continue
        
        try:
            u = UserModel(name, datetime.datetime.now())
            db.users[name] = u
            db.commit()
            print("{name} added".format(name=name))
            
            print("do you want to add more users? (y/n)")
            find = input(">> ")
            if find == "y" or find == "Y":
                continue
            else:
                add_user = True
        except Exception as e:
            print(e)
            print(traceback.print_exc())
        
    

def option_parse(opt):

    if opt == 1:
        create_fresh_db()
        pass

    if opt == 2:
        export_backup_db()
        pass

    if opt == 3:
        import_db_backup()
        pass
    if opt == 4:
        add_admin_user()
        pass
    if opt == 5:
        add_new_user()
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

import threading
break_input = False
if __name__ == "__main__":


    try:
        for args in sys.argv:
            if args.startswith('--zeo'):
                load_db_with_zeo = True
                print ("Loading db_utils with ZEO Support")
            if args.startswith('--no-zeo'):
                print ("Loading db_utils without ZEO Support")
                load_db_with_zeo = False
            elif args.startswith("--compress"):
                use_compression = True
    except IndexError as ie:
        print(ie)
        print("Loading cb_utils without ZEO ")
        
    print("ZEO Server: {at}".format(at=load_db_with_zeo))
    print("Compression: {comp}".format(comp=use_compression))
    print("Database Version: {db} ".format(db=get_database_version()))
    main()
    pass
