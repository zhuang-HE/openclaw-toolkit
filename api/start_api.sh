#!/bin/bash
# 机器人数据库 API 服务启动脚本

set -e

WORKSPACE="/home/admin/.openclaw/workspace"
API_DIR="$WORKSPACE/api"
LOG_DIR="$WORKSPACE/logs"

echo "========================================="
echo "🤖 机器人数据库 API 服务"
echo "========================================="

# 确保目录存在
mkdir -p "$LOG_DIR"

# 进入 API 目录
cd "$API_DIR"

# 检查依赖
echo "检查依赖..."
python3 -c "import fastapi" 2>/dev/null || {
    echo "❌ FastAPI 未安装，正在安装依赖..."
    pip3 install -r requirements.txt --user -i https://pypi.tuna.tsinghua.edu.cn/simple
}

# 启动服务
echo ""
echo "启动 API 服务..."
echo "访问地址：http://localhost:8000"
echo "API 文档：http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo "========================================="
echo ""

python3 robot_api_server.py
