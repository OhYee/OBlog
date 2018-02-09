from flask import render_template, request, session, redirect, url_for, send_from_directory, flash
from OBlog import app
from OBlog.back.setData import Discuss

@app.route('/admin/discuss/')
def admin_discuss():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    return render_template("admin/discuss.html")


@app.route('/admin/discuss/add/', methods=["POST", "GET"])
def admin_discuss_add():
    if request.method == "POST":
        keys = ['email', 'raw', 'url']
        _set = dict((key, request.form[key]) for key in keys)
        _set['sendemail'] = '1' if 'check' in request.values else '0'
        _set['ip'] = request.remote_addr
        errorcode = Discuss.add(_set)
        if errorcode == 1:
            flash("发布失败：格式错误")
    return redirect(_set['url'])


@app.route('/admin/discuss/update/', methods=["POST", "GET"])
def admin_discuss_update():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    if request.method == "POST":
        keys = ['email']
        _set = dict((key, request.form[key]) for key in keys)

        _set['sendemail'] = '1' if 'sendemail' in request.values else '0'
        _set['show'] = '1' if 'show' in request.values else '0'
        
        _where = {'id': request.form['id']}

        errorcode = Discuss.update(_set, _where)

        if errorcode == 1:
            flash("更新失败：格式错误")
    return redirect(url_for('admin_discuss'))


# @app.route('/admin/posts/delete/', methods=["POST", "GET"])
# def admin_posts_delete():
#     if 'admin' not in session:
#         return redirect(url_for('admin'))
#     if request.method == "POST":
#         keys = ['url']
#         _where = dict((key, request.form[key]) for key in keys)
#         print('\n',_where)
#         setPost.delete(_where)
#     return redirect(url_for('admin_posts'))
