from OBlog import app
import os
os.environ['database']='./sql.db'
app.run(threaded=True)