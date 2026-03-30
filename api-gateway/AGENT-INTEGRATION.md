# 🤖 智能体集成指南

本文档说明如何在各类智能体平台中集成机器人数据库 API。

---

## 一、前置准备

### 1.1 创建智能体专用 API Key

在 API 密钥管理表中创建新记录：

| 字段 | 值 |
|------|-----|
| API Key | `sk_agent_xxxxxxxxxxxxx`（自动生成） |
| 调用方名称 | `智能体名称` |
| 权限级别 | `read`（推荐）或 `write` |
| 状态 | `启用` |
| 请求次数限制 | `50000`（根据需求调整） |
| 过期时间 | `2027-12-31` |
| 备注 | `智能体专用密钥 - 只读权限` |

### 1.2 配置环境变量

```bash
# .env 文件
ROBOT_API_URL=https://api.yourdomain.com
ROBOT_API_KEY=sk_agent_xxxxxxxxxxxxx
ROBOT_API_TIMEOUT=5000
```

---

## 二、LangChain 集成

### 2.1 安装依赖

```bash
npm install langchain @langchain/core
```

### 2.2 创建自定义 Tool

```javascript
import { tool } from '@langchain/core/tools';
import { RobotApiClient } from './agent-client.js';

const robotClient = new RobotApiClient(process.env.ROBOT_API_KEY, {
  baseUrl: process.env.ROBOT_API_URL,
});

// 定义搜索工具
const searchRobotsTool = tool(
  async ({ query, category }) => {
    const result = await robotClient.searchBots({ q: query, category });
    
    if (!result.success) {
      return `搜索失败：${result.error}`;
    }
    
    // 格式化结果为智能体友好的文本
    const bots = result.data.map(bot => 
      `- **${bot.name}**: ${bot.description} (分类：${bot.category})`
    ).join('\n');
    
    return `找到 ${result.data.length} 个相关机器人:\n${bots}`;
  },
  {
    name: 'search_robot_database',
    description: '从机器人数据库搜索工具。当用户需要找某个功能的机器人时使用。',
    schema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: '用户需求描述，如"帮我找一个能翻译的机器人"',
        },
        category: {
          type: 'string',
          description: '可选的分类筛选',
          enum: ['效率', '工具', '娱乐', '教育', '其他'],
        },
      },
      required: ['query'],
    },
  }
);

// 创建智能体
import { createReactAgent } from 'langchain/agents';
import { ChatOpenAI } from '@langchain/openai';

const model = new ChatOpenAI({ model: 'gpt-4' });
const agent = await createReactAgent({
  llm: model,
  tools: [searchRobotsTool],
});

// 使用示例
const result = await agent.invoke({
  messages: [{ role: 'user', content: '帮我找个能处理文档的 AI 机器人' }],
});
```

### 2.3 多工具场景

```javascript
import { DynamicStructuredTool } from '@langchain/core/tools';

// 获取单个机器人详情工具
const getBotDetailTool = new DynamicStructuredTool({
  name: 'get_bot_detail',
  description: '获取指定机器人的详细信息',
  schema: {
    type: 'object',
    properties: {
      botId: { type: 'string', description: '机器人 ID' },
    },
    required: ['botId'],
  },
  func: async ({ botId }) => {
    const result = await robotClient.getBot(botId);
    return JSON.stringify(result.data);
  },
});

// 组合多个工具
const tools = [searchRobotsTool, getBotDetailTool];
```

---

## 三、Dify 集成

### 3.1 创建 API 工具

在 Dify 控制台：

1. 进入「工具」→「创建工具」
2. 选择「API 工具」
3. 配置如下：

**基础信息**
- 名称：`机器人数据库搜索`
- 图标：🤖
- 描述：`从机器人数据库搜索合适的工具`

**API 配置**
```yaml
Method: GET
URL: {{ROBOT_API_URL}}/api/v1/bots
Headers:
  X-API-Key: {{ROBOT_API_KEY}}
  Content-Type: application/json
Parameters:
  - name: q
    type: string
    required: true
    description: 搜索关键词
  - name: category
    type: string
    required: false
    description: 分类筛选
```

**响应解析**
```javascript
// 解析脚本
const bots = response.data || [];
if (bots.length === 0) {
  return '未找到相关机器人';
}

return bots.map(bot => 
  `名称：${bot.name}\n描述：${bot.description}\n分类：${bot.category}`
).join('\n\n');
```

### 3.2 在编排中使用

1. 在「编排」页面添加「工具」节点
2. 选择「机器人数据库搜索」
3. 将用户输入连接到 `q` 参数
4. 后续节点处理搜索结果

---

## 四、AutoGen 集成

### 4.1 创建自定义函数

```python
# Python 版本
import requests
import os
from typing import List, Dict, Optional

class RobotDatabaseClient:
    def __init__(self):
        self.api_key = os.getenv('ROBOT_API_KEY')
        self.base_url = os.getenv('ROBOT_API_URL')
    
    def search_bots(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """搜索机器人数据库"""
        params = {'q': query}
        if category:
            params['category'] = category
        
        response = requests.get(
            f'{self.base_url}/api/v1/bots',
            headers={'X-API-Key': self.api_key},
            params=params
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        return []

# 注册为 AutoGen 函数
from autogen import register_function

robot_client = RobotDatabaseClient()

def search_robots(query: str, category: str = None) -> str:
    """
    Search for robots in the database.
    
    Args:
        query: Search query describing user needs
        category: Optional category filter
    
    Returns:
        Formatted list of matching robots
    """
    results = robot_client.search_bots(query, category)
    
    if not results:
        return "No matching robots found."
    
    formatted = []
    for bot in results[:5]:  # 限制返回 5 个
        formatted.append(f"🤖 {bot['name']}: {bot['description']}")
    
    return "\n".join(formatted)

# 注册到助手
register_function(
    search_robots,
    caller=assistant_agent,
    executor=user_proxy_agent,
    name="search_robots",
    description="Search robot database for tools matching user needs"
)
```

