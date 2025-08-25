# Gunicorn配置文件
# gunicorn.conf.py

import multiprocessing
import os

# 服务器套接字
bind = "0.0.0.0:8000"
backlog = 2048

# 工作进程
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 30
keepalive = 2

# 重启
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# 日志
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 进程命名
proc_name = "xiaoyuweihan_backend"

# 其他设置
user = None
group = None
tmp_upload_dir = None

# 启动钩子
def on_starting(server):
    """服务器启动时执行"""
    # 创建日志目录
    os.makedirs("logs", exist_ok=True)
    server.log.info("小雨微寒后端服务启动中...")

def on_reload(server):
    """重载时执行"""
    server.log.info("小雨微寒后端服务重载中...")

def when_ready(server):
    """服务器准备就绪时执行"""
    server.log.info("小雨微寒后端服务启动完成！")

def on_exit(server):
    """服务器退出时执行"""
    server.log.info("小雨微寒后端服务已关闭")