import sys,os
os.environ['database']='/data/wwwroot/default/OBlog/sql.db'
sys.path.insert(0,'/data/wwwroot/default/OBlog')
print('wsgi start')
from OBlog import app as application