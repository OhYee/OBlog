import re
from .. import database as db


def add(_dict):

    # 后端验证
    if not re.match(r'^.*$', _dict['urlpath']):
        return 1
    if db.exist_db("pages", {'urlpath': _dict['urlpath']}) == True:
        return 2

    db.insert_db("pages", _dict)
    return 0


def update(_set, _where):
    # 后端验证
    if not re.match(r'^.*$', _set['urlpath']):
        return 1
    if _where['urlpath'] != _set['urlpath'] and db.exist_db("pages", {'urlpath': _where['urlpath']}) == True:
        return 2

    db.update_db("pages", _set, _where)
    return 0


def delete(_where):
    db.delete_db("pages", _where)
