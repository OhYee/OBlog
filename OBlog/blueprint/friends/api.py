from . import friendsApiBP
from flask import request
import json


@friendsApiBP.route('/add/', methods=['POST'])
def add():
    postRequest = request.form.to_dict()
    from .main import addFriends
    status = addFriends(postRequest)
    return json.dumps({'status': str(status)})


@friendsApiBP.route('/update/', methods=['POST'])
def update():
    from .main import updateFriends
    postRequest = request.form.to_dict()
    # postRequest['show'] = '1' if 'show' in request.values else '0'
    status = updateFriends(postRequest)
    return json.dumps({'status': str(status)})


@friendsApiBP.route('/delete/', methods=['POST'])
def delete():
    from .main import deleteFriends
    status = deleteFriends(request.form.to_dict())
    return json.dumps({'status': str(status)})
