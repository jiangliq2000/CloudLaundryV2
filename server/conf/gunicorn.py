import os
import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing

#debug = True

# 并行工作进程数
workers = 4
# 指定每个工作者的线程数
threads = 2
# 监听内网端口5000
bind = '0.0.0.0:6678'
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
# 工作模式协程
worker_class = 'gevent'
# 设置最大并发量
#worker_connections = 200
# 设置进程文件目录
pidfile = './logs/gunicorn.pid'
# 设置访问日志和错误信息日志路径
accesslog = './logs/gunicorn_acess.log'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"' 
errorlog = './logs/gunicorn_error.log'
# 设置日志记录水平
loglevel = 'debug'

def pre_request(worker, req):
    print("pre_request")
    worker.log.debug("%s %s" % (req.method, req.path))