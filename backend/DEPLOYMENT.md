# 小雨微寒后端部署指南

## 系统要求

- **操作系统**: Ubuntu 20.04+ / CentOS 7+
- **Python**: 3.8+
- **MySQL**: 5.7+ (已安装)
- **Nginx**: 1.18+
- **服务器**: 47.105.52.49

## 部署步骤

### 1. 创建项目目录

```bash
# 创建项目目录
sudo mkdir -p /opt/xiaoyuweihan
cd /opt/xiaoyuweihan

# 设置权限
sudo chown -R www-data:www-data /opt/xiaoyuweihan
sudo chmod -R 755 /opt/xiaoyuweihan
```

### 2. 上传后端代码

将整个 `backend` 目录上传到服务器的 `/opt/xiaoyuweihan/` 路径下：

```bash
# 示例：使用scp上传
scp -r ./backend root@47.105.52.49:/opt/xiaoyuweihan/

# 设置权限
sudo chown -R www-data:www-data /opt/xiaoyuweihan/backend
```

### 3. 安装Python依赖

```bash
cd /opt/xiaoyuweihan/backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 如果pip版本较老，可能需要升级
pip install --upgrade pip
```

### 4. 配置环境变量

```bash
cd /opt/xiaoyuweihan/backend

# 编辑环境配置文件
nano .env
```

检查并修改以下配置：

```env
# FastAPI后端配置
DEBUG=False
SECRET_KEY=xiaoyuweihan_secret_key_2025_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=Duan1999
DB_NAME=xiaoyuweihan

# 文件上传配置
UPLOAD_DIR=/opt/xiaoyuweihan/backend/uploads
MAX_FILE_SIZE=50000000
ALLOWED_EXTENSIONS=.jpg,.jpeg,.png,.gif,.bmp,.webp,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.md,.mp3,.mp4,.avi,.mov,.zip,.rar

# CORS配置
ALLOWED_ORIGINS=http://47.105.52.49,http://47.105.52.49:80,http://47.105.52.49:443,https://47.105.52.49
```

### 5. 数据库初始化

```bash
# 登录MySQL
mysql -u root -p

# 创建数据库（如果还没有）
CREATE DATABASE IF NOT EXISTS xiaoyuweihan CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建专用用户（推荐）
CREATE USER 'xiaoyuweihan'@'localhost' IDENTIFIED BY 'Duan1999';
GRANT ALL PRIVILEGES ON xiaoyuweihan.* TO 'xiaoyuweihan'@'localhost';
FLUSH PRIVILEGES;

EXIT;
```

### 6. 测试后端服务

```bash
cd /opt/xiaoyuweihan/backend

# 激活虚拟环境
source venv/bin/activate

# 测试启动
python main.py

# 如果成功，应该看到类似输出：
# INFO:     Started server process [xxxx]
# INFO:     Waiting for application startup.
# ✅ 后端服务启动完成！
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

按 `Ctrl+C` 停止测试服务。

### 7. 配置systemd服务

```bash
# 复制服务文件
sudo cp /opt/xiaoyuweihan/backend/xiaoyuweihan-backend.service /etc/systemd/system/

# 重新加载systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start xiaoyuweihan-backend

# 检查状态
sudo systemctl status xiaoyuweihan-backend

# 设置开机自启
sudo systemctl enable xiaoyuweihan-backend
```

### 8. 配置Nginx

```bash
# 安装Nginx（如果还没有）
sudo apt update
sudo apt install nginx

# 复制Nginx配置
sudo cp /opt/xiaoyuweihan/backend/nginx.conf /etc/nginx/sites-available/xiaoyuweihan

# 创建软链接
sudo ln -s /etc/nginx/sites-available/xiaoyuweihan /etc/nginx/sites-enabled/

# 删除默认配置（可选）
sudo rm -f /etc/nginx/sites-enabled/default

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### 9. 部署前端文件

```bash
# 创建前端目录
sudo mkdir -p /var/www/xiaoyuweihan

# 上传前端文件
# 将除了backend目录外的所有文件上传到 /var/www/xiaoyuweihan/

# 设置权限
sudo chown -R www-data:www-data /var/www/xiaoyuweihan
sudo chmod -R 755 /var/www/xiaoyuweihan
```

### 10. 防火墙配置

