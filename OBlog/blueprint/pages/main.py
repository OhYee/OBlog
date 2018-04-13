from OBlog import database as db
from flask import g, current_app


def getPages():
    if not hasattr(g, "getPages"):
        res = db.query_db("select * from pages;")
        res.sort(key=lambda x: int(x["idx"]))
        g.getPages = res
    return g.getPages


def getPagesDict():
    if not hasattr(g, "getPagesDict"):
        pages = getPages()
        res = dict((page['url'], page) for page in pages)
        g.getPagesDict = res
    return g.getPagesDict


def addPages(postRequest):
    current_app.logger.debug(postRequest)
    if db.exist_db('pages', {'url': postRequest['url']}):
        # 已经存在
        return 1

    keyList = ['url', 'title', 'idx']
    postRequest = dict((key, postRequest[key])for key in keyList)
    postRequest['show'] = '1'

    db.insert_db('pages', postRequest)
    return 0


def updatePage(postRequest):
    current_app.logger.debug(postRequest)

    oldurl = postRequest['oldurl']
    url = postRequest['url']

    if url != oldurl and db.exist_db('pages', {'url': url}):
        # 重复url
        return 1

    keyList = ['url', 'title', 'idx', 'show']
    postRequest = dict((key, postRequest[key])for key in keyList)

    db.update_db("pages", postRequest, {'url': oldurl})
    return 0


def deletePage(postRequest):
    current_app.logger.debug(postRequest)
    url = postRequest['url']

    if not db.exist_db('pages', {'url': url}):
        # 不存在
        return 1

    db.delete_db("pages", {'url': url})
    return 0


import os


def absPath(path):
    from OBlog import app
    path = os.path.join(app.config['ROOTPATH'],
                        "OBlog/templates/pages", path)
    return path


def fileExist(path):
    return os.path.exists(path) == True


def getPageTemplate(path):
    path = absPath(path)

    if not fileExist(path):
        return (1, "")

    content = ""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    return (0, content)


def getPageTemplateList():
    return listFiles(absPath('.'))


def listFiles(path):
    return [file
            for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file))]


def setPageTemplate(path, content):
    path = absPath(path)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    return 0


def delPageTemplate(path):
    path = absPath(path)

    if not fileExist(path):
        return 1

    os.remove(path)
    return 0
