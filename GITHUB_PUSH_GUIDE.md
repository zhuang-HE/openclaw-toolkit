# GitHub 推送指南

## 当前状态

✅ 本地提交已完成
⚠️ 需要配置 GitHub 认证

## 推送方法

### 方法 1: 使用 GitHub Token (推荐)

```bash
# 1. 创建 GitHub Token
# 访问：https://github.com/settings/tokens
# 创建新的 token，勾选 repo 权限

# 2. 设置 token 到 git
git config --global credential.helper store

# 3. 推送代码
git push origin master
# 输入 GitHub 用户名
# 输入 GitHub token (作为密码)
```

### 方法 2: 配置 SSH Key

```bash
# 1. 生成 SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. 添加 SSH key 到 GitHub
# 访问：https://github.com/settings/keys
# 添加新的 SSH key (复制 ~/.ssh/id_ed25519.pub 内容)

# 3. 更改 remote 为 SSH
git remote set-url origin git@github.com:zhuang-HE/non-motor-insurance-product.git

# 4. 推送
git push origin master
```

### 方法 3: 使用 GitHub Desktop

1. 下载 GitHub Desktop: https://desktop.github.com/
2. 登录 GitHub 账号
3. 克隆项目到本地
4. 将 workspace 更改复制到克隆的项目
5. 通过 GUI 推送

## 推送的文件

本次更新包含：

**核心优化:**
- integrated/ (3 个集成工具)
- skills/graphify/ (知识图谱技能)
- skills/integrated-search/ (综合搜索技能)
- skills/agentshield/ (安全扫描技能)
- skills/continuous-learning/ (持续学习技能)
- skills/deep-research/ (深度研究技能)
- skills/documentation-lookup/ (文档查找技能)

**Agents (4 个):**
- agents/security-reviewer.md
- agents/build-error-resolver.md
- agents/planner.md
- agents/architect.md

**Commands (3 个):**
- commands/quality-gate.md
- commands/harness-audit.md
- commands/security-scan.md

**Hooks 系统 (24 个):**
- hooks/hooks.json
- hooks/scripts/*.js (23 个脚本)

**数据文件:**
- drone_data/ (货运 + 消费级无人机数据库)
- 无人机 BI 数据库_货运*.csv (多个版本)

**脚本工具 (6 个):**
- scripts/build_knowledge_graph.py
- scripts/generate_cargo_drone_*.py
- scripts/validate_cargo_drone_data.py
- scripts/货运无人机数据收集自动化.py

**文档:**
- RELEASE-v2.0.0.md
- integrated/综合性优化方案.md
- scripts/README_无人机数据库字段优化.md

**总计:** 约 50+ 个新文件，2,452 行代码

## 推送后验证

```bash
# 1. 检查 GitHub 仓库
# 访问：https://github.com/zhuang-HE/non-motor-insurance-product

# 2. 验证最新提交
# 应显示：release: v2.0.0 三大项目综合性融合优化

# 3. 检查文件结构
# 确认 integrated/, skills/, hooks/, drone_data/ 目录存在
```

## 回滚方案

如果推送出现问题：

```bash
# 查看推送前状态
git reflog

# 回滚到推送前
git reset --hard HEAD~1

# 强制推送（谨慎使用）
git push origin master --force
```

## 联系支持

如有问题，请联系：
- GitHub Docs: https://docs.github.com/
- Git 教程：https://git-scm.com/book/zh/v2

---

**创建时间:** 2026-04-09  
**版本:** v2.0.0