```bash
# 允许HTTP和HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 如果直接访问后端，允许8000端口（可选）
sudo ufw allow 8000/tcp

# 重新加载防火墙
sudo ufw reload
```

## 服务管理

### 启动/停止/重启服务

```bash
# 后端服务
sudo systemctl start xiaoyuweihan-backend
sudo systemctl stop xiaoyuweihan-backend
sudo systemctl restart xiaoyuweihan-backend

# Nginx
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
```

### 查看日志

```bash
# 后端服务日志
sudo journalctl -u xiaoyuweihan-backend -f

# 后端应用日志
tail -f /opt/xiaoyuweihan/backend/logs/error.log
tail -f /opt/xiaoyuweihan/backend/logs/access.log

# Nginx日志
tail -f /var/log/nginx/xiaoyuweihan_access.log
tail -f /var/log/nginx/xiaoyuweihan_error.log
```

## 备份策略

### 数据库备份

```bash
# 创建备份脚本
sudo nano /opt/xiaoyuweihan/backup.sh
```

```bash
#!/bin/bash
# 数据库备份脚本

BACKUP_DIR="/opt/xiaoyuweihan/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="xiaoyuweihan"
DB_USER="root"
DB_PASS="Duan1999"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
mysqldump -u$DB_USER -p$DB_PASS $DB_NAME > $BACKUP_DIR/xiaoyuweihan_$DATE.sql

# 删除7天前的备份
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete

echo "数据库备份完成: xiaoyuweihan_$DATE.sql"
```

```bash
# 设置执行权限
sudo chmod +x /opt/xiaoyuweihan/backup.sh

# 设置定时任务（每天凌晨2点备份）
sudo crontab -e
# 添加：0 2 * * * /opt/xiaoyuweihan/backup.sh
```

### 文件备份

```bash
# 备份上传的文件
tar -czf /opt/xiaoyuweihan/backups/uploads_$(date +%Y%m%d).tar.gz /opt/xiaoyuweihan/backend/uploads/
```

## 监控和维护

### 健康检查

```bash
# 检查API健康状态
curl http://localhost:8000/api/health

# 检查前端访问
curl http://47.105.52.49/

# 检查服务状态
sudo systemctl status xiaoyuweihan-backend
sudo systemctl status nginx
```

### 性能优化

1. **Gunicorn工作进程调优**：
   - 根据CPU核心数调整 `workers` 数量
   - 监控内存使用情况

2. **Nginx缓存配置**：
   - 静态文件缓存已配置
   - 可根据需要调整缓存时间

3. **数据库优化**：
   - 定期清理无用数据
   - 添加必要的索引

## 故障排除

### 常见问题

1. **后端服务无法启动**：
   ```bash
   # 检查日志
   sudo journalctl -u xiaoyuweihan-backend -n 50
   
   # 检查端口占用
   sudo netstat -tlnp | grep 8000
   ```

2. **数据库连接失败**：
   - 检查MySQL服务状态
   - 验证数据库配置
   - 确认网络连接

3. **文件上传失败**：
   - 检查上传目录权限
   - 确认磁盘空间
   - 查看文件大小限制

4. **前端无法访问API**：
   - 检查CORS配置
   - 确认Nginx代理配置
   - 查看防火墙设置

## 更新部署

### 后端更新

```bash
# 备份当前版本
cp -r /opt/xiaoyuweihan/backend /opt/xiaoyuweihan/backend_backup_$(date +%Y%m%d)

# 停止服务
sudo systemctl stop xiaoyuweihan-backend

# 更新代码
# ... 上传新代码 ...

# 更新依赖（如果需要）
cd /opt/xiaoyuweihan/backend
source venv/bin/activate
pip install -r requirements.txt

# 启动服务
sudo systemctl start xiaoyuweihan-backend

# 检查状态
sudo systemctl status xiaoyuweihan-backend
```

### 前端更新

```bash
# 备份当前版本
cp -r /var/www/xiaoyuweihan /var/www/xiaoyuweihan_backup_$(date +%Y%m%d)

# 上传新的前端文件
# ... 

# 重新加载Nginx（可选）
sudo systemctl reload nginx
```

---

## 联系信息

如有问题，请联系系统管理员。

部署完成后，可以通过以下地址访问：
- 前端：http://47.105.52.49/
- API文档：http://47.105.52.49/api/docs
- 健康检查：http://47.105.52.49/api/health