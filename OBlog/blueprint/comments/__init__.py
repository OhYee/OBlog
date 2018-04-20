from flask import Blueprint

commentsApiBP = Blueprint('commentsApiBlueprint', __name__)
commentsAdminBP = Blueprint('commentsAdminBlueprint', __name__)

from . import admin, api
