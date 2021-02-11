import BTrees.OOBTree as _oob

def db_version_1(root):
    pass

VERSION_UPDATE = {
    1: db_version_1
}


def blank_db(root):
    root['users'] = _oob.OOBTree()
    root['admin'] = _oob.OOBTree()
    root['piadas'] = _oob.OOBTree()
    root['version'] = 1



def init_db(zodb):
    update(zodb, 'version', blank_db, VERSION_UPDATE)
    pass

def update(zodb, version_key = 'version', init_callback = None, update = None):


    version = zodb.root.get(version_key)

    if version is None:
        init_callback(zodb.root)
        msg = "Starting a New Database Version {ver}".format(ver=version)
        print(msg)
        zodb.commit("system", msg)
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
        return