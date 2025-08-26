#!/bin/bash
# 小雨微寒后端服务启动脚本

set -e

# 配置变量
BACKEND_DIR="/www/wwwroot/xiaoyuweihan/backend"
PYTHON_BIN="/usr/local/bin/python3.10"
VENV_DIR="${BACKEND_DIR}/venv"
LOG_DIR="${BACKEND_DIR}/logs"
UPLOAD_DIR="${BACKEND_DIR}/uploads"

# 检查Python版本
check_python() {
    echo "🔍 检查Python环境..."
    if [ ! -f "$PYTHON_BIN" ]; then
        echo "❌ 未找到Python 3.10，请确保已正确安装"
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_BIN --version 2>&1)
    echo "✅ $PYTHON_VERSION"
}

# 创建必要目录
create_directories() {
    echo "📁 创建必要目录..."
    mkdir -p "$LOG_DIR"
    mkdir -p "$UPLOAD_DIR"
    echo "✅ 目录创建完成"
}

# 设置权限
set_permissions() {
    echo "🔐 设置文件权限..."
    chown -R www:www "$BACKEND_DIR"
    chmod -R 755 "$BACKEND_DIR"
    chmod -R 775 "$LOG_DIR"
    chmod -R 775 "$UPLOAD_DIR"
    echo "✅ 权限设置完成"
}

# 创建虚拟环境
create_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        echo "🐍 创建Python虚拟环境..."
        $PYTHON_BIN -m venv "$VENV_DIR"
        echo "✅ 虚拟环境创建完成"
    else
        echo "ℹ️ 虚拟环境已存在"
    fi
}

# 安装依赖
install_dependencies() {
    echo "📦 安装Python依赖..."
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install -r "$BACKEND_DIR/requirements.txt"
    echo "✅ 依赖安装完成"
}

# 数据库初始化
init_database() {
    echo "🗄️ 初始化数据库..."
    source "$VENV_DIR/bin/activate"
    cd "$BACKEND_DIR"
    $PYTHON_BIN -c "
from app.database import create_tables, test_connection
if test_connection():
    print('✅ 数据库连接成功')
    create_tables()
    print('✅ 数据库表创建完成')
else:
    print('❌ 数据库连接失败')
    exit(1)
"
}

# 启动服务
start_service() {
    echo "🚀 启动后端服务..."
    source "$VENV_DIR/bin/activate"
    cd "$BACKEND_DIR"
    
    # 检查是否已经在运行
    if pgrep -f "gunicorn.*main:app" > /dev/null; then
        echo "⚠️ 服务已在运行，正在重启..."
        pkill -f "gunicorn.*main:app" || true
        sleep 2
    fi
    
    # 启动Gunicorn
    nohup $VENV_DIR/bin/gunicorn --config gunicorn.conf.py main:app > "$LOG_DIR/gunicorn.log" 2>&1 &
    
    # 等待服务启动
    sleep 3
    
    # 检查服务状态
    if pgrep -f "gunicorn.*main:app" > /dev/null; then
        echo "✅ 后端服务启动成功"
        echo "📊 服务状态:"
        ps aux | grep -v grep | grep "gunicorn.*main:app"
    else
        echo "❌ 后端服务启动失败"
        echo "📋 查看日志:"
        tail -20 "$LOG_DIR/gunicorn.log"
        exit 1
    fi
}

# 主执行逻辑
main() {
    echo "🌟 小雨微寒后端服务启动脚本"
    echo "=================================="
    
    cd "$BACKEND_DIR" || {
        echo "❌ 无法切换到后端目录: $BACKEND_DIR"
        exit 1
    }
    
    check_python
    create_directories
    create_venv
    install_dependencies
    set_permissions
    init_database
    start_service
    
    echo "=================================="
    echo "🎉 小雨微寒后端服务部署完成!"
    echo "📍 API地址: http://47.105.52.49/api/"
    echo "📖 API文档: http://47.105.52.49/docs"
    echo "📋 日志目录: $LOG_DIR"
}

# 如果直接执行此脚本
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi