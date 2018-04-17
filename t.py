import os


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


print(listDir('./OBlog/static/img'))
