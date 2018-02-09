DATABASE = '/data/wwwroot/default/OBlog/sql.db'
SECRET_KEY = '\xf2\x92Y\xdf\x8ejY\x04\x96\xc4V\x88\xfb\xfc\xb2\x18F\xa3\xee\xb9\xb9t\x01\xf0\x96'

STATIC_FOLDER = r'front/static'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

DEBUG = True

from flask import Flask
app = Flask(__name__, template_folder='front/theme/default',
            static_folder=STATIC_FOLDER)
app.config.from_object(__name__)
from .views import *
