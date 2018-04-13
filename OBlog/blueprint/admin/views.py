from OBlog import app
from flask import session, render_template, redirect, url_for, abort, request, current_app
from . import adminBP

@adminBP.route('/')
def index():
    from .main import getSiteConfig
    return render_template('admin/index.html')


@app.errorhandler(401)
@adminBP.route('/login/')
def login(e=None):
    if session.get('admin', False) == True:
        return redirect(url_for('.index'))
    return render_template("admin/login.html")

@adminBP.route('/logout/')
def logout():
    if 'admin' in session:
        session.pop('admin', None)
    else:
        current_app.logger.error('unlogin user logout.')
    return redirect(url_for('.login'))
