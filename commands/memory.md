# /memory - 记忆管理命令

trigger: /memory [action] [options]

## Description
记忆系统管理，支持整理、查询、归档等操作。

## Actions

| Action | 说明 | 示例 |
|--------|------|------|
| `status` | 查看状态 | `/memory status` |
| `consolidate` | 整理记忆 | `/memory consolidate` |
| `search` | 搜索记忆 | `/memory search keyword` |
| `archive` | 归档旧记忆 | `/memory archive --days=30` |
| `export` | 导出记忆 | `/memory export --format=md` |

## Examples

### 查看状态
```bash
/memory status
```

输出：
```markdown
## 记忆系统状态

### 存储概览
- MEMORY.md: 45 KB
- 活跃记忆条目：128 条
- memory/ 文件：12 个

### 最近整理
- 上次整理：2026-03-28
- 待处理日志：5 个
- 建议：执行记忆整理

### 记忆分类
| 分类 | 条目数 | 最后更新 |
|------|--------|----------|
| 用户偏好 | 25 | 2026-04-01 |
| 项目上下文 | 40 | 2026-04-02 |
| 技能和能力 | 30 | 2026-03-30 |
| 教训和洞察 | 33 | 2026-04-01 |
```

### 整理记忆
```bash
/memory consolidate
```

输出：
```markdown
## 记忆整理报告

### 整理周期
- 开始：2026-03-28
- 结束：2026-04-03
- 处理文件：5 个

### 新增记忆

#### 用户偏好
- 偏好使用飞书作为主要沟通渠道
- 代码审查优先关注安全问题

#### 项目进展
- OpenClaw 技能迁移项目：已完成核心 Skills 创建
- Claude Code 研究：完成架构分析

#### 重要决策
- 采用 Skills + Agents 双层架构
- 命令系统使用 Markdown 定义

### 学习洞察
- 多 Agent 协作适合复杂任务分解
- 记忆定期整理保持系统高效

### 归档内容
- 已归档文件：3 个
- 归档路径：memory/archive/2026-03/

### 记忆统计
- MEMORY.md 大小：48 KB (+3 KB)
- 活跃记忆条目：135 条 (+7 条)

---
整理完成！是否查看详细报告？(是/否)
```

### 搜索记忆
```bash
/memory search Agent
```

输出：
```markdown
## 搜索结果："Agent"

### 相关记忆 (5 条)

1. **Agent 架构设计** (2026-04-02)
   采用研究员、审查员、文档员三层 Agent 架构...

2. **多 Agent 协作模式** (2026-04-01)
   复杂任务通过 sessions_spawn 启动多个子代理并行...

3. **Agent 记忆持久化** (2026-03-30)
   每个 Agent 应有独立记忆，通过 memory/目录管理...

...

---
是否查看完整内容？(是/否)
```

### 归档旧记忆
```bash
/memory archive --days=30
```

输出：
```markdown
## 归档操作

### 归档范围
- 时间范围：2026-02-01 之前
- 文件数量：8 个
- 总大小：120 KB

### 归档目标
- 目录：memory/archive/2026-02/
- 保留摘要：✓

### 影响
- 归档后 memory/ 目录：4 个文件
- MEMORY.md 保持不变

---
是否执行归档？(确认/取消)
```

## Related
- skill: memory-consolidation
- command: /status

## Notes
- 定期整理保持记忆高效
- 归档文件可随时查看
- 敏感记忆注意保密
