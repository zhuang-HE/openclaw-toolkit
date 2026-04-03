# Commands System - 命令系统框架

## Overview

本目录包含 OpenClaw 的快捷命令定义，类似 Claude Code 的 `/command` 系统。

每个命令文件定义了一个可快速触发的任务模板。

## Command Format

```markdown
# [命令名称]

trigger: /command-name [arguments]

## Description
[命令功能简述]

## Arguments
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| ...  | ...  | ...  | ...    | ...  |

## Handler
1. [执行步骤 1]
2. [执行步骤 2]
3. [执行步骤 3]

## Examples
/command-name arg1 arg2

## Related
- [相关技能]
- [相关代理]
```

## Available Commands

### 研究类
| 命令 | 功能 | 调用技能 |
|------|------|----------|
| `/research` | 深度研究 | web-research |
| `/compare` | 对比分析 | web-research |
| `/analyze` | 技术分析 | researcher agent |

### 开发类
| 命令 | 功能 | 调用技能 |
|------|------|----------|
| `/review` | 代码审查 | code-review |
| `/docs` | 生成文档 | documentation |
| `/git` | Git 操作 | git-workflow |

### 系统类
| 命令 | 功能 | 调用技能 |
|------|------|----------|
| `/memory` | 记忆整理 | memory-consolidation |
| `/connect` | 外部连接 | mcp-connector |
| `/status` | 系统状态 | 内置 |

## Usage

### 在会话中使用

```javascript
// 解析命令
if (input.startsWith('/')) {
  const [cmd, ...args] = input.slice(1).split(' ');
  
  switch (cmd) {
    case 'research':
      // 调用 web-research skill
      break;
    case 'review':
      // 调用 code-review skill
      break;
    // ...
  }
}
```

### 在 Skill 中路由

```markdown
# SKILL.md 中的命令处理

## Command Routing

当输入匹配以下模式时触发：

- `/research [topic]` → web-research skill
- `/review [file]` → code-review skill
- `/docs [module]` → documentation skill
```

## Implementation Template

```markdown
# /research - 研究命令

trigger: /research [topic] [--depth=1|2|3] [--sources=min]

## Description
对指定主题进行深度网络研究，生成结构化报告。

## Arguments
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| topic | string | ✓ | - | 研究主题 |
| --depth | number | ✗ | 2 | 研究深度 (1-3) |
| --sources | number | ✗ | 3 | 最少来源数 |

## Handler
1. 解析主题和参数
2. 调用 web-research skill
3. 设置研究深度和来源要求
4. 等待完成并返回报告

## Examples
/research AI Agent 框架 2026
/research 量子计算 --depth=3 --sources=5

## Related
- skill: web-research
- agent: researcher
```

## Command Registry

```javascript
// commands/index.js (可选，用于集中管理)

const commands = {
  research: {
    handler: 'web-research',
    args: ['topic', '--depth', '--sources'],
    description: '深度研究'
  },
  review: {
    handler: 'code-review',
    args: ['file', '--depth'],
    description: '代码审查'
  },
  docs: {
    handler: 'documentation',
    args: ['module', '--type'],
    description: '生成文档'
  },
  git: {
    handler: 'git-workflow',
    args: ['action'],
    description: 'Git 操作'
  },
  memory: {
    handler: 'memory-consolidation',
    args: ['--days'],
    description: '记忆整理'
  },
  connect: {
    handler: 'mcp-connector',
    args: ['service', '--action'],
    description: '外部连接'
  }
};

module.exports = { commands };
```

## Best Practices

1. **命令命名**: 使用简短易记的动词
2. **参数设计**: 必需参数在前，可选参数用 `--flag` 格式
3. **错误处理**: 参数缺失时提供友好提示
4. **帮助信息**: 每个命令支持 `--help` 显示用法
5. **权限控制**: 敏感命令需要确认

## Future Enhancements

- [ ] 命令别名支持
- [ ] 命令链式调用
- [ ] 命令历史记录
- [ ] 自定义命令注册
- [ ] 命令权限系统
