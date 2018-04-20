from OBlog import database as db
from flask import g
import re
'''
####################################################
                    get tags
####################################################
'''


def getTagsOfPost(url):
    '''
    description:    get the tags of the post
    input:          post url
    output:         List - tags list
    '''
    from ..posts.main import getPostForEdit
    post = getPostForEdit(url)
    return tagSplit(post['tags'])


def tagSplit(tag):
    '''
    description:    from tags string to tags list
    input:          string - tags string
    output:         List - tags list
    '''
    return re.split(r',', tag)


def getRawTags():
    '''
    description:    query all tags
    input:
    output:         List - tags list
    '''
    if not hasattr(g, "tags_getRawTags"):
        g.tags_getRawTags = db.query_db("select * from tags")
    return g.tags_getRawTags


def getChinese(_tag):
    '''
    description:    get the tag by english
    input:          text - tag english
    output:         dict - tag
    '''
    return db.query_db(
            "select * from tags where english='%s'" % _tag, one=True)


def getTag(chinese):
    '''
    description:    get the tag by english
    input:          text - tag english
    output:         dict - tag
    '''
    return db.query_db(
            "select * from tags where chinese='%s'" % chinese, one=True)

def getTags():
    '''
    description:    get all tags
    input:
    output:         dict -  key: tag chinese, 
                            value: dict - tag   
    '''
    if not hasattr(g, "tags_getTags"):
        _Tags = getRawTags()
        Tags = {}
        for Tag in _Tags:
            Tags[Tag['chinese']] = [Tag['english'],
                                    Tag['cnt'], Tag['img'], Tag['class']]
        g.tags_getTags = Tags
    return g.tags_getTags


'''
####################################################
                    set tags
####################################################
'''


def encode(t):
    '''
    description:    encode sha512
    input:          text
    output:         text
    '''
    import hashlib
    return hashlib.sha512(t.encode()).hexdigest()


def addTag(chinese):
    '''
    description:    tag num plus 1
    input:          tag id(chinese)
    output:         0
    '''
    if db.exist_db("tags", {"chinese": chinese}) == True:
        cnt = db.query_db(
            "select cnt from tags where chinese='%s'" % chinese, one=True)['cnt']
        cnt = str(int(cnt) + 1)
        db.update_db("tags", {'cnt': cnt}, {'chinese': chinese})
    else:
        db.insert_db("tags", {"chinese": chinese,
                              "english": encode(chinese), "cnt": "1", "img": "", "class": ""})
    return 0


def subtractTag(chinese):
    '''
    description:    tag num subtract 1
    input:          tag id(chinese)
    output:         0
    '''
    if db.exist_db("tags", {"chinese": chinese}) == True:
        cnt = db.query_db(
            "select cnt from tags where chinese='%s'" % chinese, one=True)['cnt']
        cnt = str(int(cnt) - 1)
        db.update_db("tags", {'cnt': cnt}, {'chinese': chinese})
        if int(cnt) <= 0:
            deleteTag(chinese)


def updateTag(postRequest):
    '''
    description:    set tag attribution
    input:          dict - post request
    output:         0
    '''

    # 后端验证
    pattern = r'^\w+$'
    if not re.match(pattern, postRequest["newenglish"]):
        return 1

    if postRequest['english'] != postRequest['newenglish'] and db.exist_db("tags", {'english': postRequest["newenglish"]}) == True:
        return 2

    oldEnglish = postRequest['english']
    postRequest['english'] = postRequest['newenglish']

       # 删除前端传入的其他参数
    keyList = ['english', 'img', 'class']
    postRequest = dict((key, postRequest[key])for key in keyList)


    db.update_db("tags", postRequest, {'english':oldEnglish})
    return 0


def deleteTag(chinese):
    '''
    description:    delete the tag from database
    input:          tag id(chinese)
    output:         0
    '''
    db.delete_db("tags", {"chinese": chinese})
    return 0
