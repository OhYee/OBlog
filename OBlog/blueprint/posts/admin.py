from . import postsAdminBP
from flask import render_template,abort

@postsAdminBP.route('/')
def index():
    from .main import getPosts
    return render_template("admin/posts.html",posts = getPosts())

@postsAdminBP.route('/edit/')
def edit():
    return render_template("admin/post_edit.html")