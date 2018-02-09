from flask import render_template, request, session, redirect, url_for, send_from_directory, flash
from OBlog import app
from OBlog.back.getData import Site
from OBlog.back.setData import SiteConfig
import hashlib


@app.route('/admin/')
def admin():
    return render_template("admin/admin.html")


@app.route('/admin/login/', methods=["POST", "GET"])
def admin_login():
    if request.method == 'POST':
        password = Site.getConfig()['Password']
        passwd = request.form['passwd']
        if hashlib.md5(passwd.encode()).hexdigest() == password:
            session["admin"] = True
    return redirect(url_for('admin'))


@app.route('/admin/logout/')
def admin_logout():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    session.pop('admin', None)
    return redirect(url_for('index'))


@app.route('/admin/update/', methods=["POST", "GET"])
def admin_update():
    if request.method == 'POST':
        _set = request.form.to_dict()
        SiteConfig.update(_set)
    return redirect(url_for('admin'))
