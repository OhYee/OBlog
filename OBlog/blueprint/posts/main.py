from OBlog import database as db
from flask import g, current_app
import re

'''
####################################################
                    get posts
####################################################
'''


def existPost(url):
    return db.exist_db('posts', {'url': url})


def getPostsForList():
    if not hasattr(g, "getPostsForList"):
        res = db.query_db("select * from posts_list;")
        # res.sort(key=lambda x: int(x["idx"]))
        g.getPostsForList = res
    return g.getPostsForList


def getPostForEdit(url):
    '''
    description:    get the post for edit
    input:          text - url of the post
    output:         dict - post
    '''
    if not hasattr(g, "getPostForEdit"):
        res = db.query_db(
            "select * from posts_edit where url='%s';" % url, one=True)
        # res.sort(key=lambda x: int(x["idx"]))
        g.getPostForEdit = res
    return g.getPostForEdit


def getPostForShow(url):
    '''
    description:    get the post for show(post pages)
    input:          text - url of the post
    output:         dict - post
    '''
    if not hasattr(g, "getPostForShow"):
        res = db.query_db(
            "select * from posts_show where url='%s';" % url, one=True)
        # res.sort(key=lambda x: int(x["idx"]))
        g.getPostForShow = res
    return g.getPostForShow


# def getPost(url):
#     post = db.query_db("select * from posts where url='%s'" % url, one=True)
#     tags = getTags()
#     #formatTags(post)
#     return post


'''
####################################################
                    set posts
####################################################
'''


def addPost(postRequest):
    current_app.logger.debug(postRequest)

    pattern = [
        r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$',
        r'^[0-9]+$',
        r'^[\w\-\.,@?^=%&:~\+#]+(?:\/[\w\-\.,@?^=%&:~\+#]+)*$'
    ]
    if not (re.match(pattern[0], postRequest["time"]) and re.match(pattern[0], postRequest["updatetime"]) and
            re.match(pattern[1], postRequest["view"]) and re.match(pattern[2], postRequest["url"])):
        return 1
    if db.exist_db("posts", {'url': postRequest["url"]}) == True:
        return 2

    if postRequest['tags'] == '':
        postRequest['tags'] = '无标签'

    from OBlog.markdown import renderMarkdown
    import json
    from ..search.main import getCntDict, getKeywords

    postRequest['html'] = renderMarkdown(postRequest['raw'])
    postRequest['keywords'] = postRequest['tags'] + \
        getKeywords(postRequest['title'] + postRequest['raw'])
    postRequest['searchdict1'] = json.dumps(
        getCntDict(postRequest["title"] + " " + postRequest['tags']))
    postRequest['searchdict2'] = json.dumps(
        getCntDict(postRequest['abstruct'] + " " + postRequest["raw"]))

    # 新的标签计数加1
    from ..tags.main import tagSplit, addTag
    tags = tagSplit(postRequest['tags'])
    for tag in tags:
        addTag(tag)

    # 去除前导零
    postRequest["view"] = str(int(postRequest["view"]))

    # 删除前端传入的其他参数
    keyList = ['url', 'title', 'time', 'updatetime',
               'view', 'tags', 'abstruct', 'raw', 'html', 'keywords', 'searchdict1', 'searchdict2', 'published']
    postRequest = dict((key, postRequest[key])for key in keyList)

    db.insert_db("posts", postRequest)
    return 0


def updatePost(postRequest):
    current_app.logger.debug(postRequest)

    oldurl = postRequest["oldurl"]

    # 后端验证
    pattern = [
        r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$',
        r'^[0-9]+$',
        r'^[\w\-\.,@?^=%&:~\+#]+(?:\/[\w\-\.,@?^=%&:~\+#]+)*$'
    ]
    if not (re.match(pattern[0], postRequest["time"]) and re.match(pattern[0], postRequest["updatetime"]) and
            re.match(pattern[1], postRequest["view"]) and re.match(pattern[2], postRequest["url"])):
        return 1
    if oldurl != postRequest['url'] and db.exist_db("posts", {'url': postRequest["url"]}) == True:
        return 2

    if postRequest['tags'] == '':
        postRequest['tags'] = '无标签'

    from OBlog.markdown import renderMarkdown
    import json
    from ..search.main import getCntDict, getKeywords

    postRequest['html'] = renderMarkdown(postRequest['raw'])
    postRequest['keywords'] = postRequest['tags'] + \
        getKeywords(postRequest['title'] + postRequest['raw'])
    postRequest['searchdict1'] = json.dumps(
        getCntDict(postRequest["title"] + " " + postRequest['tags']))
    postRequest['searchdict2'] = json.dumps(
        getCntDict(postRequest['abstruct'] + " " + postRequest["raw"]))

    # 更新标签
    from ..tags.main import getTagsOfPost, tagSplit, addTag, subtractTag

    oldtags = getTagsOfPost(oldurl)
    newtags = tagSplit(postRequest['tags'])
    alltags = set(oldtags + newtags)
    for tag in alltags:
        if tag in oldtags and tag not in newtags:
            subtractTag(tag)
        elif tag not in oldtags and tag in newtags:
            addTag(tag)

    # 去除前导零
    postRequest["view"] = str(int(postRequest["view"]))

    # 删除前端传入的其他参数
    keyList = ['url', 'title', 'time', 'updatetime',
               'view', 'tags', 'abstruct', 'raw', 'html', 'keywords', 'searchdict1', 'searchdict2', 'published']
    postRequest = dict((key, postRequest[key])for key in keyList)

    db.update_db("posts", postRequest, {'url': oldurl})
    return 0


def deletePost(postRequest):
    current_app.logger.debug(postRequest)

    url = postRequest['url']

    # 老的标签计数减1
    from ..tags.main import getTagsOfPost, subtractTag
    tags = getTagsOfPost(url)
    for tag in tags:
        subtractTag(tag)

    db.delete_db("posts", {'url': url})
    return 0
