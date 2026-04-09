# Changelog

所有重要的项目更新都会记录在此文件中。

## [1.0.1] - 2026-04-09

### 🎉 新增

#### Fusion Workflow Hub（融合工作流中心）
- **融合三大工具**：Graphify + Everything Claude Code + OpenClaw
- **Graphify 集成**：代码知识图谱构建与查询（71.5x Token 节省）
- **ECC 集成**：68 个命令、36 个代理、151 个技能
- **三大推荐工作流**：
  - 代码库深度分析
  - 功能开发（TDD）
  - 持续学习优化

### 📦 包含文件
- `skills/fusion-workflow-hub/SKILL.md` - 核心技能说明
- `skills/fusion-workflow-hub/references/graphify-commands.md` - Graphify 命令参考
- `skills/fusion-workflow-hub/references/ecc-best-practices.md` - ECC 最佳实践

### 🚀 安装方式
```bash
clawhub install fusion-workflow-hub
```

---

## [1.0.0] - 2026-04-05

### 🎉 初始版本

#### Commands（命令层）
- `/research` - 深度网络研究
- `/review` - 代码审查
- `/docs` - 文档生成
- `/git` - Git 工作流
- `/memory` - 记忆管理
- `/connect` - 外部连接

#### Agents（代理层）
- `researcher` - 研究代理
- `code-reviewer` - 审查代理
- `documentation-writer` - 文档代理

#### Skills（技能层）
- `web-research` - 网络研究
- `code-review` - 代码审查
- `documentation` - 文档生成
- `git-workflow` - Git 工作流
- `memory-consolidation` - 记忆整理
- `mcp-connector` - MCP 连接器

---

## 版本说明

- **Major**: 不兼容的 API 变更
- **Minor**: 向后兼容的功能新增
- **Patch**: 向后兼容的问题修复
