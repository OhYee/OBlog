from flask import render_template, request, session, redirect, url_for, send_from_directory, flash
from OBlog import app
from OBlog.back.getData import Site as Site
from OBlog.back.setData import Nav as setNav

@app.route('/admin/nav/')
def admin_nav():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    return render_template("admin/nav.html")


@app.route('/admin/nav/add/', methods=["POST", "GET"])
def admin_nav_add():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        idx = request.form['idx']
        name = request.form['name']
        url = request.form['url']
        icon = request.form['icon']

        errorcode = setNav.add(idx, name, url, icon)
        if errorcode == 1:
            flash('有重复项，插入失败')
        elif errorcode == 2:
            flash('序号格式错误')

    return redirect(url_for('admin_nav'))


@app.route('/admin/nav/update/', methods=["POST", "GET"])
def admin_nav_update():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        oldname = request.form['oldname']
        idx = request.form['idx']
        name = request.form['name']
        url = request.form['url']
        icon = request.form['icon']

        errorcode = setNav.update(oldname, idx, name, url, icon)
        if errorcode == 1:
            flash('有重复项，修改失败')
        elif errorcode == 2:
            flash('序号格式错误')

    return redirect(url_for('admin_nav'))


@app.route('/admin/nav/delete/', methods=["POST", "GET"])
def admin_nav_delete():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        oldname = request.form['oldname']
        setNav.delete(oldname)
    return redirect(url_for('admin_nav'))
