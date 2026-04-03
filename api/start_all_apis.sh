#!/bin/bash
# 三个数据库 API 服务统一启动脚本

WORKSPACE="/home/admin/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs"
API_DIR="$WORKSPACE/api"

mkdir -p "$LOG_DIR"

echo "========================================="
echo "启动三个数据库 API 服务"
echo "========================================="
echo ""

# 机器人数据库 API (端口 8000)
echo "🤖 启动机器人数据库 API (端口 8000)..."
cd "$API_DIR"
nohup python3 robot_api_server.py > "$LOG_DIR/robot_api.log" 2>&1 &
ROBOT_PID=$!
echo "   PID: $ROBOT_PID"

# 无人机数据库 API (端口 8081)
echo "🛸 启动无人机数据库 API (端口 8081)..."
cd "$API_DIR"
nohup python3 drone_api_server.py > "$LOG_DIR/drone_api.log" 2>&1 &
DRONE_PID=$!
echo "   PID: $DRONE_PID"

# 临床试验数据库 API (端口 8082)
echo "🏥 启动临床试验数据库 API (端口 8082)..."
cd "$API_DIR"
nohup python3 clinical_trial_api_server.py > "$LOG_DIR/clinical_api.log" 2>&1 &
CLINICAL_PID=$!
echo "   PID: $CLINICAL_PID"

echo ""
echo "========================================="
echo "所有 API 服务已启动"
echo "========================================="
echo ""
echo "📊 服务状态："
echo "   机器人数据库：http://localhost:8000"
echo "   无人机数据库：http://localhost:8081"
echo "   临床试验数据库：http://localhost:8082"
echo ""
echo "📖 API 文档："
echo "   http://localhost:8000/docs"
echo "   http://localhost:8081/docs"
echo "   http://localhost:8082/docs"
echo ""
echo "🛑 停止服务："
echo "   kill $ROBOT_PID $DRONE_PID $CLINICAL_PID"
echo ""
