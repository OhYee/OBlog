from . import backupAdminBP

from flask import render_template


@backupAdminBP.route('/')
def index():
    return render_template("admin/backup.html")
