from .. import database as db


def getPages():
    Pages = db.query_db("select * from pages")
    return Pages
