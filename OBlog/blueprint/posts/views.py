from . import postsBP
from flask import redirect, url_for, abort, render_template


@postsBP.route('/index/')
def index():
    return redirect(url_for('index'))


@postsBP.route('/<path:url>/')
def posts(url):
    from .main import getPostsDict
    posts = getPostsDict()
    if url in posts:
        render_template("posts/%s.html" % url, thisPost=url)
    else:
        abort(404)
