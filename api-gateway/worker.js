// Cloudflare Workers - 机器人数据库 API 网关
// 部署指南：https://developers.cloudflare.com/workers/

// ==================== 配置 ====================
const CONFIG = {
  FEISHU_APP_ID: '你的飞书应用 App ID',
  FEISHU_APP_SECRET: '你的飞书应用 App Secret',
  FEISHU_BITABLE_APP_TOKEN: 'XC2nbCyx3acaPls7bsRcVOBnnOh', // API 密钥管理表
  FEISHU_BITABLE_TABLE_ID: 'tbl6iFEirXgZhoXP', // API 密钥管理表 ID
  FEISHU_ROBOT_BITABLE_TOKEN: 'GkYVbxSFpaxpBAstJZ9c7BArnug', // 机器人数据库
  FEISHU_ROBOT_TABLE_ID: 'tbl2eyXwJxZ8pdn0', // 机器人数据表 ID
  CACHE_TTL: 300, // 缓存时间 5 分钟
  RATE_LIMIT_PER_MINUTE: 100,
};

// ==================== 工具函数 ====================

// 生成唯一 API Key
function generateApiKey() {
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let result = 'sk_';
  for (let i = 0; i < 32; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// 验证 API Key
async function validateApiKey(apiKey, env) {
  if (!apiKey) return { valid: false, reason: '缺少 API Key' };
  
  try {
    const token = await getFeishuTenantToken(env.FEISHU_APP_ID, env.FEISHU_APP_SECRET);
    const url = `https://open.feishu.cn/open-apis/bitable/v1/apps/${CONFIG.FEISHU_BITABLE_APP_TOKEN}/tables/${CONFIG.FEISHU_BITABLE_TABLE_ID}/records/search`;
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        filter: {
          conjunction: 'and',
          conditions: [
            { field_name: 'API Key', operator: 'is', value: apiKey },
            { field_name: '状态', operator: 'is', value: '启用' }
          ]
        }
      })
    });
    
    const data = await response.json();
    
    if (data.code !== 0 || !data.data?.items?.length) {
      return { valid: false, reason: 'API Key 无效或已禁用' };
    }
    
    const record = data.data.items[0];
    const expires = record.fields['过期时间'];
    
    if (expires && new Date(expires) < new Date()) {
      return { valid: false, reason: 'API Key 已过期' };
    }
    
    return {
      valid: true,
      permission: record.fields['权限级别'] || 'read',
      rateLimit: record.fields['请求次数限制'] || 1000
    };
  } catch (error) {
    console.error('验证 API Key 失败:', error);
    return { valid: false, reason: '验证服务异常' };
  }
}

// 获取飞书 tenant_access_token
async function getFeishuTenantToken(appId, appSecret) {
  const cacheKey = 'feishu_tenant_token';
  const cached = await FEISHU_TOKEN_CACHE.get(cacheKey);
  
  if (cached) {
    return cached;
  }
  
  const response = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: appId, app_secret: appSecret })
  });
  
  const data = await response.json();
  
  if (data.code !== 0) {
    throw new Error('获取飞书 token 失败: ' + data.msg);
  }
  
  // 缓存 token（过期时间略小于实际过期时间）
  await FEISHU_TOKEN_CACHE.put(cacheKey, data.tenant_access_token, { expirationTtl: 7000 });
  
  return data.tenant_access_token;
}

// 检查速率限制
async function checkRateLimit(request, env, apiKey) {
  const key = `rate_limit:${apiKey}:${Math.floor(Date.now() / 60000)}`;
  const count = await env.RATE_LIMIT_KV.get(key);
  
  if (count && parseInt(count) >= CONFIG.RATE_LIMIT_PER_MINUTE) {
    return { limited: true, message: '请求频率超限，请稍后重试' };
  }
  
  await env.RATE_LIMIT_KV.put(key, (parseInt(count) || 0) + 1, { expirationTtl: 120 });
  return { limited: false };
}

