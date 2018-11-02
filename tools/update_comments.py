from OBlog.markdown import render_markdown
from . import database as db


comments = db.query_db("select * from comments;")
for item in comments:
    db.update_db("comments", {
        'html': render_markdown(item['raw'])
    }, {'id': item['id']})