from . import goodsAdminBP
from flask import render_template


@goodsAdminBP.route('/')
def index():
    from .main import getAllGoods
    return render_template("admin/goods.html", goods=getAllGoods())
