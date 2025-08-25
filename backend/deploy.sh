#!/bin/bash

# 小雨微寒快速部署脚本
# Quick deployment script for XiaoYuWeiHan project

set -e  # 遇到错误立即退出

echo "🚀 小雨微寒项目快速部署脚本"
echo "================================"

# 检查是否为root用户
if [[ $EUID -ne 0 ]]; then
   echo "❌ 此脚本需要root权限运行"
   echo "请使用: sudo $0"
   exit 1
fi

# 配置变量
PROJECT_DIR="/opt/xiaoyuweihan"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="/var/www/xiaoyuweihan"
SERVICE_NAME="xiaoyuweihan-backend"

# 获取当前脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "📁 项目目录: $PROJECT_DIR"
echo "🖥️  后端目录: $BACKEND_DIR"
echo "🌐 前端目录: $FRONTEND_DIR"
echo "📄 脚本目录: $SCRIPT_DIR"
echo ""

# 检查系统依赖
echo "🔍 检查系统依赖..."

# 检查Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    echo "正在安装Python3..."
    apt update
    apt install -y python3 python3-venv python3-pip
fi

# 检查MySQL
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL 未安装"
    echo "请先安装MySQL服务器"
    exit 1
fi

# 检查Nginx
if ! command -v nginx &> /dev/null; then
    echo "📦 正在安装Nginx..."
    apt update
    apt install -y nginx
fi

echo "✅ 系统依赖检查完成"

# 创建项目目录
echo "📁 创建项目目录..."
mkdir -p $PROJECT_DIR
mkdir -p $FRONTEND_DIR

# 复制后端文件
echo "📋 复制后端文件..."
if [ -d "$SCRIPT_DIR" ]; then
    cp -r $SCRIPT_DIR $BACKEND_DIR
    echo "✅ 后端文件复制完成"
else
    echo "❌ 找不到后端源文件目录"
    exit 1
fi

# 设置权限
echo "🔐 设置文件权限..."
chown -R www-data:www-data $PROJECT_DIR
chown -R www-data:www-data $FRONTEND_DIR
chmod -R 755 $PROJECT_DIR
chmod -R 755 $FRONTEND_DIR

# 创建Python虚拟环境
echo "🐍 创建Python虚拟环境..."
cd $BACKEND_DIR
python3 -m venv venv

# 激活虚拟环境并安装依赖
echo "📦 安装Python依赖..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p logs
mkdir -p uploads/{image,document,audio,video,archive,other}

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

# 配置Nginx
echo "🌐 配置Nginx..."
cp $BACKEND_DIR/nginx.conf /etc/nginx/sites-available/xiaoyuweihan
ln -sf /etc/nginx/sites-available/xiaoyuweihan /etc/nginx/sites-enabled/

# 删除默认配置
rm -f /etc/nginx/sites-enabled/default

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

# 启动Nginx
systemctl restart nginx
systemctl enable nginx

# 配置防火墙
echo "🛡️  配置防火墙..."
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# 验证服务状态
echo "🔍 验证服务状态..."
sleep 3

backend_status=$(systemctl is-active $SERVICE_NAME)
nginx_status=$(systemctl is-active nginx)

echo "后端服务状态: $backend_status"
echo "Nginx状态: $nginx_status"

if [ "$backend_status" = "active" ] && [ "$nginx_status" = "active" ]; then
    echo ""
    echo "🎉 部署成功！"
    echo "================================"
    echo "前端访问地址: http://$(hostname -I | awk '{print $1}')/"
    echo "API文档地址: http://$(hostname -I | awk '{print $1}')/docs"
    echo "健康检查: http://$(hostname -I | awk '{print $1}')/api/health"
    echo ""
    echo "管理命令:"
    echo "  查看后端日志: journalctl -u $SERVICE_NAME -f"
    echo "  重启后端: systemctl restart $SERVICE_NAME"
    echo "  重启Nginx: systemctl restart nginx"
    echo ""
    echo "现在需要："
    echo "1. 将前端文件上传到 $FRONTEND_DIR"
    echo "2. 检查 $BACKEND_DIR/.env 配置文件"
    echo "3. 根据需要调整数据库配置"
else
    echo ""
    echo "❌ 部署过程中出现问题"
    echo "请检查日志:"
    echo "  后端日志: journalctl -u $SERVICE_NAME"
    echo "  Nginx日志: journalctl -u nginx"
fi

echo ""
echo "📚 详细文档请查看: $BACKEND_DIR/DEPLOYMENT.md"