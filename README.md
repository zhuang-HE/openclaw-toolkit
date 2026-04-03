# OpenClaw Claude Code Toolkit

🚀 将 Claude Code 的最佳实践迁移到 OpenClaw 框架的工具包

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-blue)](https://github.com/openclaw/openclaw)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Inspired-orange)](https://code.claude.com)

---

## 📖 项目简介

本项目将 [Claude Code](https://code.claude.com) 的核心架构模式和最佳实践迁移到 [OpenClaw](https://github.com/openclaw/openclaw) 框架，让你可以在 OpenClaw 中享受类似 Claude Code 的开发体验。

### 核心特性

- 🎯 **Commands 系统** - 6 个开箱即用的快捷命令
- 🤖 **Agents 模板** - 3 个专业代理定义
- 🛠️ **Skills 库** - 6 个核心技能模块
- 📚 **完整文档** - 详细的使用指南和示例
- 🔌 **MCP 风格连接** - 外部服务集成能力

### 架构对比

| Claude Code | OpenClaw Toolkit | 状态 |
|-------------|-----------------|------|
| `.claude/commands/` | `commands/` | ✅ |
| `.claude/agents/` | `agents/` | ✅ |
| `.claude/skills/` | `skills/` | ✅ |
| `CLAUDE.md` | `AGENTS.md` + `SOUL.md` | ✅ |
| MCP Protocol | `mcp-connector` | ✅ |
| AutoDream | `memory-consolidation` | ✅ |

---

## 🚀 快速开始

### 前置条件

- OpenClaw 已安装并配置
- 基础 Node.js 环境
- Git（用于版本控制）

### 安装

```bash
# 1. 克隆或下载本仓库
git clone https://github.com/YOUR_USERNAME/openclaw-claude-code-toolkit.git

# 2. 复制到 OpenClaw workspace
cp -r openclaw-claude-code-toolkit/* ~/.openclaw/workspace/

# 3. 验证安装
ls ~/.openclaw/workspace/commands/
ls ~/.openclaw/workspace/agents/
ls ~/.openclaw/workspace/skills/
```

### 使用命令

在 OpenClaw 会话中直接使用：

```bash
# 深度研究
/research AI Agent 框架

# 代码审查
/review src/auth.ts

# 生成文档
/docs src/api/

# Git 操作
/git commit

# 记忆整理
/memory consolidate

# 外部连接
/connect status
```

---

## 📦 项目结构

```
openclaw-claude-code-toolkit/
├── commands/                  # 快捷命令定义
│   ├── README.md              # 命令系统说明
│   ├── research.md            # /research 命令
│   ├── review.md              # /review 命令
│   ├── docs.md                # /docs 命令
│   ├── git.md                 # /git 命令
│   ├── memory.md              # /memory 命令
│   └── connect.md             # /connect 命令
├── agents/                    # 子代理定义
│   ├── researcher.md          # 研究代理
│   ├── code-reviewer.md       # 代码审查代理
│   └── documentation-writer.md # 文档代理
├── skills/                    # 技能模块
│   ├── web-research/          # 网络研究技能
│   ├── code-review/           # 代码审查技能
│   ├── documentation/         # 文档生成技能
│   ├── git-workflow/          # Git 工作流技能
│   ├── memory-consolidation/  # 记忆整理技能
│   └── mcp-connector/         # 外部连接技能
├── docs/                      # 文档
│   ├── installation.md        # 安装指南
│   ├── usage.md               # 使用手册
│   └── customization.md       # 自定义指南
├── examples/                  # 示例
│   ├── workflow-examples.md   # 工作流示例
│   └── integration-examples.md # 集成示例
├── LICENSE                    # 许可证
└── README.md                  # 本文件
```

---

## 🛠️ 核心组件

### Commands（命令）

| 命令 | 功能 | 调用技能 |
|------|------|----------|
| `/research` | 深度网络研究 | web-research |
| `/review` | 代码审查 | code-review |
| `/docs` | 文档生成 | documentation |
| `/git` | Git 工作流 | git-workflow |
| `/memory` | 记忆管理 | memory-consolidation |
| `/connect` | 外部连接 | mcp-connector |

### Agents（代理）

| 代理 | 职责 | 适用场景 |
|------|------|----------|
| `researcher` | 信息搜集分析 | 市场调研、竞品分析 |
| `code-reviewer` | 代码审查 | PR 审查、安全审计 |
| `documentation-writer` | 文档编写 | API 文档、教程 |

### Skills（技能）

| 技能 | 功能 | 复杂度 |
|------|------|--------|
| `web-research` | 多源网络研究 | ⭐⭐ |
| `code-review` | 代码质量审查 | ⭐⭐⭐ |
| `documentation` | 技术文档生成 | ⭐⭐ |
| `git-workflow` | Git 操作自动化 | ⭐⭐ |
| `memory-consolidation` | 记忆整理压缩 | ⭐⭐⭐ |
| `mcp-connector` | 外部服务连接 | ⭐⭐⭐⭐ |

---

## 📖 使用示例

### 1. 深度研究

```bash
# 标准研究
/research AI Agent 框架 2026

# 深度研究（更多来源）
/research 量子计算 --depth=3 --sources=5

# 输出格式指定
/research 区块链 --format=markdown
```

### 2. 代码审查

```bash
# 审查当前文件
/review

# 审查指定文件
/review src/auth.ts

# 专注安全审查
/review src/api/ --focus=security

# 深度审查
/review src/ --depth=3
```

### 3. 文档生成

```bash
# 生成 API 文档
/docs src/api/

# 生成 README
/docs --type=readme --output=.

# 生成教程
/docs src/ --type=tutorial
```

### 4. Git 工作流

```bash
# 查看状态
/git status

# 智能提交
/git commit

# 创建分支
/git branch feature/new-feature

# 准备 PR
/git pr
```

### 5. 记忆管理

```bash
# 查看状态
/memory status

# 整理记忆
/memory consolidate

# 搜索记忆
/memory search Agent

# 归档旧记忆
/memory archive --days=30
```

### 6. 外部连接

```bash
# 查看连接状态
/connect status

# GitHub 操作
/connect github --action=list

# 数据库查询
/connect database --action=query "SELECT * FROM users"

# Docker 管理
/connect docker --action=list
```

---

## 🔧 自定义

### 添加新命令

在 `commands/` 目录创建新文件：

```markdown
# commands/my-command.md

trigger: /my-command [arguments]

## Description
[命令功能]

## Handler
1. [步骤 1]
2. [步骤 2]

## Examples
/my-command arg1 arg2
```

### 添加新 Agent

在 `agents/` 目录创建新文件：

```markdown
# agents/my-agent.md

name: my-agent

## Your Role
[角色定义]

## Responsibilities
- [职责 1]
- [职责 2]

## Workflow
1. [步骤 1]
2. [步骤 2]
```

### 添加新 Skill

在 `skills/` 目录创建新目录：

```
skills/my-skill/
└── SKILL.md
```

---

## 📚 文档

- [安装指南](docs/installation.md) - 详细安装步骤
- [使用手册](docs/usage.md) - 完整使用说明
- [自定义指南](docs/customization.md) - 扩展和定制

---

## 🤝 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 致谢

- [Claude Code](https://code.claude.com) - Anthropic 的命令行 AI 助手，本项目的灵感来源
- [claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) - Claude Code 最佳实践整理
- [OpenClaw](https://github.com/openclaw/openclaw) - 本地 AI 助手框架

---

## 📬 联系方式

- 项目地址：https://github.com/YOUR_USERNAME/openclaw-claude-code-toolkit
- 问题反馈：https://github.com/YOUR_USERNAME/openclaw-claude-code-toolkit/issues
- OpenClaw 文档：https://docs.openclaw.ai

---

**Made with ❤️ for the OpenClaw Community**
