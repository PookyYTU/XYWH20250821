#!/bin/bash
# 小雨微寒网站快速更新脚本
# 用于快速更新代码而无需完整重新部署

set -e

# ====== 配置变量 ======
SITE_ROOT="/www/wwwroot/xiaoyuweihan"
BACKEND_DIR="${SITE_ROOT}/backend"
SERVICE_NAME="xiaoyuweihan-backend"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# ====== 备份当前版本 ======
backup_current() {
    log_info "📦 备份当前版本..."
    
    BACKUP_DIR="${SITE_ROOT}/backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # 备份后端代码
    if [ -d "${BACKEND_DIR}/app" ]; then
        cp -r "${BACKEND_DIR}/app" "$BACKUP_DIR/"
        cp "${BACKEND_DIR}/main.py" "$BACKUP_DIR/" 2>/dev/null || true
        cp "${BACKEND_DIR}/requirements.txt" "$BACKUP_DIR/" 2>/dev/null || true
        log_success "当前版本已备份到: $BACKUP_DIR"
    else
        log_warning "未找到现有后端代码"
    fi
}

# ====== 停止服务 ======
stop_services() {
    log_info "🛑 停止服务..."
    
    systemctl stop "$SERVICE_NAME" 2>/dev/null || {
        log_warning "无法通过systemctl停止服务，尝试直接杀死进程"
        pkill -f "gunicorn.*main:app" 2>/dev/null || true
    }
    
    sleep 2
    log_success "服务已停止"
}

# ====== 更新代码 ======
update_code() {
    log_info "📝 更新代码..."
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # 更新后端代码
    if [ -d "${SCRIPT_DIR}/app" ]; then
        cp -r "${SCRIPT_DIR}/app" "$BACKEND_DIR/"
        cp "${SCRIPT_DIR}/main.py" "$BACKEND_DIR/"
        cp "${SCRIPT_DIR}/requirements.txt" "$BACKEND_DIR/"
        
        # 检查是否需要更新环境变量
        if [ -f "${SCRIPT_DIR}/.env" ] && [ -f "${BACKEND_DIR}/.env" ]; then
            if ! cmp -s "${SCRIPT_DIR}/.env" "${BACKEND_DIR}/.env"; then
                log_warning "检测到.env文件变化，请手动检查配置"
                cp "${SCRIPT_DIR}/.env" "${BACKEND_DIR}/.env.new"
                log_info "新配置文件保存为: ${BACKEND_DIR}/.env.new"
            fi
        fi
        
        log_success "代码更新完成"
    else
        log_error "未找到新版本代码"
        exit 1
    fi
}

# ====== 更新依赖 ======
update_dependencies() {
    log_info "📦 检查并更新依赖..."
    
    cd "$BACKEND_DIR"
    
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        
        # 比较requirements.txt是否有变化
        if pip freeze | sort > current_deps.txt; then
            if ! cmp -s requirements.txt <(cat current_deps.txt | cut -d'=' -f1 | xargs -I {} grep "^{}=" requirements.txt 2>/dev/null || true); then
                log_info "检测到依赖变化，正在更新..."
                pip install -r requirements.txt
                log_success "依赖更新完成"
            else
                log_info "依赖无变化，跳过更新"
            fi
            rm -f current_deps.txt
        fi
    else
        log_error "未找到Python虚拟环境"
        exit 1
    fi
}

# ====== 数据库迁移 ======
migrate_database() {
    log_info "🗄️ 检查数据库..."
    
    cd "$BACKEND_DIR"
    source venv/bin/activate
    
    # 运行数据库创建（如果有新表）
    python3 -c "
from app.database import create_tables, test_connection
import sys

if test_connection():
    print('✅ 数据库连接正常')
    try:
        create_tables()
        print('✅ 数据库表检查完成')
    except Exception as e:
        print(f'⚠️ 数据库操作警告: {e}')
else:
    print('❌ 数据库连接失败')
    sys.exit(1)
"
    
    log_success "数据库检查完成"
}

# ====== 设置权限 ======
fix_permissions() {
    log_info "🔐 修复文件权限..."
    
    chown -R www:www "$BACKEND_DIR"
    chmod -R 755 "$BACKEND_DIR"
    chmod -R 775 "${BACKEND_DIR}/logs" 2>/dev/null || true
    chmod -R 775 "${BACKEND_DIR}/uploads" 2>/dev/null || true
    
    log_success "权限修复完成"
}

# ====== 启动服务 ======
start_services() {
    log_info "🚀 启动服务..."
    
    systemctl start "$SERVICE_NAME"
    sleep 3
    
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        log_success "服务启动成功"
    else
        log_error "服务启动失败"
        systemctl status "$SERVICE_NAME"
        exit 1
    fi
}

# ====== 健康检查 ======
health_check() {
    log_info "🩺 健康检查..."
    
    local max_attempts=6
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "http://127.0.0.1:8000/api/health" > /dev/null; then
            log_success "服务运行正常"
            return 0
        fi
        
        log_info "等待服务启动... (${attempt}/${max_attempts})"
        sleep 5
        ((attempt++))
    done
    
    log_error "服务健康检查失败"
    return 1
}

# ====== 回滚函数 ======
rollback() {
    log_warning "🔄 开始回滚到备份版本..."
    
    local latest_backup=$(ls -t "${SITE_ROOT}/backups/" 2>/dev/null | head -1)
    
    if [ -n "$latest_backup" ] && [ -d "${SITE_ROOT}/backups/$latest_backup" ]; then
        log_info "回滚到备份: $latest_backup"
        
        systemctl stop "$SERVICE_NAME" 2>/dev/null || true
        
        cp -r "${SITE_ROOT}/backups/$latest_backup/"* "$BACKEND_DIR/"
        
        systemctl start "$SERVICE_NAME"
        
        if health_check; then
            log_success "回滚成功"
        else
            log_error "回滚失败，请手动检查"
        fi
    else
        log_error "未找到备份文件，无法回滚"
    fi
}

# ====== 显示更新信息 ======
show_update_info() {
    echo ""
    echo "======================================"
    log_success "🎉 小雨微寒网站更新完成!"
    echo "📍 网站地址: http://47.105.52.49/"
    echo "📖 API文档: http://47.105.52.49/docs"
    echo "⏰ 更新时间: $(date)"
    echo "======================================"
    echo ""
    echo "🔧 如果遇到问题，可以执行回滚:"
    echo "  $0 --rollback"
    echo ""
}

# ====== 主更新流程 ======
main() {
    echo "🔄 小雨微寒网站快速更新脚本"
    echo "=================================="
    echo "⏰ 开始时间: $(date)"
    echo ""
    
    # 检查参数
    if [ "$1" = "--rollback" ]; then
        rollback
        exit 0
    fi
    
    # 检查权限
    if [[ $EUID -ne 0 ]]; then
        log_error "此脚本需要root权限运行"
        exit 1
    fi
    
    # 执行更新步骤
    backup_current
    stop_services
    update_code
    update_dependencies
    migrate_database
    fix_permissions
    start_services
    
    # 健康检查，失败则回滚
    if ! health_check; then
        log_error "更新后健康检查失败，正在回滚..."
        rollback
        exit 1
    fi
    
    show_update_info
    log_success "更新流程完成!"
}

# 错误处理
handle_error() {
    log_error "更新过程中发生错误"
    log_info "尝试回滚到备份版本..."
    rollback
    exit 1
}

trap 'handle_error' ERR

# 执行主函数
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi