# 📊 监控与告警配置指南

## 概述

监控系统提供以下功能：
- ✅ API 调用日志记录
- ✅ 错误追踪与告警
- ✅ 使用统计分析
- ✅ 健康检查
- ✅ 飞书机器人告警通知

## 配置步骤

### 1. 创建额外的 KV 命名空间

```bash
# API 日志存储
wrangler kv:namespace create "API_LOGS_KV"

# 错误日志存储
wrangler kv:namespace create "ERROR_LOGS_KV"

# 统计数据存储
wrangler kv:namespace create "STATS_KV"
```

将输出的 ID 填入 `wrangler.toml`：

```toml
[[kv_namespaces]]
binding = "API_LOGS_KV"
id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

[[kv_namespaces]]
binding = "ERROR_LOGS_KV"
id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

[[kv_namespaces]]
binding = "STATS_KV"
id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### 2. 配置飞书告警机器人

#### 2.1 创建飞书群机器人

1. 在飞书中创建一个群（如「API 监控告警」）
2. 点击右上角「...」→「群机器人」
3. 点击「添加机器人」→「自定义机器人」
4. 设置机器人名称：API 监控助手
5. 复制 Webhook 地址

#### 2.2 配置 Webhook

```bash
wrangler secret put FEISHU_WEBHOOK_URL
# 粘贴你的 Webhook 地址
# 格式：https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx
```

### 3. 集成监控模块

在 `worker.js` 中导入并使用监控模块：

```javascript
import { createMonitoringMiddleware } from './monitoring';

export default {
  async fetch(request, env, ctx) {
    const monitor = createMonitoringMiddleware(env);
    const context = await monitor.onRequest(request);
    
    try {
      // ... 你的业务逻辑
      const response = await handleRequest(request, env);
      
      await monitor.onResponse(context, response);
      return response;
    } catch (error) {
      await monitor.onError(error, context);
      throw error;
    }
  }
};
```

### 4. 添加监控端点

在 `worker.js` 中添加监控 API：

```javascript
if (path === '/api/v1/metrics' && request.method === 'GET') {
  // 需要 admin 权限的 API Key
  const apiKey = request.headers.get('X-API-Key');
  const validation = await validateApiKey(apiKey, env);
  
  if (!validation.valid || validation.permission !== 'admin') {
    return new Response(JSON.stringify({ error: '需要 admin 权限' }), { status: 403 });
  }
  
  const result = await handleGetMetrics(request, env);
  return new Response(JSON.stringify(result));
}
```

## 监控仪表板

### 查询 API 使用统计

```bash
curl "https://api.yourdomain.com/api/v1/metrics?action=stats&days=7" \
  -H "X-API-Key: sk_admin_xxxxxxxx"
```

响应示例：
```json
{
  "success": true,
  "data": [
    {
      "date": "2026-03-25",
      "apiKey": "sk_test_7x9k2m4n***",
      "permission": "read",
      "totalRequests": 1520,
      "successRequests": 1498,
      "failedRequests": 22,
      "avgDuration": 145
    }
  ]
}
```

### 查看最近错误

```bash
curl "https://api.yourdomain.com/api/v1/metrics?action=recent_errors&limit=10" \
  -H "X-API-Key: sk_admin_xxxxxxxx"
```

### 系统健康检查

```bash
curl "https://api.yourdomain.com/api/v1/metrics?action=health" \
  -H "X-API-Key: sk_admin_xxxxxxxx"
```

响应示例：
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2026-03-25T14:30:00Z",
    "checks": {
      "feishu_api": true,
      "kv_storage": true,
      "rate_limiting": true
    }
  }
}
```

## 告警规则

系统会自动触发告警的场景：

| 告警类型 | 触发条件 | 通知方式 |
|----------|----------|----------|
| 严重错误 | 系统异常、飞书 API 失败 | 飞书机器人 |
| 错误率过高 | 5 分钟内错误率 > 5% | 飞书机器人 |
| 认证失败 | 1 分钟内连续失败 10 次 | 飞书机器人 |
| 响应过慢 | P95 响应时间 > 2 秒 | 日志记录 |

## 自定义告警

在 `monitoring.js` 中调整告警阈值：

```javascript
export const ALERT_RULES = {
  errorRate: {
    threshold: 0.05, // 调整为 3%
    window: 300,
  },
  // ... 其他规则
};
```

## 日志查询

### Cloudflare Dashboard

1. 访问 https://dash.cloudflare.com/
2. 选择你的 Worker
3. 点击「Logs」查看实时日志
4. 使用筛选器查询特定错误

### Wrangler CLI

```bash
# 实时查看日志
wrangler tail

# 查看特定环境的日志
wrangler tail --env production

# 带筛选查看
wrangler tail --status error
```

## 数据保留策略

| 数据类型 | 保留时间 | 存储位置 |
|----------|----------|----------|
| API 日志 | 7 天 | API_LOGS_KV |
| 错误日志 | 30 天 | ERROR_LOGS_KV |
| 统计数据 | 30 天 | STATS_KV |

## 最佳实践

1. **定期检查告警** - 每天查看飞书告警消息
2. **分析错误趋势** - 每周查看统计数据分析趋势
3. **优化慢查询** - 关注 P95 响应时间
4. **容量规划** - 根据使用量调整配额
5. **安全审计** - 定期检查异常 API Key 使用

## 扩展建议

- 集成 Cloudflare Analytics
- 添加自定义监控仪表板（如 Grafana）
- 配置 PagerDuty/Slack 告警
- 实现自动扩缩容

---

**监控是为了更好地服务，不是为了增加焦虑。** 合理配置告警阈值，避免告警疲劳。
