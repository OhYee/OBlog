import re
from .. import database as db


def TagSplit(tag):
    return re.split(r',', tag)


def getRawTags():
    return db.query_db("select * from tags")


def getChinese(_tag):
    return db.query_db("select * from tags where english='%s'" % _tag,one=True)


def getTags():
    _Tags = getRawTags()
    Tags = {}
    for Tag in _Tags:
        Tags[Tag['chinese']] = [Tag['english'],
                                Tag['cnt'], Tag['img'], Tag['class']]
    return Tags

    # Tags = {
    #     "测试": "test",
    #     "测试2": "test2",
    # }
    # return Tags
