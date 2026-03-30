/**
 * 机器人数据库 API 客户端
 * 适用于各类智能体（LangChain、AutoGen、Dify 等）
 * 
 * 使用示例：
 * const client = new RobotApiClient('sk_prod_xxxxx');
 * const bots = await client.searchBots({ category: '效率', q: 'AI' });
 */

export class RobotApiClient {
  constructor(apiKey, options = {}) {
    this.apiKey = apiKey;
    this.baseUrl = options.baseUrl || 'https://api.yourdomain.com';
    this.timeout = options.timeout || 5000;
    this.cache = new Map();
    this.cacheTTL = options.cacheTTL || 60000; // 1 分钟
  }

  // 通用请求方法
  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': this.apiKey,
          ...options.headers,
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new RobotApiError(
          error.error || `HTTP ${response.status}`,
          response.status,
          error
        );
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      if (error.name === 'AbortError') {
        throw new RobotApiError('请求超时', 408);
      }
      throw error;
    }
  }

  // 带缓存的 GET 请求
  async cachedGet(endpoint, cacheKey) {
    const cached = this.cache.get(cacheKey);
    if (cached && Date.now() - cached.timestamp < this.cacheTTL) {
      return cached.data;
    }

    const data = await this.request(endpoint);
    this.cache.set(cacheKey, { data, timestamp: Date.now() });
    return data;
  }

  // ==================== API 方法 ====================

  /**
   * 搜索机器人
   * @param {Object} params - 搜索参数
   * @param {string} params.q - 关键词
   * @param {string} params.category - 分类
   * @param {number} params.limit - 每页数量
   * @param {number} params.page - 页码
   */
  async searchBots(params = {}) {
    const queryParams = new URLSearchParams();
    if (params.q) queryParams.set('q', params.q);
    if (params.category) queryParams.set('category', params.category);
    if (params.limit) queryParams.set('limit', params.limit);
    if (params.page) queryParams.set('page', params.page);

    const cacheKey = `search:${queryParams.toString()}`;
    return await this.cachedGet(`/api/v1/bots?${queryParams}`, cacheKey);
  }

  /**
   * 获取单个机器人详情
   * @param {string} botId - 机器人 ID
   */
  async getBot(botId) {
    return await this.request(`/api/v1/bots/${botId}`);
  }

  /**
   * 获取所有分类
   */
  async getCategories() {
    return await this.cachedGet('/api/v1/categories', 'categories');
  }

  /**
   * 创建机器人（需要 write 权限）
   * @param {Object} botData - 机器人数据
   */
  async createBot(botData) {
    return await this.request('/api/v1/bots', {
      method: 'POST',
      body: JSON.stringify(botData),
    });
  }

  /**
   * 更新机器人（需要 write 权限）
   * @param {string} botId - 机器人 ID
   * @param {Object} botData - 更新数据
   */
  async updateBot(botId, botData) {
    return await this.request(`/api/v1/bots/${botId}`, {
      method: 'PUT',
      body: JSON.stringify(botData),
    });
  }

  /**
   * 删除机器人（需要 admin 权限）
   * @param {string} botId - 机器人 ID
   */
  async deleteBot(botId) {
    return await this.request(`/api/v1/bots/${botId}`, {
      method: 'DELETE',
    });
  }

  /**
   * 健康检查
   */
  async healthCheck() {
    return await this.request('/health');
  }

  // ==================== 智能体工具方法 ====================

  /**
   * LangChain Tool 格式
   * 用于 LangChain 智能体自动调用
   */
  toLangChainTool() {
    return {
      name: 'search_robot_database',
      description: '从机器人数据库中搜索合适的机器人工具',
      parameters: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: '搜索关键词，描述用户需求',
          },
          category: {
            type: 'string',
            description: '机器人分类（可选）',
            enum: ['效率', '工具', '娱乐', '教育', '其他'],
          },
        },
        required: ['query'],
      },
      execute: async ({ query, category }) => {
        const result = await this.searchBots({ q: query, category });
        return JSON.stringify(result.data);
      },
    };
  }

  /**
   * Dify API 工具格式
   */
  toDifyTool() {
    return {
      type: 'api',
      label: '机器人数据库搜索',
      icon: '🤖',
      schema: {
        method: 'get',
        url: `${this.baseUrl}/api/v1/bots`,
        headers: {
          'X-API-Key': this.apiKey,
        },
        parameters: [
          {
            name: 'q',
            type: 'string',
            required: true,
            description: '搜索关键词',
          },
          {
            name: 'category',
            type: 'string',
            required: false,
            description: '分类筛选',
          },
        ],
      },
    };
  }
}

// ==================== 错误类 ====================

export class RobotApiError extends Error {
  constructor(message, status, details = {}) {
    super(message);
    this.name = 'RobotApiError';
    this.status = status;
    this.details = details;
  }
}

// ==================== 工厂函数 ====================

/**
 * 创建智能体专用的 API 客户端
 * 自动处理认证、重试、降级
 */
export function createAgentClient(config) {
  const client = new RobotApiClient(config.apiKey, {
    baseUrl: config.baseUrl,
    timeout: config.timeout || 5000,
  });

  // 添加重试逻辑
  const originalRequest = client.request.bind(client);
  client.request = async (endpoint, options) => {
    let lastError;
    for (let i = 0; i < 3; i++) {
      try {
        return await originalRequest(endpoint, options);
      } catch (error) {
        lastError = error;
        if (error.status >= 500) {
          // 服务器错误，重试
          await new Promise(r => setTimeout(r, 1000 * (i + 1)));
          continue;
        }
        // 客户端错误，不重试
        throw error;
      }
    }
    throw lastError;
  };

  // 添加降级逻辑
  client.searchBotsWithFallback = async (params) => {
    try {
      return await client.searchBots(params);
    } catch (error) {
      console.warn('API 调用失败，使用本地缓存降级:', error.message);
      // 返回空结果或本地缓存
      return { success: false, data: [], fallback: true };
    }
  };

  return client;
}
