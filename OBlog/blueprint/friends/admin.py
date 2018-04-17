from . import friendsAdminBP
from flask import render_template, abort


@friendsAdminBP.route('/')
def index():
    return render_template("admin/friends.html")
