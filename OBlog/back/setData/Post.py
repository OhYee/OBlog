import re
import json
from jieba.analyse import textrank
from .. import database as db
from ..setData import Tags as setTags
from ..getData import Tags as getTags
from ..markdown.markdown import renderMarkdown
from ..search import getCntDict


def getKeywords(text):
    lst = textrank(text)
    return ',' + ','.join(lst)


def add(_map):
    # 后端验证
    pattern = [
        r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$',
        r'^[0-9]+$',
        r'^[\w\-\.,@?^=%&:~\+#]+(?:\/[\w\-\.,@?^=%&:~\+#]+)*$'
    ]
    if not (re.match(pattern[0], _map["time"]) and re.match(pattern[0], _map["updatetime"]) and
            re.match(pattern[1], _map["view"]) and re.match(pattern[2], _map["url"])):
        return 1
    if db.exist_db("posts", {'url': _map["url"]}) == True:
        return 2

    if _map['tags'] == '':
        _map['tags'] = '无标签'

    _map['html'] = renderMarkdown(_map['raw'])
    _map['keywords'] = _map['tags'] + getKeywords(_map['title'] + _map['raw'])
    _map['searchdict1'] = json.dumps(
        getCntDict(_map["title"] + " " + _map['tags']))
    _map['searchdict2'] = json.dumps(
        getCntDict(_map['abstruct'] + " " + _map["raw"]))

    # 新的标签计数加1
    tags = getTags.TagSplit(_map['tags'])
    for tag in tags:
        setTags.add(tag)

    # 去除前导零
    _map["view"] = str(int(_map["view"]))
    #_map["discuss"] = str(int(_map["discuss"]))

    db.insert_db("posts", _map)
    return 0


def update(_set, _where):
    # 后端验证
    pattern = [
        r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$',
        r'^[0-9]+$',
        r'^[\w\-\.,@?^=%&:~\+#]+(?:\/[\w\-\.,@?^=%&:~\+#]+)*$'
    ]
    if not (re.match(pattern[0], _set["time"]) and re.match(pattern[0], _set["updatetime"]) and
            re.match(pattern[1], _set["view"]) and re.match(pattern[2], _set["url"])):
        return 1
    if _where['url'] != _set['url'] and db.exist_db("posts", {'url': _set["url"]}) == True:
        return 2

    if _set['tags'] == '':
        _set['tags'] = '无标签'

    _set['html'] = renderMarkdown(_set['raw'])
    _set['keywords'] = _set['tags'] + getKeywords(_set['title'] + _set['raw'])
    _set['searchdict1'] = json.dumps(
        getCntDict(_set["title"] + " " + _set['tags']))
    _set['searchdict2'] = json.dumps(
        getCntDict(_set['abstruct'] + " " + _set["raw"]))
    # 更新标签
    oldtags = getTags.TagSplit(db.query_db(
        "select tags from posts where url='%s'" % _where['url'], one=True)["tags"])
    newtags = getTags.TagSplit(_set['tags'])
    alltags = set(oldtags + newtags)
    for tag in alltags:
        if tag in oldtags and tag not in newtags:
            setTags.subtract(tag)
        elif tag not in oldtags and tag in newtags:
            setTags.add(tag)

    # 去除前导零
    _set["view"] = str(int(_set["view"]))
    #_set["discuss"] = str(int(_set["discuss"]))

    db.update_db("posts", _set, _where)
    return 0


def delete(_where):
    # 老的标签计数减1
    tags = db.query_db("select tags from posts where url='%s'" %
                       _where['url'], one=True)
    tags = getTags.TagSplit(tags['tags'])
    for tag in tags:
        setTags.subtract(tag)

    db.delete_db("posts", _where)
