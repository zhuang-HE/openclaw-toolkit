# /review - 代码审查命令

trigger: /review [file|directory] [--depth=1|2|3] [--focus=security|performance|quality]

## Description
对指定代码文件或目录进行质量审查和安全审计。

## Arguments

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| file|dir | string | ✗ | 当前目录 | 目标文件/目录 |
| --depth | number | ✗ | 2 | 审查深度 (1=快速/2=标准/3=深度) |
| --focus | string | ✗ | all | 审查重点 (security/performance/quality/all) |
| --language | string | ✗ | auto | 代码语言 (auto/js/ts/py/go/rust) |

## Handler

1. **定位目标**
   - 解析文件/目录路径
   - 验证文件存在
   - 识别代码语言

2. **配置审查策略**
   - depth=1: 快速扫描，只查 Blocker
   - depth=2: 标准审查，查 Blocker+High
   - depth=3: 深度审查，全面分析

3. **启动审查**
   - 调用 code-review skill
   - 或启动 code-reviewer agent
   - 传递审查参数

4. **返回报告**
   - 显示审查结果
   - 按优先级排序问题
   - 提供修复建议

## Examples

```bash
# 审查当前文件
/review

# 审查指定文件
/review src/auth.ts

# 审查整个目录
/review src/ --depth=3

# 专注安全审查
/review src/api/ --focus=security

# 性能审查
/review src/database/ --focus=performance
```

## Output Example

```markdown
# 代码审查报告

## 审查概览
- 文件：src/auth.ts
- 语言：TypeScript
- 行数：342 行
- 审查时间：2026-04-03 14:00

## 问题汇总
| 级别 | 数量 | 说明 |
|------|------|------|
| 🔴 Blocker | 1 | 必须立即修复 |
| 🟠 High | 2 | 应尽快修复 |
| 🟡 Medium | 3 | 建议修复 |
| 🟢 Low | 2 | 可选优化 |

## 详细问题

### 🔴 SQL 注入风险
**位置**: `src/auth.ts:45`

**问题描述**:
用户输入直接拼接到 SQL 查询中

**风险**:
攻击者可构造恶意输入执行任意 SQL

**修复建议**:
```typescript
// 修复前
const query = `SELECT * FROM users WHERE id = ${userId}`;

// 修复后
const query = 'SELECT * FROM users WHERE id = $1';
await db.query(query, [userId]);
```

## 总体评分
- 安全性：⭐⭐⭐☆☆ (3/5)
- 代码质量：⭐⭐⭐⭐☆ (4/5)
- 性能：⭐⭐⭐☆☆ (3/5)
- 可维护性：⭐⭐⭐⭐☆ (4/5)
```

## Related
- skill: code-review
- agent: code-reviewer
- command: /docs, /git

## Notes
- 大文件可能需要较长时间
- 敏感代码审查注意保密
- 可配合 linter 工具使用
