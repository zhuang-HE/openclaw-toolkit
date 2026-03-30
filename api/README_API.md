# 🤖 机器人数据库 API 文档

## 📋 概述

基于 FastAPI 的机器人数据库 REST API 服务，提供机器人产品数据的查询和搜索接口。

**服务地址**: `http://localhost:8000`  
**API 文档**: `http://localhost:8000/docs`  
**数据文件**: `/workspace/机器人数据库_核心版.csv`（174 条记录）

---

## 🚀 快速开始

### 安装依赖

```bash
cd /home/admin/.openclaw/workspace/api
pip3 install -r requirements.txt --user -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 启动服务

```bash
# 方式 1: 使用启动脚本
bash start_api.sh

# 方式 2: 直接运行
python3 robot_api_server.py
```

### 访问文档

浏览器打开：`http://localhost:8000/docs`

---

## 🔐 认证方式

### API Key 认证

所有 API 端点需要在 Header 中包含 API Key：

```bash
X-API-Key: sk_robot_demo_key_123456
```

### 默认 API Keys

| Key | 名称 | 权限 | 限流 |
|-----|------|------|------|
| `sk_robot_demo_key_123456` | Demo Key | read | 60 次/分钟 |
| `sk_robot_ai_agent_001` | AI Agent Key | read | 100 次/分钟 |

### 添加新 API Key

编辑 `api_keys.json`：

```json
{
  "api_keys": {
    "sk_robot_your_key": {
      "name": "Your App",
      "permission": "read",
      "created_at": "2026-03-25",
      "rate_limit": 60,
      "enabled": true
    }
  }
}
```

---

## 📖 API 端点

### 1. 健康检查

```http
GET /health
```

**响应示例：**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-25T15:30:00",
  "database": "loaded"
}
```

---

### 2. 获取机器人列表

```http
GET /api/robots?page=1&page_size=20
```

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | int | 1 | 页码 |
| page_size | int | 20 | 每页数量（1-100） |

**响应示例：**
```json
{
  "success": true,
  "data": {
    "data": [...],
    "total": 174,
    "page": 1,
    "page_size": 20,
    "total_pages": 9
  }
}
```

---

### 3. 搜索机器人

```http
GET /api/robots/search?q=人形&category=人形机器人&price_min=100000&price_max=500000
```

**参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | 否 | 搜索关键词（公司/型号/用途） |
| category | string | 否 | 类型/分类 |
| company | string | 否 | 公司名称 |
| price_min | number | 否 | 最低价格 |
| price_max | number | 否 | 最高价格 |
| page | int | 否 | 页码 |
| page_size | int | 否 | 每页数量 |

**示例：**
```bash
# 搜索人形机器人
curl "http://localhost:8000/api/robots/search?q=人形" \
  -H "X-API-Key: sk_robot_demo_key_123456"

# 搜索特定价格范围
curl "http://localhost:8000/api/robots/search?price_min=100000&price_max=300000" \
  -H "X-API-Key: sk_robot_demo_key_123456"

# 搜索特定公司
curl "http://localhost:8000/api/robots/search?company=智元" \
  -H "X-API-Key: sk_robot_demo_key_123456"
```

---

### 4. 获取机器人详情

```http
GET /api/robots/{robot_id}
```

**参数：**
- `robot_id`: 机器人型号或公司简称

**示例：**
```bash
# 获取 A2 旗舰版详情
curl "http://localhost:8000/api/robots/A2 旗舰版" \
  -H "X-API-Key: sk_robot_demo_key_123456"

# 获取智元机器人信息
curl "http://localhost:8000/api/robots/智元" \
  -H "X-API-Key: sk_robot_demo_key_123456"
```

**响应示例：**
```json
{
  "success": true,
  "data": {
    "公司全称": "智元创新（上海）科技股份有限公司",
    "公司简称": "智元机器人",
    "品牌": "Agibot",
    "产品系列": "远征 A2",
    "型号": "A2 旗舰版",
    "类型": "人形机器人",
    "价格 (元)": 298000,
    ...
  }
}
```

---

### 5. 获取公司列表

```http
GET /api/companies
```

**响应示例：**
```json
{
  "success": true,
  "data": [
    {
      "公司全称": "智元创新（上海）科技股份有限公司",
      "产品数量": 13,
      "最低价格": 14800,
      "最高价格": 298000,
      "产品类型": ["人形机器人", "四足机器人"]
    }
  ]
}
```

---

### 6. 获取统计数据

```http
GET /api/stats
```

**响应示例：**
```json
{
  "success": true,
  "data": {
    "total_robots": 174,
    "total_companies": 52,
    "type_distribution": {
      "人形机器人": 25,
      "四足机器人": 18,
      "工业机械臂": 30,
      ...
    },
    "price_stats": {
      "min": 1999,
      "max": 15000000,
      "avg": 285000,
      "median": 168000
    },
    "accident_stats": {
      "total_accidents": 72,
      "total_casualties": 26
    }
  }
}
```

---

### 7. 获取事故统计

```http
GET /api/accidents/stats?company=智元&year=2025
```

**参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| company | string | 否 | 公司名称筛选 |
| year | int | 否 | 年份筛选 |

**响应示例：**
```json
{
  "success": true,
  "data": {
    "total": 5,
    "casualties": 2,
    "total_loss": 1250000,
    "data": [...],
    "summary": {
      "by_company": {...},
      "by_type": {...}
    }
  }
}
```

---

## 🔒 安全配置

### 限流配置

默认：**60 次/分钟**

修改 `robot_api_server.py`：
```python
class Config:
    RATE_LIMIT_PER_MINUTE = 60  # 修改此值
