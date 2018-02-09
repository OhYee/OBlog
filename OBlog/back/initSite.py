from flask import g
from .getData import Site
from .sendemail import thirdSMTP
import jieba


def initSite():
    jieba.initialize()
    # app.app_context().push()  
    # current_app.name  
    # g.test="test"
    # g.Site = Site.getSite()
    # if g.Site["config"]["smtp"] == '1':
    #     g.smtp = thirdSMTP(g.Site["config"]["smtpservice"], g.Site["config"]["smtpuser"],
    #                        g.Site["config"]["smtppassword"], g.Site["config"]["smtpport"])
    # # g.db.close()
