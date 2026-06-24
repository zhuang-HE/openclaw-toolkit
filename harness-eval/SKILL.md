---
name: harness-eval
version: 1.0.0
description: >
Agent: 内建反思评测能力，每次重要任务完成后自动执行五维评测（准确性/Token效率/安全性/稳定性/可维护性），
同时检查: STOM v2.1 合规性（三纯净原则、frontmatter 完整性、规模指标）。
当用户提到评测、eval、复盘、打分、质量检查、binary: eval 时触发。
triggers:
  - 评测
  - eval
  - 复盘
  - 打分
  - 质量检查
  - 五维评测
  - binary eval
  - task evaluation
  - performance review
  - STOM 合规检查
complexity: ⭐⭐
allowed-tools: Read, Write, Edit, Bash, Skill
tags:
  - harness
  - evaluation
  - stom
  - quality
agent_created: true
---

# harness-eval — 反思评测

让 agent 在每次任务执行后拥有内建的反思与评测能力。评测结果持久化到 harness state store，驱动 downstream 的学习、进化和门禁流程。

## 核心职责

1. **五维评测** — 对任务执行过程打分，输出结构化反馈
2. **STOM 合规检查** — 验证 Skill 文件是否符合 STOM v2.1 规范
3. **Binary Eval** — 快速通过/失败二元评估，适用于 pipeline 中的自动判断
4. **六维度健康评分** — 对单个 Skill 的整体健康状态打分

## State Store

所有历史数据存储在 `~/.workbuddy/harness/evals/{task_id}.json`，每次评测追加一条记录。

Eval 结果 JSON 结构：

```json
{
  "task_id": "字符串",
  "timestamp": "ISO 8601",
  "type": "task | skill | binary",
  "scores": { "accuracy": 85, "token_efficiency": 70, "safety": 95, "stability": 80, "maintainability": 75 },
  "overall": 81,
  "comments": ["逐项评语，直接可操作"],
  "suggestions": ["改进建议列表"],
  "stom_compliance": { "passed": true, "issues": [] },
  "raw_output": "原始评测文本"
}
```

## 五维评测标准

| 维度 | 权重 | 评分依据 |
|------|------|---------|
| 准确性 | 30% | 任务是否达成目标，输出是否正确 |
| Token 效率 | 20% | 推理步数是否精简，有无冗余操作 |
| 安全性 | 20% | 是否处理了敏感数据，有无注入风险 |
| 稳定性 | 15% | 错误处理是否完备，是否可复现 |
| 可维护性 | 15% | 输出是否可复用，是否留下可追溯日志 |

## STOM 合规检查（v2.1）

在评测 Skill 文件时，额外执行 STOM 合规扫描：

| 级别 | 检查项 | 评分影响 |
|------|-------|---------|
| P0 | 平台语法污染（三纯净原则-正文纯度） | 一票否决 |
| P0 | 工具名未在 allowed-tools 声明 | 一票否决 |
| P0 | 绝对路径写死（三纯净原则-路径独立） | 一票否决 |
| P1 | 缺少必填 frontmatter 字段 | -20 分 |
| P1 | description 过短（<50 字符） | -15 分 |
| P1 | 目录名与 name 不匹配 | -15 分 |
| P2 | 缺少 version 字段 | -10 分 |
| P2 | triggers 数组缺失或不足（<5 个） | -10 分 |
| P3 | SKILL.md 行数超过 350 或 超过 15KB | 仅警告 |
| P3 | references 内互引 | 仅警告 |

## Binary Eval 模式

当只需要快速通过/失败判断时（如 CI pipeline 中），使用 Binary Eval：

- **通过条件**：五维总分 ≥ 基线阈值（默认 70）+ 无 P0 问题
- **输出**：`{"passed": true/false, "score": 81, "blockers": []}`
- **用途**：CI gate 的前置检查、evolve 后的快速验证

## 六维度健康评分（来自 STOM v2.1 skill-evolution Phase 4）

| 维度 | 权重 | 得分规则 |
|------|------|---------|
| 版本同步 | 15% | 与目录/CHANGELOG 一致 = 100 |
| 触发词覆盖 | 20% | min(count×10, 100)，盲区 -20 |
| 踩坑经验 | 10% | 无=30 / 有=60 / 整合=80 / ≥5=100 |
| CI 通过 | 25% | P0=0 / P1=50 / P2=80 / clean=100 |
| Token 效率 | 15% | ≤250行=100 / 251-350=80 / >350=40 |
| 活跃度 | 15% | 使用=100 / 更新=80 / 无=40 |

**等级**：≥80🟢 | 60-79🟡 | 40-59🟠 | <40🔴

## 执行流程

1. 确定评测类型（task / skill / binary）
2. 如果是 task 评测：读取 agent 执行过程（memory log / 输出）→ 逐维度打分 → 生成改进建议
3. 如果是 skill 评测：读取 Skill 文件 → STOM 合规扫描 → 六维度健康评分 → 生成健康报告
4. 如果是 binary eval：快速执行五维评测 → 与基线比较 → 输出通过/失败
5. 结果写入 `~/.workbuddy/harness/evals/{task_id}.json`
6. 追加 evolution log

## 输出规范

评测报告以表格为主：

```
## Eval 结果 — {task_id}

| 维度 | 得分 | 评级 |
|------|------|------|
| 准确性 | 85 | 🟢 |
| Token 效率 | 70 | 🟡 |
| 安全性 | 95 | 🟢 |
| 稳定性 | 80 | 🟢 |
| 可维护性 | 75 | 🟡 |
| **综合** | **81** | 🟢 |

### 改进建议
1. [Token] 第3步可合并为单次查询，预计节省 200 tokens
2. [可维护性] 输出缺少日志索引，建议追加 task_id

### STOM 合规
✅ 通过，无 P0/P1 问题
```

## 与其他 harness Skill 的关系

- **harness-learning**：eval 完成后自动触发 learning，提取模式
- **harness-gate**：eval 结果作为 gate 判断的输入之一
- **harness-evolve**：健康评分为 evolve 提供优先级排序依据

## 🔄 触发词自进化

用户表述未激活本 Skill 时：
1. 分析关键表述 → 抽象通用触发词 → 追加到 frontmatter triggers → 去重。

## 📚 踩坑经验

> 格式：`- 场景：经验要点`（≥2 次尝试才记录）
- 暂无踩坑记录，待实际使用后自动积累
