# 小雨微寒网站后端部署指南

## 概述

本文档说明如何在宝塔面板环境中部署小雨微寒个人网站的FastAPI后端服务。

## 服务器环境要求

- **操作系统**: Linux (CentOS/Ubuntu)
- **面板**: 宝塔面板
- **Python**: 3.10+
- **数据库**: MySQL 5.7+
- **Web服务器**: Nginx
- **服务器**: 47.105.52.49

## 部署前准备

### 1. 数据库配置

确保MySQL数据库已创建并配置：

```sql
-- 数据库信息
数据库名: xiaoyuweihan
用户名: xiaoyuweihan
密码: Duan1999
主机: 47.105.52.49
端口: 3306
```

### 2. 文件上传

将整个 `backend` 目录上传到服务器的临时位置，例如 `/tmp/xiaoyuweihan-backend/`

## 自动部署

### 快速部署命令

```bash
# 1. 切换到根用户
sudo su -

# 2. 进入上传的目录
cd /tmp/xiaoyuweihan-backend

# 3. 给部署脚本执行权限
chmod +x deploy-baota.sh

# 4. 运行部署脚本
./deploy-baota.sh
```

### 部署脚本功能

部署脚本 `deploy-baota.sh` 会自动完成以下工作：

1. ✅ **环境检查** - 检查Python、MySQL、Nginx等依赖
2. 📁 **目录准备** - 创建网站目录和日志目录
3. 📋 **文件复制** - 复制后端代码到部署目录
4. 🐍 **Python环境** - 创建虚拟环境并安装依赖
5. 🗄️ **数据库初始化** - 创建数据库表结构
6. 🌐 **Nginx配置** - 配置反向代理和静态文件服务
7. ⚙️ **系统服务** - 配置systemd服务自动启动
8. 🔐 **权限设置** - 设置正确的文件权限
9. 🚀 **服务启动** - 启动后端API服务
10. ✅ **部署验证** - 验证服务是否正常运行

## 手动部署步骤

如果自动部署脚本出现问题，可以按以下步骤手动部署：

### 1. 准备目录

```bash
mkdir -p /www/wwwroot/xiaoyuweihan/backend
mkdir -p /www/wwwroot/xiaoyuweihan/backend/logs
mkdir -p /www/wwwroot/xiaoyuweihan/backend/uploads
```

### 2. 复制文件

```bash
cp -r /tmp/xiaoyuweihan-backend/* /www/wwwroot/xiaoyuweihan/backend/
```

### 3. 创建Python虚拟环境

```bash
cd /www/wwwroot/xiaoyuweihan/backend
/usr/local/bin/python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. 配置环境变量

检查 `.env` 文件中的数据库配置：

```bash
# 编辑 .env 文件
vi .env

# 确保以下配置正确：
DATABASE_URL=mysql+pymysql://xiaoyuweihan:Duan1999@47.105.52.49:3306/xiaoyuweihan
DB_HOST=47.105.52.49
DB_PORT=3306
DB_USER=xiaoyuweihan
DB_PASSWORD=Duan1999
DB_NAME=xiaoyuweihan
```

### 5. 初始化数据库

```bash
python test_db_connection.py
```

### 6. 配置Nginx

```bash
cp nginx.conf /www/server/nginx/conf/conf.d/xiaoyuweihan.conf
/www/server/nginx/sbin/nginx -t
/www/server/nginx/sbin/nginx -s reload
```

### 7. 配置系统服务

```bash
cp xiaoyuweihan-backend.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable xiaoyuweihan-backend
systemctl start xiaoyuweihan-backend
```

### 8. 设置权限

```bash
chown -R www:www /www/wwwroot/xiaoyuweihan
chmod -R 755 /www/wwwroot/xiaoyuweihan
chmod -R 775 /www/wwwroot/xiaoyuweihan/backend/logs
chmod -R 775 /www/wwwroot/xiaoyuweihan/backend/uploads
```

## 服务管理

### 常用命令

```bash
# 查看服务状态
systemctl status xiaoyuweihan-backend

# 启动服务
systemctl start xiaoyuweihan-backend

# 停止服务
systemctl stop xiaoyuweihan-backend

# 重启服务
systemctl restart xiaoyuweihan-backend

# 查看服务日志
journalctl -u xiaoyuweihan-backend -f

# 重载Nginx配置
/www/server/nginx/sbin/nginx -s reload
```

### 健康检查

```bash
# 检查API服务
curl http://127.0.0.1:8000/api/health

# 检查网站访问
curl http://47.105.52.49/

# 查看进程
ps aux | grep gunicorn
```

## 更新部署

### 快速更新

使用快速更新脚本：

```bash
# 上传新版本文件后
cd /www/wwwroot/xiaoyuweihan/backend
chmod +x update.sh
./update.sh
```

### 手动更新

```bash
# 1. 停止服务
systemctl stop xiaoyuweihan-backend

