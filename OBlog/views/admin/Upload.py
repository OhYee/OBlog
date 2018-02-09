from flask import render_template, request, session, redirect, url_for, send_from_directory, flash
from OBlog import app
from OBlog.back.getData import Site as Site
from OBlog.back.setData import Tags as setTags
from OBlog.back.upload import getImageList, upload_file, rename, delete


@app.route('/admin/upload/')
def admin_upload():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    return render_template("admin/upload.html", imgList=getImageList())


@app.route('/admin/upload/add/', methods=["POST", "GET"])
def admin_upload_add():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    if request.method == 'POST':
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
    if 'admin' not in session:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        path = {'0': 'img', '1': 'img/posts', '2': 'img/tags'}
        oldfilename = request.form['oldfilename']
        filename = request.form['filename']
        rename(oldfilename, filename, path[request.form['path']])

    return redirect(url_for('admin_upload'))


@app.route('/admin/upload/delete/', methods=["POST", "GET"])
def admin_upload_delete():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        path = {'0': 'img', '1': 'img/posts', '2': 'img/tags'}
        oldfilename = request.form['oldfilename']
        delete(oldfilename, path[request.form['path']])

    return redirect(url_for('admin_upload'))
