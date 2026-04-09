# Graphify Skill for OpenClaw

## Purpose

将任何文件夹（代码、文档、数据）转换为可查询的知识图谱，实现 71.5 倍 Token 节省。

## When to Use

- 理解大型代码库结构
- 查询跨文件的架构决策
- 从论文、文档、截图中提取知识
- 需要持久化知识库（跨会话）
- 减少 LLM Token 消耗

## Quick Start

```bash
# 安装
/graphify install

# 构建图谱
/graphify .                    # 当前目录
/graphify ./drone_data        # 指定目录
/graphify ./skills --mode deep  # 深度模式

# 查询图谱
/graphify query "货运无人机的风险系数如何计算？"
/graphify path "有效载荷" "保险费率"
/graphify explain "Leiden 聚类"

# 增量更新
/graphify ./drone_data --update  # 只处理变更文件
```

## Output

```
graphify-out/
├── graph.html          # 交互式图谱（点击节点、搜索、过滤）
├── GRAPH_REPORT.md     # 上帝节点、意外连接、建议问题
├── graph.json          # 持久化图谱（可查询）
└── cache/              # SHA256 缓存（增量更新）
```

## Core Features

### 1. 两步提取流程

**Pass 1: AST 确定性提取（无需 LLM）**
- 代码结构：类、函数、导入、调用图
- 文档字符串、理性注释（# WHY:, # NOTE:, # IMPORTANT:）
- 支持 20 种语言（Python, JS, TS, Go, Rust, Java 等）

**Pass 2: Claude 并行提取（Docs/Images）**
- 概念提取
- 关系提取
- 设计理性
- 跨模态连接（代码↔文档↔图像）

### 2. 图谱结构

**节点类型：**
- `code_entity` - 代码实体（类、函数、模块）
- `concept` - 概念（来自文档、论文）
- `rationale` - 设计理性（为什么这样写）
- `god_node` - 高度数节点（连接一切的核心概念）

**关系类型：**
- `calls` - 调用关系
- `imports` - 导入关系
- `implements` - 实现关系
- `related_to` - 相关关系
- `semantically_similar_to` - 语义相似（INFERRED）
- `designed_by` - 设计者
- `based_on` - 基于（论文、文档）

**置信度标记：**
- `EXTRACTED` (1.0) - 直接从源文件提取
- `INFERRED` (0.0-1.0) - 合理推断，带置信度评分
- `AMBIGUOUS` - 模糊，需要人工审查

### 3. 社区发现（无 Embeddings）

使用 **Leiden 算法** 基于边密度聚类：
- 图谱结构本身就是相似性信号
- 无需单独的 embedding 步骤
- 语义相似边直接影响社区发现

### 4. Token 优化

**基准测试：**
- 52 个文件（代码 + 论文 + 图像）
- **71.5 倍 Token 节省**（相比读取原始文件）
- SHA256 缓存：只重新处理变更文件

**查询策略：**
1. 先看 `GRAPH_REPORT.md`（高层概述）
2. 用 `/graphify query` 提取子图谱（具体问题）
3. 将聚焦的输出给 LLM（而非 dump 整个图谱）

## Integration with OpenClaw

### Always-On Hook

安装后自动注入 `AGENTS.md`：

```markdown
## Graphify Knowledge Graph

Before answering architecture questions:
1. Read `graphify-out/GRAPH_REPORT.md` for god nodes and community structure
2. Use graph structure to navigate instead of keyword matching
3. For specific questions, use `/graphify query` to extract subgraph
```

### Commands

| Command | Description |
|---------|-------------|
| `/graphify .` | 构建当前目录的知识图谱 |
| `/graphify ./path` | 构建指定目录的图谱 |
| `/graphify ./path --update` | 增量更新（只处理变更） |
| `/graphify query "question"` | 查询图谱 |
| `/graphify path "A" "B"` | 查找 A 到 B 的路径 |
| `/graphify explain "concept"` | 解释概念 |
| `/graphify add <URL>` | 添加论文/文档到图谱 |
| `/graphify --watch` | 自动同步（文件变更时更新） |
| `/graphify --wiki` | 生成可爬取的 Wiki |

### .graphifyignore

排除不需要的文件夹：

```
# .graphifyignore
node_modules/
dist/
*.generated.py
logs/
*.backup.csv
```

## Use Cases in OpenClaw

### 1. 无人机数据库知识图谱

```bash
/graphify ./drone_data
```

**提取：**
- 机型→性能规格→保险费率 的连接
- 事故模式聚类
- 风险因子关联

**查询示例：**
```
/graphify query "货运无人机的有效载荷与保险费率的关系"
/graphify path "最大起飞重量" "货物损失率"
```

### 2. 保险产品知识图谱

```bash
/graphify ./skills/agentshield
```

**提取：**
- 保险条款→风险类型→费率计算 的连接
- 跨产品的共同模式
- 监管要求关联

### 3. 代码库理解

```bash
/graphify ./scripts
```

**提取：**
- 脚本调用图
- 数据流分析
- 配置依赖关系

### 4. 文档+论文+截图混合

```bash
/graphify ./docs --mode deep
```

**支持：**
- Markdown 文档
- PDF 论文
- 截图、图表
- 白板照片（Claude Vision）

