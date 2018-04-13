from . import postsApiBP
from flask import request, session
import json


@postsApiBP.route('/add/', methods=['POST'])
def add():
    postRequest = request.form.to_dict()
    from .main import addPosts
    status = addPosts(postRequest)
    return json.dumps({'status': str(status)})


@postsApiBP.route('/update/', methods=['POST'])
def update():
    from .main import updatePost
    postRequest = request.form.to_dict()
    # postRequest['show'] = '1' if 'show' in request.values else '0'
    status = updatePost(postRequest)
    return json.dumps({'status': str(status)})


@postsApiBP.route('/delete/', methods=['POST'])
def delete():
    from .main import deletePost
    status = deletePost(request.form.to_dict())
    return json.dumps({'status': str(status)})


@postsApiBP.route('/edit/getlist/')
def getList():
    from .main import getPostTemplateList
    return json.dumps(getPostTemplateList())


@postsApiBP.route('/edit/get/', methods=['post'])
def getTemplate():
    postRequest = request.form.to_dict()
    path = postRequest.get('path', '')
    from .main import getPostTemplate
    status = getPostTemplate(path)
    return json.dumps({'status': str(status[0]), 'content': status[1]})


@postsApiBP.route('/edit/update/', methods=['POST'])
def updateTemplate():
    from .main import setPostTemplate
    status = setPostTemplate(request.form.get(
        'path', ''), request.form.get('content', ''))
    return json.dumps({'status': str(status)})


@postsApiBP.route('/edit/delete/', methods=['POST'])
def deleteTemplate():
    from .main import delPostTemplate
    status = delPostTemplate(request.form.get('path', ''))
    return json.dumps({'status': str(status)})
