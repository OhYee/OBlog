from flask import render_template, request, session, redirect, url_for, send_from_directory, flash
from OBlog import app

from OBlog.back.getData.Pages import getPages
from OBlog.back.setData import Pages as setPages


@app.route('/admin/pages/')
def admin_pages():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    return render_template("admin/pages.html", Pages=getPages())


@app.route('/admin/pages/add/', methods=["post"])
def admin_pages_add():
    if 'admin' not in session:
        return redirect(url_for('admin'))

    if request.method == 'POST':
        keys = ['urlpath', 'filepath']
        _dict = dict((key, request.form[key]) for key in keys)

        errorcode = setPages.add(_dict)
        if errorcode == 1:
            flash('有重复项，插入失败')
        elif errorcode == 2:
            flash('格式错误')

    return redirect(url_for('admin_pages'))


@app.route('/admin/pages/update/', methods=["post"])
def admin_pages_update():
    if 'admin' not in session:
        return redirect(url_for('admin'))

    if request.method == 'POST':
        keys = ['urlpath', 'filepath']
        _set = dict((key, request.form[key]) for key in keys)
        _where = {"urlpath": request.form['oldurlpath']}

        errorcode = setPages.update(_set, _where)
        if errorcode == 1:
            flash('有重复项，插入失败')
        elif errorcode == 2:
            flash('格式错误')

    return redirect(url_for('admin_pages'))


@app.route('/admin/pages/delete/', methods=["post"])
def admin_pages_delete():
    if 'admin' not in session:
        return redirect(url_for('admin'))

    if request.method == 'POST':
        keys = ['urlpath']
        _where = dict((key, request.form[key]) for key in keys)

        setPages.delete(_where)

    return redirect(url_for('admin_pages'))
