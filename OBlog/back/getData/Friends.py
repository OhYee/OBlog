from .. import database as db

def getFriends():
    Friends = db.query_db("select * from friends")
    Friends.sort(key=lambda x: int(x["idx"]))
    return Friends