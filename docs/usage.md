# 使用手册

本手册详细介绍 AI 助手 Toolkit 各组件的使用方法。

---

## Commands（命令系统）

### /research - 深度研究

**用途**: 对指定主题进行深度网络研究

**语法**:
```bash
/research [主题] [--depth=1|2|3] [--sources=N] [--format=markdown|json]
```

**参数**:
| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| 主题 | ✓ | - | 研究主题 |
| --depth | ✗ | 2 | 研究深度 (1=快速/2=标准/3=深度) |
| --sources | ✗ | 3 | 最少验证来源数 |
| --format | ✗ | markdown | 输出格式 |

**示例**:
```bash
# 快速调研
/research AI Agent 框架

# 深度研究
/research 量子计算 --depth=3 --sources=5
```

---

### /review - 代码审查

**用途**: 对代码进行质量审查和安全审计

**语法**:
```bash
/review [文件|目录] [--depth=1|2|3] [--focus=security|performance|quality]
```

**参数**:
| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| 文件/目录 | ✗ | 当前目录 | 审查目标 |
| --depth | ✗ | 2 | 审查深度 |
| --focus | ✗ | all | 审查重点 |

**示例**:
```bash
# 审查当前文件
/review

# 审查指定文件
/review src/auth.ts

# 安全审查
/review src/api/ --focus=security
```

---

### /docs - 文档生成

**用途**: 为代码模块生成技术文档

**语法**:
```bash
/docs [模块|文件] [--type=api|readme|tutorial] [--output=路径]
```

**示例**:
```bash
# 生成 API 文档
/docs src/api/

# 生成 README
/docs --type=readme --output=.
```

---

### /git - Git 工作流

**用途**: Git 版本控制操作

**语法**:
```bash
/git [action] [options]
```

**Actions**:
| Action | 说明 |
|--------|------|
| `status` | 查看状态 |
| `commit` | 智能提交 |
| `branch` | 分支管理 |
| `merge` | 合并分支 |
| `pr` | 准备 PR |
| `log` | 查看历史 |
| `diff` | 查看差异 |

**示例**:
```bash
# 查看状态
/git status

# 智能提交
/git commit

# 准备 PR
/git pr
```

---

### /memory - 记忆管理

**用途**: 记忆系统管理

**语法**:
```bash
/memory [action] [options]
```

**Actions**:
| Action | 说明 |
|--------|------|
| `status` | 查看状态 |
| `consolidate` | 整理记忆 |
| `search` | 搜索记忆 |
| `archive` | 归档旧记忆 |
| `export` | 导出记忆 |

**示例**:
```bash
# 查看状态
/memory status

# 整理记忆
/memory consolidate

# 搜索记忆
/memory search Agent
```

---

### /connect - 外部连接

**用途**: 连接和管理外部服务

**语法**:
```bash
/connect [service] [--action=list|query|exec]
```

**Services**:
| Service | 说明 |
|---------|------|
| `github` | GitHub API |
| `database` | 数据库连接 |
| `docker` | Docker 管理 |
| `k8s` | Kubernetes |
| `aws` | AWS 服务 |
| `status` | 连接状态 |

**示例**:
```bash
# 查看连接状态
/connect status

# GitHub 操作
/connect github --action=list

# 数据库查询
/connect database --action=query "SELECT * FROM users"
```

---

## Agents（代理）

### researcher - 研究代理

**用途**: 专业信息搜集和分析

**使用方式**:
```javascript
sessions_spawn({
  task: "研究 AI Agent 市场趋势",
  agentId: "researcher",
  runtime: "subagent"
})
```

**输出**: 结构化研究报告

---

### code-reviewer - 代码审查代理

**用途**: 专业代码审查

**使用方式**:
```javascript
sessions_spawn({
  task: "审查这个代码文件的安全问题",
  agentId: "code-reviewer",
  attachments: [{name: "code.js", content: "..."}],
  runtime: "subagent"
})
```

**输出**: 代码审查报告（含问题分级和修复建议）

---

### documentation-writer - 文档代理

**用途**: 技术文档编写

**使用方式**:
```javascript
sessions_spawn({
  task: "为这个模块生成 API 文档",
  agentId: "documentation-writer",
  attachments: [{name: "api.ts", content: "..."}],
  runtime: "subagent"
})
```

**输出**: 完整的技术文档

---

## Skills（技能）

### web-research

**用途**: 网络研究和信息整理

**调用方式**:
```javascript
// 通过命令调用
/research 主题

// 或通过子代理调用
sessions_spawn({
  task: "研究 XXX",
  runtime: "subagent"
})
```

---

### code-review

**用途**: 代码质量审查

**调用方式**:
```javascript
// 通过命令调用
/review src/file.ts

// 或通过子代理调用
sessions_spawn({
  task: "审查代码",
  runtime: "subagent"
})
```

---

### documentation

**用途**: 技术文档生成

**调用方式**:
```javascript
// 通过命令调用
/docs src/api/

// 或通过子代理调用
sessions_spawn({
  task: "生成文档",
  runtime: "subagent"
})
```

---

### git-workflow

**用途**: Git 工作流管理

**调用方式**:
```javascript
// 通过命令调用
/git commit

// 或通过 exec 调用
exec({command: "git status"})
```

---

### memory-consolidation

**用途**: 记忆整理和压缩

**调用方式**:
```javascript
// 通过命令调用
/memory consolidate

// 或定期自动执行（heartbeat）
```

---

### mcp-connector

**用途**: 外部服务连接

**调用方式**:
```javascript
// 通过命令调用
/connect github --action=list

// 或通过 exec 调用外部 CLI
exec({command: "gh issue list"})
```

---

## 组合使用示例

### 示例 1: 完整开发工作流

```bash
# 1. 研究需求
/research 用户认证最佳实践

# 2. 开发代码（手动或 AI 辅助）

# 3. 审查代码
/review src/auth/ --focus=security

# 4. 生成文档
/docs src/auth/

# 5. 提交代码
/git commit

# 6. 准备 PR
/git pr
```

### 示例 2: 项目分析

```bash
# 1. 研究项目背景
/research 竞品分析

# 2. 审查现有代码
/review src/ --depth=3

# 3. 整理记忆
/memory consolidate

# 4. 生成报告
# （通过 researcher 代理）
```

---

## 最佳实践

### 1. 命令使用

- 使用 `--depth` 参数控制研究/审查深度
- 大项目分模块处理
- 敏感操作前确认

### 2. 代理使用

- 复杂任务使用专用代理
- 传递清晰的 task 描述
- 使用 attachments 传递上下文

### 3. 技能使用

- 优先使用命令调用（更简洁）
- 复杂场景使用子代理
- 定期整理记忆保持高效

### 4. 外部连接

- 使用只读凭证优先
- 敏感操作需确认
- 记录所有外部调用

---

## 故障排除

参考 [installation.md](installation.md) 的故障排除章节。

---

**需要更多帮助？查看 [examples/](../examples/) 中的实际示例！**
