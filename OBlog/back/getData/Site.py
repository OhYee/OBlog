import hashlib
import re
import time

from .. import database as db
from . import Nav, Friends, Posts


def timedeFormat(t):
    return time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S"))


def getSite():
    Site = {
        "Nav": Nav.getNav(),
        "Friends": Friends.getFriends(),
        "config": getConfig(),
    }
    return Site


def getConfig():
    temp = db.query_db("select * from SiteConfig")
    res = {}
    for i in temp:
        res[i["name"]] = i["value"]
    return res


def getUserNumber():
    UserNumber = 100
    return UserNumber


def getRecord():
    Record = "豫ICP备17000379号"
    return Record
