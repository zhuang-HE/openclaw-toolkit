#!/bin/bash
# ngrok 快速启动脚本

echo "========================================="
echo "🚀 ngrok 隧道启动脚本"
echo "========================================="
echo ""

# 检查是否已配置 token
if ! grep -q "authtoken" ~/.config/ngrok/ngrok.yml 2>/dev/null; then
    echo "❌ 未检测到 ngrok 认证 token"
    echo ""
    echo "请先配置 token："
    echo "1. 访问 https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "2. 复制你的 Auth Token"
    echo "3. 运行：ngrok config add-authtoken YOUR_TOKEN"
    echo ""
    echo "配置完成后重新运行此脚本"
    exit 1
fi

echo "✅ ngrok 已配置"
echo ""

# 检查 API 服务是否运行
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "⚠️  检测到 API 服务未运行，正在启动..."
    cd /home/admin/.openclaw/workspace/api
    nohup python3 robot_api_server.py > /home/admin/.openclaw/workspace/logs/api.log 2>&1 &
    sleep 3
fi

echo "✅ API 服务运行中"
echo ""

# 启动 ngrok
echo "正在启动 ngrok 隧道..."
echo "目标地址：http://localhost:8000"
echo ""

# 后台启动 ngrok
nohup ngrok http 8000 --log=/home/admin/.openclaw/workspace/logs/ngrok.log > /home/admin/.openclaw/workspace/logs/ngrok_stdout.log 2>&1 &
NGROK_PID=$!

echo "✅ ngrok 已启动（PID: $NGROK_PID）"
echo ""

# 等待 5 秒获取隧道信息
echo "正在获取隧道信息..."
sleep 5

# 尝试获取公网 URL
echo ""
echo "========================================="
echo "📡 隧道信息"
echo "========================================="
echo ""

# 方法 1: 从日志获取
if [ -f /home/admin/.openclaw/workspace/logs/ngrok.log ]; then
    PUBLIC_URL=$(grep -o 'https://[a-zA-Z0-9.-]*.ngrok-free.app' /home/admin/.openclaw/workspace/logs/ngrok.log | head -1)
    if [ -n "$PUBLIC_URL" ]; then
        echo "🌐 公网地址：$PUBLIC_URL"
        echo ""
        echo "📖 API 文档：$PUBLIC_URL/docs"
        echo ""
        echo "🧪 测试命令："
        echo "curl $PUBLIC_URL/health"
        echo "curl $PUBLIC_URL/api/stats -H 'X-API-Key: sk_robot_demo_key_123456'"
        echo ""
    fi
fi

# 方法 2: 从 ngrok API 获取
echo "备用方法：查看实时隧道信息"
echo "访问：http://127.0.0.1:4040"
echo ""

echo "========================================="
echo "💡 提示信息"
echo "========================================="
echo ""
echo "1. 查看 ngrok 状态：ps aux | grep ngrok"
echo "2. 查看 ngrok 日志：tail -f /home/admin/.openclaw/workspace/logs/ngrok.log"
echo "3. 停止 ngrok: kill $NGROK_PID"
echo "4. Web 界面：http://127.0.0.1:4040"
echo ""
echo "⚠️  注意：ngrok 免费版每次重启会变更域名"
echo ""

# 保存 PID
echo $NGROK_PID > /home/admin/.openclaw/workspace/logs/ngrok.pid
echo "✅ PID 已保存：/home/admin/.openclaw/workspace/logs/ngrok.pid"
