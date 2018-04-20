from flask import g, current_app
from OBlog import database as db


def getSiteConfig():
    if not hasattr(g, 'getSiteConfig'):
        res = db.query_db("select * from siteConfig;")
        g.getSiteConfig = res
    return g.getSiteConfig


def getSiteConfigDict():
    if not hasattr(g, 'getSiteConfigDict'):
        siteConfig = getSiteConfig()
        print(siteConfig)
        res = dict((item['sid'], item) for item in siteConfig)
        g.getSiteConfigDict = res
    return g.getSiteConfigDict


def checkPassword(postRequest):
    password = getSiteConfigDict()['password']['value']
    passwd = postRequest.get("password", "")
    status = 0

    print("\n123\n",password,passwd,"\n\n")

    import hashlib
    if hashlib.md5(passwd.encode()).hexdigest() == password:
        current_app.logger.debug("login successfully.")
        status = 0
    else:
        current_app.logger.debug("login failed.")
        status = 1
    return status


def setSite(postRequest):
    current_app.logger.debug(postRequest)

    siteConfig = getSiteConfigDict()
    password = siteConfig['password']

    sid = postRequest['sid']
    value = postRequest['value']

    if sid == 'password' and password != value:
        import hashlib
        value = hashlib.md5(value.encode()).hexdigest()

    db.update_db("siteConfig", {"value": value}, {"sid": sid})

    return 0
