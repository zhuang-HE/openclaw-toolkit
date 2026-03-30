# 🚀 ngrok 配置指南

## 快速开始（5 分钟）

### 步骤 1: 注册 ngrok 账号

1. 访问 https://dashboard.ngrok.com/signup
2. 注册免费账号（支持 GitHub/Google 快捷登录）
3. 验证邮箱

### 步骤 2: 获取 Auth Token

1. 登录 https://dashboard.ngrok.com
2. 访问 https://dashboard.ngrok.com/get-started/your-authtoken
3. 复制你的 Auth Token（格式类似：`2aBcDeFgHiJkLmNoPqRsTuVwXyZ123456789`）

### 步骤 3: 配置 Token

```bash
# 运行配置命令
ngrok config add-authtoken YOUR_TOKEN_HERE

# 替换 YOUR_TOKEN_HERE 为你的实际 token
# 示例：
# ngrok config add-authtoken 2aBcDeFgHiJkLmNoPqRsTuVwXyZ123456789
```

### 步骤 4: 启动隧道

```bash
# 方法 A: 使用自动脚本（推荐）
bash /home/admin/.openclaw/workspace/api/start_ngrok.sh

# 方法 B: 手动启动
ngrok http 8000 --log=/home/admin/.openclaw/workspace/logs/ngrok.log
```

### 步骤 5: 获取公网地址

启动后，ngrok 会显示类似信息：

```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:8000
```

你的公网 API 地址就是：`https://abc123.ngrok-free.app`

---

## 📖 使用示例

### 测试 API

```bash
# 健康检查
curl https://YOUR_SUBDOMAIN.ngrok-free.app/health

# 获取统计
curl https://YOUR_SUBDOMAIN.ngrok-free.app/api/stats \
  -H "X-API-Key: sk_robot_demo_key_123456"

# 搜索机器人
curl "https://YOUR_SUBDOMAIN.ngrok-free.app/api/robots/search?q=人形" \
  -H "X-API-Key: sk_robot_demo_key_123456"
```

### AI 智能体调用

```python
import requests

# 替换为你的 ngrok 域名
API_BASE = "https://YOUR_SUBDOMAIN.ngrok-free.app"
API_KEY = "sk_robot_demo_key_123456"

# 搜索
response = requests.get(
    f"{API_BASE}/api/robots/search",
    headers={"X-API-Key": API_KEY},
    params={"q": "人形", "price_max": 300000}
)

robots = response.json()['data']['data']
for robot in robots:
    print(f"{robot['型号']}: {robot['价格 (元)']} 元")
```

---

## 🔧 常用命令

### 启动

```bash
# 自动启动（推荐）
bash /home/admin/.openclaw/workspace/api/start_ngrok.sh

# 手动启动
ngrok http 8000

# 指定域名（需要付费计划）
ngrok http 8000 --domain=robot-api.ngrok.io
```

### 停止

```bash
# 找到进程
ps aux | grep ngrok

# 停止
kill <PID>

# 或使用保存的 PID
kill $(cat /home/admin/.openclaw/workspace/logs/ngrok.pid)
```

### 查看状态

```bash
# 查看进程
ps aux | grep ngrok

# 查看日志
tail -f /home/admin/.openclaw/workspace/logs/ngrok.log

# Web 界面
浏览器访问：http://127.0.0.1:4040
```

---

## 📊 ngrok Web 界面

访问 `http://127.0.0.1:4040` 可以查看：

- ✅ 隧道状态
- ✅ 请求历史
- ✅ 请求/响应详情
- ✅ 流量统计
- ✅ 重放请求（调试用）

---

## ⚠️ 注意事项

### 免费版限制

| 限制 | 免费版 | 付费版 |
|------|--------|--------|
| 域名变更 | 每次重启变更 | 可固定域名 |
| 带宽 | 有限制 | 更高限额 |
| 隧道数量 | 1 个 | 多个 |
| HTTPS | ✅ 支持 | ✅ 支持 |
| 请求日志 | 7 天 | 更长 |

### 安全建议

1. **不要公开分享 ngrok 域名**
   - 免费版域名是公开的，任何人都可能访问
   - 建议仅用于测试和开发

2. **使用 API Key 认证**
   - 所有请求必须包含 `X-API-Key` Header
   - 默认已配置限流（60 次/分钟）

3. **定期更换域名**
   - 重启 ngrok 会获得新域名
   - 旧域名自动失效

4. **监控请求日志**
   - 定期检查 `/home/admin/.openclaw/workspace/logs/ngrok.log`
   - 发现异常请求及时停止服务

---

## 🔐 加固配置（可选）

### 添加 IP 白名单

编辑 `robot_api_server.py`：

```python
class Config:
    ALLOWED_IPS = [
        "1.2.3.4",  # 你的 IP
        "5.6.7.8",  # AI 服务器 IP
    ]
```

### 限制 Referer

```python
@app.middleware("http")
async def check_referer(request, call_next):
    referer = request.headers.get("referer", "")
    if referer and "yourdomain.com" not in referer:
        return JSONResponse(status_code=403, content={"error": "Forbidden"})
    return await call_next(request)
```

### 启用请求日志

```python
import logging

logging.basicConfig(
    filename='/var/log/api_access.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"{request.method} {request.url} - {request.client.host}")
    return await call_next(request)
```

---

## 🎯 下一步

### 测试公开访问

1. **从其他设备测试**
   ```bash
   # 用手机或其他电脑访问
   curl https://YOUR_SUBDOMAIN.ngrok-free.app/health
   ```

2. **配置到 AI 智能体**
   ```python
   API_BASE = "https://YOUR_SUBDOMAIN.ngrok-free.app"
   ```

3. **分享给团队成员**
   - 将 ngrok 域名和 API Key 分享给团队
   - 提醒他们妥善保管

### 生产环境升级

当需要稳定服务时，考虑：

1. **Cloudflare Tunnel**（免费 + 固定域名）
2. **云服务器部署**（完全控制）
3. **Vercel/Render**（自动部署）

---

## 📞 故障排查

### 问题 1: ngrok 启动失败

```bash
# 检查 token 是否配置
ngrok config check

# 重新配置 token
ngrok config add-authtoken YOUR_TOKEN
```

### 问题 2: API 服务未运行

```bash
# 检查 API 状态
curl http://localhost:8000/health

# 启动 API
bash /home/admin/.openclaw/workspace/api/start_api.sh
```

### 问题 3: 无法访问 ngrok 域名

- 检查网络连接
- 确认 ngrok 进程运行
- 查看 ngrok 日志
- 尝试重启 ngrok

---

*文档版本：1.0*  
*更新时间：2026-03-25*
