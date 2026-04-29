---
name: agent-workflow-hub
version: 1.0.0
description: >
  Agent 融合工作流中心（fusion-workflow-hub + self-improvement 融合版）。
  整合 Graphify 知识图谱、TDD 开发流程、自我反思优化、质量评分体系。
  触发词：知识图谱、代码分析、代码图谱、构建图谱、查询图谱、代码依赖分析、
  理解代码库、深度分析代码库、融合工作流、fusion workflow、
  自我优化、反思一下、复盘、总结经验、工作复盘、优化工作流、
  会话总结、质量评分、执行复盘
triggers:
  - 知识图谱
  - graphify
  - 代码图谱
  - 深度分析代码库
  - TDD
  - 融合工作流
  - fusion workflow
  - 代码库分析
  - 构建图谱
  - 查询图谱
  - 代码依赖分析
  - 代码结构分析
  - 上下文压缩
  - 代码理解
  - 理解代码库
  - 自我优化
  - 自我改进
  - self improvement
  - 反思一下
  - 复盘
  - 总结经验
  - 工作复盘
  - 优化工作流
  - 会话总结
  - 质量评分
  - 执行复盘
complexity: ⭐⭐⭐⭐
tools:
  - execute_command
  - read_file
  - write_to_file
  - replace_in_file
  - list_dir
  - task
  - web_fetch
references:
  - references/detailed-flows-and-templates.md
---

# Agent Workflow Hub

## 🎯 融合定位

整合代码分析能力（fusion-workflow-hub）和自我反思优化（self-improvement），
提供从代码理解到执行优化的完整闭环。

### 核心能力矩阵

| 能力层 | 组件来源 | 功能 |
|--------|---------|------|
| **代码分析** | Graphify | 知识图谱、依赖分析、概念追踪 |
| **工作流** | fusion-workflow-hub | TDD、持续学习、分析工作流 |
| **自我反思** | self-improvement | 五维反思、模式识别 |
| **质量体系** | self-improvement | 置信度评估、质量评分 |
| **升级机制** | fusion-workflow-hub | Escalation Rules |
| **完成协议** | fusion-workflow-hub | 状态定义与报告格式 |

---

## 🔄 四大工作模式

### 模式 1️⃣：代码库深度分析

适用场景：接手新项目、理解大型代码库、寻找特定功能

```bash
# Step 1: 构建知识图谱
python -m graphify <目录路径>

# Step 2: 读取图谱报告
cat graphify-out/GRAPH_REPORT.md

# Step 3: 精准查询
python -m graphify query "认证系统是如何实现的？"

# Step 4: 追踪概念路径
python -m graphify path "用户登录" "数据库写入"
```

### 模式 2️⃣：TDD 功能开发

适用场景：新功能开发、严格质量要求

```
规划 → 编写测试 → 实现最小代码 → 代码审查 → 更新图谱 → 重构
```

### 模式 3️⃣：自我反思优化

适用场景：任务完成后的质量评估和经验积累

**五维反思（D1-D5）**：

| 维度 | 问题 | 行动 |
|------|------|------|
| D1 执行质量 | 重试？工具选择最优？ | 记踩坑 |
| D2 用户理解 | 误解？需求偏差？ | 更新偏好 |
| D3 知识漏洞 | 触发词盲区？该封装 Skill？ | 更新触发词 |
| D4 记忆系统 | 实质性工作未记录？ | 写 MEMORY |
| D5 序列模式 | 跨 turn 低效模式？ | 优化流程 |

**自动触发阈值**：

| 场景 | 阈值 | 动作 |
|------|------|------|
| 同一错误重试 | ≥ 2 次 | 记踩坑 |
| 复杂任务完成 | 调用 ≥ 5 次 | 静默自检 |
| 用户负面反馈 | 任何 | D2 专项 |
| 新偏好发现 | 任何 | 立即写 MEMORY |
| 任务全部完成 | — | 完整反思 + 评分 |

### 模式 4️⃣：融合工作流（推荐）

完整闭环：分析 → 开发 → 反思 → 优化

```
用户请求 → 代码分析（Graphify）
    ↓
发现问题区域 → TDD 开发（code-review）
    ↓
任务完成 → 自我反思（五维）
    ↓
质量评分 → 踩坑记录 → 记忆更新
```

---

## 📊 质量评分系统

**五维度加权评分（1.0-5.0）**：

| 维度 | 权重 | 评估点 |
|------|------|--------|
| 目标达成 | 30% | 需求完成度、输出质量 |
| 执行效率 | 25% | 工具选择、步骤冗余、Token 消耗 |
| 工具选择 | 15% | 适合场景？无更好替代？ |
| 用户理解 | 15% | 需求偏差、沟通质量 |
| 知识复用 | 15% | 踩坑积累、Skill 复用 |

---

## 🔔 置信度体系

| 优先级 | 置信度 | 内容类型 |
|--------|--------|---------|
| P0 | [0.9] | 用户明确说"记住" |
| P1 | [0.7] | 强调的选择 |
| P2 | [0.7] | 多次遵循（≥2） |
| P3 | [0.5] | 提及1次未强调 |
| P4 | [0.3] | AI 观察未声明 |

---

## 🚨 Escalation Rules

**必须立即 STOP 并升级**：

| 触发条件 | 处理方式 |
|---------|---------|
| Graphify 安装失败 | STOP，报告错误，提供 pip install |
| 代码库过大超时 | STOP，建议缩小范围或 `--update` |
| 发现可疑代码 | STOP，报告可疑区域，建议 code-review |
| 3次分析均失败 | STOP，建议手动分析 |
| 涉及敏感代码 | STOP，不分析敏感区域 |

---

## ✅ 完成状态协议

| 状态 | 含义 | 场景 |
|------|------|------|
| DONE | 成功完成 | 图谱构建/分析完成/反思完成 |
| DONE_WITH_CONCERNS | 完成但有警告 | 部分成功/有改进空间 |
| BLOCKED | 无法继续 | 工具未安装/无法访问 |
| NEEDS_CONTEXT | 缺少信息 | 需要用户指定范围 |

---

## 🔍 Search Before Building

**三层检查（强制）**：

**Layer 1 - 现有资源**：
```bash
ls graphify-out/ 2>/dev/null
cat graphify-out/GRAPH_REPORT.md 2>/dev/null | head -50
```

**Layer 2 - 工作记忆**：
```bash
cat MEMORY.md 2>/dev/null
cat $(date +%Y-%m-%d).md 2>/dev/null
```

**Layer 3 - Skill 列表**：
```bash
ls ~/.workbuddy/skills/
```

---

## 📦 Graphify 命令速查

```bash
pip install graphifyy

python -m graphify <目录>              # 构建图谱
python -m graphify <目录> --update    # 增量更新
python -m graphify query "<问题>"      # 自然语言查询
python -m graphify path "<A>" "<B>"   # 概念关联路径
```

---

## 🔄 触发词自进化规则

当用户表述未触发本 Skill 时，完成任务后**必须**执行：
1. 分析用户请求中的关键表述
2. 抽象为通用触发词（避免过于具体）
3. 追加到 frontmatter triggers（去重）

---

## 📚 踩坑经验

> AI 自动积累，请勿手动删除。格式：`- 场景：经验要点`

（暂无记录）

---

## 🔗 联动关系

```
上游：代码分析/自我优化请求
下游：code-review / documentation / skill-evolution

关键路径：
代码分析 → Graphify → 发现问题 → TDD → code-review → 反思 → 评分 → 记忆更新
```

---

_融合版 v1.0.0 | 基于 fusion-workflow-hub v1.1.0 + self-improvement v3.0.0_
