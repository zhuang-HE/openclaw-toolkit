// 监控与日志模块 - 可集成到 worker.js
// 提供 API 调用监控、异常告警、使用统计

// ==================== 日志记录 ====================

// 记录 API 调用
async function logApiCall(env, logData) {
  const log = {
    timestamp: new Date().toISOString(),
    apiKey: logData.apiKey?.substring(0, 8) + '***', // 脱敏
    method: logData.method,
    path: logData.path,
    statusCode: logData.statusCode,
    duration: logData.duration,
    ip: logData.ip,
    userAgent: logData.userAgent,
  };
  
  // 写入 KV 存储（用于分析）
  const logKey = `api_log:${Date.now()}:${Math.random().toString(36).substring(7)}`;
  await env.API_LOGS_KV.put(logKey, JSON.stringify(log), { expirationTtl: 86400 * 7 });
  
  // 异常请求单独记录
  if (log.statusCode >= 400) {
    await logError(env, { ...log, type: 'api_error' });
  }
}

// 记录错误
async function logError(env, errorData) {
  const error = {
    timestamp: new Date().toISOString(),
    type: errorData.type || 'unknown',
    message: errorData.message,
    stack: errorData.stack,
    context: errorData.context,
  };
  
  const errorKey = `error:${Date.now()}:${Math.random().toString(36).substring(7)}`;
  await env.ERROR_LOGS_KV.put(errorKey, JSON.stringify(error), { expirationTtl: 86400 * 30 });
  
  // 严重错误发送告警
  if (errorData.type === 'critical') {
    await sendAlert(env, error);
  }
}

// ==================== 告警通知 ====================

// 发送告警（飞书机器人）
async function sendAlert(env, alertData) {
  if (!env.FEISHU_WEBHOOK_URL) {
    console.warn('未配置告警 Webhook');
    return;
  }
  
  const message = {
    msg_type: 'interactive',
    card: {
      header: {
        title: {
          tag: 'plain_text',
          content: '🚨 API 告警通知'
        },
        template: alertData.type === 'critical' ? 'red' : 'orange'
      },
      elements: [
        {
          tag: 'div',
          text: {
            tag: 'lark_md',
            content: `**告警类型**: ${alertData.type}\n**时间**: ${alertData.timestamp}\n**详情**: ${alertData.message}`
          }
        },
        {
          tag: 'action',
          actions: [
            {
              tag: 'button',
              text: {
                tag: 'plain_text',
                content: '查看日志'
              },
              url: 'https://dash.cloudflare.com/',
              type: 'default'
            }
          ]
        }
      ]
    }
  };
  
  try {
    await fetch(env.FEISHU_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(message)
    });
  } catch (error) {
    console.error('发送告警失败:', error);
  }
}

// ==================== 统计分析 ====================

// 更新使用统计
async function updateStats(env, apiKey, permission) {
  const today = new Date().toISOString().split('T')[0];
  const statsKey = `stats:${today}:${apiKey.substring(0, 16)}`;
  
  const existing = await env.STATS_KV.get(statsKey);
  const stats = existing ? JSON.parse(existing) : {
    date: today,
    apiKey: apiKey.substring(0, 16) + '***',
    permission,
    totalRequests: 0,
    successRequests: 0,
    failedRequests: 0,
    avgDuration: 0,
  };
  
  stats.totalRequests++;
  
  // 保存到 KV
  await env.STATS_KV.put(statsKey, JSON.stringify(stats), { expirationTtl: 86400 * 30 });
}

// 获取统计数据
async function getStats(env, days = 7) {
  const stats = [];
  const today = new Date();
  
  for (let i = 0; i < days; i++) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    const dateStr = date.toISOString().split('T')[0];
    
    // 获取当天的所有统计
    const prefix = `stats:${dateStr}:`;
    const list = await env.STATS_KV.list({ prefix });
    
    for (const key of list.keys) {
      const data = await env.STATS_KV.get(key.name);
      if (data) {
        stats.push(JSON.parse(data));
      }
    }
  }
  
  return stats;
}

