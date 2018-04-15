from . import postsApiBP
from flask import request, session
import json




@postsApiBP.route('/edit/exist/', methods=['POST'])
def exist():
    postRequest = request.form.to_dict()
    from .main import existPost
    status = existPost(postRequest.get('url', ''))
    return json.dumps({'status': '0' if status else '1'})


@postsApiBP.route('/edit/add/', methods=['POST'])
def add():
    postRequest = request.form.to_dict()
    from .main import addPost
    status = addPost(postRequest)
    return json.dumps({'status': '0' if status else '1'})



