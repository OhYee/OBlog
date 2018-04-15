from . import postsAdminBP
from flask import render_template, abort


@postsAdminBP.route('/')
def index():
    from .main import getPostsForList
    return render_template("admin/posts.html", posts=getPostsForList())


@postsAdminBP.route('/edit/')
def edit():
    return render_template("admin/post_edit.html")


@postsAdminBP.route('/edit/<path:url>/')
def editPost(url):
    from .main import getPostForEdit
    return render_template("admin/post_edit.html", post=getPostForEdit(url))
