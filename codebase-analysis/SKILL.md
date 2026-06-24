---
name: codebase-analysis
version: 1.2.0
description: "代码库深度分析 Skill，基于 codebase-memory-mcp MCP Server。支持 158 种语言文件级分析；TypeScript/JavaScript/Python 支持函数级分析（调用链、死代码检测）。⚠️ 重要：索引时必须使用纯 ASCII 路径（不含中文），否则 Python 函数级分析会静默失败。"
triggers:
  - 代码库分析
  - 架构分析
  - 索引项目
  - 代码搜索
  - 文件树
  - 影响分析
  - 索引代码
  - 查看架构
  - 调用链
  - 死代码
  - 语义搜索
  - codebase analysis
  - code architecture
  - index repository
  - dead code
  - semantic search
  - call chain
  - 函数调用链
  - 代码影响分析
metadata:
  source: user
  emoji: 🔍
  agent_created: true
allowed_tools: Read, Edit, Bash, Skill, DeferExecuteTool
---

# Codebase Analysis Skill v1.2

## ⚠️ 重要：路径要求（必读）

**索引项目时必须使用纯 ASCII 路径！**

| 路径示例 | 状态 | 说明 |
|---------|------|------|
| `C:/quant-method` | ✅ | 纯 ASCII，所有功能正常 |
| `C:/temp-py-test` | ✅ | 纯 ASCII，所有功能正常 |
| `C:/Users/庄赫/quant-method` | ❌ | 含中文，Python 函数级分析静默失败 |
| `C:/Users/庄赫/temp-py-test` | ❌ | 含中文，Python 函数级分析静默失败 |

**原因**：路径含非 ASCII 字符时，Hybrid LSP 静默失败，只提取文件级节点。
**对应 GitHub issue**：#571（Project name strips non-ASCII (CJK) characters from path）

**解决方案**：
```bash
# 方法1：复制项目到 ASCII 路径（推荐）
cp -r "C:/Users/庄赫/quant-method" "C:/quant-method"
# 然后索引 C:/quant-method

# 方法2：创建符号链接
mklink /J "C:\qm" "C:\Users\庄赫\quant-method"
# 然后索引 C:/qm
```

---

## 核心能力矩阵

| 功能 | 文件级（所有语言） | 函数级（TS/JS/Python） |
|------|----------------|----------------|
| 索引代码库 | ✅ | ✅（额外提取函数/类节点） |
| 架构概览（文件树） | ✅ | ✅（+ 调用图、分层） |
| 代码搜索（BM25） | ✅ | ✅ |
| Cypher 查询 | ✅（文件节点） | ✅（文件+函数节点） |
| Git 变更影响 | ✅（文件级） | ✅（函数级） |
| 调用链追踪 | ❌ | ✅ |
| 死代码检测 | ❌ | ✅ |
| 语义搜索 | ❌ | ✅ |

> **Python 函数级分析**：v1.2 已验证可用（需使用 ASCII 路径）。之前误判为工具 bug，实为路径问题。

---

## Workflow 1：快速架构分析（所有语言）

**适用**：首次接触代码库，快速理解整体结构。

**步骤**：
1. 询问用户项目路径
2. **检查路径是否含非 ASCII 字符**，如有则提示用户复制到 ASCII 路径
3. 调用 `index_repository` 索引（如未索引）
4. 调用 `get_architecture` 获取概览
5. 返回结构化报告

**示例对话**：
```
用户：分析 C:/Users/庄赫/quant-method 的架构
→ 检查路径：含中文 ❌
→ 提示：请先将项目复制到 ASCII 路径，如 C:/quant-method
→ 用户：已复制到 C:/quant-method
→ 调用 index_repository({"repo_path": "C:/quant-method"})
→ 调用 get_architecture({"project": "C-quant-method", "aspects": ["all"]})
→ 返回：语言分布、文件树、节点/边统计、分层
```

---

## Workflow 2：文件搜索（所有语言）

**适用**：按关键词查找文件。

**步骤**：
1. 询问搜索关键词和项目名
2. 调用 `search_code`（正则）或 `search_graph`（节点名）
3. 返回匹配文件列表

