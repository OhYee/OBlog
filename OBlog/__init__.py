import os
import sys
ROOTPATH = sys.path[0]
DATABASE = os.path.join(ROOTPATH, 'sql.db')
LOGFILE = os.path.join(ROOTPATH, 'log/log.log')

SECRET_KEY = '\xf2\x92Y\xdf\x8ejY\x04\x96\xc4V\x88\xfb\xfc\xb2\x18F\xa3\xee\xb9\xb9t\x01\xf0\x96'

STATIC_FOLDER = r'front/static'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024


def Log(text, *args):
    logStr = (text + '\n') % args
    with open(os.path.join(sys.path[0], r'log/test.log'), 'a+') as f:
        f.write(logStr)


Log("run __init__ 1")

from flask import Flask
app = Flask(__name__, template_folder='front/theme/default',
            static_folder=STATIC_FOLDER)
app.config.from_object(__name__)
from .views import *

import jieba
jieba.initialize()
print("__init__ start")


Log("run __init__ 2")
