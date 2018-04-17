from flask import Blueprint

friendsApiBP = Blueprint('friendsApiBlueprint', __name__)
friendsAdminBP = Blueprint('friendsAdminBlueprint', __name__)

from . import admin,api

