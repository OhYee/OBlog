workers = 4
threads = 4

daemon = True

bind = ['127.0.0.1:8000']

accesslog = './log/access.log'
errorlog = './log/error.log'

loglevel = 'error'

proc_name = 'OBlog'
access_log_format = '%(t)s %({X-Forwarded-For}i)s %(l)s "%(s)s" %(l)s "%(r)s" %(l)s "%(a)s" %(l)s "%(f)s"'

pidfile = './PID'

def on_starting(sever):
    import jieba 
    jieba.initialize()

def on_reload(server):
    pass

def when_ready(sever):
    pass

def post_fork(sever, worker):
    pass

def post_worker_init(worker):
    pass

def worker_int(worker):
    pass

def worker_abort(worker):
    pass

def pre_exec(server):
    pass

def pre_request(worker, req):
    pass

def post_request(worker, req, environ, resp):
    pass

def child_ext(sever, worker):
    pass

def worker_exit(server, worker):
    pass

def nworkers_changed(server, new_value, old_value):
    pass

def on_exit(server):
    pass
