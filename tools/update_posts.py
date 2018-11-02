from OBlog.markdown import render_markdown
from . import database as db


posts = db.query_db("select * from posts;")
length = len(posts)
for (idx, item) in enumerate(posts):
    print("{}/{} {}".format(idx+1, length, item['url']))
    db.update_db("posts", {
        'html': render_markdown(item['raw'])
    }, {'url': item['url']})
