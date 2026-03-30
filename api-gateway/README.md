# 🚀 部署指南

## 前置准备

### 1. 安装 Node.js 和 Wrangler
```bash
# 安装 Node.js (v18+)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 Wrangler CLI
npm install -g wrangler
```

### 2. 登录 Cloudflare
```bash
wrangler login
```

### 3. 创建 KV 命名空间
```bash
# 创建 token 缓存 KV
wrangler kv:namespace create "FEISHU_TOKEN_CACHE"

# 创建速率限制 KV
wrangler kv:namespace create "RATE_LIMIT_KV"
```

将输出的 ID 填入 `wrangler.toml` 对应位置。

### 4. 配置飞书开放平台

1. 访问 https://open.feishu.cn/
2. 创建企业自建应用
3. 获取凭证：
   - App ID
   - App Secret
4. 配置权限：
   - 知识库与文档 → 获取多维表格数据
   - 知识库与文档 → 编辑多维表格数据

### 5. 设置环境变量
```bash
wrangler secret put FEISHU_APP_ID
wrangler secret put FEISHU_APP_SECRET
wrangler secret put FEISHU_ROBOT_BITABLE_TOKEN
wrangler secret put FEISHU_ROBOT_TABLE_ID
```

## 部署

### 测试环境
```bash
wrangler deploy --env staging
```

### 生产环境
```bash
wrangler deploy --env production
```

## 测试 API

### 健康检查
```bash
curl https://api.yourdomain.com/health
```

### 查询机器人列表
```bash
curl https://api.yourdomain.com/api/v1/bots \
  -H "X-API-Key: sk_test_7x9k2m4n8p1q5r3t" \
  -H "Content-Type: application/json"
```

### 带筛选查询
```bash
curl "https://api.yourdomain.com/api/v1/bots?category=效率&limit=10" \
  -H "X-API-Key: sk_test_7x9k2m4n8p1q5r3t"
```

### 创建机器人
```bash
curl -X POST https://api.yourdomain.com/api/v1/bots \
  -H "X-API-Key: sk_test_7x9k2m4n8p1q5r3t" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "新机器人",
    "description": "这是一个新机器人",
    "category": "工具",
    "avatar": "https://example.com/avatar.png"
  }'
```

## 监控与日志

### 查看实时日志
```bash
wrangler tail
```

### 查看部署列表
```bash
wrangler deploy --list
```

### 回滚版本
```bash
wrangler rollback
```

## 安全加固建议

1. **启用 Cloudflare 防护**
   - 在 Cloudflare Dashboard 启用 WAF
   - 配置速率限制规则
   - 启用 DDoS 防护

2. **API Key 管理**
   - 定期轮换密钥
   - 为不同调用方创建独立密钥
   - 设置合理的过期时间

3. **监控告警**
   - 配置 Cloudflare Analytics
   - 设置异常请求告警
   - 监控 API 使用量

## 故障排查

### 常见问题

**Q: 401 Unauthorized**
- 检查 API Key 是否正确
- 确认密钥状态为"启用"
- 检查是否过期

**Q: 429 Too Many Requests**
- 降低请求频率
- 联系管理员提升限额

**Q: 飞书 API 调用失败**
- 检查 App ID/Secret 配置
- 确认权限已授予
- 查看飞书开放平台配额

## 成本估算

| 项目 | 免费额度 | 超出后价格 |
|------|----------|------------|
| Workers 请求 | 10 万/天 | $0.30/百万 |
| KV 读取 | 10 万/天 | $0.063/百万 |
| KV 写入 | 1000/天 | $0.50/百万 |

小型应用完全够用，中大型应用月成本约 $5-20。
