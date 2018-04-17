from flask import render_template, request
from OBlog import app
from ..main import getImageList, upload_file, rename, delete


@app.route('/admin/upload/')
def admin_upload():
    return render_template("admin/upload.html", images=getImageList())


@app.route('/admin/upload/add/', methods=["POST"])
def admin_upload_add():
    path = {'0': 'img', '1': 'img/posts', '2': 'img/tags'}

    status = upload_file(request.files['file'], path[request.form['path']])

    if status[0] == 1:
        print(123)
        flash('上传失败')
    else:
        url = status[1]
        flash("上传成功" + url)

    return redirect(url_for('admin_upload'))


@app.route('/admin/upload/update/', methods=["POST", "GET"])
def admin_upload_update():
    if request.method == 'POST':
        path = {'0': 'img', '1': 'img/posts', '2': 'img/tags'}
        oldfilename = request.form['oldfilename']
        filename = request.form['filename']
        rename(oldfilename, filename, path[request.form['path']])

    return redirect(url_for('admin_upload'))


@app.route('/admin/upload/delete/', methods=["POST", "GET"])
def admin_upload_delete():
    if request.method == 'POST':
        path = {'0': 'img', '1': 'img/posts', '2': 'img/tags'}
        oldfilename = request.form['oldfilename']
        delete(oldfilename, path[request.form['path']])

    return redirect(url_for('admin_upload'))
