from . import postsApiBP
from flask import request, session
import json


@postsApiBP.route('/exist/', methods=['POST'])
def exist():
    postRequest = request.form.to_dict()
    from .main import existPost
    status = existPost(postRequest.get('url', ''))
    print(status)
    return json.dumps({'status': '1' if status == True else '0'})


@postsApiBP.route('/add/', methods=['POST'])
def add():
    postRequest = request.form.to_dict()
    from .main import addPost
    status = addPost(postRequest)
    return json.dumps({'status': str(status)})


@postsApiBP.route('/update/', methods=['POST'])
def update():
    postRequest = request.form.to_dict()
    from .main import updatePost
    status = updatePost(postRequest)
    return json.dumps({'status': str(status)})

@postsApiBP.route('/delete/', methods=['POST'])
def delete():
    postRequest = request.form.to_dict()
    from .main import deletePost
    status = deletePost(postRequest)
    return json.dumps({'status': str(status)})
