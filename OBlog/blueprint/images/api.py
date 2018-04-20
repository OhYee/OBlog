from . import imagesApiBP
from .main import uploadFile, renameFile, deleteFile
import json
from flask import request


@imagesApiBP.route('/upload/', methods=["POST"])
def upload():
    dirname = request.form.to_dict().get('path', '/')
    status = uploadFile(request.files['file'], dirname)
    print(status)
    ret = {}
    if status[0] == 0:
        ret = {'status': '0', 'filename': status[1], 'path': status[2]}
    else:
        ret = {'status': '1'}
    return json.dumps(ret)


@imagesApiBP.route('/rename/', methods=["POST"])
def rename():
    oldfilename = request.form['oldfilename']
    filename = request.form['filename']
    status = renameFile(oldfilename, filename)
    return json.dumps({'status': str(status)})


@imagesApiBP.route('/delete/', methods=["POST"])
def delete():
    filename = request.form['filename']
    status = deleteFile(filename)
    return json.dumps({'status': str(status)})
