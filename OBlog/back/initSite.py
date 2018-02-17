from flask import g
from .getData import Site
from .sendemail import thirdSMTP
import jieba


import sys
import os

def Log(text, *args):
    logStr = (text + '\n') % args
    with open(os.path.join(sys.path[0], r'log/test.log'), 'a+') as f:
        f.write(logStr)


def initSite():
    print("OBlog start")
    Log("run initSite")
    
    #jieba.initialize()
    # app.app_context().push()  
    # current_app.name  
    # g.test="test"
    # g.Site = Site.getSite()
    # if g.Site["config"]["smtp"] == '1':
    #     g.smtp = thirdSMTP(g.Site["config"]["smtpservice"], g.Site["config"]["smtpuser"],
    #                        g.Site["config"]["smtppassword"], g.Site["config"]["smtpport"])
    # # g.db.close()
