from . import commentsAdminBP
from flask import render_template


@commentsAdminBP.route('/')
def index():
    from .main import getAllComments
    return render_template("admin/comments.html", comments=getAllComments())
