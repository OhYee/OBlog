
import _thread
from .GlobalVariable import getGV, setGV
from .getData.Tags import getRawTags
import json


def exportTagsThread():
    tags = getRawTags()
    res = {}
    for tag in tags:
        res[tag['chinese']] = {
            'english': tag['english'],
            'img': tag['img'],
            'class': tag['class']
        }
    console = getGV('console')
    if console:
        console = json.loads(console)
        console['output'] += '\n' + str(res)
        setGV('console', json.dumps(console))
    else:
        setGV('console', json.dumps(
            {"now": 0, "total": 100, "output": "线程错误"}))


def exportTags():
    try:
        _thread.start_new_thread(exportTagsThread)
        setGV('console', json.dumps(
            {"now": 0, "total": 100, "output": "后台线程启动，开始执行任务-输出标签"}))
    except:
        setGV('console', json.dumps(
            {"now": 0, "total": 100, "output": "无法启动后台线程"}))
    count = 0
