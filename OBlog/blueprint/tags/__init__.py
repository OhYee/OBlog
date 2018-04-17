from flask import Blueprint

tagsBP = Blueprint('tagsBlueprint', __name__)
tagsAdminBP = Blueprint('tagsAdminBlueprint', __name__)
tagsApiBP = Blueprint('tagsAPIBlueprint', __name__)

from . import views,admin,api