# 2. 备份当前版本
cp -r /www/wwwroot/xiaoyuweihan/backend /www/wwwroot/xiaoyuweihan/backend.backup.$(date +%Y%m%d_%H%M%S)

# 3. 复制新文件
cp -r /path/to/new/backend/* /www/wwwroot/xiaoyuweihan/backend/

# 4. 更新依赖（如果需要）
cd /www/wwwroot/xiaoyuweihan/backend
source venv/bin/activate
pip install -r requirements.txt

# 5. 启动服务
systemctl start xiaoyuweihan-backend
```

## 故障排查

### 常见问题

1. **服务启动失败**
   ```bash
   # 查看详细日志
   journalctl -u xiaoyuweihan-backend -n 50
   
   # 检查配置文件
   cd /www/wwwroot/xiaoyuweihan/backend
   source venv/bin/activate
   python -c "from app.config import settings; print('配置加载成功')"
   ```

2. **数据库连接失败**
   ```bash
   # 测试数据库连接
   python test_db_connection.py
   
   # 检查MySQL服务
   systemctl status mysql
   ```

3. **权限问题**
   ```bash
   # 重新设置权限
   chown -R www:www /www/wwwroot/xiaoyuweihan
   chmod -R 755 /www/wwwroot/xiaoyuweihan
   ```

4. **Nginx配置问题**
   ```bash
   # 测试Nginx配置
   /www/server/nginx/sbin/nginx -t
   
   # 查看Nginx错误日志
   tail -f /www/wwwroot/xiaoyuweihan/logs/nginx_error.log
   ```

### 日志文件位置

- **应用日志**: `/www/wwwroot/xiaoyuweihan/backend/logs/`
- **Nginx访问日志**: `/www/wwwroot/xiaoyuweihan/logs/nginx_access.log`
- **Nginx错误日志**: `/www/wwwroot/xiaoyuweihan/logs/nginx_error.log`
- **系统服务日志**: `journalctl -u xiaoyuweihan-backend`

## 备份策略

### 定期备份

建议设置定期备份任务：

```bash
# 创建备份脚本
cat > /www/wwwroot/xiaoyuweihan/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/www/backup/xiaoyuweihan/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 备份代码
cp -r /www/wwwroot/xiaoyuweihan/backend "$BACKUP_DIR/"

# 备份数据库
mysqldump -h 47.105.52.49 -u xiaoyuweihan -pDuan1999 xiaoyuweihan > "$BACKUP_DIR/database.sql"

echo "备份完成: $BACKUP_DIR"
EOF

chmod +x /www/wwwroot/xiaoyuweihan/backup.sh

# 添加到定时任务
echo "0 2 * * * /www/wwwroot/xiaoyuweihan/backup.sh" | crontab -
```

## 安全配置

### 防火墙设置

```bash
# 如果使用iptables
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# 禁止直接访问后端端口
iptables -A INPUT -p tcp --dport 8000 -s 127.0.0.1 -j ACCEPT
iptables -A INPUT -p tcp --dport 8000 -j DROP
```

### SSL配置（可选）

如果需要HTTPS，可以通过宝塔面板申请SSL证书，然后修改Nginx配置文件启用HTTPS重定向部分。

## 监控和维护

### 性能监控

```bash
# 查看系统资源
htop

# 查看服务资源占用
systemctl status xiaoyuweihan-backend

# 查看数据库连接数
mysql -h 47.105.52.49 -u xiaoyuweihan -pDuan1999 -e "SHOW STATUS LIKE 'Threads_connected';"
```

### 日志轮转

配置日志轮转避免日志文件过大：

```bash
cat > /etc/logrotate.d/xiaoyuweihan << 'EOF'
/www/wwwroot/xiaoyuweihan/backend/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    postrotate
        systemctl reload xiaoyuweihan-backend
    endscript
}
EOF
```

## 联系支持

如果遇到部署问题，请检查：

1. 📋 **部署日志** - 查看部署脚本输出
2. 🔍 **系统日志** - `journalctl -u xiaoyuweihan-backend`
3. 📁 **应用日志** - `/www/wwwroot/xiaoyuweihan/backend/logs/`
4. 🌐 **Nginx日志** - `/www/wwwroot/xiaoyuweihan/logs/nginx_error.log`
5. 🗄️ **数据库连接** - 运行 `python test_db_connection.py`

---

**部署完成后访问地址：**
- 🌐 **网站主页**: http://47.105.52.49/
- 📖 **API文档**: http://47.105.52.49/docs
- 🔧 **API接口**: http://47.105.52.49/api/