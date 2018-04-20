from flask import Blueprint

imagesApiBP = Blueprint('imagesApiBlueprint', __name__)
imagesAdminBP = Blueprint('imagesAdminBlueprint', __name__)

from . import admin, api
