from OBlog import database as db
import re


def getShowGoodsOfID(_id):
    return db.query_db('select * from goods where id="{}" and show="true"', _id, one=True)


def getAllGoods():
    return db.query_db('select * from goods;')


def getAllShowGoods():
    return db.query_db('select * from goods where show="true";')


def getLastID():
    res = db.raw_query_db('select count(gid) from goods')
    return res[0][0]


def addGood(postRequest):

     # 后端验证
    pattern = [r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', r'^[0-9]+$']
    if not (re.match(pattern[0], postRequest["time"]) and
            re.match(pattern[1], postRequest['value1'])):
        return 1

    postRequest['gid'] = str(getLastID() + 1)
    postRequest['show'] = "true"

    keyList = ["gid", "name", "abstruct", "time", "img",
               "value1", "value2", "value3", "value4", "value5", "show"]
    postRequest = dict(
        (key, postRequest[key] if key in postRequest else "")for key in keyList)

    db.insert_db("goods", postRequest)
    return 0


def updateGood(postRequest):
    # 后端验证
    pattern = [r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', r'^[0-9]+$']
    if not (re.match(pattern[0], postRequest["time"]) and
            re.match(pattern[1], postRequest['value1'])):
        return 1

    gid = postRequest['gid']

    keyList = ["name", "abstruct", "time", "img",
               "value1", "value2", "value3", "value4", "value5", "show"]
    postRequest = dict(
        (key, postRequest[key] if key in postRequest else "")for key in keyList)

    db.update_db("goods", postRequest, {'gid': gid})
    return 0
