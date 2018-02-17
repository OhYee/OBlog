import sys
import os


def Log(text, *args):
    logStr = (text + '\n') % args
    with open(os.path.join(sys.path[0], r'log/test.log'), 'a+') as f:
        f.write(logStr)


Log("run mod")
