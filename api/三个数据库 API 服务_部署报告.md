# 🚀 三个数据库 API 服务 - 部署完成报告

**部署时间**: 2026-04-02  
**部署状态**: ✅ 全部完成

---

## 📊 服务总览

| 数据库 | 端口 | 状态 | 文档 | 数据量 |
|--------|------|------|------|--------|
| **🤖 机器人数据库** | 8000 | ✅ 运行中 | `/docs` | 24 款产品 |
| **🛸 无人机数据库** | 8081 | ✅ 运行中 | `/docs` | 17 款机型 |
| **🏥 临床试验数据库** | 8082 | ✅ 运行中 | `/docs` | 10 例事故 |

---

## 🌐 访问地址

### 机器人数据库 API
- **基础 URL**: `http://localhost:8000`
- **API 文档**: `http://localhost:8000/docs`
- **健康检查**: `http://localhost:8000/health`

### 无人机数据库 API
- **基础 URL**: `http://localhost:8081`
- **API 文档**: `http://localhost:8081/docs`
- **健康检查**: `http://localhost:8081/health`

### 临床试验数据库 API
- **基础 URL**: `http://localhost:8082`
- **API 文档**: `http://localhost:8082/docs`
- **健康检查**: `http://localhost:8082/health`

---

## 🔑 API Keys

### 机器人数据库
```
sk_robot_demo_key_123456    # 测试/演示
sk_robot_ai_agent_001       # AI 智能体
```

### 无人机数据库
```
sk_drone_demo_key_123456    # 测试/演示
sk_drone_ai_agent_001       # AI 智能体
```

### 临床试验数据库
```
sk_clinical_demo_key_123456  # 测试/演示
sk_clinical_ai_agent_001     # AI 智能体
```

---

## 📡 API 端点

### 机器人数据库端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `GET /` | - | API 信息 |
| `GET /health` | - | 健康检查 |
| `GET /api/stats` | 🔑 | 统计数据 |
| `GET /api/robots` | 🔑 | 机器人列表（分页） |
| `GET /api/robots/search` | 🔑 | 搜索机器人 |
| `GET /api/companies` | 🔑 | 公司列表 |
| `GET /api/accidents/stats` | 🔑 | 事故统计 |

### 无人机数据库端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `GET /` | - | API 信息 |
| `GET /health` | - | 健康检查 |
| `GET /api/stats` | 🔑 | 统计数据 |
| `GET /api/drones` | 🔑 | 无人机列表（分页） |
| `GET /api/drones/search` | 🔑 | 搜索无人机 |
| `GET /api/brands` | 🔑 | 品牌列表 |
| `GET /api/accidents/stats` | 🔑 | 事故统计 |

### 临床试验数据库端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `GET /` | - | API 信息 |
| `GET /health` | - | 健康检查 |
| `GET /api/stats` | 🔑 | 统计数据 |
| `GET /api/accidents` | 🔑 | 事故案例（分页） |
| `GET /api/accidents/search` | 🔑 | 搜索事故案例 |
| `GET /api/rates` | 🔑 | 保险费率数据 |
| `GET /api/phase/stats` | 🔑 | 分期统计 |

🔑 = 需要 API Key 认证

---

## 💻 使用示例

### Python 示例

```python
import requests

# 机器人数据库
ROBOT_API = "http://localhost:8000"
ROBOT_KEY = "sk_robot_demo_key_123456"

# 获取统计
response = requests.get(f"{ROBOT_API}/api/stats", headers={"X-API-Key": ROBOT_KEY})
data = response.json()
print(f"机器人总数：{data['data']['total_robots']}")

# 搜索
response = requests.get(
    f"{ROBOT_API}/api/robots/search",
    headers={"X-API-Key": ROBOT_KEY},
    params={"q": "人形", "price_max": 300000}
)
robots = response.json()['data']['data']
for robot in robots:
    print(f"型号：{robot['型号']}, 价格：{robot['价格 (元)']}")


# 无人机数据库
DRONE_API = "http://localhost:8081"
DRONE_KEY = "sk_drone_demo_key_123456"

response = requests.get(f"{DRONE_API}/api/stats", headers={"X-API-Key": DRONE_KEY})
data = response.json()
print(f"无人机总数：{data['data']['total_drones']}")
print(f"事故总数：{data['data']['accident_stats']['total_accidents']}")


# 临床试验数据库
CLINICAL_API = "http://localhost:8082"
CLINICAL_KEY = "sk_clinical_demo_key_123456"

response = requests.get(f"{CLINICAL_API}/api/stats", headers={"X-API-Key": CLINICAL_KEY})
data = response.json()
print(f"事故案例总数：{data['data']['total_accidents']}")
```

### cURL 示例

```bash
# 机器人数据库
curl "http://localhost:8000/api/stats" \
  -H "X-API-Key: sk_robot_demo_key_123456"

# 无人机数据库 - 搜索大疆无人机
curl "http://localhost:8081/api/drones/search?q=大疆" \
  -H "X-API-Key: sk_drone_demo_key_123456"

# 临床试验数据库 - 获取事故案例
curl "http://localhost:8082/api/accidents?page=1&page_size=10" \
  -H "X-API-Key: sk_clinical_demo_key_123456"
```

---

## 🛠️ 运维管理

### 启动所有 API 服务

```bash
cd /home/admin/.openclaw/workspace/api
bash start_all_apis.sh
```

