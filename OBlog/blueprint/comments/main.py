from OBlog import database as db
from .sendEmail import Email
from ..posts.main import getPostForShow
from OBlog.markdown import renderMarkdown
import re
import time

from ..admin.main import getSiteConfigDict


def getCommentsOfUrlForShow(url):
    res = db.query_db(
        "select id,html,username,time,sendemail,ad from comments where url='%s' and show='true'" % url)
    return res


def getCommentsOfID(_id):
    return db.query_db("select * from comments where id='%s'" % (_id), one=True)


def getAllComments():
    return db.query_db("select * from comments;")


def getLastID():
    res = db.raw_query_db("select count(id) from comments")
    # print(res[0][0])
    return res[0][0]


def contain_zh(word):
    '''
    description:    检测是否存在中文
    input:          文本
    output:         bool - True:存在中文;False:不存在中文
    '''
    return len(re.findall(u'[\u4e00-\u9fa5]+', word)) != 0


def mail(postUrl, raw):
    '''
    description:    给该评论@的所有用户以及站长发信
    input:          text - postUrl  评论的页面链接
                    text - raw      评论内容
    output:         
    '''
    config = getSiteConfigDict()
    if config['smtp'] != '1':  # 未开启smtp
        return

    rooturl = config['rooturl']
    if rooturl:  # 未填写相应项
        rooturl = "/"
    rooturl = rooturl + '/' if rooturl[-1] != '/' else rooturl

    post = getPostForShow(postUrl[5:]) if len(postUrl) > 5 else None
    title = post['title'] if post else '评论区'

    url = rooturl + postUrl

    mailList = re.match(r'@([0-9]+)#', raw)

    for _id in mailList:
        d = getDiscussOfID(_id)
        if d and d["sendemail"] == 'true' and d["show"] == 'true':
            Email([d['email']], d['email'],
                  "评论通知", "您好<br>有人在评论中@您，点击链接查看评论内容<br><a href='" +
                  url + "'>" + title + "</a><br>若无法点击链接，可以将网址(" + url + ")复制到地址栏")
    Email(["oyohyee@oyohyee.com"], config["email"], "评论通知", postRequest['email'] +
          "评论了文章<a href='" + url + "'>" + title + "</a>(" + url + ")<br>内容如下<br>" + postRequest['html'])


def addComment(postRequest):
    print(postRequest)

    if not re.match(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[A-Za-z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', postRequest['email']):
        return [1,'']
    if not contain_zh(postRequest['raw']):
        return [2,'']

    postRequest['id'] = str(getLastID() + 1)
    postRequest['html'] = renderMarkdown(postRequest['raw'], allowHtml=False)
    postRequest['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    postRequest['username'] = postRequest['email'][0:2] + \
        '******' + postRequest['email'][-2:]
    postRequest['show'] = 'true'
    postRequest['ad'] = 'false'

    keyList = ['id', 'raw', 'html', 'time', 'username',
               'email', 'sendemail', 'show', 'ad', 'url', 'ip']
    postRequest = dict((key, postRequest[key])for key in keyList)

    print(postRequest)

    db.insert_db("comments", postRequest)

    mail(postRequest['url'], postRequest['raw'])
    return [0,postRequest]

def updateComment(postRequest):
    cid = postRequest['id']

    keyList = ['sendemail', 'show', 'ad']
    postRequest = dict((key, postRequest[key])for key in keyList)

    db.update_db("comments", postRequest, {'id': cid})
    return 0