// 从飞书获取机器人数据
async function fetchRobotData(token, filters = {}) {
  const url = `https://open.feishu.cn/open-apis/bitable/v1/apps/${CONFIG.FEISHU_ROBOT_BITABLE_TOKEN}/tables/${CONFIG.FEISHU_ROBOT_TABLE_ID}/records`;
  
  const params = new URLSearchParams();
  if (filters.page_token) params.set('page_token', filters.page_token);
  if (filters.page_size) params.set('page_size', filters.page_size);
  
  const response = await fetch(`${url}?${params}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    }
  });
  
  const data = await response.json();
  
  if (data.code !== 0) {
    throw new Error('获取数据失败: ' + data.msg);
  }
  
  return data.data;
}

// ==================== 请求处理 ====================

// 处理机器人列表查询
async function handleGetBots(request, env, permission) {
  const url = new URL(request.url);
  const search = url.searchParams.get('q');
  const category = url.searchParams.get('category');
  const page = parseInt(url.searchParams.get('page')) || 1;
  const pageSize = Math.min(parseInt(url.searchParams.get('limit')) || 20, 100);
  
  try {
    const token = await getFeishuTenantToken(env.FEISHU_APP_ID, env.FEISHU_APP_SECRET);
    const data = await fetchRobotData(token, { page_size: pageSize });
    
    // 数据过滤和格式化
    let robots = data.items.map(item => ({
      id: item.record_id,
      name: item.fields['名称'] || '未命名',
      description: item.fields['描述'] || '',
      category: item.fields['分类'] || '其他',
      avatar: item.fields['头像'] || '',
      created_at: item.fields['创建时间'] || null,
    }));
    
    // 搜索过滤
    if (search) {
      const searchLower = search.toLowerCase();
      robots = robots.filter(bot => 
        bot.name.toLowerCase().includes(searchLower) ||
        bot.description.toLowerCase().includes(searchLower)
      );
    }
    
    // 分类过滤
    if (category) {
      robots = robots.filter(bot => bot.category === category);
    }
    
    // 权限过滤：非 admin 只能看到公开字段
    if (permission !== 'admin') {
      robots = robots.map(({ id, name, description, category, avatar }) => ({
        id, name, description, category, avatar
      }));
    }
    
    return {
      success: true,
      data: robots,
      pagination: {
        total: data.total,
        page,
        per_page: pageSize,
        has_more: data.has_more
      }
    };
  } catch (error) {
    console.error('获取机器人数据失败:', error);
    throw error;
  }
}

// 处理创建机器人
async function handleCreateBot(request, env, permission) {
  if (permission === 'read') {
    return { success: false, error: '权限不足，需要 write 或 admin 权限' };
  }
  
  try {
    const body = await request.json();
    const token = await getFeishuTenantToken(env.FEISHU_APP_ID, env.FEISHU_APP_SECRET);
    
    const url = `https://open.feishu.cn/open-apis/bitable/v1/apps/${CONFIG.FEISHU_ROBOT_BITABLE_TOKEN}/tables/${CONFIG.FEISHU_ROBOT_TABLE_ID}/records`;
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        fields: {
          '名称': body.name,
          '描述': body.description,
          '分类': body.category,
          '头像': body.avatar,
        }
      })
    });
    
    const data = await response.json();
    
    if (data.code !== 0) {
      return { success: false, error: data.msg };
    }
    
    return {
      success: true,
      data: { id: data.data.record_id, ...body }
    };
  } catch (error) {
    console.error('创建机器人失败:', error);
    return { success: false, error: error.message };
  }
}

// ==================== 主入口 ====================

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    
    // CORS 预检请求
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
        }
      });
    }
    
    // 健康检查
    if (path === '/health') {
      return new Response(JSON.stringify({ status: 'ok', timestamp: new Date().toISOString() }));
    }
    
    // API 路由
    if (path.startsWith('/api/v1/bots')) {
      // 验证 API Key
      const apiKey = request.headers.get('X-API-Key');
      const validation = await validateApiKey(apiKey, env);
      
      if (!validation.valid) {
        return new Response(JSON.stringify({
          success: false,
          error: validation.reason
        }), {
          status: 401,
          headers: { 'Content-Type': 'application/json' }
        });
      }
      
      // 检查速率限制
      const rateCheck = await checkRateLimit(request, env, apiKey);
      if (rateCheck.limited) {
        return new Response(JSON.stringify({
          success: false,
          error: rateCheck.message
        }), {
          status: 429,
          headers: { 'Content-Type': 'application/json' }
        });
      }
      
      const permission = validation.permission;
      let result;
      
      try {
        if (path === '/api/v1/bots' && request.method === 'GET') {
          result = await handleGetBots(request, env, permission);
        } else if (path === '/api/v1/bots' && request.method === 'POST') {
          result = await handleCreateBot(request, env, permission);
        } else if (path.startsWith('/api/v1/bots/') && request.method === 'GET') {
          // 获取单个机器人
          const id = path.split('/').pop();
          result = { success: true, data: { id } }; // TODO: 实现单个查询
        } else {
          result = { success: false, error: '不支持的请求方法或路径' };
        }
      } catch (error) {
        result = { success: false, error: error.message };
      }
      
      return new Response(JSON.stringify(result), {
        status: result.success ? 200 : 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        }
      });
    }
    
    // 404
    return new Response(JSON.stringify({ error: 'Not Found' }), {
      status: 404,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
