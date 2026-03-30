# ⚡ ngrok 快速配置 - 5 分钟上线

## 🎯 目标
将本地 API 暴露到公开网络，让 AI 智能体和外部应用可以访问

---

## 📝 3 步配置

### 步骤 1: 获取 ngrok Token（2 分钟）

```
1. 访问：https://dashboard.ngrok.com/signup
2. 注册免费账号
3. 复制 Auth Token：https://dashboard.ngrok.com/get-started/your-authtoken
```

### 步骤 2: 配置 Token（1 分钟）

```bash
# 运行命令（替换 YOUR_TOKEN 为你的实际 token）
ngrok config add-authtoken YOUR_TOKEN
```

### 步骤 3: 启动隧道（1 分钟）

```bash
# 启动 ngrok
bash /home/admin/.openclaw/workspace/api/start_ngrok.sh
```

**完成！** 你会看到类似输出：
```
🌐 公网地址：https://abc123.ngrok-free.app
```

---

## 🧪 立即测试

### 从浏览器访问
```
https://YOUR_SUBDOMAIN.ngrok-free.app/docs
```

### 从命令行测试
```bash
# 替换 YOUR_SUBDOMAIN 为你的实际域名
curl https://YOUR_SUBDOMAIN.ngrok-free.app/health
curl https://YOUR_SUBDOMAIN.ngrok-free.app/api/stats -H "X-API-Key: sk_robot_demo_key_123456"
```

### AI 智能体调用
```python
API_BASE = "https://YOUR_SUBDOMAIN.ngrok-free.app"
API_KEY = "sk_robot_demo_key_123456"
```

---

## 📋 常用命令速查

```bash
# 启动
bash /workspace/api/start_ngrok.sh

# 停止
kill $(cat /workspace/logs/ngrok.pid)

# 查看状态
ps aux | grep ngrok

# 查看日志
tail -f /workspace/logs/ngrok.log

# Web 界面
浏览器访问：http://127.0.0.1:4040
```

---

## ⚠️ 重要提示

| 项目 | 说明 |
|------|------|
| **域名变更** | 每次重启 ngrok 会变更域名 |
| **免费限制** | 免费版带宽有限，适合测试 |
| **安全性** | 使用 API Key 认证，已配置限流 |
| **有效期** | 隧道在 ngrok 进程停止后失效 |

---

## 🆘 遇到问题？

### 问题：未检测到 token
```bash
# 解决：
ngrok config add-authtoken YOUR_TOKEN
```

### 问题：API 服务未运行
```bash
# 解决：
bash /workspace/api/start_api.sh
```

### 问题：无法访问
```bash
# 检查：
curl http://localhost:8000/health
ps aux | grep ngrok
```

---

## 📚 详细文档

查看 `/workspace/api/NGROK_SETUP.md` 获取完整指南

---

*配置时间：5 分钟*  
*有效期：ngrok 运行期间*
