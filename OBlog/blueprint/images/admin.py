from . import imagesAdminBP
from flask import render_template, abort
from .main import getImageList

@imagesAdminBP.route('/')
def index():
    return render_template("admin/images.html",images = getImageList())