```

### CORS 配置

允许跨域访问：
```python
class Config:
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "https://yourdomain.com",
    ]
```

### API Key 管理

- 定期轮换 API Key
- 为不同应用分配独立 Key
- 监控异常请求

---

## 📊 使用示例

### Python 示例

```python
import requests

API_BASE = "http://localhost:8000"
API_KEY = "sk_robot_demo_key_123456"

headers = {"X-API-Key": API_KEY}

# 搜索机器人
response = requests.get(
    f"{API_BASE}/api/robots/search",
    headers=headers,
    params={"q": "人形", "price_max": 500000}
)

data = response.json()
print(f"找到 {data['data']['total']} 个机器人")

# 获取详情
response = requests.get(
    f"{API_BASE}/api/robots/A2 旗舰版",
    headers=headers
)

robot = response.json()['data']
print(f"价格：{robot['价格 (元)']} 元")
```

### JavaScript 示例

```javascript
const API_BASE = 'http://localhost:8000';
const API_KEY = 'sk_robot_demo_key_123456';

// 搜索机器人
async function searchRobots(query) {
  const response = await fetch(
    `${API_BASE}/api/robots/search?q=${query}`,
    {
      headers: { 'X-API-Key': API_KEY }
    }
  );
  const data = await response.json();
  return data.data;
}

// 使用
searchRobots('人形').then(result => {
  console.log(`找到 ${result.total} 个机器人`);
});
```

### cURL 示例

```bash
# 搜索
curl "http://localhost:8000/api/robots/search?q=人形" \
  -H "X-API-Key: sk_robot_demo_key_123456"

# 统计
curl "http://localhost:8000/api/stats" \
  -H "X-API-Key: sk_robot_demo_key_123456"

# 公司列表
curl "http://localhost:8000/api/companies" \
  -H "X-API-Key: sk_robot_demo_key_123456"
```

---

## 🛠️ 运维

### 查看日志

```bash
tail -f /home/admin/.openclaw/workspace/logs/api.log
```

### 后台运行

```bash
# 使用 nohup
nohup python3 robot_api_server.py > /workspace/logs/api.log 2>&1 &

# 使用 screen
screen -S robot_api
python3 robot_api_server.py
# Ctrl+A, D 分离
```

### 重启服务

```bash
# 找到进程
ps aux | grep robot_api_server

# 杀死进程
kill <PID>

# 重新启动
python3 robot_api_server.py
```

---

## 📈 性能优化

### 缓存策略

- 数据缓存：60 秒
- 可调整 `cache_ttl` 参数

### 数据库优化

- 当前：CSV + Pandas
- 未来可迁移到 SQLite/PostgreSQL

### 限流优化

- 当前：内存计数
- 未来可使用 Redis

---

## 🎯 AI 智能体集成

### LangChain Tool

```python
from langchain.tools import tool
import requests

@tool
def search_robot_database(query: str, category: str = None):
    """搜索机器人数据库"""
    response = requests.get(
        "http://localhost:8000/api/robots/search",
        headers={"X-API-Key": "sk_robot_ai_agent_001"},
        params={"q": query, "category": category}
    )
    return response.json()
```

### 自然语言查询

AI 智能体可以这样使用：

```
用户：帮我找个 50 万以下的人形机器人
AI: （调用 API）
    找到 15 个符合条件的人形机器人：
    1. 智元灵犀 X2 旗舰版 - 158,000 元
    2. 宇树 G1 - 198,000 元
    3. ...
```

---

## 📝 错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 401 | 未授权（缺少/无效 API Key） |
| 404 | 未找到 |
| 429 | 请求频率超限 |
| 500 | 服务器错误 |

---

*文档版本：1.0*  
*更新时间：2026-03-25*
