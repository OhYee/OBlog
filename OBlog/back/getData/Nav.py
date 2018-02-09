from .. import database as db

def getNav():
    Nav = db.query_db("select * from nav")
    Nav.sort(key=lambda x: int(x["idx"]))
    return Nav