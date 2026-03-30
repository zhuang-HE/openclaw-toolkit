#!/bin/bash
# API 服务快速测试脚本

API_BASE="http://localhost:8000"
API_KEY="sk_robot_demo_key_123456"

echo "========================================="
echo "🤖 机器人数据库 API - 快速测试"
echo "========================================="
echo ""

# 1. 健康检查
echo "【1】健康检查..."
curl -s "$API_BASE/health" | python3 -m json.tool
echo ""

# 2. 获取统计
echo "【2】获取统计数据..."
curl -s "$API_BASE/api/stats" -H "X-API-Key: $API_KEY" | python3 -c "import sys,json; d=json.load(sys.stdin); print('总机器人:', d['data']['total_robots']); print('总公司:', d['data']['total_companies']); print('价格范围:', d['data']['price_stats']['min'], '-', d['data']['price_stats']['max'], '元')"
echo ""

# 3. 搜索测试
echo "【3】搜索人形机器人..."
curl -s "$API_BASE/api/robots/search?q=人形&page_size=3" -H "X-API-Key: $API_KEY" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"找到 {d['data']['total']} 个结果，显示前 3 个:\"); [print(f\"  - {r['型号']}: {r['价格 (元)']} 元\") for r in d['data']['data']]"
echo ""

# 4. 公司列表
echo "【4】获取公司列表（前 5 个）..."
curl -s "$API_BASE/api/companies" -H "X-API-Key: $API_KEY" | python3 -c "import sys,json; d=json.load(sys.stdin); [print(f\"  - {c['公司全称']}: {c['产品数量']} 款产品\") for c in d['data'][:5]]"
echo ""

# 5. 事故统计
echo "【5】事故统计..."
curl -s "$API_BASE/api/accidents/stats" -H "X-API-Key: $API_KEY" | python3 -c "import sys,json; d=json.load(sys.stdin); print('总事故:', d['data']['total']); print('伤亡:', d['data']['casualties']); print('损失:', d['data']['total_loss'], '元')"
echo ""

echo "========================================="
echo "✅ 测试完成！"
echo ""
echo "📚 API 文档：$API_BASE/docs"
echo "🔑 API Key: $API_KEY"
echo "========================================="
