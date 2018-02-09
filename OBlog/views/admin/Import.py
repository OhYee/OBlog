from flask import g, render_template, request, session, redirect, url_for, send_from_directory, flash
from OBlog import app

from OBlog.back.setData import Tags as setTags
from OBlog.back.getData import Tags as getTags

from OBlog.back.getData import Posts as getPosts
from OBlog.back.setData import Post as setPosts

from OBlog.back.upload import getImageList, upload_file, rename, delete
from OBlog.back.GlobalVariable import getGV, setGV
from OBlog.back import Import
import json
import time


@app.route('/admin/import/')
def admin_import():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    setGV('console',
          json.dumps({
              "now": 100,
              "total": 100,
              "output": "等待您的操作"
          }))
    # print(session['console'])

    return render_template("admin/import.html")


# 废用
@app.route('/admin/import/console/')
def admin_import_console():
    # fetch的时候无法判断身份，会导致302
    # if 'admin' not in session:
    #     return redirect(url_for('admin'))

    console = getGV("console")
    res = []
    if console:
        res = json.loads(console)
    else:
        res = {'output': 'error'}

    return json.dumps(res)


@app.route('/admin/import/exportTags/')
def admin_import_exportTags():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    tags = getTags.getRawTags()
    res = {}
    for tag in tags:
        res[tag['chinese']] = {
            'english': tag['english'],
            'img': tag['img'],
            'class': tag['class']
        }
    f = open("tags.json", 'w')
    f.write(json.dumps(res))
    f.close()
    flash("已写出到 tags.json ")
    return redirect(url_for("admin_import"))


@app.route('/admin/import/importTags/')
def admin_import_importTags():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    f = open("tags.json", 'r')
    tags = json.loads(f.read())
    f.close()

    cnt = len(tags)
    for (idx, tag) in enumerate(tags):
        print(str(idx + 1) + '/' + str(cnt), tag)
        setTags.update(
            {
                'english': tags[tag]['english'],
                'img': tags[tag]['img'],
                'class': tags[tag]['class']
            },
            {
                'chinese': tag
            }
        )

    flash("已导入 tags.json")
    return redirect(url_for("admin_import"))


@app.route('/admin/import/importPosts/')
def admin_import_importPosts():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    f = open('./posts.json', 'r')
    posts = json.loads(f.read())
    cnt = len(posts)
    for (idx, post) in enumerate(posts):
        print(str(idx + 1) + '/' + str(cnt), post['url'])
        post['abstruct'] = ''
        post['updatetime'] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())
        post['view'] = '0'
        post['published'] = '1'
        if getPosts.getPost(post['url']):
            setPosts.update(post, {'url', post['url']})
        else:
            setPosts.add(post)
    f.close()
    flash("已导入 posts.json")
    return redirect(url_for('admin_posts'))


@app.route('/admin/import/exportPosts/')
def admin_import_exportPosts():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    f = open('./posts.json', 'w')
    f.write(json.dumps(getPosts.getAllPosts()))
    f.close()
    flash("已导出 posts.json")
    return redirect(url_for('admin_posts'))