**示例**：
```
用户：在 quant-method 中搜索包含 calculator 的文件
→ 调用 search_code({"project": "C-quant-method", "pattern": "calculator"})
→ 返回：匹配的文件路径列表
```

---

## Workflow 3：Cypher 查询（所有语言）

**适用**：复杂查询文件/函数节点属性。

**示例**：
```
用户：查询 quant-method 中所有 Python 文件
→ 调用 query_graph({"project": "C-quant-method", "query": "MATCH (f:File) WHERE f.path ENDS WITH '.py' RETURN f.name, f.path"})
```

---

## Workflow 4：Git 变更影响分析（所有语言）

**适用**：修改代码前，评估影响范围。

**步骤**：
1. 调用 `detect_changes` 检测未提交变更
2. 返回变更文件列表
3. （如项目有函数节点）调用 `trace_path` 追踪影响的函数

**限制**：文件级影响分析所有语言可用；函数级需项目有函数节点。

---

## Workflow 5：函数级深度分析（TS/JS/Python）

**适用**：TypeScript/JavaScript/Python 项目，需要调用链、死代码检测、语义搜索。

**前提**：
- 项目已用 `mode="full"` 索引
- 路径为纯 ASCII
- `get_architecture` 返回了 Method/Function/Class 节点

**步骤**：
1. 验证项目是否有函数节点（`get_architecture` 查看 node_labels）
2. 调用 `trace_path` 追踪调用链
3. 调用 `dead_code_detection` 检测死代码
4. 调用 `semantic_query` 语义搜索

---

## 输出格式

### 架构概览报告模板

```markdown
## 架构概览：<项目名>

### 基本信息
- 项目路径：<path>
- 总节点数：<nodes>
- 总边数：<edges>
- 语言分布：<lang1> <count> 文件, <lang2> <count> 文件

### 文件树（前 20 个文件）
<递归文件树结构>

### 节点类型分布
| 类型 | 数量 |
|------|------|
| Method | <count> |
| Class | <count> |
| Function | <count> |
| File | <count> |

### 架构分层
| 层 | 模块 | fan-in | fan-out |
|------|------|--------|---------|
| entry | cli | 0 | 4 |
| core | strategy | 36 | 0 |

### 热点函数（fan-in 排行）
1. <function_name>（<fan_in> 次调用）
2. ...

### 建议
- <基于分层和热点函数的建议>
```

---

## 工具参数速查

### index_repository
```json
{
  "repo_path": "C:/path/to/project",  // 必需，⚠️ 必须是纯 ASCII 路径
  "mode": "full"  // 可选："fast"|"full"，默认 "full"
}
```

### get_architecture
```json
{
  "project": "C-quant-method",  // 必需，从 list_projects 获取（ASCII 格式）
  "aspects": ["all"]  // 可选：["structure", "languages", "entry_points", "all"]
}
```

### search_code（正则搜索）
```json
{
  "pattern": "calculator",  // 必需，正则模式
  "project": "C-quant-method",  // 必需
  "mode": "compact",  // 可选："compact"|"full"|"files"
  "limit": 10  // 可选，默认 10
}
```

### search_graph（节点名搜索）
```json
{
  "project": "C-quant-method",  // 必需
  "label": "Function",  // 可选：按节点类型过滤
  "query": "calculator",  // 可选：BM25 全文搜索
  "limit": 10  // 可选，默认 200
}
```

### query_graph（Cypher 查询）
```json
{
  "project": "C-quant-method",  // 必需
  "query": "MATCH (f:Function) RETURN f.name LIMIT 5"  // 必需，Cypher 查询
}
```

### trace_path（调用链追踪）
```json
{
  "function_name": "FactorRegistry.get",  // 必需，函数名（可带类名）
  "project": "C-quant-method",  // 必需
  "direction": "both",  // 可选："inbound"|"outbound"|"both"
  "depth": 3  // 可选，默认 3
}
```

### search_graph（语义搜索，通过 semantic_query 参数）
```json
{
  "project": "C-quant-method",  // 必需
  "semantic_query": ["calculate", "moving average"],  // 必需，关键词数组（非字符串！）
  "limit": 5  // 可选，默认 200
}
```
> **注意**：`semantic_query` 是 `search_graph` 的参数，不是独立工具。必须是数组格式，如 `["calculate", "moving", "average"]`。

