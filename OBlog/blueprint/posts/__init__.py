from flask import Blueprint

postsBP = Blueprint('postsBlueprint', __name__)
postsAdminBP = Blueprint('postsAdminBlueprint', __name__)
postsApiBP = Blueprint('postsAPIBlueprint', __name__)

from . import views,admin,api

