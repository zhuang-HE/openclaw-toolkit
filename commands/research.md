# /research - 研究命令

trigger: /research [topic] [--depth=1|2|3] [--sources=N]

## Description
对指定主题进行深度网络研究，生成结构化研究报告。

## Arguments

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| topic | string | ✓ | - | 研究主题 |
| --depth | number | ✗ | 2 | 研究深度 (1=快速/2=标准/3=深度) |
| --sources | number | ✗ | 3 | 最少验证来源数 |
| --format | string | ✗ | markdown | 输出格式 (markdown/json) |

## Handler

1. **解析输入**
   - 提取研究主题
   - 解析可选参数
   - 验证参数有效性

2. **配置研究策略**
   - depth=1: 快速调研，1-2 个搜索，摘要输出
   - depth=2: 标准研究，3-5 个搜索，详细报告
   - depth=3: 深度研究，5+ 搜索，全面分析

3. **启动研究**
   - 调用 web-research skill
   - 传递研究参数
   - 等待完成

4. **返回结果**
   - 显示研究报告
   - 提供来源链接
   - 询问是否需要深入

## Examples

```bash
# 快速调研
/research AI Agent 框架

# 标准研究（默认）
/research AI Agent 框架 --depth=2

# 深度研究
/research AI Agent 框架 --depth=3 --sources=5

# 指定输出格式
/research 量子计算 --depth=2 --format=markdown
```

## Output Example

```markdown
# AI Agent 框架 研究报告

## 核心摘要
2026 年 AI Agent 框架呈现多极化发展趋势，主要玩家包括...

## 关键发现
1. **OpenClaw** - 开源本地框架，支持多渠道集成
   来源：GitHub, 官方文档 - 置信度：高

2. **业界主流 AI 助手 CLI** - 参考设计
   来源：Anthropic 文档，npm - 置信度：高

3. **LangChain** - 成熟的 Agent 开发框架
   来源：官方文档，社区 - 置信度：高

## 详细对比
[表格和详细分析]

## 数据来源
| 来源 | 类型 | 链接 |
|------|------|------|
| GitHub | 代码仓库 | https://... |
| 官方文档 | 文档 | https://... |
```

## Related
- skill: web-research
- agent: researcher
- command: /compare, /analyze

## Notes
- 深度研究可能需要较长时间
- 敏感话题会多方验证
- 付费内容寻找替代来源
