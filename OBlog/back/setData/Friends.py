import re
from .. import database as db


def add(idx, name, url):
    _map = {"idx": idx, "name": name, "url": url}

    if not re.match(r'^[0-9]+$', idx):
        return 1
    if db.exist_db("friends", {'name': name}) == True:
        return 2

    db.insert_db("friends", _map)
    return 0


def update(oldname, idx, name, url):
    _where = {"name": oldname}
    _map = {"idx": idx, "name": name, "url": url}

    if not re.match(r'^[0-9]+$', idx):
        return 1
    if oldname != name and db.exist_db("friends", {'name': name}) == True:
        return 2

    db.update_db("friends", _map, _where)
    return 0


def delete(oldname):
    _where = {"name": oldname}
    db.delete_db("friends", _where)
