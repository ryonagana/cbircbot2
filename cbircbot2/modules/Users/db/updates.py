import BTrees.OOBTree as _oob
import BTrees.IOBTree as _iobtree

def db_version_1(root):
    pass

def db_version_2(root):

    piada_list = []

    if root['piadas']:
        for index,p in enumerate(root['piadas'].values()):
            piada_list.append(p)
            del root.piadas[index]

        root.commit()

    del root['piadas']

    root['piadas'] = _iobtree.IOBTree()

    for p in piada_list:
        root['piadas'].append(p)

    pass

VERSION_UPDATE = {
    1: db_version_1,
    2: db_version_2
}


def blank_db(root):
    root['users'] = _oob.OOBTree()
    root['admin'] = _oob.OOBTree()
    root['piadas'] = _iobtree.IOBTree()
    root['version'] = 1




def init_db(zodb):
    update(zodb, 'version', blank_db, VERSION_UPDATE)
    pass

def update(zodb, version_key = 'version', init_callback = None, update = None):


    version = zodb.root.get(version_key)

    if version is None:
        init_callback(zodb.root)
        msg = "Starting a New Database Version {ver}".format(ver=version)
        zodb.commit("system", msg)
        print(msg)
        return

    keys = list(update.keys())
    sorted(keys)
    print(keys)

    last_key = keys[-1] + 1

    for value_from in range (version, last_key):
        update[value_from](zodb.root)
        zodb.root['version'] = value_from + 1

        msg = "updating Database rom version {old_ver} to {new_ver}".format(old_ver=version, new_ver=value_from+1)
        zodb.commit("system", msg)
        print(msg)
        return