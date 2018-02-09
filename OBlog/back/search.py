import math
import jieba
import json
from jieba.analyse import textrank

from .getData import Tags
from .getData import Posts


def dictSort(dic, reverse=False):
    lst = [item for item in dic]
    lst.sort(key=lambda x: dic[x], reverse=reverse)
    res = dict((item, dic[item])for item in lst)
    return res


def getCntDict(text):
    lt = jieba.lcut_for_search(text)
    dic = {}
    for i in lt:
        if i in dic:
            dic[i] += 1
        else:
            dic[i] = 1
    return dictSort(dic, reverse=False)


def cross(searchArray, targetDict):
    score = 0.0
    for word in searchArray:
        if word in targetDict:
            score += targetDict[word]
    score = math.log10(1 + score)
    return score


def calc_posts(searchArray, post):
    # print(post)
    res = 2 * cross(searchArray, json.loads(post['searchdict1']))
    res += cross(searchArray, json.loads(post['searchdict2']))
    return res


def calc_tags(searchArray, tag):
    # print(tag)
    Str = tag["chinese"]
    if len(tag["english"]) < 10:
        Str += " " + tag["english"]
    res = cross(searchArray, getCntDict(Str))
    return res


def deleteUnmatched(dic):
    keys = [key for key in dic if dic[key] == 0]
    for key in keys:
        dic.pop(key)
    return dic


def search(searchtext, items, calc):
    searchtext = searchtext.replace(' ', '')
    searchArray = jieba.lcut_for_search(searchtext)
    print("searchArray:", searchArray)
    res = dict((idx, calc(searchArray, item))
               for (idx, item) in enumerate(items))
    res = dictSort(res, reverse=True)
    # print('res', res)
    res = deleteUnmatched(res)
    reslist = [items[idx] for idx in res]
    return reslist


def search_Tags(searchtext):
    return search(searchtext, Tags.getRawTags(), calc_tags)


def search_PublishedPosts(searchtext):
    posts = search(searchtext, Posts.getPublishedPostsForSearch(), calc_posts)
    urls = [post['url'] for post in posts]
    return Posts.getPostsDetailByUrlForSearch(urls)


def search_AllPosts(searchtext):
    posts = search(searchtext, Posts.getAllPostsForSearch(), calc_posts)
    urls = [post['url'] for post in posts]
    return Posts.getPostsDetailByUrlForSearch(urls)
