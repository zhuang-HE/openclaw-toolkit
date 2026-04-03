# /git - Git 工作流命令

trigger: /git [action] [options]

## Description
Git 版本控制操作，支持智能提交、分支管理、PR 准备等。

## Actions

| Action | 说明 | 示例 |
|--------|------|------|
| `status` | 查看状态 | `/git status` |
| `commit` | 智能提交 | `/git commit` |
| `branch` | 分支管理 | `/git branch feature/xxx` |
| `merge` | 合并分支 | `/git merge main` |
| `pr` | 准备 PR | `/git pr` |
| `log` | 查看历史 | `/git log -10` |
| `diff` | 查看差异 | `/git diff` |

## Examples

### 查看状态
```bash
/git status
```

输出：
```markdown
## Git 状态

**当前分支**: feature/oauth2-login

**变更文件**:
| 文件 | 状态 | 行数变化 |
|------|------|----------|
| src/auth.ts | 修改 | +150 -20 |
| tests/auth.test.ts | 新增 | +80 -0 |
| docs/auth.md | 修改 | +30 -5 |

**建议操作**:
- 执行 `/git commit` 提交变更
- 执行 `/git branch` 创建新分支
```

### 智能提交
```bash
/git commit
```

输出：
```markdown
## 提交建议

### 提交 1: `feat(auth): add OAuth2 login support`
**文件**:
- src/auth.ts (+150 -20)
- tests/auth.test.ts (+80)

**变更说明**:
- 新增 OAuth2 认证流程
- 添加 Google 和 GitHub  provider
- 添加相关测试用例

### 提交 2: `docs(auth): update authentication guide`
**文件**:
- docs/auth.md (+30 -5)

**变更说明**:
- 更新认证文档
- 添加 OAuth2 配置说明

---
是否执行上述提交？(确认/修改/取消)
```

### 创建分支
```bash
/git branch feature/new-feature
```

输出：
```markdown
## 分支操作

**操作**: 创建新分支
**分支名**: feature/new-feature
**基于分支**: main

```bash
git checkout -b feature/new-feature
```

是否执行？(确认/取消)
```

### 准备 PR
```bash
/git pr
```

输出：
```markdown
## PR 准备

### 变更概览
- 分支：feature/oauth2-login → main
- 提交数：5
- 文件变更：12
- 行数变化：+450 -80

### PR 描述草稿
```markdown
## ✨ 功能：OAuth2 登录支持

### 变更类型
- [x] ✨ 新功能 (feat)

### 描述
添加 OAuth2 登录支持，包括 Google 和 GitHub provider。

### 变更详情
- 新增 OAuth2 认证流程
- 添加 provider 配置
- 添加测试用例
- 更新文档

### 测试
- [x] 单元测试通过
- [x] 手动测试完成

### 检查清单
- [x] 代码符合项目规范
- [x] 已更新相关文档
```

### 建议 Reviewer
- @tech-lead (代码审查)
- @security-team (安全审查)

---
是否推送到远程并创建 PR？(确认/取消)
```

## Related
- skill: git-workflow
- command: /review, /docs

## Notes
- 敏感操作需要确认
- 提交前建议先审查代码
- 大变更建议分多次提交
