from flask import render_template, request, session, redirect, url_for, send_from_directory, flash
from OBlog import app
from OBlog.back.getData import Site as Site
from OBlog.back.setData import Post as setPost
from OBlog.back.getData import Posts

import time
import json


@app.route('/admin/posts/')
def admin_posts():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    return render_template("admin/posts.html", Posts=Posts.getAllPosts())


@app.route('/admin/posts/edit/')
def admin_posts_edit():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    return render_template("admin/posts_edit.html", nowtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), Post="")


@app.route('/admin/posts/edit/<path:url>')
def admin_posts_edit_url(url):
    if 'admin' not in session:
        return redirect(url_for('admin'))
    return render_template("admin/posts_edit.html", nowtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), Post=url)


@app.route('/admin/posts/add/', methods=["POST", "GET"])
def admin_posts_add():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    if request.method == "POST":
        keys = ['title', 'url', 'time', 'updatetime', "abstruct",
                'view', 'tags', 'raw', 'published']

        _map = dict((key, request.form[key]) for key in keys)

        errorcode = setPost.add(_map)
        if errorcode == 1:
            flash("发布失败：格式错误")
        elif errorcode == 2:
            flash("发布失败：有重复文章")
        else:
            if _map['published'] == '0':
                return redirect(url_for('admin_posts_edit_url', url=_map['url']))
    return redirect(url_for('admin_posts'))


@app.route('/admin/posts/update/', methods=["POST", "GET"])
def admin_posts_update():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    if request.method == "POST":
        keys = ['title', 'url', 'time', 'updatetime', "abstruct",
                'view', 'tags', 'raw', 'published']

        _set = dict((key, request.form[key]) for key in keys)
        _where = {'url': request.form['oldurl']}

        errorcode = setPost.update(_set, _where)
        if errorcode == 1:
            flash("更新失败：格式错误")
        elif errorcode == 2:
            flash("更新失败：有重复文章")
        else:
            if _set['published'] == '0':
                return redirect(url_for('admin_posts_edit_url', url=_where['url']))
    return redirect(url_for('admin_posts'))


@app.route('/admin/posts/delete/', methods=["POST", "GET"])
def admin_posts_delete():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    if request.method == "POST":
        keys = ['url']
        _where = dict((key, request.form[key]) for key in keys)
        print('\n', _where)
        setPost.delete(_where)
    return redirect(url_for('admin_posts'))


