from . import backupApiBP
import json


@backupApiBP.route('/exportTags/')
def exportTags():
    from ..tags.main import getRawTags
    tags = getRawTags()
    res = {}
    for tag in tags:
        res[tag['chinese']] = {
            'english': tag['english'],
            'img': tag['img'],
            'class': tag['class']
        }
    f = open("tags.json", 'w')
    f.write(json.dumps(res))
    f.close()
    return json.dumps({'status': '0','hint':'导出标签到tags.json完成'})


@backupApiBP.route('/importTags/')
def importTags():
    f = open("tags.json", 'r')
    tags = json.loads(f.read())
    f.close()

    cnt = len(tags)
    from ..tags.main import updateTag
    for (idx, tag) in enumerate(tags):
        print(str(idx + 1) + '/' + str(cnt), tag)
        updateTag({
            'chinese': tag,
            'english': tags[tag]['english'],
            'newenglish': tags[tag]['english'],
            'img': tags[tag]['img'],
            'class': tags[tag]['class']
        })

    return json.dumps({'status': '0','hint':'从tags.json导入标签完成'})


@backupApiBP.route('/importPosts/')
def importPosts():
    f=open('./posts.json', 'r')
    posts=json.loads(f.read())
    cnt=len(posts)
    for (idx, post) in enumerate(posts):
        print(str(idx + 1) + '/' + str(cnt), post['url'])
        from ..posts.main import existPost, addPost, updatePost
        if existPost(post['url']):
            post['oldurl']=post['url']
            updatePost(post)
        else:
            addPost(post)
    f.close()
    return json.dumps({'status': '0','hint':'从posts.json导入文章完成'})


@backupApiBP.route('/exportPosts/')
def exportPosts():
    f=open('./posts.json', 'w')
    from ..posts.main import getAllPosts
    f.write(json.dumps(getAllPosts()))
    f.close()
    return json.dumps({'status': '0','hint':'导出文章到posts.json完成'})
