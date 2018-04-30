from flask import Blueprint

goodsApiBP = Blueprint('goodsApiBlueprint', __name__)
goodsAdminBP = Blueprint('goodsAdminBlueprint', __name__)

from . import admin, api,view
