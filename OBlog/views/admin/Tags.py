from flask import render_template, request, session, redirect, url_for, send_from_directory, flash
from OBlog import app
from OBlog.back.getData import Site as Site
from OBlog.back.setData import Tags as setTags


@app.route('/admin/tags/')
def admin_tags():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    return render_template("admin/tags.html")


@app.route('/admin/tags/update/', methods=["POST", "GET"])
def admin_tags_update():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        _where = {"chinese": request.form["chinese"],
                  "english": request.form["oldenglish"]}
        _set = {"english": request.form["english"],
                "img": request.form["img"],
                "class": request.form["class"]}

        errorcode = setTags.update(_set, _where)
        if errorcode == 1:
            flash("修改失败：格式错误")
        elif errorcode == 2:
            flash("修改失败：有重复名称")

    return redirect(url_for('admin_tags'))
