from . import adminApiBP
from flask import request, session, current_app, redirect, url_for
import json


@adminApiBP.route('/login/', methods=['POST'])
def login():
    from .main import checkPassword
    status = checkPassword(request.form.to_dict())
    if status == 0:
        session['admin'] = True
    return json.dumps({'status': str(status)})


@adminApiBP.route('/update/', methods=['POST'])
def update():
    if session.get('admin',False)!=True:
        abort(401)
    from .main import setSite
    status = setSite(request.form.to_dict())
    return json.dumps({'status': str(status)})