### 单独启动服务

```bash
# 机器人数据库
nohup python3 /home/admin/.openclaw/workspace/api/robot_api_server.py > /home/admin/.openclaw/workspace/logs/robot_api.log 2>&1 &

# 无人机数据库
nohup python3 /home/admin/.openclaw/workspace/api/drone_api_server.py > /home/admin/.openclaw/workspace/logs/drone_api.log 2>&1 &

# 临床试验数据库
nohup python3 /home/admin/.openclaw/workspace/api/clinical_trial_api_server.py > /home/admin/.openclaw/workspace/logs/clinical_api.log 2>&1 &
```

### 查看进程

```bash
ps aux | grep -E "robot_api|drone_api|clinical_api" | grep -v grep
```

### 查看端口

```bash
netstat -tlnp | grep -E "8000|8081|8082"
```

### 查看日志

```bash
# 实时日志
tail -f /home/admin/.openclaw/workspace/logs/robot_api.log
tail -f /home/admin/.openclaw/workspace/logs/drone_api.log
tail -f /home/admin/.openclaw/workspace/logs/clinical_api.log

# 错误日志
tail -f /home/admin/.openclaw/workspace/logs/robot_api_error.log
tail -f /home/admin/.openclaw/workspace/logs/drone_api_error.log
tail -f /home/admin/.openclaw/workspace/logs/clinical_api_error.log
```

### 停止服务

```bash
pkill -f robot_api_server.py
pkill -f drone_api_server.py
pkill -f clinical_trial_api_server.py
```

---

## 📦 文件清单

### API 服务器代码
```
/home/admin/.openclaw/workspace/api/
├── robot_api_server.py           # 机器人数据库 API
├── drone_api_server.py           # 无人机数据库 API (新增)
├── clinical_trial_api_server.py  # 临床试验数据库 API (新增)
├── start_all_apis.sh             # 统一启动脚本 (新增)
├── robot-api.service             # systemd 服务配置
├── drone-api.service             # systemd 服务配置 (新增)
├── clinical-api.service          # systemd 服务配置 (新增)
├── api_keys.json                 # API 密钥配置
└── README_API.md                 # API 文档
```

### 日志文件
```
/home/admin/.openclaw/workspace/logs/
├── robot_api.log
├── robot_api_error.log
├── drone_api.log                 # 新增
├── drone_api_error.log           # 新增
├── clinical_api.log              # 新增
└── clinical_api_error.log        # 新增
```

### 数据库文件
```
/home/admin/.openclaw/workspace/
├── 机器人数据库_核心版.csv
├── 无人机 BI 数据库_核心版.csv
└── clinical_trial_data/
    ├── 临床试验事故案例库.csv
    └── 保险费率历史趋势.csv
```

---

## 🔧 特性

### 通用特性
- ✅ RESTful API 设计
- ✅ API Key 认证
- ✅ 请求限流（60 次/分钟）
- ✅ CORS 支持
- ✅ 数据缓存（60 秒 TTL）
- ✅ 分页支持
- ✅ 模糊搜索
- ✅ Swagger/OpenAPI 文档
- ✅ 健康检查端点
- ✅ 错误处理

### 数据特性
- 🤖 **机器人数据库**: 24 款产品，2 家公司，事故统计
- 🛸 **无人机数据库**: 17 款机型，7 个品牌，销量/事故数据
- 🏥 **临床试验数据库**: 10 例事故，保险费率，分期统计

---

## 📊 测试验证

### 健康检查
```bash
$ curl http://localhost:8000/health
{"status":"healthy","database":"loaded"} ✅

$ curl http://localhost:8081/health
{"status":"healthy","database":"loaded"} ✅

$ curl http://localhost:8082/health
{"status":"healthy","database":"loaded"} ✅
```

### 统计 API
```bash
# 机器人
$ curl "http://localhost:8000/api/stats" -H "X-API-Key: sk_robot_demo_key_123456"
{"success":true,"data":{"total_robots":24,...}} ✅

# 无人机
$ curl "http://localhost:8081/api/stats" -H "X-API-Key: sk_drone_demo_key_123456"
{"success":true,"data":{"total_drones":17,...}} ✅

# 临床试验
$ curl "http://localhost:8082/api/stats" -H "X-API-Key: sk_clinical_demo_key_123456"
{"success":true,"data":{"total_accidents":10,...}} ✅
```

---

## ⚠️ 注意事项

1. **API Key 安全**: 生产环境请修改默认 API Key
2. **端口占用**: 确保 8000/8081/8082 端口未被占用
3. **日志管理**: 建议配置 logrotate 防止日志过大
4. **数据更新**: 数据收集脚本运行后，API 会自动加载最新数据（缓存 60 秒）
5. **防火墙**: 如需外网访问，请配置防火墙规则

---

## 🎯 下一步建议

- [ ] 配置 HTTPS（Nginx 反向代理）
- [ ] 添加监控告警（Prometheus + Grafana）
- [ ] 配置日志轮转（logrotate）
- [ ] 添加 API 调用统计
- [ ] 实现 systemd 服务开机自启
- [ ] 添加数据更新 webhook 通知

---

**部署完成时间**: 2026-04-02 00:03  
**服务状态**: ✅ 全部运行中  
**API 文档**: 可访问各端口的 `/docs` 端点查看

*三个数据库 API 服务已就绪，可以进行对接！*