### query_graph（死代码检测，通过 Cypher 查询）
```cypher
// 查找无调用者的函数（死代码）
MATCH (f:Function)
OPTIONAL MATCH (f)<-[c:CALLS]-()
WITH f, count(c) as caller_count
WHERE caller_count = 0
RETURN f.name, f.qualified_name
LIMIT 10
```
> **注意**：`dead_code_detection` 不是独立工具，需通过 `query_graph` 执行 Cypher 查询实现。

### detect_changes（Git 变更检测）
```json
{
  "project": "C-quant-method"  // 必需
}
```

---

## 常见错误和修复

### 错误 1：路径包含非 ASCII 字符

**症状**：索引后只有 File/Folder/Project 节点，没有 Method/Function/Class 节点。

**修复**：
1. 将项目复制到纯 ASCII 路径（如 `C:/quant-method`）
2. 重新索引
3. 验证节点类型（`get_architecture` 查看 node_labels）

**预防**：在 Workflow 1 中增加路径检查步骤。

---

### 错误 2：project 参数值不正确

**症状**：工具返回 "project not found" 或空结果。

**修复**：使用 `list_projects` 获取正确的项目名（ASCII 格式）。

```python
# 项目路径：C:/quant-method
# 正确项目名：C-quant-method
# 错误项目名：C-Users-庄赫-quant-method（中文路径会被截断）
```

---

### 错误 3：search_code 和 search_graph 混淆

**区别**：
- `search_code`：正则搜索代码内容（基于 grep）
- `search_graph`：搜索节点名（基于图数据库）

**建议**：
- 搜索函数名 → `search_graph`（更快）
- 搜索代码模式 → `search_code`（更灵活）

---

## 语言支持矩阵

| 语言 | 文件级 | 函数级（Hybrid LSP） | 测试状态 |
|------|--------|----------------|---------|
| TypeScript | ✅ | ✅ | ✅ 已验证 |
| JavaScript | ✅ | ✅ | ✅ 已验证 |
| Python | ✅ | ✅（需 ASCII 路径） | ✅ 已验证（v1.2 修复） |
| Go | ✅ | ✅ | 未测试 |
| Rust | ✅ | ✅ | 未测试 |
| C/C++ | ✅ | ⚠️（语法级，无类型分析） | 未测试 |
| Java | ✅ | ✅ | 未测试 |
| 其他 151 种 | ✅（语法级） | ❌ | 未测试 |

---

## 踩坑经验

- **场景**：Python 项目索引后只有 File/Folder/Project 节点
  **经验**：先检查路径是否含中文/特殊字符！这是 #571 issue，不是工具 bug。复制到 ASCII 路径即可修复。

- **场景**：项目路径包含中文，`project` 参数怎么写都不对
  **经验**：用 `list_projects` 获取实际项目名（会自动转 ASCII），不要用路径直接猜。

- **场景**：`search_graph` 用 `path` 参数搜不到文件
  **经验**：用 `query`（BM25）或 `label`（节点类型）代替。`search_code` 适合搜代码内容。

- **场景**：索引大型项目（>10k 文件）超时
  **经验**：首次索引可能需要 3-5 分钟，耐心等待。后续增量更新很快。

- **场景**：调用 `trace_path` 返回空结果
  **经验**：先检查项目是否有函数节点（`get_architecture` 查看 node_labels）。如果没有，说明路径含非 ASCII 字符。

---

## Resources

- **GitHub**: https://github.com/DeusData/codebase-memory-mcp
- **PyPI**: https://pypi.org/project/codebase-memory-mcp/
- **已知问题**: 参见 GitHub issues #571（非 ASCII 路径）、#581（内存泄漏）
- **修复验证**: v1.2 已验证 Python 函数级分析可用（需 ASCII 路径）

---

## 触发词自进化规则

当用户输入某种表述但本 Skill 未被自动激活时，完成任务后**必须**执行：
1. 分析用户原始请求中的关键表述
2. 将其抽象为通用触发词（避免过于具体的个例）
3. 用 Edit 工具将触发词追加到本文件 YAML frontmatter `triggers` 字段末尾
4. 不得重复添加已存在的触发词
