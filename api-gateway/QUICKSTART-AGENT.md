# ⚙️ 智能体集成配置清单

## 📋 快速配置（5 分钟）

### Step 1: 创建 API Key ✅

访问密钥管理表：https://xcnt0p90gry4.feishu.cn/base/XC2nbCyx3acaPls7bsRcVOBnnOh

添加新记录：
```
API Key:          sk_agent_[自动生成]
调用方名称：       我的智能体
权限级别：        read
状态：            启用
请求次数限制：    10000
过期时间：        2027-12-31
备注：            智能体专用密钥
```

### Step 2: 配置环境变量 ✅

```bash
# .env 文件
ROBOT_API_URL=https://api.yourdomain.com
ROBOT_API_KEY=sk_agent_xxxxxxxxxxxxx
ROBOT_API_TIMEOUT=5000
```

### Step 3: 安装客户端 ✅

```bash
# 复制客户端代码
cp api-gateway/agent-client.js your-project/

# 或使用 npm（待发布）
npm install @robot-db/client
```

### Step 4: 集成代码 ✅

```javascript
import { RobotApiClient } from './agent-client.js';

const client = new RobotApiClient('sk_agent_xxxxx', {
  baseUrl: 'https://api.yourdomain.com'
});

// 搜索机器人
const result = await client.searchBots({ q: '翻译' });
console.log(result.data);
```

### Step 5: 测试 ✅

```bash
# 测试连接
curl https://api.yourdomain.com/health

# 测试搜索
curl https://api.yourdomain.com/api/v1/bots?q=test \
  -H "X-API-Key: sk_agent_xxxxx"
```

---

## 🎯 按平台配置

### LangChain

```bash
# 1. 安装依赖
npm install langchain @langchain/core

# 2. 复制示例代码
cp api-gateway/examples/langchain-agent.js your-project/

# 3. 运行测试
node langchain-agent.js
```

### Dify

1. 登录 Dify 控制台
2. 工具 → 创建工具 → API 工具
3. 按 `AGENT-INTEGRATION.md` 配置
4. 在编排中添加工具节点

### AutoGen (Python)

```bash
# 1. 安装依赖
pip install requests autogen

# 2. 复制示例
cp api-gateway/examples/autogen-agent.py your-project/

# 3. 配置环境变量
export ROBOT_API_URL=...
export ROBOT_API_KEY=...
```

### Coze/扣子

1. 插件 → 创建插件
2. 添加 API 端点
3. 配置认证 Header
4. 在 Bot 中启用插件

---

## 🔧 常见问题排查

### ❌ 401 Unauthorized

```bash
# 检查 API Key
echo $ROBOT_API_KEY

# 验证密钥状态
# 访问密钥管理表确认状态为"启用"
```

### ❌ 429 Too Many Requests

```javascript
// 增加缓存
const client = new RobotApiClient(apiKey, {
  cacheTTL: 120000, // 2 分钟
});

// 降低请求频率
// 或联系管理员提升限额
```

### ❌ 超时

```javascript
// 增加超时时间
const client = new RobotApiClient(apiKey, {
  timeout: 10000, // 10 秒
});

// 添加重试
// 使用 createAgentClient 自动包含重试逻辑
```

---

## 📊 监控与维护

### 查看使用量

```bash
curl https://api.yourdomain.com/api/v1/metrics?action=stats \
  -H "X-API-Key: sk_admin_xxxxx"
```

### 设置告警

1. 配置飞书 Webhook
2. 在 Cloudflare 设置告警规则
3. 错误率 > 5% 时通知

### 定期维护

- [ ] 每月检查 API Key 使用量
- [ ] 每季度轮换密钥
- [ ] 监控错误日志
- [ ] 更新缓存策略

---

## 🚀 优化建议

### 性能优化

1. **启用缓存** - 减少重复请求
2. **批量查询** - 合并多个请求
3. **预加载** - 提前加载热门数据
4. **CDN** - 使用 Cloudflare 边缘缓存

### 安全加固

1. **最小权限** - 只给 read 权限
2. **独立密钥** - 每个智能体独立 Key
3. **IP 白名单** - 限制来源 IP
4. **密钥轮换** - 定期更换

### 成本控制

| 优化项 | 预期节省 |
|--------|----------|
| 缓存热门查询 | 40-60% |
| 批量请求 | 20-30% |
| 合理限流 | 避免超额 |

---

## 📚 相关文档

- [API 网关代码](./worker.js)
- [客户端库](./agent-client.js)
- [集成指南](./AGENT-INTEGRATION.md)
- [监控配置](./monitoring-guide.md)
- [部署指南](./README.md)

---

## 💬 获取帮助

遇到问题？

1. 查看错误日志
2. 检查文档
3. 联系管理员
4. 提交 Issue

---

**配置完成后，你的智能体就可以安全、高效地调用机器人数据库了！** 🎉
