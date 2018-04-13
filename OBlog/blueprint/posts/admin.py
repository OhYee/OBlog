from . import postsAdminBP
from flask import render_template,abort

@postsAdminBP.route('/')
def index():
    return render_template("admin/posts.html")

@postsAdminBP.route('/edit/')
def edit():
    return render_template("admin/post_edit.html")