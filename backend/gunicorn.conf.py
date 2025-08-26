# -*- coding: utf-8 -*-
"""
Gunicorn配置文件 - 小雨微寒后端服务
"""

import multiprocessing
import os

# 服务器配置
bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100

# 应用配置
module = "main:app"
chdir = "/www/wwwroot/xiaoyuweihan/backend"

# 进程配置
daemon = False
pidfile = "/tmp/xiaoyuweihan-backend.pid"
user = "www"
group = "www"

# 日志配置
accesslog = "/www/wwwroot/xiaoyuweihan/backend/logs/access.log"
errorlog = "/www/wwwroot/xiaoyuweihan/backend/logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 性能配置
preload_app = True
timeout = 120
keepalive = 5
worker_tmp_dir = "/dev/shm"

# 安全配置
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# SSL配置（如果需要）
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

def pre_fork(server, worker):
    """工作进程fork前的钩子"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    """工作进程fork后的钩子"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def worker_exit(server, worker):
    """工作进程退出时的钩子"""
    server.log.info("Worker exited (pid: %s)", worker.pid)

def when_ready(server):
    """服务器准备就绪时的钩子"""
    server.log.info("小雨微寒后端服务已启动")

def on_exit(server):
    """服务器退出时的钩子"""
    server.log.info("小雨微寒后端服务已停止")