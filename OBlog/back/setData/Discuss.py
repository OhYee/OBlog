from .. import database as db
from ..markdown.markdown import renderMarkdown
from ..getData.Discuss import getLastID, getDiscussOfID
import time
import re

from ..sendemail import Email


def add(_set):
    if not re.match(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[A-Za-z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', _set['email']):
        return 1

    res = re.match(r'@([0-9]+)#', _set['raw'])
    if res:
        for _id in res.groups():
            d = getDiscussOfID(_id)
            if d and d["sendemail"] == '1':
                Email([d['email']], d['email'],
                          "评论通知", "有人回复了您在<a href='" +
                          _set['url'] + "'>OhYee</a>的评论")

    _set['id'] = str(getLastID() + 1)
    _set['html'] = renderMarkdown(_set['raw'], allowHtml=False)
    _set['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    _set['username'] = _set['email'][0:2] + '******' + _set['email'][-2:]
    _set['show'] = '1'

    # print(_set)
    db.insert_db("discuss", _set)
    return 0


def update(_set, _where):
    if not re.match(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[A-Za-z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', _set['email']):
        return 1

    db.update_db("discuss", _set, _where)
    return 0
