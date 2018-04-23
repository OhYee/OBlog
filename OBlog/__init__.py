import os
import sys
ROOTPATH = sys.path[0]
DATABASE = os.path.join(ROOTPATH, 'database.db')
SECRET_KEY = '\xf2\x92Y\xdf\x8ejY\x04\x96\xc4V\x88\xfb\xfc\xb2\x18F\xa3\xee\xb9\xb9t\x01\xf0\x96'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
TEMPLATES_AUTO_RELOAD = True

from flask import Flask
app = Flask(__name__)
app.config.from_object(__name__)

from . import blueprint
from . import views