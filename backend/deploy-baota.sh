#!/bin/bash

# 小雨微寒宝塔部署脚本
# 适用于宝塔面板环境的快速部署

set -e  # 遇到错误立即退出

echo "🚀 小雨微寒项目宝塔部署脚本"
echo "================================"

# 检查是否为root用户
if [[ $EUID -ne 0 ]]; then
   echo "❌ 此脚本需要root权限运行"
   echo "请使用: sudo $0"
   exit 1
fi

# 配置变量
PROJECT_DIR="/www/wwwroot/xiaoyuweihan"
BACKEND_DIR="$PROJECT_DIR/backend"
SERVICE_NAME="xiaoyuweihan-backend"
BT_NGINX_DIR="/www/server/nginx"

echo "📁 项目目录: $PROJECT_DIR"
echo "🖥️  后端目录: $BACKEND_DIR"
echo "🌐 宝塔Nginx目录: $BT_NGINX_DIR"
echo ""

# 检查宝塔环境
echo "🔍 检查宝塔环境..."

if [ ! -d "/www/server" ]; then
    echo "❌ 未检测到宝塔面板，请先安装宝塔面板"
    exit 1
fi

if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ 项目目录不存在，请先将项目拉取到 $PROJECT_DIR"
    echo "建议命令："
    echo "cd /www/wwwroot && git clone <your-repo-url> xiaoyuweihan"
    exit 1
fi

echo "✅ 宝塔环境检查完成"

# 检查Python3
if ! command -v python3 &> /dev/null; then
    echo "📦 正在安装Python3..."
    yum install -y python3 python3-pip || apt update && apt install -y python3 python3-venv python3-pip
fi

# 检查MySQL
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL 未安装，请在宝塔面板中安装MySQL"
    exit 1
fi

# 设置权限
echo "🔐 设置文件权限..."

# 处理宝塔的.user.ini文件保护
echo "🔧 处理宝塔文件保护..."
if [ -f "$PROJECT_DIR/.user.ini" ]; then
    echo "发现.user.ini文件，移除保护属性..."
    chattr -i $PROJECT_DIR/.user.ini 2>/dev/null || true
fi

# 查找并处理其他可能被保护的ini文件
find $PROJECT_DIR -name "*.ini" -exec chattr -i {} \; 2>/dev/null || true

chown -R www:www $PROJECT_DIR
chmod -R 755 $PROJECT_DIR

# 恢复.user.ini文件保护（如果存在）
if [ -f "$PROJECT_DIR/.user.ini" ]; then
    echo "恢复.user.ini文件保护..."
    chattr +i $PROJECT_DIR/.user.ini 2>/dev/null || true
fi

# 创建Python虚拟环境
echo "🐍 创建Python虚拟环境..."
cd $BACKEND_DIR

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 激活虚拟环境并安装依赖
echo "📦 安装Python依赖..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p logs
mkdir -p uploads/{image,document,audio,video,archive,other}
chown -R www:www uploads logs

# 配置数据库
echo "🗄️  配置数据库..."
read -p "请输入MySQL root密码: " -s mysql_password
echo ""

# 测试数据库连接
mysql -u root -p$mysql_password -e "SELECT 1;" &> /dev/null
if [ $? -ne 0 ]; then
    echo "❌ 数据库连接失败，请检查密码"
    exit 1
fi

# 创建数据库
mysql -u root -p$mysql_password -e "CREATE DATABASE IF NOT EXISTS xiaoyuweihan CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
echo "✅ 数据库创建成功"

# 配置systemd服务
echo "⚙️  配置系统服务..."
cp $BACKEND_DIR/xiaoyuweihan-backend.service /etc/systemd/system/
systemctl daemon-reload

# 配置Nginx（宝塔版本）
echo "🌐 配置Nginx..."

# 检查是否已有站点配置
BT_SITE_CONF="/www/server/panel/vhost/nginx/47.105.52.49.conf"
if [ -f "$BT_SITE_CONF" ]; then
    echo "📄 发现现有宝塔站点配置，备份原配置..."
    cp $BT_SITE_CONF $BT_SITE_CONF.backup.$(date +%Y%m%d_%H%M%S)
fi

# 创建宝塔兼容的Nginx配置
cat > $BT_SITE_CONF << 'EOF'
server {
    listen 80;
    server_name 47.105.52.49;
    
    # 设置客户端最大请求体大小
    client_max_body_size 50M;
    
    # 前端静态文件
    location / {
        root /www/wwwroot/xiaoyuweihan;
        index index.html;
        try_files $uri $uri/ /index.html;
        
        # 设置缓存
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
    
    # 后端API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # 处理WebSocket连接
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # 文件上传下载
    location /uploads/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # 健康检查
    location /health {
        proxy_pass http://127.0.0.1:8000/api/health;
        access_log off;
    }
    
    # 安全设置
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # 日志
    access_log /www/wwwlogs/xiaoyuweihan_access.log;
    error_log /www/wwwlogs/xiaoyuweihan_error.log;
}
EOF

# 测试Nginx配置
nginx -t
if [ $? -ne 0 ]; then
    echo "❌ Nginx配置错误"
    exit 1
fi

# 启动服务
echo "🚀 启动服务..."

# 启动后端服务
systemctl start $SERVICE_NAME
systemctl enable $SERVICE_NAME

# 重启Nginx
systemctl reload nginx

# 配置防火墙（如果需要）
echo "🛡️  配置防火墙..."
if command -v firewall-cmd &> /dev/null; then
    # CentOS/RHEL firewalld
    firewall-cmd --permanent --add-port=80/tcp
    firewall-cmd --permanent --add-port=443/tcp
    firewall-cmd --reload
elif command -v ufw &> /dev/null; then
    # Ubuntu ufw
    ufw allow 80/tcp
    ufw allow 443/tcp
fi

# 验证服务状态
echo "🔍 验证服务状态..."
sleep 3

backend_status=$(systemctl is-active $SERVICE_NAME)
nginx_status=$(systemctl is-active nginx)

echo "后端服务状态: $backend_status"
echo "Nginx状态: $nginx_status"

if [ "$backend_status" = "active" ] && [ "$nginx_status" = "active" ]; then
    echo ""
    echo "🎉 宝塔部署成功！"
    echo "================================"
    echo "前端访问地址: http://47.105.52.49/"
    echo "API文档地址: http://47.105.52.49/docs"
    echo "健康检查: http://47.105.52.49/api/health"
    echo ""
    echo "宝塔面板管理："
    echo "  - 网站管理：在宝塔面板的'网站'中可以看到配置"
    echo "  - SSL配置：可在宝塔面板中配置SSL证书"
    echo "  - 日志查看：宝塔面板网站日志或命令行查看"
    echo ""
    echo "管理命令:"
    echo "  查看后端日志: journalctl -u $SERVICE_NAME -f"
    echo "  重启后端: systemctl restart $SERVICE_NAME"
    echo "  重启Nginx: systemctl restart nginx"
    echo ""
    echo "注意事项："
    echo "1. 后端服务运行在8000端口，不要在宝塔中删除此端口配置"
    echo "2. 如需修改配置，编辑后重启对应服务"
    echo "3. 定期备份数据库和上传的文件"
else
    echo ""
    echo "❌ 部署过程中出现问题"
    echo "请检查日志:"
    echo "  后端日志: journalctl -u $SERVICE_NAME"
    echo "  Nginx日志: tail -f /www/wwwlogs/xiaoyuweihan_error.log"
fi

echo ""
echo "📚 详细文档请查看: $BACKEND_DIR/DEPLOYMENT.md"