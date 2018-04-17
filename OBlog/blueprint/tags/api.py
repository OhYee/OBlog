from . import tagsApiBP
from flask import request
import json

@tagsApiBP.route('/update/', methods=['POST'])
def update():
    postRequest = request.form.to_dict()
    from .main import updateTag
    status = updateTag(postRequest)
    return json.dumps({'status': str(status)})
