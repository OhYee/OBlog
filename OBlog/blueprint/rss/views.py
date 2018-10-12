from . import rssBP
from flask import render_template

from OBlog.main import getSite


@rssBP.route('/top20/')
def top20():
    from ..posts.main import getPostsByTime
    return render_template("layout/rss.xml", posts=getPostsByTime(20), site=getSite()),  {'Content-Type': 'text/xml; charset=utf-8'}


@rssBP.route('/all/')
def allPosts():
    from ..posts.main import getPostsForList
    posts = getPostsForList()
    posts.reverse()
    return render_template("layout/rss.xml", posts=posts, site=getSite()), {'Content-Type': 'text/xml; charset=utf-8'}
