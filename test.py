import re
import math

import jieba
from jieba.analyse import textrank

posts = [
    {
        "title": "正则表达式详解",
        "content": "使用正则表达式能够非常方便地匹配文本"
    },
    {
        "title": "Git使用详解",
        "content": "使用Git帮助你进行代码管理"
    },
    {
        "title": "笔记",
        "content": "使用正则表达式进行文本匹配，使用git进行代码管理"
    }
]


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


def calc(searchArray, post):
    res = 2 * cross(searchArray, getCntDict(post["title"]))
    res += cross(searchArray, getCntDict(post["content"]))
    return res


def search(searchtext, items):
    searchArray = jieba.lcut_for_search(searchtext)
    res = dict((idx, calc(searchArray, item))
               for (idx, item) in enumerate(items))
    res = dictSort(res, reverse=True)
    print(res)


search("正则表达式", posts)

# ls = jieba.lcut(text)
# ans = {}
# for item in ls:
#     if item in ans:
#         ans[item] += 1
#     else:
#         ans[item]=1


# print(ans)

# res = textrank(text, topK=50, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
# # ChineseAnalyzer
# print(res)
