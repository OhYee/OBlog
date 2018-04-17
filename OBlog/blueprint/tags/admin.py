from flask import render_template
from . import tagsAdminBP

@tagsAdminBP.route('/')
def tagsIndex():
    from .main import getRawTags
    return render_template("admin/tags.html", tags=getRawTags())