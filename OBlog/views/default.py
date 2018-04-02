from flask import g, render_template, request, session, redirect, url_for, send_from_directory, flash, make_response
from OBlog import app
import sqlite3

import OBlog.back.getData.Site as getSite
import OBlog.back.getData.Posts as getPosts
import OBlog.back.getData.Tags as getTags
import OBlog.back.viewercount as viewercount
from OBlog.back.initSite import initSite
from OBlog.back.getData.Pages import getPages


@app.route('/')
def index():
    return render_template(
        "index.html",
        newPosts=getPosts.getNewestPosts(),
        recommendPosts=getPosts.getRecommendPosts()
    )


@app.route('/post/<path:url>/')
def post(url):
    post = getPosts.getPost(url)
    if post == None:
        return page_not_found()
    return render_template("post.html", Post=post)


@app.route('/post/<path:url>.html')
def post_redirect(url):
    return redirect(url_for("post", url=url), code=301)


@app.route('/post/img/<path:url>')
def img_redirect(url):
    return redirect('/static/img/posts/' + url)


@app.route('/tag/<url>/')
def tag(url):
    tag = getTags.getChinese(url)
    if not tag:
        return page_not_found()
    posts = getPosts.getPostByTags(tag['chinese'])
    return render_template("tag.html", posts=posts, tag=tag)


@app.route('/<path:url>/')
def pages(url):
    Pages = getPages()
    template = None
    for page in Pages:
        if url == page['urlpath']:
            template = page['filepath']
            break
    if template != None:
        return render_template(template)
    return page_not_found()


@app.route('/sitemap.xml')
def sitemapxml():
    xml = '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    posts = getPosts.getAllPosts()
    for post in posts:
        xml += '<url><loc>%s</loc></url>' % (
            'http://www.oyohyee.com/' + post['url'])
    xml += '</urlset>'
    return xml


@app.route('/sitemap.txt')
def sitemaptxt():
    xml = ""
    posts = getPosts.getAllPosts()
    for post in posts:
        xml += 'http://www.oyohyee.com/' + post['url'] + '\n'
    return xml


@app.errorhandler(404)
def page_not_found(e=None):
    return render_template("404.html", e=e), 404


@app.before_first_request
def init():
    initSite()


@app.before_request
def before_request():
    g.db = sqlite3.connect(app.config['DATABASE'])
    viewercount.viewpath(request.remote_addr, request.path)
    # print("database connected")


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()
    # print("database closed")


@app.context_processor
def inject_site():
    return dict(Site=getSite.getSite())
