import re
from .. import database as db
from flask import g


def TagSplit(tag):
    return re.split(r',', tag)


def getRawTags():
    if not hasattr(g, "tags_getRawTags"):
        g.tags_getRawTags = db.query_db("select * from tags")
    return g.tags_getRawTags


def getChinese(_tag):
    if not hasattr(g, "tags_getChinese"):
        g.tags_getChinese = db.query_db(
            "select * from tags where english='%s'" % _tag, one=True)
    return g.tags_getChinese


def getTags():
    if not hasattr (g,"tags_getTags"):
        _Tags = getRawTags()
        Tags = {}
        for Tag in _Tags:
            Tags[Tag['chinese']] = [Tag['english'],
                                    Tag['cnt'], Tag['img'], Tag['class']]
        g.tags_getTags= Tags
    return g.tags_getTags
