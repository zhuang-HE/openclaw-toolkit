# 🌐 机器人数据库 API - ngrok 公开访问部署说明

**部署时间**: 2026-03-25  
**访问方式**: ngrok 内网穿透  
**状态**: ⏳ 待配置 Token

---

## 📋 当前状态

### ✅ 已完成

| 项目 | 状态 | 说明 |
|------|------|------|
| API 服务 | ✅ 运行中 | http://localhost:8000 |
| ngrok 安装 | ✅ 完成 | v3.37.2 |
| 启动脚本 | ✅ 创建 | start_ngrok.sh |
| 配置文档 | ✅ 完成 | 2 份文档 |

### ⏳ 待配置

| 项目 | 说明 | 紧急度 |
|------|------|--------|
| ngrok Token | 需要注册获取 | ⭐⭐⭐⭐⭐ |
| 启动隧道 | 配置 Token 后执行 | ⭐⭐⭐⭐⭐ |
| 公开测试 | 从外网访问测试 | ⭐⭐⭐⭐ |

---

## 🚀 立即执行（3 步）

### 步骤 1: 获取 Token

```
访问：https://dashboard.ngrok.com/get-started/your-authtoken
复制：你的 Auth Token
```

### 步骤 2: 配置 Token

```bash
# 在终端运行（替换 YOUR_TOKEN）
ngrok config add-authtoken YOUR_TOKEN
```

### 步骤 3: 启动隧道

```bash
bash /home/admin/.openclaw/workspace/api/start_ngrok.sh
```

**完成！** 你会获得一个公网域名，如：
```
https://abc123.ngrok-free.app
```

---

## 📁 创建的文件

```
✅ /workspace/api/start_ngrok.sh (2.4KB) - 自动启动脚本
✅ /workspace/api/NGROK_SETUP.md (4.3KB) - 详细配置指南
✅ /workspace/api/快速配置_NGROK.md (1.7KB) - 快速参考
```

---

## 🧪 测试清单

配置完成后，按顺序测试：

### 1. 本地测试
```bash
curl http://localhost:8000/health
# 应返回：{"status": "healthy", ...}
```

### 2. ngrok 状态
```bash
ps aux | grep ngrok
# 应看到 ngrok 进程
```

### 3. 公网访问
```bash
# 替换 YOUR_SUBDOMAIN
curl https://YOUR_SUBDOMAIN.ngrok-free.app/health
# 应返回：{"status": "healthy", ...}
```

### 4. API 功能
```bash
curl https://YOUR_SUBDOMAIN.ngrok-free.app/api/stats \
  -H "X-API-Key: sk_robot_demo_key_123456"
# 应返回统计数据
```

### 5. 手机/其他设备测试
```
用手机浏览器访问：
https://YOUR_SUBDOMAIN.ngrok-free.app/docs
```

---

## 🔐 安全配置

### 已配置的安全措施

| 措施 | 状态 | 说明 |
|------|------|------|
| API Key 认证 | ✅ 已启用 | 所有端点需要 X-API-Key |
| 限流保护 | ✅ 已配置 | 60 次/分钟 |
| 日志记录 | ✅ 已启用 | 记录所有请求 |
| 只读 API | ✅ 已配置 | 无写入端点 |

### 建议的安全实践

1. **不要公开分享完整 URL**
   - 仅分享给需要的人
   - 定期更换（重启 ngrok）

2. **使用不同的 API Key**
   - 为不同应用分配独立 Key
   - 编辑 `/workspace/api/api_keys.json`

3. **监控请求日志**
   ```bash
   tail -f /workspace/logs/ngrok.log
   ```

4. **及时停止服务**
   ```bash
   # 不使用时停止
   kill $(cat /workspace/logs/ngrok.pid)
   ```

---

## 📊 ngrok 免费版限制

| 项目 | 限制 | 影响 |
|------|------|------|
| 域名 | 每次重启变更 | 需要更新 API 地址 |
| 带宽 | 有限制 | 不适合大量请求 |
| 隧道数 | 1 个 | 只能暴露一个服务 |
| 请求日志 | 7 天 | 足够调试使用 |

---

## 🎯 使用场景

### ✅ 适合

- AI 智能体开发和测试
- 小团队内部使用
- 原型验证
- 临时公开 API

### ❌ 不适合

- 生产环境
- 高并发场景
- 需要固定域名
- 企业级应用

---

## 🔄 下一步计划

### 短期（测试阶段）
- [ ] 配置 ngrok Token
- [ ] 启动隧道
- [ ] 测试公开访问
- [ ] 集成到 AI 智能体

### 中期（1-2 周）
- [ ] 评估使用量
- [ ] 如需稳定域名 → Cloudflare Tunnel
- [ ] 如需高性能 → 云服务器

### 长期（生产环境）
- [ ] 云服务器部署
- [ ] 配置 HTTPS
- [ ] 添加监控系统
- [ ] 完善文档

---

## 📞 快速命令

```bash
# 启动 ngrok
bash /workspace/api/start_ngrok.sh

# 查看隧道信息
cat /workspace/logs/ngrok.log | grep ngrok-free.app

# 停止 ngrok
kill $(cat /workspace/logs/ngrok.pid)

# 重启 API + ngrok
pkill -f robot_api_server
pkill -f ngrok
bash /workspace/api/start_api.sh &
sleep 3
bash /workspace/api/start_ngrok.sh
```

---

## 📚 相关文档

| 文档 | 路径 |
|------|------|
| 快速配置 | `/workspace/api/快速配置_NGROK.md` |
| 详细指南 | `/workspace/api/NGROK_SETUP.md` |
| API 文档 | `/workspace/api/README_API.md` |
| 部署报告 | `/workspace/机器人数据库_API_部署完成报告.md` |

---

## 💡 提示

1. **Token 是敏感信息**，不要分享到公开场合
2. **ngrok 域名会变化**，AI 智能体配置需要更新
3. **定期重启**可以获得新域名（安全考虑）
4. **监控日志**，发现异常及时处理
5. **生产环境**建议迁移到云服务器或 Cloudflare Tunnel

---

**准备就绪！请完成 Token 配置后启动隧道。** 🚀

*更新时间：2026-03-25 15:48*
