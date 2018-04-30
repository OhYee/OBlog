from flask import request
from . import goodsApiBP
import json


@goodsApiBP.route('/add/', methods=["POST"])
def add():
    postRequest = request.form.to_dict()
    from .main import addGood    
    status = addGood(postRequest)
    return json.dumps({'status': str(status)})


@goodsApiBP.route('/update/', methods=["POST"])
def update():
    postRequest = request.form.to_dict()
    from .main import updateGood    
    status = updateGood(postRequest)
    return json.dumps({'status': str(status)})
