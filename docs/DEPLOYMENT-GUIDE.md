# 小雨微寒 - 部署指南

## 📋 目录

- [部署概述](#部署概述)
- [服务器环境](#服务器环境)
- [宝塔面板部署](#宝塔面板部署)
- [手动部署](#手动部署)
- [Nginx配置](#nginx配置)
- [SSL证书配置](#ssl证书配置)
- [监控与维护](#监控与维护)
- [故障排除](#故障排除)

## 📖 部署概述

本项目支持两种部署方式：
1. **宝塔面板部署**（推荐）- 适合快速部署和管理
2. **手动部署** - 适合定制化需求

### 部署架构

```
Internet
    ↓
Nginx (端口80/443)
    ↓
FastAPI应用 (端口8000)
    ↓
MySQL数据库 (端口3306)
```

## 🖥️ 服务器环境

### 最低配置要求

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| CPU | 1核 | 2核+ |
| 内存 | 1GB | 2GB+ |
| 存储 | 20GB | 50GB+ |
| 带宽 | 1Mbps | 5Mbps+ |

### 系统要求

- **操作系统**: CentOS 7+, Ubuntu 18+, Debian 9+
- **Python**: 3.10+
- **MySQL**: 5.7+
- **Nginx**: 1.18+

### 防火墙配置

```bash
# 开放必要端口
firewall-cmd --permanent --add-port=80/tcp    # HTTP
firewall-cmd --permanent --add-port=443/tcp   # HTTPS
firewall-cmd --permanent --add-port=22/tcp    # SSH
firewall-cmd --reload

# 或使用ufw (Ubuntu)
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp
ufw enable
```

## 🎛️ 宝塔面板部署

### 1. 安装宝塔面板

```bash
# CentOS安装命令
yum install -y wget && wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh

# Ubuntu/Debian安装命令
wget -O install.sh http://download.bt.cn/install/install-ubuntu_6.0.sh && sudo bash install.sh
```

### 2. 配置宝塔环境

登录宝塔面板后安装：
- **Nginx** 1.20+
- **MySQL** 5.7+
- **Python** 3.10+
- **phpMyAdmin**（可选，数据库管理）

### 3. 创建网站

1. 在宝塔面板中点击"网站" → "添加站点"
2. 域名填写：`47.105.52.49`（或您的域名）
3. 根目录设置为：`/www/wwwroot/xiaoyuweihan`
4. 选择"纯静态"类型

### 4. 配置数据库

1. 在"数据库"页面创建数据库：
   - 数据库名：`xiaoyuweihan`
   - 用户名：`xiaoyuweihan`
   - 密码：`Duan1999`

### 5. 上传项目代码

```bash
# 使用Git克隆项目
cd /www/wwwroot
git clone <your-repo-url> xiaoyuweihan
cd xiaoyuweihan

# 设置文件权限
chown -R www:www /www/wwwroot/xiaoyuweihan
chmod -R 755 /www/wwwroot/xiaoyuweihan
```

### 6. 运行部署脚本

```bash
cd /www/wwwroot/xiaoyuweihan/backend
chmod +x deploy-baota.sh
sudo ./deploy-baota.sh
```

部署脚本会自动执行以下操作：
- 检测和安装Python 3.10
- 创建虚拟环境
- 安装Python依赖
- 配置环境变量
- 创建数据库表
- 配置systemd服务
- 配置Nginx
- 启动服务

### 7. 验证部署

```bash
# 检查服务状态
systemctl status xiaoyuweihan-backend.service

# 检查API健康状态
curl http://47.105.52.49/api/health

# 访问API文档
curl http://47.105.52.49/docs
```

## 🔧 手动部署

### 1. 准备服务器环境

```bash
# 更新系统
yum update -y  # CentOS
# 或
apt update && apt upgrade -y  # Ubuntu

# 安装基础软件
yum install -y git wget curl vim  # CentOS
# 或
apt install -y git wget curl vim  # Ubuntu
```

### 2. 安装Python 3.10

```bash
# CentOS 7 编译安装Python 3.10
yum groupinstall -y "Development Tools"
yum install -y openssl-devel bzip2-devel libffi-devel

cd /tmp
wget https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz
tar xzf Python-3.10.12.tgz
cd Python-3.10.12
./configure --enable-optimizations
make altinstall

# 创建软链接
ln -sf /usr/local/bin/python3.10 /usr/bin/python3.10
ln -sf /usr/local/bin/pip3.10 /usr/bin/pip3.10
```

### 3. 安装MySQL

```bash
# CentOS 7
wget https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
rpm -ivh mysql80-community-release-el7-3.noarch.rpm
yum install -y mysql-server
systemctl start mysqld
systemctl enable mysqld

# 获取临时密码
grep 'temporary password' /var/log/mysqld.log

# 安全配置
mysql_secure_installation
```

### 4. 安装Nginx

```bash
# CentOS 7
yum install -y epel-release
yum install -y nginx
systemctl start nginx
systemctl enable nginx

# Ubuntu
apt install -y nginx
systemctl start nginx
systemctl enable nginx
```

### 5. 部署应用代码

```bash
# 创建应用目录
mkdir -p /www/wwwroot
cd /www/wwwroot

# 克隆项目
git clone <your-repo-url> xiaoyuweihan
cd xiaoyuweihan

# 设置权限
useradd -r -s /bin/false www
chown -R www:www /www/wwwroot/xiaoyuweihan
```

### 6. 配置后端服务

```bash
cd /www/wwwroot/xiaoyuweihan/backend

# 创建虚拟环境
python3.10 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
vim .env  # 修改配置
```

### 7. 配置数据库

```bash
# 登录MySQL
mysql -u root -p

# 创建数据库和用户
CREATE DATABASE xiaoyuweihan CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'xiaoyuweihan'@'localhost' IDENTIFIED BY 'Duan1999';
GRANT ALL PRIVILEGES ON xiaoyuweihan.* TO 'xiaoyuweihan'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# 测试数据库连接
python test_db_simple.py
```

### 8. 配置systemd服务

```bash
# 复制服务文件
cp xiaoyuweihan-backend.service /etc/systemd/system/

# 重新加载systemd
systemctl daemon-reload

# 启动并启用服务
systemctl start xiaoyuweihan-backend.service
systemctl enable xiaoyuweihan-backend.service

# 检查状态
systemctl status xiaoyuweihan-backend.service
```

## 🔀 Nginx配置

### 基础配置

```nginx
# /etc/nginx/conf.d/xiaoyuweihan.conf
server {
    listen 80;
    server_name 47.105.52.49;  # 替换为您的域名或IP
    
    # 设置客户端最大body大小
    client_max_body_size 10M;
    
    # API路径代理到后端
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # API文档路径
    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /redoc {
        proxy_pass http://127.0.0.1:8000/redoc;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /openapi.json {
        proxy_pass http://127.0.0.1:8000/openapi.json;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # 静态文件服务
    location / {
        root /www/wwwroot/xiaoyuweihan;
        index index.html;
        try_files $uri $uri/ /index.html;
        
        # 静态文件缓存
        location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
    
    # 上传文件服务
    location /uploads/ {
        alias /www/wwwroot/xiaoyuweihan/backend/uploads/;
        expires 1M;
        add_header Cache-Control "public";
    }
    
    # 日志配置
    access_log /var/log/nginx/xiaoyuweihan_access.log;
    error_log /var/log/nginx/xiaoyuweihan_error.log;
}
```

### 测试和重载配置

```bash
# 测试Nginx配置
nginx -t

# 重载Nginx配置
nginx -s reload
# 或
systemctl reload nginx
```

## 🔐 SSL证书配置

### 使用Let's Encrypt免费证书

```bash
# 安装certbot
yum install -y epel-release
yum install -y certbot python3-certbot-nginx

# 获取证书
certbot --nginx -d yourdomain.com

# 自动续期
echo "0 0,12 * * * root python3 -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew -q" | sudo tee -a /etc/crontab > /dev/null
```

### HTTPS配置示例

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # 其他配置同HTTP配置...
}

# HTTP重定向到HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## 📊 监控与维护

### 服务监控

```bash
# 检查服务状态
systemctl status xiaoyuweihan-backend.service
systemctl status nginx
systemctl status mysql

# 查看服务日志
journalctl -u xiaoyuweihan-backend.service -f
tail -f /var/log/nginx/xiaoyuweihan_access.log
tail -f /var/log/nginx/xiaoyuweihan_error.log
```

### 性能监控

```bash
# 系统资源监控
top
htop
free -h
df -h

# 网络连接监控
netstat -tlnp
ss -tlnp

# 数据库监控
mysql -u root -p -e "SHOW PROCESSLIST;"
mysql -u root -p -e "SHOW STATUS LIKE 'Threads_connected';"
```

### 定期维护

#### 1. 数据库备份

```bash
#!/bin/bash
# 创建备份脚本 /root/backup_db.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/mysql"
DB_NAME="xiaoyuweihan"
DB_USER="xiaoyuweihan"
DB_PASS="Duan1999"

mkdir -p $BACKUP_DIR

mysqldump -u$DB_USER -p$DB_PASS $DB_NAME > $BACKUP_DIR/xiaoyuweihan_$DATE.sql

# 保留最近30天的备份
find $BACKUP_DIR -name "xiaoyuweihan_*.sql" -mtime +30 -delete

echo "数据库备份完成: xiaoyuweihan_$DATE.sql"
```

#### 2. 定时任务配置

```bash
# 编辑crontab
crontab -e

# 添加以下任务
# 每天凌晨2点备份数据库
0 2 * * * /root/backup_db.sh

# 每周清理日志文件
0 3 * * 0 find /var/log/nginx/ -name "*.log" -mtime +7 -delete

# 每月重启服务（可选）
0 4 1 * * systemctl restart xiaoyuweihan-backend.service
```

### 更新部署

```bash
# 更新代码
cd /www/wwwroot/xiaoyuweihan
git pull origin main

# 如果后端有更新
cd backend
source venv/bin/activate
pip install -r requirements.txt
systemctl restart xiaoyuweihan-backend.service

# 如果前端有更新，清除浏览器缓存即可
# 可选：重载Nginx配置
nginx -s reload
```

## 🐛 故障排除

### 常见问题及解决方案

#### 1. 后端服务无法启动

**问题症状**：
```bash
systemctl status xiaoyuweihan-backend.service
● xiaoyuweihan-backend.service - 小雨微寒后端服务
   Loaded: loaded
   Active: failed (Result: exit-code)
```

**排查步骤**：
```bash
# 查看详细错误信息
journalctl -u xiaoyuweihan-backend.service -n 50

# 检查Python环境
which python3.10
/www/wwwroot/xiaoyuweihan/backend/venv/bin/python --version

# 检查依赖安装
cd /www/wwwroot/xiaoyuweihan/backend
source venv/bin/activate
pip list

# 手动启动测试
cd /www/wwwroot/xiaoyuweihan/backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 2. 数据库连接失败

**问题症状**：
```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server")
```

**排查步骤**：
```bash
# 检查MySQL服务
systemctl status mysql

# 测试数据库连接
mysql -u xiaoyuweihan -p xiaoyuweihan

# 检查网络连接
netstat -tlnp | grep 3306

# 检查配置文件
cat /www/wwwroot/xiaoyuweihan/backend/.env
```

#### 3. Nginx配置问题

**问题症状**：
- 502 Bad Gateway
- 404 Not Found
- API路径无法访问

**排查步骤**：
```bash
# 检查Nginx配置语法
nginx -t

# 查看Nginx错误日志
tail -f /var/log/nginx/error.log

# 检查后端服务是否运行
curl http://127.0.0.1:8000/api/health

# 检查端口占用
netstat -tlnp | grep :8000
```

#### 4. 文件权限问题

**问题症状**：
- 文件上传失败
- 日志写入失败
- 静态文件无法访问

**解决方案**：
```bash
# 设置正确的文件权限
chown -R www:www /www/wwwroot/xiaoyuweihan
chmod -R 755 /www/wwwroot/xiaoyuweihan

# 创建上传目录
mkdir -p /www/wwwroot/xiaoyuweihan/backend/uploads
chown www:www /www/wwwroot/xiaoyuweihan/backend/uploads
chmod 755 /www/wwwroot/xiaoyuweihan/backend/uploads

# 创建日志目录
mkdir -p /www/wwwroot/xiaoyuweihan/backend/logs
chown www:www /www/wwwroot/xiaoyuweihan/backend/logs
chmod 755 /www/wwwroot/xiaoyuweihan/backend/logs
```

### 应急处理

#### 服务异常重启

```bash
# 快速重启所有服务
systemctl restart xiaoyuweihan-backend.service
systemctl restart nginx
systemctl restart mysql

# 检查服务状态
systemctl status xiaoyuweihan-backend.service nginx mysql
```

#### 数据库恢复

```bash
# 从备份恢复数据库
mysql -u xiaoyuweihan -p xiaoyuweihan < /backup/mysql/xiaoyuweihan_20250115_020000.sql
```

### 联系支持

如果遇到无法解决的问题，请提供以下信息：

1. 错误日志输出
2. 系统环境信息
3. 操作步骤描述
4. 问题发生时间

---

*本部署指南涵盖了完整的生产环境部署流程，确保服务稳定运行*