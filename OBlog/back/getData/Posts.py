import time
import re
from .. import database as db
from . import Tags


def timedeFormat(t):
    return time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S"))



def getPost(url):
    Post = db.query_db("select * from posts where url='%s'" % url, one=True)
    tags = Tags.getTags()

    if Post != None:
        Post["tagsstr"] = Post["tags"]
        tagsList = Tags.TagSplit(Post["tagsstr"])
        Post['tags'] = [[tag] + tags[tag] for tag in tagsList]
    return Post


def getPostByTags(_tag):
    posts = db.query_db("select * from posts where tags like '%%%s%%'" % _tag)
    tags = Tags.getTags()

    res = list()
    for idx, post in enumerate(posts):
        tagsList = Tags.TagSplit(post["tags"])
        if _tag in tagsList:
            post["tagsstr"] = post["tags"]
            post['tags'] = [[tag] + tags[tag] for tag in tagsList]
            res.append(posts[idx])

    res.sort(key=lambda x: timedeFormat(x['time']))

    return res


def getAllPosts():
    Posts = db.query_db("select * from posts")
    tags = Tags.getTags()

    Posts.sort(key=lambda x: timedeFormat(x['time']))
    for post in Posts:
        post["tagsstr"] = post["tags"]
        tagsList = Tags.TagSplit(post["tagsstr"])
        post['tags'] = [[tag] + tags[tag] for tag in tagsList]
    return Posts


def getPublishedPosts():
    Posts = db.query_db("select * from posts where published='1'")
    tags = Tags.getTags()

    Posts.sort(key=lambda x: timedeFormat(x['time']))
    for post in Posts:
        post["tagsstr"] = post["tags"]
        tagsList = Tags.TagSplit(post["tagsstr"])
        post['tags'] = [[tag] + tags[tag] for tag in tagsList]
    return Posts


def getAllPostsForSearch():
    '''
    获得所有文章的搜索部分信息，只用于搜索
    '''
    return db.query_db("select url,searchdict1,searchdict2 from posts;")


def getPublishedPostsForSearch():
    '''
    获得所有已发布文章的搜索部分信息，只用于搜索
    '''
    return db.query_db("select url,searchdict1,searchdict2 from posts where published='1';")


def getPostsDetailByUrlForSearch(urls):
    '''
    获取给定URL的具体信息（只用于搜索）
    '''
    posts = db.query_db("select url,title,abstruct,html,tags,time from posts where url in ('%s');"% "','".join(urls))
    tags = Tags.getTags()

    for post in posts:
        post["tagsstr"] = post["tags"]
        tagsList = Tags.TagSplit(post["tagsstr"])
        post['tags'] = [[tag] + tags[tag] for tag in tagsList]
    return posts
