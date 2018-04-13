from . import pagesBP
from flask import redirect, url_for, abort, render_template


@pagesBP.route('/index/')
def index():
    return redirect(url_for('index'))


@pagesBP.route('/<path:url>/')
def pages(url):
    from .main import getPagesDict
    pages = getPagesDict()
    if url in pages:
        render_template("pages/%s.html" % url, thisPage=url)
    else:
        abort(404)
