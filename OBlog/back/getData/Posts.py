import time
import re
from .. import database as db
from . import Tags
from flask import g
from . import Site


def timedeFormat(t):
    return time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S"))

def formatTags(posts):
    if posts != None:
        tags = Tags.getTags()        
        if type(posts)==list:
            for post in posts:
                post["tagsstr"] = post["tags"]
                tagsList = Tags.TagSplit(post["tagsstr"])
                post['tags'] = [[tag] + tags[tag] for tag in tagsList]
        else:
            posts["tagsstr"] = posts["tags"]
            tagsList = Tags.TagSplit(posts["tagsstr"])
            posts['tags'] = [[tag] + tags[tag] for tag in tagsList]
    return posts
   
def getPost(url):
    post = db.query_db("select * from posts where url='%s'" % url, one=True)
    tags = Tags.getTags()
    formatTags(post)
    return post

def getPostForCard(url):
    post = db.query_db("select * from posts_card where url='%s'" % url, one=True)
    tags = Tags.getTags()
    formatTags(post)
    return post


def getPostByTags(_tag):
    posts = db.query_db("select * from posts_card where tags like '%%%s%%'" % _tag)
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
    posts = db.query_db("select * from posts_card")
    formatTags(posts)
    posts.sort(key=lambda x: timedeFormat(x['time']))
    return posts


def getPublishedPosts():
    posts = db.query_db("select * from posts_card where published='1'")
    formatTags(posts)    
    posts.sort(key=lambda x: timedeFormat(x['time']))
    return posts


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
    posts = db.query_db("select * from posts_card where url in ('%s');"% "','".join(urls))
    formatTags(posts)
    return posts

def getNewestPosts():
    posts = db.query_db("select * from posts_card order by time desc limit 5")
    formatTags(posts)
    return posts

def getRecommendPosts():
    Config = Site.getConfig()
    posts = []
    for url in Config['recommend'].split(','):
        posts.append(getPostForCard(url))
    return posts