## Advanced Features

### 增量更新

```bash
# 首次构建
/graphify ./drone_data

# 后续更新（只处理变更文件）
/graphify ./drone_data --update

# 后台监听（代码变更自动更新）
/graphify ./drone_data --watch
```

### Git Hooks

```bash
# 安装 Git Hooks
graphify hook install

# 自动在 commit 和 branch switch 后重建图谱
# 失败时 git 会显示错误（不静默继续）
```

### Wiki 生成

```bash
/graphify ./drone_data --wiki
```

生成 Wikipedia 风格的 Markdown：
- `index.md` - 入口
- 每个社区一篇文章
- 上帝节点专题文章

### 导出格式

```bash
/graphify ./data --svg       # 导出 SVG
/graphify ./data --graphml   # Gephi, yEd
/graphify ./data --neo4j     # Neo4j Cypher
/graphify ./data --mcp       # MCP 服务器
```

## Token Budget Control

```bash
# 限制查询输出 Token 数
/graphify query "show auth flow" --budget 1500

# DFS 模式（追踪具体路径）
/graphify query "what connects attention to optimizer?" --dfs
```

## Confidence Scoring

每个 INFERRED 边都有置信度：

```json
{
  "source": "有效载荷",
  "target": "高风险等级",
  "relation": "correlates_with",
  "confidence": 0.85,
  "tag": "INFERRED",
  "source_file": "货运无人机数据库_完整版.csv",
  "rationale": "高有效载荷机型通常用于高价值货物运输"
}
```

## Best Practices

### Do's
✅ 首次运行在完整数据集上
✅ 使用 `--update` 增量更新
✅ 查询时先用 `GRAPH_REPORT.md` 概览
✅ 用 `--budget` 控制 Token 消耗
✅ 定期用 `--wiki` 生成人类可读文档

### Don'ts
❌ 不要将整个 graph.json paste 到 prompt
❌ 不要在每次小改动后全量重建
❌ 不要忽略置信度标记
❌ 不要在 `.graphifyignore` 中排除核心数据

## Performance

| Corpus | Files | Token Reduction | Output |
|--------|-------|-----------------|--------|
| Karpathy repos + papers + images | 52 | 71.5x | worked/ |
| Graphify source + Transformer paper | 4 | 5.4x | worked/ |
| Small library | 6 | ~1x | worked/ |

**Token 节省随数据集规模增长：**
- 6 个文件：适合 context window，图谱价值在于结构清晰
- 52 个文件：71 倍+ 节省
- 100+ 文件：100 倍+ 节省

## Troubleshooting

### Graph build fails
```bash
# 检查缓存
ls -la graphify-out/cache/

# 强制全量重建
rm -rf graphify-out/
/graphify ./data
```

### Query returns nothing
```bash
# 检查图谱是否存在
ls graphify-out/graph.json

# 查看上帝节点
cat graphify-out/GRAPH_REPORT.md

# 尝试更宽泛的查询
/graphify query "无人机"  # 而非 "无人机 BI 数据库_货运完整版"
```

### Token budget exceeded
```bash
# 降低 budget
/graphify query "..." --budget 500

# 使用 DFS 模式（更聚焦）
/graphify query "..." --dfs
```

## Integration Examples

### OpenClaw Session

```markdown
# Before answering
[Graphify] Knowledge graph exists in ./drone_data
Reading: graphify-out/GRAPH_REPORT.md

[Graphify] Found 3 god nodes:
1. 有效载荷 (degree: 15)
2. 保险费率 (degree: 12)
3. 风险等级 (degree: 10)

[Graphify] Community structure:
- Community 1: 性能规格 (8 nodes)
- Community 2: 保险数据 (6 nodes)
- Community 3: 事故统计 (5 nodes)

Now answering user question with graph context...
```

### Query Output Format

```markdown
## Graph Query: "货运无人机的风险系数如何计算？"

### Relevant Nodes (5)
1. **风险系数** (god_node, degree: 12)
   - Source: 无人机 BI 数据库_货运对齐版.csv
   - Communities: 保险数据

2. **风险等级** (degree: 10)
   - Source: 无人机 BI 数据库_货运对齐版.csv

3. **货物损失率** (degree: 8)
   - Source: 无人机 BI 数据库_货运对齐版.csv

### Relationships (4)
1. 风险等级 → 风险系数 [EXTRACTED, confidence: 1.0]
   - Relation: determines
   - Source: 货运无人机真实数据核对报告.md

2. 货物损失率 → 风险等级 [INFERRED, confidence: 0.85]
   - Relation: correlates_with
   - Rationale: 高损失率通常对应高等级风险

### Answer
基于图谱结构，风险系数的计算逻辑：
1. 首先确定风险等级（高/中/低）
2. 风险等级由货物损失率决定（阈值：0.1‰, 0.5‰）
3. 每个风险等级对应固定系数（高：1.7, 中：1.5, 低：1.45）

详见：货运无人机真实数据核对报告.md
```

## Resources

- **GitHub:** https://github.com/safishamsi/graphify
- **PyPI:** `graphifyy` (临时名称)
- **Docs:** https://github.com/safishamsi/graphify/blob/v3/README.md
- **Worked Examples:** https://github.com/safishamsi/graphify/tree/v3/worked/
