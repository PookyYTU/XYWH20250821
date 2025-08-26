#!/bin/bash
# 小雨微寒网站自动部署脚本 (宝塔面板环境)
# 适用于服务器 47.105.52.49
# 部署目标: /www/wwwroot/xiaoyuweihan

set -e

# ====== 配置变量 ======
SITE_ROOT="/www/wwwroot/xiaoyuweihan"
BACKEND_DIR="${SITE_ROOT}/backend"
NGINX_CONF_DIR="/www/server/nginx/conf/conf.d"
SITE_CONF="${NGINX_CONF_DIR}/xiaoyuweihan.conf"
PYTHON_BIN="/usr/local/bin/python3.10"
SERVICE_NAME="xiaoyuweihan-backend"
SYSTEMD_DIR="/etc/systemd/system"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ====== 工具函数 ======
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查文件是否存在
file_exists() {
    [ -f "$1" ]
}

# 检查目录是否存在
dir_exists() {
    [ -d "$1" ]
}

# ====== 环境检查 ======
check_environment() {
    log_info "🔍 检查部署环境..."
    
    # 检查是否为root用户
    if [[ $EUID -ne 0 ]]; then
        log_error "此脚本需要root权限运行"
        exit 1
    fi
    
    # 检查Python 3.10
    if ! file_exists "$PYTHON_BIN"; then
        log_error "未找到Python 3.10，请先安装"
        exit 1
    fi
    
    # 检查宝塔环境
    if ! dir_exists "/www/server"; then
        log_error "未检测到宝塔面板环境"
        exit 1
    fi
    
    # 检查Nginx
    if ! command_exists "nginx"; then
        log_error "未找到Nginx"
        exit 1
    fi
    
    # 检查MySQL
    if ! command_exists "mysql"; then
        log_error "未找到MySQL"
        exit 1
    fi
    
    log_success "环境检查通过"
}

# ====== 目录准备 ======
prepare_directories() {
    log_info "📁 准备部署目录..."
    
    # 创建网站根目录
    mkdir -p "$SITE_ROOT"
    mkdir -p "$BACKEND_DIR"
    mkdir -p "${BACKEND_DIR}/logs"
    mkdir -p "${BACKEND_DIR}/uploads"
    
    # 处理.user.ini文件的不可变属性
    if file_exists "${SITE_ROOT}/.user.ini"; then
        log_info "处理.user.ini文件..."
        chattr -i "${SITE_ROOT}/.user.ini" 2>/dev/null || true
        rm -f "${SITE_ROOT}/.user.ini"
    fi
    
    log_success "目录准备完成"
}

# ====== 复制后端文件 ======
copy_backend_files() {
    log_info "📋 复制后端文件..."
    
    # 当前脚本所在目录（假设脚本和源码在同一目录）
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # 复制后端源码
    if dir_exists "${SCRIPT_DIR}/app"; then
        cp -r "${SCRIPT_DIR}/app" "$BACKEND_DIR/"
        cp "${SCRIPT_DIR}/main.py" "$BACKEND_DIR/"
        cp "${SCRIPT_DIR}/requirements.txt" "$BACKEND_DIR/"
        cp "${SCRIPT_DIR}/.env" "$BACKEND_DIR/"
        cp "${SCRIPT_DIR}/gunicorn.conf.py" "$BACKEND_DIR/"
        cp "${SCRIPT_DIR}/start.sh" "$BACKEND_DIR/"
        chmod +x "${BACKEND_DIR}/start.sh"
        
        log_success "后端文件复制完成"
    else
        log_error "未找到后端源码目录"
        exit 1
    fi
}

# ====== Python环境配置 ======
setup_python_environment() {
    log_info "🐍 配置Python环境..."
    
    cd "$BACKEND_DIR"
    
    # 创建虚拟环境
    if ! dir_exists "venv"; then
        log_info "创建Python虚拟环境..."
        $PYTHON_BIN -m venv venv
    fi
    
    # 激活虚拟环境并安装依赖
    log_info "安装Python依赖..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    log_success "Python环境配置完成"
}

# ====== 数据库配置 ======
setup_database() {
    log_info "🗄️ 配置数据库..."
    
    cd "$BACKEND_DIR"
    source venv/bin/activate
    
    # 测试数据库连接并创建表
    python3 -c "
from app.database import create_tables, test_connection
import sys

if test_connection():
    print('✅ 数据库连接成功')
    try:
        create_tables()
        print('✅ 数据库表创建完成')
    except Exception as e:
        print(f'❌ 创建数据库表失败: {e}')
        sys.exit(1)
else:
    print('❌ 数据库连接失败，请检查配置')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        log_success "数据库配置完成"
    else
        log_error "数据库配置失败"
        exit 1
    fi
}

# ====== Nginx配置 ======
setup_nginx() {
    log_info "🌐 配置Nginx..."
    
    # 复制Nginx配置文件
    cp "${BACKEND_DIR}/nginx.conf" "$SITE_CONF"
    
    # 测试Nginx配置
    if /www/server/nginx/sbin/nginx -t; then
        log_info "重载Nginx配置..."
        /www/server/nginx/sbin/nginx -s reload
        log_success "Nginx配置完成"
    else
        log_error "Nginx配置文件有误"
        exit 1
    fi
}

