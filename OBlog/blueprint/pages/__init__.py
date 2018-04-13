from flask import Blueprint

pagesBP = Blueprint('pagesBlueprint', __name__)
pagesAdminBP = Blueprint('pagesAdminBlueprint', __name__)
pagesApiBP = Blueprint('pagesAPIBlueprint', __name__)

from . import views,admin,api

