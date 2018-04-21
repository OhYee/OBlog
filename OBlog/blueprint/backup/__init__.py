from flask import Blueprint

backupAdminBP = Blueprint('backupAdminBlueprint', __name__)
backupApiBP = Blueprint('backupApiBlueprint', __name__)

from . import admin, api
