import hashlib
import re
import time
from flask import g
from .. import database as db
from . import Nav, Friends


def timedeFormat(t):
    return time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S"))


def getSite():
    if not hasattr(g, "site_getSite"):
        g.site_getSite = {
            "Nav": Nav.getNav(),
            "Friends": Friends.getFriends(),
            "config": getConfig(),
        }
    return g.site_getSite


def getConfig():
    if not hasattr(g, "site_getConfig"):
        temp = db.query_db("select * from SiteConfig")
        res = {}
        for i in temp:
            res[i["name"]] = i["value"]
        g.site_getConfig = res
    return g.site_getConfig