// ==================== 监控端点 ====================

// 监控仪表板数据
async function handleGetMetrics(request, env) {
  const url = new URL(request.url);
  const action = url.searchParams.get('action');
  
  switch (action) {
    case 'stats':
      const days = parseInt(url.searchParams.get('days')) || 7;
      const stats = await getStats(env, days);
      return { success: true, data: stats };
    
    case 'recent_errors':
      const limit = parseInt(url.searchParams.get('limit')) || 20;
      const errors = await getRecentErrors(env, limit);
      return { success: true, data: errors };
    
    case 'health':
      const health = await checkSystemHealth(env);
      return { success: true, data: health };
    
    default:
      return { success: false, error: '未知的监控动作' };
  }
}

// 获取最近的错误日志
async function getRecentErrors(env, limit = 20) {
  const errors = [];
  const list = await env.ERROR_LOGS_KV.list({ prefix: 'error:' });
  
  // 获取最新的 limit 条错误
  const keys = list.keys.slice(-limit);
  for (const key of keys.reverse()) {
    const data = await env.ERROR_LOGS_KV.get(key.name);
    if (data) {
      errors.push(JSON.parse(data));
    }
  }
  
  return errors;
}

// 系统健康检查
async function checkSystemHealth(env) {
  const checks = {
    feishu_api: false,
    kv_storage: false,
    rate_limiting: false,
  };
  
  // 检查飞书 API
  try {
    const token = await getFeishuTenantToken(env.FEISHU_APP_ID, env.FEISHU_APP_SECRET);
    checks.feishu_api = !!token;
  } catch (error) {
    checks.feishu_api = false;
  }
  
  // 检查 KV 存储
  try {
    await env.STATS_KV.get('health_check');
    checks.kv_storage = true;
  } catch (error) {
    checks.kv_storage = false;
  }
  
  // 检查速率限制
  try {
    await env.RATE_LIMIT_KV.get('health_check');
    checks.rate_limiting = true;
  } catch (error) {
    checks.rate_limiting = false;
  }
  
  const allHealthy = Object.values(checks).every(v => v);
  
  return {
    status: allHealthy ? 'healthy' : 'degraded',
    timestamp: new Date().toISOString(),
    checks
  };
}

// ==================== 中间件集成 ====================

// 在 worker.js 中使用的监控中间件
export function createMonitoringMiddleware(env) {
  return {
    // 请求前
    async onRequest(request) {
      const startTime = Date.now();
      const url = new URL(request.url);
      
      return {
        startTime,
        path: url.pathname,
        method: request.method,
        apiKey: request.headers.get('X-API-Key'),
        ip: request.headers.get('CF-Connecting-IP'),
        userAgent: request.headers.get('User-Agent'),
      };
    },
    
    // 请求后
    async onResponse(context, response) {
      const duration = Date.now() - context.startTime;
      
      await logApiCall(env, {
        ...context,
        statusCode: response.status,
        duration,
      });
      
      await updateStats(env, context.apiKey || 'anonymous', 'unknown');
    },
    
    // 错误处理
    async onError(error, context) {
      await logError(env, {
        type: 'request_error',
        message: error.message,
        stack: error.stack,
        context,
      });
    }
  };
}

// ==================== 告警规则配置 ====================

export const ALERT_RULES = {
  // 错误率超过阈值
  errorRate: {
    threshold: 0.05, // 5%
    window: 300, // 5 分钟
  },
  
  // 请求量突增
  requestSpike: {
    threshold: 10, // 10 倍
    baseline: 100, // 基准请求数
  },
  
  // 响应时间过长
  slowResponse: {
    threshold: 2000, // 2 秒
    percentile: 95, // P95
  },
  
  // 连续认证失败
  authFailures: {
    threshold: 10,
    window: 60, // 1 分钟
  }
};
