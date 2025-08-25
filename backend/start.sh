#!/bin/bash

# 小雨微寒后端服务启动脚本
# start.sh

echo "🚀 小雨微寒后端服务启动脚本"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "⚡ 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📚 安装依赖包..."
pip install -r requirements.txt

# 创建必要的目录
echo "📁 创建目录..."
mkdir -p logs
mkdir -p uploads/{image,document,audio,video,archive,other}

# 设置环境变量
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 启动服务
echo "🎯 启动后端服务..."
if [ "$1" = "dev" ]; then
    echo "🔧 开发模式启动..."
    python main.py
else
    echo "🚀 生产模式启动..."
    gunicorn -c gunicorn.conf.py main:app
fi