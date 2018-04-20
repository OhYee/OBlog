import os
import time
from flask import current_app
# from werkzeug import secure_filename

import os
from OBlog import app


ALLOWED_EXTENSIONS = set(['jpg', 'png', 'gif', 'jpeg', 'bmp'])


def getImageFolder():
    res = os.path.join(app.config['ROOTPATH'], 'OBlog', 'static', 'img')
    return res


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def secure_filename(filename):
    filename = filename.replace('/','_').replace('\\','_')
    return filename

def uploadFile(file, dirname):
    print(file, dirname)
    filename = secure_filename(file.filename)
    path = getImageFolder() + dirname + filename
    print(path)
    if file and allowed_file(file.filename) and not os.path.exists(path):
        print("upload: ", path)
        file.save(path)
        return [0, filename, path]
    else:
        return [1]


def renameFile(oldfilename, filename):
    # 这里由于前端传入的参数，使用 os.path.join() 会被认为是根目录
    oldfilename = oldfilename.replace('/', '\\')
    filename = filename.replace('/', '\\')

    oldfilename = getImageFolder() + oldfilename
    filename = getImageFolder() + filename
    os.rename(oldfilename, filename)
    return 0


def deleteFile(filename):
    filename = filename.replace('/', '\\')
    filename = getImageFolder() + filename
    os.remove(filename)
    return 0


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
        #'path': relativePath,
        'file': fileList,
        'dir': dict((dirname, tree(root, os.path.join(relativePath, dirname), dirname))for dirname in dirList)
    }
    return res


def getImageList():
    return tree(root=getImageFolder())
