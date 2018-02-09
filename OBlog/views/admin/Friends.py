from flask import render_template, request, session, redirect, url_for, send_from_directory, flash
from OBlog import app
from OBlog.back.getData import Site as Site
from OBlog.back.setData import Friends as setFriends

@app.route('/admin/friends/')
def admin_friends():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    return render_template("admin/friends.html")


@app.route('/admin/friends/add/', methods=["POST", "GET"])
def admin_friends_add():
    if request.method == 'POST':
        idx = request.form['idx']
        name = request.form['name']
        url = request.form['url']

        errorcode = setFriends.add(idx, name, url)
        if errorcode == 1:
            flash('有重复项，插入失败')
        elif errorcode == 2:
            flash('序号格式错误')

    return redirect(url_for('admin_friends'))


@app.route('/admin/friends/update/', methods=["POST", "GET"])
def admin_friends_update():
    if request.method == 'POST':
        oldname = request.form['oldname']
        idx = request.form['idx']
        name = request.form['name']
        url = request.form['url']

        errorcode = setFriends.update(oldname, idx, name, url)
        if errorcode == 1:
            flash('有重复项，修改失败')
        elif errorcode == 2:
            flash('序号格式错误')

    return redirect(url_for('admin_friends'))


@app.route('/admin/friends/delete/', methods=["POST", "GET"])
def admin_friends_delete():
    if request.method == 'POST':
        oldname = request.form['oldname']
        setFriends.delete(oldname)
    return redirect(url_for('admin_friends'))
