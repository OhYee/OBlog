from flask import g
from . import database as db
from OBlog import app
from .blueprint.posts.main import getPostForShow
from .blueprint.admin.main import getSiteConfigDict
import re

def getSite():
    if not hasattr(g, 'getSite'):
        res = getSiteConfigDict()
        from .blueprint.pages.main import getPagesDict
        res['pages'] = getPagesDict()
        from .blueprint.friends.main import getFriends
        res['friends'] = getFriends()
        g.getSite = res
        
        rooturl = res['rooturl']['value']
        if not rooturl:  # 未填写相应项
            rooturl = "/"
        res["rooturl"]["value"] = rooturl + '/' if rooturl[-1] != '/' else rooturl
    return g.getSite

def getRoot():
    return getSite()['rooturl']['value']


def viewpath(ip, addr):
    prefix = addr[0:5]
    if prefix != "/stati" and prefix != "/api/" and prefix != "/admi":
        #if addr not in session:
            #session[addr] = True
        view = getSiteConfigDict()
        view = str(int(view['view']['value']) + 1)
        db.commit_db(r"update siteConfig set value='%s' where sid='view'" % view)

        match = re.match(r'^/post/(.*?)/$', addr)
        if match != None:
            url = match.group(1)
            post = getPostForShow(url)
            if post != None:
                view = str(int(post['view']) + 1)
                db.commit_db("update posts set view='%s' where url='%s'" % (view, url))
