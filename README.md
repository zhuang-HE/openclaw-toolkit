# OpenClaw Toolkit

🚀 AI 助手最佳实践集成到 OpenClaw 框架的工具包

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-blue)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-openclaw--toolkit-green)](https://clawhub.com/skills/openclaw-toolkit)

---

## 📖 项目简介

本项目将业界领先的 AI 助手最佳实践集成到 [OpenClaw](https://github.com/openclaw/openclaw) 框架，让你可以享受高效、结构化的开发体验。

### 核心特性

🎯 开箱即用 - 15 个预定义组件，无需从零开始
🧩 模块化设计 - Commands/Agents/Skills 三层解耦架构
📚 最佳实践 - 融合业界领先的 AI 助手设计模式
🔧 高度可扩展 - 轻松添加自定义命令、代理和技能
🌐 本地优先 - 支持完全本地部署，数据可控

### 架构设计

采用业界标准的三层架构：

```
Commands（命令层）→ Agents（代理层）→ Skills（技能层）
```

用户交互层 (Commands)
    ↓
任务执行层 (Agents)
    ↓
能力模块层 (Skills)

---

## 🚀 快速开始

### 前置条件

- OpenClaw 已安装并配置
- 基础 Node.js 环境
- Git（用于版本控制）

层级            组件数            职责
Commands        6 个             用户快捷入口 (/research, /review, /docs 等)
Agents          3 个             专业任务执行者 (researcher, code-reviewer, documentation-writer)
Skills          6 个             可复用能力模块 (web-research, code-review, documentation 等)


### 安装

#### 方式一：通过 ClawHub（推荐）

```bash
# 使用 ClawHub 安装
clawhub install openclaw-toolkit

# 验证安装
ls ~/.openclaw/workspace/commands/
ls ~/.openclaw/workspace/agents/
ls ~/.openclaw/workspace/skills/
```

#### 方式二：手动安装

```bash
# 1. 克隆或下载本仓库
git clone https://github.com/openclaw/openclaw-toolkit.git

# 2. 复制到 OpenClaw workspace
cp -r openclaw-toolkit/* ~/.openclaw/workspace/

# 3. 验证安装
ls ~/.openclaw/workspace/commands/
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
openclaw-toolkit/
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
│   └── usage.md               # 使用手册
├── examples/                  # 示例
│   └── workflow-examples.md   # 工作流示例
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
- [工作流示例](examples/workflow-examples.md) - 实际使用场景

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

- [OpenClaw](https://github.com/openclaw/openclaw) - 本地 AI 助手框架
- AI 助手最佳实践社区 - 灵感和参考

---

## 📬 联系方式

- 项目地址：https://github.com/zhuang-HE/openclaw-toolkit
- 问题反馈：https://github.com/zhuang-HE/openclaw-toolkit/issues
- OpenClaw 文档：https://docs.openclaw.ai
- ClawHub: https://clawhub.com/skills/openclaw-toolkit

## 🏷️ Topics

[![Topics](https://img.shields.io/badge/topics-openclaw%20%7C%20ai--assistant%20%7C%20productivity%20%7C%20automation%20%7C%20workflow-blue)](https://github.com/zhuang-HE/openclaw-toolkit)

---

**Made with ❤️ for the OpenClaw Community**
