from . import database as db


def getGV(name):
    res = db.query_db(
        "select value from GlobalVariable where name='%s'" % name, one=True)
    if res:
        return res['value']
    else:
        return None


def setGV(name, value):
    if db.exist_db('GlobalVariable', {'name': name}):
        db.update_db('GlobalVariable', {'value': value}, {'name': name})
    else:
        db.insert_db('GlobalVariable', {"name": name, "value": value})


def delGV(name):
    db.delete_db('GlobalVariable', {'name': name})
