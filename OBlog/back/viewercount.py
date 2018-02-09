from flask import session
from . import database as db
from .getData import Posts
import re
from OBlog import app


def viewpath(ip, addr):
    prefix = addr[0:5]
    if prefix != "/stati" and prefix != "/api/" and prefix != "/admi":
        #if addr not in session:
            #session[addr] = True
        view = db.raw_query_db(
            "select value from SiteConfig where name='view'", one=True)
        view = str(int(view[0]) + 1)
        db.commit_db(
            r"update SiteConfig set value='%s' where name='view'" % view)

        match = re.match(r'^/post/(.*?)$', addr)
        if match != None:
            url = match.group(1)
            post = Posts.getPost(url)
            if post != None:
                view = str(int(post['view']) + 1)
                db.commit_db(
                    "update posts set view='%s' where url='%s'" % (view, url))
