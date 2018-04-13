from OBlog import app
from .admin import adminBP, adminApiBP
from .pages import pagesBP, pagesAdminBP, pagesApiBP
from .posts import postsBP, postsAdminBP, postsApiBP

from flask import session, current_app, request, abort


@adminBP.before_request
@pagesBP.before_request
@pagesAdminBP.before_request
@pagesApiBP.before_request
@postsAdminBP.before_request
@postsApiBP.before_request
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

app.register_blueprint(postsBP, url_prefix='/posts')
app.register_blueprint(postsAdminBP, url_prefix='/admin/posts')
app.register_blueprint(postsApiBP, url_prefix='/api/posts')