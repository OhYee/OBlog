from . import app
from flask import g, current_app, request, render_template, abort
import sqlite3


@app.route('/')
def index():
    from .blueprint.admin.main import getSiteConfigDict
    from .blueprint.posts.main import getPostForShow, getPostsByTime
    Site = getSiteConfigDict()
    recommentStr = Site['recommend']['value']
    recommentPosts = [getPostForShow(url)
                      for url in recommentStr.split(',') if url != '']
    return render_template("pages/index.html", thisPage='index', newPosts=getPostsByTime(5), recommentPosts=recommentPosts)


@app.route('/archives/')
@app.route('/archives/<int:page>/')
def archives(page=1):
    prePagePostsNumber = 20
    from .blueprint.posts.main import getPostsByTime, getPostsNumber
    import math
    totalPage = math.ceil(getPostsNumber() / prePagePostsNumber)
    posts = getPostsByTime(prePagePostsNumber, (page - 1) * prePagePostsNumber)
    if len(posts) == 0:
        abort(418)
    return render_template("pages/archives.html", thisPage='archives', posts=posts, totalPage=totalPage, nowPage=page)


@app.route('/tags/')
def tags():
    from .blueprint.tags.main import getTags
    return render_template("pages/tags.html", thisPage='tags', tags=getTags())


@app.route('/goods/')
def goods():
    from .blueprint.goods.main import getAllShowGoods
    return render_template("pages/goods.html", thisPage='goods', goods=getAllShowGoods())


@app.route('/sitemap.xml')
def sitemapxml():
    xml = '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    from .blueprint.posts.main import getPublishedPostsUrl
    posts = getPublishedPostsUrl()
    for post in posts:
        xml += '<url><loc>%s</loc></url>' % (
            'http://www.oyohyee.com/' + post['url'])
    xml += '</urlset>'
    return xml


@app.route('/sitemap.txt')
def sitemaptxt():
    xml = ""
    from .blueprint.posts.main import getPublishedPostsUrl
    posts = getPublishedPostsUrl()
    for post in posts:
        xml += 'http://www.oyohyee.com/' + post['url'] + '\n'
    return xml


@app.errorhandler(404)
def page_not_found(e=None):
    current_app.logger.warning('404 path=%s' % request.path)
    return render_template("pages/404.html", e=e), 404


@app.errorhandler(418)
def i_am_a_tea_pot(e=None):
    current_app.logger.warning('418 path=%s' % request.path)
    return render_template("pages/418.html", e=e), 418


@app.before_request
def before_request():
    current_app.logger.debug('before_request at path=%s' % request.path)
    g.db = sqlite3.connect(app.config['DATABASE'], timeout=20)
    from .main import viewpath
    viewpath(
        request.headers.get('X-Forwarded-For', request.remote_addr),
        request.path)
    # print("database connected")


@app.teardown_request
def teardown_request(exception):
    current_app.logger.debug('after_request at path=%s' % request.path)
    if hasattr(g, 'db'):
        g.db.close()
    # print("database closed")


@app.context_processor
def inject_site():
    from .main import getSite
    return dict(Site=getSite())
