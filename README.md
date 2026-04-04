# OpenClaw Toolkit

<div align="center">

🚀 AI 助手最佳实践 · 开箱即用的 OpenClaw 增强工具包

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ClawHub](https://img.shields.io/badge/ClawHub-published-green?logo=rocket)](https://clawhub.ai/plugins/openclaw-toolkit)
[![GitHub stars](https://img.shields.io/github/stars/zhuang-HE/openclaw-toolkit?style=social)](https://github.com/zhuang-HE/openclaw-toolkit/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/zhuang-HE/openclaw-toolkit?style=social)](https://github.com/zhuang-HE/openclaw-toolkit/network/members)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**15 个预定义组件 · Commands / Agents / Skills 三层解耦 · 一键安装**

[快速开始](#-快速开始) · [核心组件](#-核心组件) · [使用演示](#-使用演示) · [安装方式](#-安装) · [贡献指南](CONTRIBUTING.md)

</div>

---

## 🎯 项目简介

OpenClaw Toolkit 将业界领先的 AI 助手最佳实践打包成开箱即用的组件，集成到 OpenClaw 框架。

### 核心特性

| 特性 | 说明 |
|------|------|
| 🧩 **三层解耦架构** | Commands → Agents → Skills，职责清晰，易于扩展 |
| 🚀 **15 个预定义组件** | 覆盖研究、审查、文档、工作流、记忆、外部集成 |
| 🌍 **多源研究** | 聚合搜索引擎 + 微信公众号 + 通用搜索，结果更全面 |
| 🔍 **安全代码审查** | 自动识别安全漏洞、代码质量问题和优化建议 |
| 🧠 **记忆系统** | 自动整理和压缩工作记忆，保持长期知识可用 |
| 🔗 **外部服务集成** | GitHub、Docker、数据库等外部工具无缝连接 |

---

## 📂 项目结构

```
openclaw-toolkit/
├── commands/               # 6 个快捷命令（用户入口）
│   ├── research.md        # /research  深度研究
│   ├── review.md          # /review    代码审查
│   ├── docs.md            # /docs      文档生成
│   ├── git.md             # /git       Git 工作流
│   ├── memory.md          # /memory    记忆管理
│   └── connect.md         # /connect   外部连接
│
├── agents/                 # 3 个专业代理（任务执行）
│   ├── researcher.md      # 研究代理：多源信息搜集分析
│   ├── code-reviewer.md   # 审查代理：代码质量 + 安全审计
│   └── documentation-writer.md  # 文档代理：技术文档编写
│
├── skills/                 # 6 个技能模块（可复用能力）
│   ├── web-research/       # 网络研究
│   ├── code-review/       # 代码审查
│   ├── documentation/     # 文档生成
│   ├── git-workflow/      # Git 工作流
│   ├── memory-consolidation/  # 记忆整理
│   └── mcp-connector/    # 外部连接
│
└── examples/              # 工作流示例
    └── workflow-examples.md
```

---

## 🖥️ 使用演示

### 安装后，在 OpenClaw 会话中直接调用：

```
你：帮我深度研究一下无人机保险的市场现状
─────────────────────────────────────────────────
[Tool] /research 无人机保险市场 2026

  ✓ 搜索 12 个来源（微信公众号 + 网络搜索）
  ✓ 整理行业报告 3 份、政策文件 2 份
  ✓ 生成结构化分析报告

─────────────────────────────────────────────────

你：review 这段代码有没有安全问题
─────────────────────────────────────────────────
[Tool] /review src/auth.ts

  🔍 扫描中...
  ⚠️ 发现 2 个风险点：
     • SQL 注入风险（第 23 行）
     • 敏感信息明文存储（第 45 行）
  ✅ 代码质量评分：78/100
  💡 优化建议已生成

─────────────────────────────────────────────────

你：帮我生成 API 文档
─────────────────────────────────────────────────
[Tool] /docs src/api/ --type=openapi

  ✓ 分析 12 个端点
  ✓ 生成 OpenAPI 3.0 文档
  ✓ 保存至 docs/api.md
```

### 命令速查

```bash
/research <主题>        # 深度网络研究
/review <文件或目录>    # 代码审查 + 安全审计
/docs <路径> --type=<类型>  # 文档生成
/git <操作>             # Git 工作流自动化
/memory <操作>          # 记忆整理与压缩
/connect <服务>          # 外部服务连接
```

---

## 🚀 快速开始

### 方式一：通过 ClawHub 安装（推荐）

```bash
# 一键安装（安装整个工具包）
clawhub install zhuang-HE/openclaw-toolkit

# 或者安装单个 skill
clawhub install web-research
clawhub install code-review
```

### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/zhuang-HE/openclaw-toolkit.git
cd openclaw-toolkit

# Windows
xcopy /E /I skills\* %USERPROFILE%\.workbuddy\skills\

# macOS / Linux
cp -r skills/* ~/.workbuddy/skills/

# 验证
ls ~/.workbuddy/skills/
```

> **提示**：安装到 `~/.workbuddy/skills/` 后，WorkBuddy 会根据 SKILL.md 中的 frontmatter 触发词自动加载对应技能，无需手动选择。

---

## 🧩 核心组件

### Commands（命令层）

| 命令 | 功能 | 底层技能 |
|------|------|---------|
| `/research` | 深度网络研究，多源聚合 | `web-research` |
| `/review` | 代码审查 + 安全审计 | `code-review` |
| `/docs` | 技术文档生成 | `documentation` |
| `/git` | Git 工作流自动化 | `git-workflow` |
| `/memory` | 记忆整理与压缩 | `memory-consolidation` |
| `/connect` | 外部服务连接 | `mcp-connector` |

### Skills（技能层）

| 技能 | 功能 | 复杂度 |
|------|------|--------|
| `web-research` | 聚合微信/网络多源搜索，结构化报告 | ⭐⭐ |
| `code-review` | 质量审查 + 安全扫描 + 优化建议 | ⭐⭐⭐ |
| `documentation` | README / API文档 / 变更日志 | ⭐⭐ |
| `git-workflow` | 智能提交 + 分支管理 + PR 准备 | ⭐⭐ |
| `memory-consolidation` | 日志压缩 + 长期记忆提炼 | ⭐⭐⭐ |
| `mcp-connector` | GitHub / Docker / 数据库 / kubectl | ⭐⭐⭐⭐ |

---

## 🛠️ 自定义扩展

### 添加新 Skill

在 `skills/` 下创建目录和 `SKILL.md` 即可：

```
skills/my-awesome-skill/
└── SKILL.md
```

Skill 会被 WorkBuddy 自动发现并根据触发词加载。

### 发布到 ClawHub

```bash
clawhub login --token <your-token>
clawhub package publish . \
  --source-repo zhuang-HE/openclaw-toolkit \
  --source-commit <commit-sha> \
  --name openclaw-toolkit \
  --version 1.0.1 \
  --changelog "Your changelog here"
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- 🐛 报告 Bug → [Issue](https://github.com/zhuang-HE/openclaw-toolkit/issues/new/choose)
- 💡 提出功能建议 → [Discussion](https://github.com/zhuang-HE/openclaw-toolkit/discussions)
- 📖 完善文档或示例

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📄 许可证

MIT License · © 2024-2026 [zhuang-HE](https://github.com/zhuang-HE)

---

## 📬 联系方式

- 🐛 问题反馈：[GitHub Issues](https://github.com/zhuang-HE/openclaw-toolkit/issues)
- 💬 功能讨论：[GitHub Discussions](https://github.com/zhuang-HE/openclaw-toolkit/discussions)
- 📦 ClawHub：[clawhub.ai/plugins/openclaw-toolkit](https://clawhub.ai/plugins/openclaw-toolkit)
- 📖 OpenClaw 文档：[docs.openclaw.ai](https://docs.openclaw.ai)

---

<div align="center">

**Made with ❤️ for the OpenClaw Community**

</div>
