from . import postsBP
from flask import redirect, url_for, abort, render_template


@postsBP.route('/<path:url>/')
def posts(url):
    from .main import getPostForShow
    post = getPostForShow(url)
    if post:
        return render_template("pages/post.html", post=post, thisPage='post')
    else:
        abort(404)
