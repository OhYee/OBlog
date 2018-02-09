import re
import hashlib
from .. import database as db


def encode(t):
    return hashlib.sha512(t.encode()).hexdigest()


def add(chinese):
    if db.exist_db("tags", {"chinese": chinese}) == True:
        cnt = db.query_db(
            "select cnt from tags where chinese='%s'" % chinese, one=True)['cnt']
        cnt = str(int(cnt) + 1)
        db.update_db("tags", {'cnt': cnt}, {'chinese': chinese})
    else:
        db.insert_db("tags", {"chinese": chinese,
                              "english": encode(chinese), "cnt": "1", "img": "", "class": ""})
    return 0


def subtract(chinese):
    if db.exist_db("tags", {"chinese": chinese}) == True:
        cnt = db.query_db(
            "select cnt from tags where chinese='%s'" % chinese, one=True)['cnt']
        cnt = str(int(cnt) - 1)
        db.update_db("tags", {'cnt': cnt}, {'chinese': chinese})
        if int(cnt) <= 0:
            delete(chinese)


def update(_set, _where):
    # 后端验证
    pattern = r'^\w+$'
    if not re.match(pattern, _set["english"]):
        return 1

    if 'english' in _where and _where['english'] != _set['english'] and db.exist_db("tags", {'english': _set["english"]}) == True:
        return 2

    db.update_db("tags", _set, _where)
    return 0


def delete(chinese):
    db.delete_db("tags", {"chinese": chinese})
