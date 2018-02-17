import sys
sys.path.insert(0,'/data/wwwroot/default/OBlog')



def Log(text, *args):
    logStr = (text + '\n') % args
    with open(r'/data/wwwroot/default/OBlog/log/test.log', 'a') as f:
        f.write(logStr)

Log("run wsgi 1")

from OBlog import app as application

Log("run wsgi 2")