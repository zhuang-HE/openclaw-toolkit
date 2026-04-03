# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

---

# 周期性任务配置

## 每日任务 (建议 heartbeat 时检查)
- [ ] 检查未读消息/邮件
- [ ] 查看日历事件 (24-48h 内)
- [ ] 天气检查 (如用户可能外出)

## 每周任务
- [ ] 记忆整理 (每周日) - 调用 `/memory consolidate`
- [ ] 项目进度回顾
- [ ] Skills 使用情况分析

## 每月任务
- [ ] MEMORY.md 全面审查
- [ ] 归档旧日志文件
- [ ] Skills 更新检查

---

# 自动任务配置

## 记忆整理
- 触发条件：memory/ 目录超过 7 个文件
- 执行：调用 memory-consolidation skill
- 输出：整理报告

## 技能使用统计
- 触发条件：每 7 天
- 执行：分析技能调用频率
- 输出：使用报告和优化建议
