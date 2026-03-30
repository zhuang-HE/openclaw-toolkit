#!/bin/bash
# ngrok 配置测试脚本

echo "========================================="
echo "🧪 ngrok 配置测试"
echo "========================================="
echo ""

# 检查 1: ngrok 是否安装
echo "【检查 1】ngrok 安装状态..."
if command -v ngrok &> /dev/null; then
    ngrok version
    echo "✅ ngrok 已安装"
else
    echo "❌ ngrok 未安装"
    exit 1
fi
echo ""

# 检查 2: Token 是否配置
echo "【检查 2】Token 配置状态..."
if [ -f ~/.config/ngrok/ngrok.yml ]; then
    echo "✅ Token 配置文件存在"
    if grep -q "authtoken" ~/.config/ngrok/ngrok.yml; then
        echo "✅ Token 已配置"
    else
        echo "❌ Token 未配置"
        echo ""
        echo "请运行：ngrok config add-authtoken YOUR_TOKEN"
        exit 1
    fi
else
    echo "❌ Token 配置文件不存在"
    echo ""
    echo "请运行：ngrok config add-authtoken YOUR_TOKEN"
    exit 1
fi
echo ""

# 检查 3: API 服务是否运行
echo "【检查 3】API 服务状态..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ API 服务运行中"
    curl -s http://localhost:8000/health | python3 -m json.tool
else
    echo "⚠️  API 服务未运行，正在启动..."
    cd /home/admin/.openclaw/workspace/api
    nohup python3 robot_api_server.py > /home/admin/.openclaw/workspace/logs/api.log 2>&1 &
    sleep 3
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ API 服务已启动"
    else
        echo "❌ API 服务启动失败"
        exit 1
    fi
fi
echo ""

# 检查 4: 启动 ngrok 隧道
echo "【检查 4】启动 ngrok 隧道..."

# 停止旧的 ngrok 进程
if [ -f /home/admin/.openclaw/workspace/logs/ngrok.pid ]; then
    OLD_PID=$(cat /home/admin/.openclaw/workspace/logs/ngrok.pid)
    if ps -p $OLD_PID > /dev/null; then
        echo "停止旧的 ngrok 进程 (PID: $OLD_PID)"
        kill $OLD_PID
        sleep 2
    fi
fi

# 启动新的 ngrok
echo "启动 ngrok 隧道..."
nohup ngrok http 8000 --log=/home/admin/.openclaw/workspace/logs/ngrok.log > /home/admin/.openclaw/workspace/logs/ngrok_stdout.log 2>&1 &
NGROK_PID=$!
echo $NGROK_PID > /home/admin/.openclaw/workspace/logs/ngrok.pid
echo "✅ ngrok 已启动 (PID: $NGROK_PID)"
echo ""

# 等待隧道建立
echo "等待隧道建立（10 秒）..."
sleep 10

# 检查 5: 获取隧道信息
echo ""
echo "【检查 5】获取隧道信息..."
echo ""

# 尝试从日志获取公网 URL
PUBLIC_URL=""
for i in {1..5}; do
    if [ -f /home/admin/.openclaw/workspace/logs/ngrok.log ]; then
        PUBLIC_URL=$(grep -o 'https://[a-zA-Z0-9.-]*.ngrok-free.app' /home/admin/.openclaw/workspace/logs/ngrok.log | head -1)
        if [ -n "$PUBLIC_URL" ]; then
            break
        fi
    fi
    sleep 2
done

if [ -n "$PUBLIC_URL" ]; then
    echo "✅ 隧道建立成功"
    echo ""
    echo "========================================="
    echo "🌐 公网访问地址"
    echo "========================================="
    echo ""
    echo "主地址：$PUBLIC_URL"
    echo "API 文档：$PUBLIC_URL/docs"
    echo "管理界面：http://127.0.0.1:4040"
    echo ""
else
    echo "⚠️  未能自动获取公网 URL"
    echo "请查看：http://127.0.0.1:4040"
    echo "或查看日志：tail -f /home/admin/.openclaw/workspace/logs/ngrok.log"
fi
echo ""

# 检查 6: 测试公网访问
echo "【检查 6】测试公网访问..."
echo ""

if [ -n "$PUBLIC_URL" ]; then
    echo "测试健康检查..."
    HEALTH_RESPONSE=$(curl -s "$PUBLIC_URL/health" 2>&1)
    if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
        echo "✅ 公网访问正常"
        echo ""
        echo "响应内容:"
        echo "$HEALTH_RESPONSE" | python3 -m json.tool
    else
        echo "❌ 公网访问失败"
        echo "响应：$HEALTH_RESPONSE"
    fi
    echo ""
    
    echo "测试 API 统计端点..."
    STATS_RESPONSE=$(curl -s "$PUBLIC_URL/api/stats" -H "X-API-Key: sk_robot_demo_key_123456" 2>&1)
    if echo "$STATS_RESPONSE" | grep -q "success"; then
        echo "✅ API 调用成功"
        echo ""
        echo "响应内容:"
        echo "$STATS_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d['data'], indent=2, ensure_ascii=False))" 2>/dev/null || echo "$STATS_RESPONSE"
    else
        echo "❌ API 调用失败"
        echo "响应：$STATS_RESPONSE"
    fi
    echo ""
    
    echo "测试搜索功能..."
    SEARCH_RESPONSE=$(curl -s "$PUBLIC_URL/api/robots/search?q=人形&page_size=3" -H "X-API-Key: sk_robot_demo_key_123456" 2>&1)
    if echo "$SEARCH_RESPONSE" | grep -q "success"; then
        echo "✅ 搜索功能正常"
        echo ""
        SEARCH_DATA=$(echo "$SEARCH_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"找到 {d['data']['total']} 个结果\")" 2>/dev/null)
        echo "$SEARCH_DATA"
    else
        echo "❌ 搜索功能失败"
        echo "响应：$SEARCH_RESPONSE"
    fi
fi
echo ""

# 总结
echo "========================================="
echo "📊 测试总结"
echo "========================================="
echo ""
echo "ngrok 版本：$(ngrok version)"
echo "ngrok 进程：$NGROK_PID"
echo "API 状态：运行中"
echo "隧道状态：$([ -n "$PUBLIC_URL" ] && echo "已建立" || echo "未建立")"
echo "公网访问：$([ -n "$PUBLIC_URL" ] && echo "✅ 正常" || echo "❌ 失败")"
echo ""

if [ -n "$PUBLIC_URL" ]; then
    echo "========================================="
    echo "🎉 配置成功！"
    echo "========================================="
    echo ""
    echo "你的公开 API 地址："
    echo "  $PUBLIC_URL"
    echo ""
    echo "API 文档："
    echo "  $PUBLIC_URL/docs"
    echo ""
    echo "使用示例："
    echo "  curl $PUBLIC_URL/api/stats -H 'X-API-Key: sk_robot_demo_key_123456'"
    echo ""
    echo "管理界面："
    echo "  http://127.0.0.1:4040"
    echo ""
    echo "停止服务："
    echo "  kill $NGROK_PID"
    echo ""
else
    echo "⚠️  配置未完成"
    echo ""
    echo "请检查："
    echo "1. ngrok token 是否正确配置"
    echo "2. 网络连接是否正常"
    echo "3. 查看日志：tail -f /home/admin/.openclaw/workspace/logs/ngrok.log"
fi
echo ""
