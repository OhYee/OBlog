from flask import Blueprint

rssBP = Blueprint('rssBlueprint', __name__)

from . import views