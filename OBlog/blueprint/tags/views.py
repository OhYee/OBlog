from . import tagsBP
from flask import redirect, url_for, abort, render_template


@tagsBP.route('/<path:url>/')
def tags(url):
    from .main import getTagByEnglish
    tag = getTagByEnglish(url)
    if tag:
        from ..posts.main import getPostsByTag
        posts = getPostsByTag(tag['chinese'])
        return render_template("pages/tag.html", tag=tag, posts=posts, thisPage='tags')
    else:
        abort(418)
