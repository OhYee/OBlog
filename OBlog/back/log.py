from OBlog import app


def openLogFile():
    return open(app.config['LOGFILE'], 'a+')


def Log(text, *args):
    logStr = (text + '\n') % args
    with openLogFile() as f:
        f.write(logStr)
