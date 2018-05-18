import jieba
from OBlog import database as db
from jieba.analyse import textrank


def getKeywords(text):
    lst = textrank(text)
    return ',' + ','.join(lst)


def searchTags(searchWord):
    searchWordList = jieba.cut_for_search(searchWord)
    res = []
    for word in searchWordList:
        res += db.query_db(
            'select chinese from tags where chinese like "%%{}%%";', word)
        res += db.query_db(
            'select chinese from tags where english like "%%{}%%";', word)

    res = [item['chinese'] for item in res]
    res = list(set(res))
    from ..tags.main import getTag
    res = [getTag(chinese) for chinese in res]
    return res


def searchPosts(searchWord):
    searchWordList = jieba.cut_for_search(searchWord)

    queryStr = [
        'title like "%{0}%" or abstruct like "%{0}%" or raw like "%{0}%" or tags like "%{0}%"'.format(
            db.escapeChar(word))
        for word in searchWordList
    ]
    queryStr = ' or '.join(queryStr)

    queryStr = 'select * from posts_card where url in (select url from posts where ({0}) and url in(select url from posts where published="true")) order by updatetime DESC;'.format(
        queryStr)

    posts = db.query_db(queryStr)

    from ..tags.main import getTags
    tags = getTags()

    for post in posts:
        post['tags'] = [tags[tag] for tag in post['tags'].split(',')]
    return posts