# ====== 系统服务配置 ======
setup_systemd_service() {
    log_info "⚙️ 配置系统服务..."
    
    # 复制systemd服务文件
    cp "${BACKEND_DIR}/xiaoyuweihan-backend.service" "${SYSTEMD_DIR}/${SERVICE_NAME}.service"
    
    # 重载systemd并启用服务
    systemctl daemon-reload
    systemctl enable "$SERVICE_NAME"
    
    log_success "系统服务配置完成"
}

# ====== 设置文件权限 ======
set_permissions() {
    log_info "🔐 设置文件权限..."
    
    # 设置用户和组
    chown -R www:www "$SITE_ROOT"
    
    # 设置目录权限
    find "$SITE_ROOT" -type d -exec chmod 755 {} \\;
    
    # 设置文件权限
    find "$SITE_ROOT" -type f -exec chmod 644 {} \\;
    
    # 设置可执行文件权限
    chmod +x "${BACKEND_DIR}/start.sh"
    
    # 设置日志和上传目录权限
    chmod -R 775 "${BACKEND_DIR}/logs"
    chmod -R 775 "${BACKEND_DIR}/uploads"
    
    log_success "文件权限设置完成"
}

# ====== 启动服务 ======
start_services() {
    log_info "🚀 启动服务..."
    
    # 停止可能运行的旧服务
    log_info "停止旧服务..."
    systemctl stop "$SERVICE_NAME" 2>/dev/null || true
    pkill -f "gunicorn.*main:app" 2>/dev/null || true
    sleep 2
    
    # 启动新服务
    log_info "启动后端服务..."
    systemctl start "$SERVICE_NAME"
    
    # 等待服务启动
    sleep 3
    
    # 检查服务状态
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        log_success "后端服务启动成功"
    else
        log_error "后端服务启动失败"
        systemctl status "$SERVICE_NAME"
        exit 1
    fi
}

# ====== 验证部署 ======
verify_deployment() {
    log_info "✅ 验证部署..."
    
    # 检查API健康状态
    sleep 5
    
    if curl -f -s "http://127.0.0.1:8000/api/health" > /dev/null; then
        log_success "API服务运行正常"
    else
        log_error "API服务无响应"
        return 1
    fi
    
    # 检查网站访问
    if curl -f -s "http://47.105.52.49/" > /dev/null; then
        log_success "网站访问正常"
    else
        log_warning "网站可能需要一些时间才能完全启动"
    fi
}

# ====== 清理工作 ======
cleanup() {
    log_info "🧹 清理临时文件..."
    
    # 清理可能的临时文件
    find /tmp -name "*xiaoyuweihan*" -mtime +1 -delete 2>/dev/null || true
    
    log_success "清理完成"
}

# ====== 部署信息输出 ======
show_deployment_info() {
    log_success "🎉 小雨微寒网站部署完成!"
    echo ""
    echo "======================================"
    echo "📍 网站地址: http://47.105.52.49/"
    echo "📖 API文档: http://47.105.52.49/docs"
    echo "🔧 API地址: http://47.105.52.49/api/"
    echo "📁 网站目录: $SITE_ROOT"
    echo "📁 后端目录: $BACKEND_DIR"
    echo "📋 日志目录: ${BACKEND_DIR}/logs"
    echo "======================================"
    echo ""
    echo "🔧 常用管理命令:"
    echo "  重启后端服务: systemctl restart $SERVICE_NAME"
    echo "  查看服务状态: systemctl status $SERVICE_NAME"
    echo "  查看服务日志: journalctl -u $SERVICE_NAME -f"
    echo "  重载Nginx: /www/server/nginx/sbin/nginx -s reload"
    echo ""
}

# ====== 主部署流程 ======
main() {
    echo "🌟 小雨微寒网站自动部署脚本"
    echo "=================================="
    echo "🎯 目标服务器: 47.105.52.49"
    echo "📁 部署目录: $SITE_ROOT"
    echo "⏰ 开始时间: $(date)"
    echo "=================================="
    echo ""
    
    # 执行部署步骤
    check_environment
    prepare_directories
    copy_backend_files
    setup_python_environment
    setup_database
    setup_nginx
    setup_systemd_service
    set_permissions
    start_services
    verify_deployment
    cleanup
    show_deployment_info
    
    log_success "部署流程全部完成!"
}

# ====== 错误处理 ======
handle_error() {
    log_error "部署过程中发生错误，正在回滚..."
    
    # 停止服务
    systemctl stop "$SERVICE_NAME" 2>/dev/null || true
    
    # 输出错误日志
    echo "请查看以下日志文件排查问题:"
    echo "- ${BACKEND_DIR}/logs/error.log"
    echo "- journalctl -u $SERVICE_NAME"
    
    exit 1
}

# 设置错误处理
trap 'handle_error' ERR

# 如果直接执行此脚本
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi