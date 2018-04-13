from . import pagesApiBP
from flask import request, session
import json


@pagesApiBP.route('/add/', methods=['POST'])
def add():
    postRequest = request.form.to_dict()
    from .main import addPages
    status = addPages(postRequest)
    return json.dumps({'status': str(status)})


@pagesApiBP.route('/update/', methods=['POST'])
def update():
    from .main import updatePage
    postRequest = request.form.to_dict()
    # postRequest['show'] = '1' if 'show' in request.values else '0'
    status = updatePage(postRequest)
    return json.dumps({'status': str(status)})


@pagesApiBP.route('/delete/', methods=['POST'])
def delete():
    from .main import deletePage
    status = deletePage(request.form.to_dict())
    return json.dumps({'status': str(status)})


@pagesApiBP.route('/edit/getlist/')
def getList():
    from .main import getPageTemplateList
    return json.dumps(getPageTemplateList())


@pagesApiBP.route('/edit/get/', methods=['post'])
def getTemplate():
    postRequest = request.form.to_dict()
    path = postRequest.get('path', '')
    from .main import getPageTemplate
    status = getPageTemplate(path)
    return json.dumps({'status': str(status[0]), 'content': status[1]})


@pagesApiBP.route('/edit/update/', methods=['POST'])
def updateTemplate():
    from .main import setPageTemplate
    status = setPageTemplate(request.form.get(
        'path', ''), request.form.get('content', ''))
    return json.dumps({'status': str(status)})


@pagesApiBP.route('/edit/delete/', methods=['POST'])
def deleteTemplate():
    from .main import delPageTemplate
    status = delPageTemplate(request.form.get('path', ''))
    return json.dumps({'status': str(status)})
