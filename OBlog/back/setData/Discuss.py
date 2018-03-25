from .. import database as db
from ..markdown.markdown import renderMarkdown
from ..getData.Discuss import getLastID, getDiscussOfID
from ..getData.Posts import getPost
from ..getData.Site import getConfig

import time
import re

from ..sendemail import Email


def contain_zh(word):
    return re.match(u'[\u4e00-\u9fa5]+',word)!=None

def add(_set):
    if not re.match(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[A-Za-z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', _set['email']):
        return 1
    if not contain_zh(_set['raw']):
        return 2

    _set['id'] = str(getLastID() + 1)
    _set['html'] = renderMarkdown(_set['raw'], allowHtml=False)
    _set['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    _set['username'] = _set['email'][0:2] + '******' + _set['email'][-2:]
    _set['show'] = '1'
    _set['ad'] = '0'

    # print(_set)
    db.insert_db("discuss", _set)

    config = getConfig()
    rooturl = config['rooturl']
    rooturl = rooturl + '/' if rooturl[-1] != '/' else rooturl

    post = getPost(_set['url'][5:]) if len(_set['url']) > 5 else None
    title = post['title'] if post else '评论区'

    url = rooturl + _set['url']

    res = re.match(r'@([0-9]+)#', _set['raw'])
    if res:
        for _id in res.groups():
            d = getDiscussOfID(_id)
            if d and d["sendemail"] == '1':
                Email([d['email']], d['email'],
                      "评论通知", "您好<br>有人在评论中@您，点击链接查看评论内容<br><a href='" +
                      url + "'>" + title + "</a><br>若无法点击链接，可以将网址(" + url + ")复制到地址栏")
    Email(["oyohyee@oyohyee.com"], config["email"], "评论通知", _set['email'] +
          "评论了文章<a href='" + url + "'>" + title + "</a>(" + url + ")<br>内容如下<br>" + _set['html'])
    return 0


def update(_set, _where):
    if not re.match(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[A-Za-z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', _set['email']):
        return 1

    db.update_db("discuss", _set, _where)
    return 0
