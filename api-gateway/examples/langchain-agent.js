/**
 * LangChain 智能体集成示例
 * 完整可运行的示例代码
 */

import { ChatOpenAI } from '@langchain/openai';
import { createReactAgent } from 'langchain/agents';
import { MemorySaver } from 'langchain/memory';
import { RobotApiClient } from './agent-client.js';

// ==================== 配置 ====================

const CONFIG = {
  ROBOT_API_URL: process.env.ROBOT_API_URL || 'https://api.yourdomain.com',
  ROBOT_API_KEY: process.env.ROBOT_API_KEY || 'sk_agent_xxxxx',
  OPENAI_API_KEY: process.env.OPENAI_API_KEY,
  MODEL: process.env.MODEL || 'gpt-4',
};

// ==================== 初始化 ====================

// 创建机器人 API 客户端
const robotClient = new RobotApiClient(CONFIG.ROBOT_API_KEY, {
  baseUrl: CONFIG.ROBOT_API_URL,
  timeout: 5000,
  cacheTTL: 120000, // 2 分钟缓存
});

// 创建 LLM 模型
const model = new ChatOpenAI({
  modelName: CONFIG.MODEL,
  temperature: 0.7,
});

// ==================== 定义工具 ====================

// 工具 1: 搜索机器人
const searchRobotsTool = {
  name: 'search_robots',
  description: `从机器人数据库搜索工具。
  
  使用场景：
  - 用户需要找某个功能的机器人
  - 用户询问有什么工具可用
  - 用户需要推荐
  
  参数说明：
  - query: 用户需求描述（必需）
  - category: 分类筛选（可选）`,
  
  parameters: {
    type: 'object',
    properties: {
      query: {
        type: 'string',
        description: '用户需求，如"帮我找一个能翻译的机器人"',
      },
      category: {
        type: 'string',
        description: '分类：效率、工具、娱乐、教育、其他',
        enum: ['效率', '工具', '娱乐', '教育', '其他'],
      },
    },
    required: ['query'],
  },
  
  execute: async ({ query, category }) => {
    console.log(`🔍 搜索机器人：query="${query}", category="${category}"`);
    
    try {
      const result = await robotClient.searchBots({ q: query, category, limit: 5 });
      
      if (!result.success) {
        return `❌ 搜索失败：${result.error}`;
      }
      
      if (result.data.length === 0) {
        return '😕 未找到相关机器人，请尝试其他关键词';
      }
      
      // 格式化结果
      const formatted = result.data.map((bot, index) => {
        return [
          `${index + 1}. **${bot.name}**`,
          `   分类：${bot.category}`,
          `   描述：${bot.description}`,
          `   ID: \`${bot.id}\``,
        ].join('\n');
      }).join('\n\n');
      
      return `✅ 找到 ${result.data.length} 个相关机器人：\n\n${formatted}`;
      
    } catch (error) {
      console.error('搜索失败:', error);
      return `❌ 服务暂时不可用：${error.message}`;
    }
  },
};

// 工具 2: 获取机器人详情
const getBotDetailTool = {
  name: 'get_bot_detail',
  description: '获取指定机器人的详细信息，当用户需要了解某个具体机器人时使用',
  
  parameters: {
    type: 'object',
    properties: {
      botId: {
        type: 'string',
        description: '机器人 ID（从搜索结果中获取）',
      },
    },
    required: ['botId'],
  },
  
  execute: async ({ botId }) => {
    console.log(`📋 获取机器人详情：${botId}`);
    
    try {
      const result = await robotClient.getBot(botId);
      
      if (!result.success) {
        return `❌ 获取失败：${result.error}`;
      }
      
      const bot = result.data;
      return [
        `🤖 **${bot.name}**`,
        ``,
        `**分类**: ${bot.category}`,
        `**描述**: ${bot.description}`,
        `**创建时间**: ${bot.created_at || '未知'}`,
        `**ID**: \`${bot.id}\``,
      ].join('\n');
      
    } catch (error) {
      return `❌ 获取失败：${error.message}`;
    }
  },
};

// 工具 3: 获取分类列表
const getCategoriesTool = {
  name: 'get_categories',
  description: '获取所有机器人分类，当用户想了解有哪些分类时使用',
  
  parameters: {
    type: 'object',
    properties: {},
  },
  
  execute: async () => {
    const categories = ['效率', '工具', '娱乐', '教育', '其他'];
    return `📂 机器人分类：${categories.join('、')}`;
  },
};

// ==================== 创建智能体 ====================

const tools = [searchRobotsTool, getBotDetailTool, getCategoriesTool];

// 内存（保存对话历史）
const memory = new MemorySaver();

// 创建智能体
const agent = await createReactAgent({
  llm: model,
  tools,
  checkpointSaver: memory,
  messageModifier: `
你是一个机器人数据库助手，帮助用户找到合适的机器人工具。

你的职责：
1. 理解用户需求，搜索相关机器人
2. 提供清晰的推荐和说明
3. 如果用户需要更多详情，调用 get_bot_detail
4. 如果用户不确定要什么，先介绍分类

回答风格：
- 友好、专业、简洁
- 使用 emoji 增加可读性
- 结果用列表展示
- 提供下一步建议
`,
});

// ==================== 使用示例 ====================

async function runExample() {
  console.log('🤖 机器人数据库智能体已就绪\n');
  
  // 示例对话
  const conversations = [
    '帮我找个能翻译的机器人',
    '第一个看起来不错，有更多信息吗？',
    '还有哪些效率类的工具？',
  ];
  
  // 运行对话
  for (const input of conversations) {
    console.log(`👤 用户：${input}`);
    
    const result = await agent.invoke(
      { messages: [{ role: 'user', content: input }] },
      { configurable: { thread_id: 'demo_thread' } }
    );
    
    console.log(`🤖 助手：${result.messages[result.messages.length - 1].content}\n`);
  }
}

// ==================== 导出 ====================

export { agent, tools, robotClient, runExample };

// 如果直接运行此文件
if (import.meta.url === `file://${process.argv[1]}`) {
  runExample().catch(console.error);
}
