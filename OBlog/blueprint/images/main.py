import os
import time
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

import os
from OBlog import app


ALLOWED_EXTENSIONS = set(['jpg', 'png', 'gif', 'jpeg', 'bmp'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_file(file, dirname):
    filename = secure_filename(file.filename)
    path = os.path.join(
        './OBlog', app.config['STATIC_FOLDER'], dirname, filename).replace('\\', '/')

    if file and allowed_file(file.filename) and not os.path.exists(path):
        print("upload: ", path)
        file.save(os.path.join(path))
        return [0, path]
    else:
        return [1]


def getRandomString():
    return (str)(time.time())


def rename(oldfilename, filename, dirname):
    oldfilename = os.path.join(
        './OBlog', app.config['STATIC_FOLDER'], dirname, oldfilename)
    filename = os.path.join(
        './OBlog', app.config['STATIC_FOLDER'], dirname, filename)
    os.rename(oldfilename, filename)


def delete(filename, dirname):
    filename = os.path.join(
        './OBlog', app.config['STATIC_FOLDER'], dirname, filename)
    os.remove(filename)


def tree(root='./', relativePath='.', nowDirname='.'):
    nowPath = os.path.join(root, relativePath)
    dirList = []
    fileList = []
    for file in os.listdir(nowPath):
        if os.path.isfile(os.path.join(nowPath, file)):
            fileList.append(file)
        else:
            dirList.append(file)

    res = {
        'path': relativePath,
        'file': fileList,
        'dir': dict((dirname, tree(root, os.path.join(relativePath, dirname), dirname))for dirname in dirList)
    }
    return res


def getImageList():
    image_folder = os.path.join(
        app.config['ROOTPATH'], 'OBlog','static','img')
    return tree(root=image_folder)
