from OBlog import app
from .admin import adminBP, adminApiBP
from .pages import pagesBP, pagesAdminBP, pagesApiBP
from .posts import postsBP, postsAdminBP, postsApiBP
from .tags import tagsBP, tagsAdminBP, tagsApiBP
from .friends import friendsAdminBP, friendsApiBP
from .images import imagesAdminBP, imagesApiBP
from .comments import commentsAdminBP, commentsApiBP
from .search import searchApiBP
from .backup import backupAdminBP, backupApiBP
from .goods import goodsAdminBP,goodsApiBP
from .rss import rssBP

from flask import session, current_app, request, abort


@adminBP.before_request
@pagesAdminBP.before_request
@pagesApiBP.before_request
@postsAdminBP.before_request
@postsApiBP.before_request
@tagsAdminBP.before_request
@tagsApiBP.before_request
@friendsAdminBP.before_request
@friendsApiBP.before_request
@imagesAdminBP.before_request
@imagesApiBP.before_request
@commentsAdminBP.before_request
@backupAdminBP.before_request
@backupApiBP.before_request
@goodsAdminBP.before_request
@goodsApiBP.before_request
def before_request():
    print(session)
    current_app.logger.debug('auth path %s.' % request.path)
    if session.get('admin', False) != True:
        current_app.logger.warning('401 at %s.' % request.path)
        abort(401)


app.register_blueprint(adminBP, url_prefix='/admin')
app.register_blueprint(adminApiBP, url_prefix='/api/admin')

app.register_blueprint(pagesBP, url_prefix='/pages')
app.register_blueprint(pagesAdminBP, url_prefix='/admin/pages')
app.register_blueprint(pagesApiBP, url_prefix='/api/pages')

app.register_blueprint(postsBP, url_prefix='/post')
app.register_blueprint(postsAdminBP, url_prefix='/admin/posts')
app.register_blueprint(postsApiBP, url_prefix='/api/posts')

app.register_blueprint(tagsBP, url_prefix='/tag')
app.register_blueprint(tagsAdminBP, url_prefix='/admin/tags')
app.register_blueprint(tagsApiBP, url_prefix='/api/tags')

app.register_blueprint(friendsApiBP, url_prefix='/api/friends')
app.register_blueprint(friendsAdminBP, url_prefix='/admin/friends')

app.register_blueprint(imagesApiBP, url_prefix='/api/images')
app.register_blueprint(imagesAdminBP, url_prefix='/admin/images')

app.register_blueprint(commentsAdminBP, url_prefix='/admin/comments')
app.register_blueprint(commentsApiBP, url_prefix='/api/comments')

app.register_blueprint(searchApiBP, url_prefix='/api/search')

app.register_blueprint(backupAdminBP, url_prefix='/admin/backup')
app.register_blueprint(backupApiBP, url_prefix='/api/backup')

app.register_blueprint(goodsAdminBP, url_prefix='/admin/goods')
app.register_blueprint(goodsApiBP, url_prefix='/api/goods')

app.register_blueprint(rssBP, url_prefix='/rss')