---

## 五、Coze/扣子集成

### 5.1 创建插件

1. 进入「插件」→「创建插件」
2. 填写信息：
   - 名称：机器人数据库
   - 描述：搜索和获取机器人信息

### 5.2 添加 API

**API 配置**
```
路径：/api/v1/bots
方法：GET
认证方式：自定义 Header
Header: X-API-Key = {{API_KEY}}
```

**请求参数**
```json
{
  "q": {
    "type": "string",
    "required": true,
    "description": "搜索关键词"
  },
  "category": {
    "type": "string",
    "required": false
  }
}
```

**响应解析**
```javascript
// 解析模板
{{#each data}}
- {{this.name}}: {{this.description}}
{{/each}}
```

### 5.3 在 Bot 中使用

在 Bot 编排中添加插件，然后智能体可以自然调用：

```
用户：帮我找个能翻译的机器人
Bot: （自动调用插件搜索）
     找到以下翻译机器人：
     - 翻译助手：支持多语言实时翻译
     - ...
```

---

## 六、自定义智能体集成

### 6.1 基础封装

```javascript
import { createAgentClient } from './agent-client.js';

// 创建客户端
const agent = createAgentClient({
  apiKey: 'sk_agent_xxxxx',
  baseUrl: 'https://api.yourdomain.com',
  timeout: 5000,
});

// 在智能体逻辑中使用
async function handleUserRequest(userQuery) {
  try {
    // 1. 搜索相关机器人
    const searchResult = await agent.searchBotsWithFallback({
      q: userQuery,
      limit: 5,
    });
    
    // 2. 格式化结果
    if (searchResult.fallback) {
      return '暂时无法访问机器人数据库，请稍后重试';
    }
    
    if (searchResult.data.length === 0) {
      return '未找到相关机器人，请尝试其他关键词';
    }
    
    // 3. 返回推荐
    const recommendations = searchResult.data.map(bot => 
      `🤖 **${bot.name}**\n${bot.description}`
    ).join('\n\n');
    
    return `找到 ${searchResult.data.length} 个相关机器人：\n\n${recommendations}`;
    
  } catch (error) {
    console.error('智能体调用失败:', error);
    return '服务暂时不可用';
  }
}
```

### 6.2 添加缓存层

```javascript
// Redis 缓存示例
import Redis from 'ioredis';

const redis = new Redis();

async function searchWithCache(query, category) {
  const cacheKey = `robot_search:${query}:${category || 'all'}`;
  
  // 尝试从缓存获取
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }
  
  // 调用 API
  const result = await agent.searchBots({ q: query, category });
  
  // 缓存 5 分钟
  await redis.setex(cacheKey, 300, JSON.stringify(result));
  
  return result;
}
```

---

## 七、最佳实践

### 7.1 错误处理

```javascript
try {
  const result = await agent.searchBots({ q: '翻译' });
} catch (error) {
  if (error.status === 401) {
    // API Key 无效
    logError('认证失败，检查 API Key');
  } else if (error.status === 429) {
    // 限流
    await sleep(1000);
    // 重试
  } else if (error.status >= 500) {
    // 服务器错误，使用降级方案
    return getFallbackResults();
  }
}
```

### 7.2 性能优化

```javascript
// 1. 批量查询
const queries = ['翻译', '文档', '效率'];
const results = await Promise.all(
  queries.map(q => agent.searchBots({ q }))
);

// 2. 预加载热门分类
const popularCategories = ['效率', '工具', '教育'];
await Promise.all(
  popularCategories.map(cat => 
    agent.searchBots({ category: cat, limit: 10 })
  )
);

// 3. 结果缓存
// 见上方 Redis 示例
```

### 7.3 安全建议

| 建议 | 说明 |
|------|------|
| 最小权限 | 智能体只给 read 权限 |
| 独立密钥 | 每个智能体独立 API Key |
| 限流保护 | 设置合理的请求限制 |
| 密钥轮换 | 定期更换 API Key |
| 监控告警 | 监控异常调用 |

---

## 八、调试技巧

### 8.1 启用详细日志

```javascript
const agent = new RobotApiClient(apiKey, {
  baseUrl,
  debug: true, // 启用调试日志
});
```

### 8.2 测试连接

```javascript
// 健康检查
const health = await agent.healthCheck();
console.log('API 状态:', health);

// 测试查询
const test = await agent.searchBots({ q: 'test', limit: 1 });
console.log('测试成功:', test.success);
```

### 8.3 常见问题

**Q: 401 Unauthorized**
- 检查 API Key 是否正确
- 确认密钥状态为"启用"

**Q: 429 Too Many Requests**
- 降低调用频率
- 增加缓存
- 联系管理员提升限额

**Q: 超时**
- 增加 timeout 配置
- 检查网络连接
- 添加重试逻辑

---

## 九、示例项目

查看完整示例：
- [LangChain 示例](./examples/langchain-agent.js)
- [Dify 配置](./examples/dify-tool.json)
- [Python AutoGen](./examples/autogen-agent.py)

---

**需要针对特定平台的支持？** 告诉我你使用的智能体平台，我可以提供定制集成方案。
