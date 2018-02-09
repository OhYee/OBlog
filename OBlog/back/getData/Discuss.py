from .. import database as db


def getDiscussOfUrl(url):
    res= db.query_db("select * from discuss where url='%s' and show='1'" % url)
    return res


def getAllDiscussOfUrl(url):
    return db.query_db("select * from discuss where url='%s'" % url)


def getDiscussOfID(_id):
    return db.query_db("select * from discuss where id='%s'"%(_id),one=True)

def getAllDiscuss():
    return db.query_db("select * from discuss order by id DESC")


def getLastID():
    res= db.raw_query_db("select count(id) from discuss")
    # print(res[0][0])
    return res[0][0]


if __name__ == "__main__":
    print(getLastID())
