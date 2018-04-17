import re
from OBlog import database as db


def getFriends():
    friends = db.query_db("select * from friends")
    friends.sort(key=lambda x: int(x["idx"]))
    return friends


def addFriends(postRequest):
    if not re.match(r'^[0-9]+$', postRequest['idx']):
        return 1
    if db.exist_db("friends", {'name': postRequest['name']}) == True:
        return 2

    keyList = ['url', 'name', 'idx']
    postRequest = dict((key, postRequest[key])for key in keyList)

    db.insert_db("friends", postRequest)
    return 0


def updateFriends(postRequest):
    oldname = postRequest['oldname']

    if not re.match(r'^[0-9]+$', postRequest['idx']):
        return 1
    if oldname != postRequest['name'] and db.exist_db("friends", {'name': postRequest['name']}) == True:
        return 2

    keyList = ['url', 'name', 'idx']
    postRequest = dict((key, postRequest[key])for key in keyList)

    db.update_db("friends", postRequest, {'name': oldname})
    return 0


def deleteFriends(postRequest):
    keyList = ['name']
    postRequest = dict((key, postRequest[key])for key in keyList)
    db.delete_db("friends", postRequest)

    return 0
