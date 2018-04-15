from . import app
from flask import g, current_app, request, render_template
import sqlite3


@app.route('/')
def index():
    return render_template("pages/index.html", thisPage='index')


@app.errorhandler(404)
def page_not_found(e=None):
    current_app.logger.warning('404 path=%s' % request.path)
    return render_template("pages/404.html", e=e), 404


@app.before_request
def before_request():
    current_app.logger.debug('before_request at path=%s' % request.path)
    g.db = sqlite3.connect(app.config['DATABASE'])

    # viewercount.viewpath(request.remote_addr, request.path)
    # print("database connected")


@app.teardown_request
def teardown_request(exception):
    current_app.logger.debug('after_request at path=%s' % request.path)
    if hasattr(g, 'db'):
        g.db.close()
    # print("database closed")


@app.context_processor
def inject_site():
    from .main import getSite
    return dict(Site=getSite())
