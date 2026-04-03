# 安装指南

本指南将帮助你在 OpenClaw 中安装和配置 AI 助手 Toolkit。

---

## 前置条件

### 1. OpenClaw 安装

确保已安装 OpenClaw：

```bash
# 检查 OpenClaw 是否已安装
openclaw --version

# 如未安装，参考官方文档
# https://docs.openclaw.ai/getting-started/installation
```

### 2. 基础环境

```bash
# Node.js (推荐 v18+)
node --version

# Git
git --version
```

---

## 安装方式

### 方式一：手动复制（推荐）

```bash
# 1. 下载或克隆本仓库
git clone https://github.com/YOUR_USERNAME/openclaw-openclaw-toolkit.git
cd openclaw-openclaw-toolkit

# 2. 复制到 OpenClaw workspace
cp -r commands/ ~/.openclaw/workspace/
cp -r agents/ ~/.openclaw/workspace/
cp -r skills/ ~/.openclaw/workspace/
cp -r docs/ ~/.openclaw/workspace/

# 3. 验证安装
ls ~/.openclaw/workspace/commands/
ls ~/.openclaw/workspace/agents/
ls ~/.openclaw/workspace/skills/
```

### 方式二：符号链接（开发模式）

```bash
# 1. 克隆到 workspace
cd ~/.openclaw/workspace/
git clone https://github.com/YOUR_USERNAME/openclaw-openclaw-toolkit.git

# 2. 创建符号链接
ln -s openclaw-openclaw-toolkit/commands commands
ln -s openclaw-openclaw-toolkit/agents agents
ln -s openclaw-openclaw-toolkit/skills skills
```

---

## 配置

### 1. 更新 HEARTBEAT.md

编辑 `~/.openclaw/workspace/HEARTBEAT.md`，添加周期性任务：

```markdown
# 周期性任务

## 每周任务
- [ ] 记忆整理 (每周日) - 调用 `/memory consolidate`
```

### 2. 更新 AGENTS.md

确保 `~/.openclaw/workspace/AGENTS.md` 包含目录结构说明。

### 3. 配置环境变量（可选）

如使用外部连接功能，配置以下环境变量：

```bash
# GitHub
export GITHUB_TOKEN=ghp_xxx

# 数据库
export DATABASE_URL=postgresql://user:pass@host:5432/db

# AWS
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
```

---

## 验证安装

### 测试 Commands

在 OpenClaw 会话中：

```bash
# 测试研究命令
/research OpenClaw

# 测试帮助（查看命令列表）
# 参考 commands/README.md
```

### 测试 Skills

```javascript
// 在会话中启动子代理测试技能
sessions_spawn({
  task: "测试 web-research 技能",
  runtime: "subagent"
})
```

### 测试 Agents

```javascript
// 测试研究者代理
sessions_spawn({
  task: "研究 AI 发展趋势",
  agentId: "researcher"
})
```

---

## 故障排除

### 问题 1: 命令不响应

**原因**: 命令路由未实现

**解决**: 在会话处理逻辑中添加命令解析：

```javascript
if (input.startsWith('/')) {
  const [cmd, ...args] = input.slice(1).split(' ');
  // 根据 cmd 调用对应 skill
}
```

### 问题 2: Skill 未找到

**原因**: 路径不正确

**解决**: 检查技能目录：

```bash
ls ~/.openclaw/workspace/skills/web-research/
# 应包含 SKILL.md
```

### 问题 3: Agent 未生效

**原因**: 未正确传递 agentId

**解决**: 确保 `sessions_spawn` 包含正确的 agentId：

```javascript
sessions_spawn({
  task: "...",
  agentId: "researcher"  // 确保与 agents/ 目录文件名匹配
})
```

---

## 更新

```bash
# 拉取最新代码
cd ~/.openclaw/workspace/openclaw-openclaw-toolkit
git pull origin main

# 重启 OpenClaw Gateway
openclaw gateway restart
```

---

## 卸载

```bash
# 删除组件
rm -rf ~/.openclaw/workspace/commands/
rm -rf ~/.openclaw/workspace/agents/
rm -rf ~/.openclaw/workspace/skills/web-research/
rm -rf ~/.openclaw/workspace/skills/code-review/
rm -rf ~/.openclaw/workspace/skills/documentation/
rm -rf ~/.openclaw/workspace/skills/git-workflow/
rm -rf ~/.openclaw/workspace/skills/memory-consolidation/
rm -rf ~/.openclaw/workspace/skills/mcp-connector/

# 恢复配置文件（如修改过）
# 手动编辑 HEARTBEAT.md 和 AGENTS.md
```

---

## 下一步

- [使用手册](usage.md) - 学习如何使用各个组件
- [自定义指南](customization.md) - 根据需求定制
- [示例](../examples/) - 查看实际使用示例

---

**安装完成后，开始 [使用手册](usage.md) 学习如何使用！**
