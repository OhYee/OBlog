from . import pagesAdminBP
from flask import render_template,abort

@pagesAdminBP.route('/')
def index():
    return render_template("admin/pages.html")

@pagesAdminBP.route('/edit/')
def edit():
    return render_template("admin/page_edit.html")