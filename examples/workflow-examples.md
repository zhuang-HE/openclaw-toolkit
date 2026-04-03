# 工作流示例

本文件展示 AI 助手 Toolkit 的实际使用场景。

---

## 示例 1: 新功能开发工作流

### 场景
开发一个新的用户认证模块

### 步骤

```bash
# 1. 研究最佳实践
/research 用户认证 最佳实践 2026 --depth=3

# 2. 开发代码（AI 辅助或手动）
# ... 编码过程 ...

# 3. 安全审查
/review src/auth/ --focus=security --depth=3

# 4. 根据审查结果修复
# ... 修复代码 ...

# 5. 生成 API 文档
/docs src/auth/ --type=api

# 6. 生成使用教程
/docs src/auth/ --type=tutorial --output=docs/tutorials/

# 7. Git 提交
/git status
/git commit

# 8. 准备 PR
/git pr
```

### 输出
- 认证模块代码
- 安全审查报告
- API 文档
- 使用教程
- Git 提交和 PR

---

## 示例 2: 代码库健康检查

### 场景
定期审查项目代码质量

### 步骤

```bash
# 1. 整体代码审查
/review src/ --depth=2

# 2. 安全专项审查
/review src/ --focus=security

# 3. 性能审查
/review src/ --focus=performance

# 4. 整理发现到记忆
/memory consolidate

# 5. 生成健康报告
# （通过 researcher 代理）
sessions_spawn({
  task: "基于审查结果生成代码健康报告",
  agentId: "researcher"
})
```

### 输出
- 代码质量报告
- 安全问题列表
- 性能优化建议
- 代码健康评分

---

## 示例 3: 技术调研

### 场景
调研 AI Agent 框架选型

### 步骤

```bash
# 1. 初步调研
/research AI Agent 框架 --depth=2

# 2. 深度对比
/research AI 助手 vs OpenClaw vs LangChain --depth=3 --sources=5

# 3. 整理调研结果
/memory consolidate

# 4. 生成调研报告
# （通过 researcher 代理）
sessions_spawn({
  task: "整理 AI Agent 框架调研报告，包含对比表格和推荐建议",
  agentId: "researcher",
  attachments: [
    {name: "research-notes.md", content: "..."}
  ]
})
```

### 输出
- 技术调研报告
- 框架对比表格
- 推荐建议

---

## 示例 4: 文档维护

### 场景
项目文档更新和维护

### 步骤

```bash
# 1. 检查文档完整性
/docs src/api/ --type=api

# 2. 更新 README
/docs --type=readme --output=.

# 3. 生成 Changelog
# （通过 documentation 代理）
sessions_spawn({
  task: "根据 git log 生成 Changelog",
  agentId: "documentation-writer"
})

# 4. 提交文档更新
/git add docs/
/git commit -m "docs: 更新 API 文档和 README"
```

### 输出
- 更新的 API 文档
- 更新的 README
- Changelog

---

## 示例 5: 外部服务集成

### 场景
连接和管理 GitHub 项目

### 步骤

```bash
# 1. 检查连接状态
/connect status

# 2. 查看 GitHub Issues
/connect github --action=list

# 3. 查看特定 Issue 详情
/connect github --action=query 42

# 4. 创建新 Issue
/connect github --action=exec "gh issue create --title 'Bug' --body 'Description'"

# 5. 查看 PR 状态
/connect github --action=exec "gh pr list --state open"
```

### 输出
- Issues 列表
- Issue 详情
- 新建 Issue
- PR 状态

---

## 示例 6: 记忆管理

### 场景
定期整理和归档记忆

### 步骤

```bash
# 1. 查看记忆状态
/memory status

# 2. 整理最近记忆
/memory consolidate

# 3. 搜索特定主题
/memory search "Agent 架构"

# 4. 归档旧记忆
/memory archive --days=30

# 5. 导出记忆备份
/memory export --format=md --output=backup/
```

### 输出
- 记忆状态报告
- 整理后的 MEMORY.md
- 搜索结果
- 归档文件

---

## 示例 7: 完整项目启动

### 场景
启动一个新项目

### 步骤

```bash
# 1. 研究类似项目
/research 类似项目 最佳实践

# 2. 创建项目结构
# （手动或 AI 辅助）

# 3. 生成初始文档
/docs --type=readme --output=.

# 4. 初始化 Git
/git init
/git branch -M main

# 5. 初始提交
/git add .
/git commit -m "Initial commit"

# 6. 创建远程仓库
/connect github --action=exec "gh repo create --private"
/git push -u origin main
```

### 输出
- 项目结构
- README.md
- Git 仓库
- 远程仓库

---

## 示例 8: 多 Agent 协作

### 场景
复杂项目的多角色协作

### 步骤

```javascript
// 1. 需求分析代理
const reqAgent = await sessions_spawn({
  task: "分析用户需求，生成需求文档",
  agentId: "researcher",
  runtime: "subagent"
});

// 2. 代码审查代理（并行）
const reviewAgent = await sessions_spawn({
  task: "审查现有代码库",
  agentId: "code-reviewer",
  runtime: "subagent"
});

// 3. 文档代理（并行）
const docAgent = await sessions_spawn({
  task: "准备文档模板",
  agentId: "documentation-writer",
  runtime: "subagent"
});

// 4. 等待所有代理完成
// 5. 整合结果
// 6. 生成综合报告
```

### 输出
- 需求分析报告
- 代码审查报告
- 文档模板
- 综合项目报告

---

## 最佳实践总结

### 1. 工作流设计
- 先研究后实施
- 审查贯穿始终
- 文档同步更新
- 定期记忆整理

### 2. 命令组合
- `/research` → 了解背景
- `/review` → 保证质量
- `/docs` → 生成文档
- `/git` → 版本控制
- `/memory` → 知识管理

### 3. 代理协作
- 简单任务用命令
- 复杂任务用代理
- 多任务并行执行
- 结果统一整合

---

**更多示例？查看实际项目中的使用案例！**
