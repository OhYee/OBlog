from flask import render_template, request, session, abort
from . import commentsApiBP
from .main import addComment, updateComment, getCommentsOfUrlForShow
import json


@commentsApiBP.route('/get/', methods=["POST"])
def get():
    postRequest = request.form.to_dict()
    status = getCommentsOfUrlForShow(postRequest['url'])
    return json.dumps(status)


@commentsApiBP.route('/add/', methods=["POST"])
def add():
    postRequest = request.form.to_dict()
    postRequest['ip'] = request.headers.get(
        'X-Forwarded-For', request.remote_addr)
    status = addComment(postRequest)
    return json.dumps({'status': str(status[0]),'comment':status[1]})


@commentsApiBP.route('/update/', methods=["POST"])
def update():
    if session.get('admin', False) == False:
        abort(401)
    postRequest = request.form.to_dict()
    status = updateComment(postRequest)
    return json.dumps({'status': str(status)})
