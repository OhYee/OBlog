from flask import Blueprint

adminBP = Blueprint('adminBlueprint', __name__)
adminApiBP = Blueprint('adminAPIBlueprint', __name__)

from . import views
from . import api
