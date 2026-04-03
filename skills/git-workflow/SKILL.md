# Git Workflow Skill

name: git-workflow

## Task
Git 版本控制和协作工作流管理，提供智能提交、分支管理和 PR 准备。

## Commands

### 代码提交
- 智能生成 commit message
- 支持约定式提交规范
- 批量文件分组提交

### 分支管理
- 创建功能分支
- 合并策略建议
- 分支清理

### 冲突解决
- 分析冲突原因
- 提供解决建议
- 验证解决结果

### PR 准备
- Diff 分析
- Changelog 生成
- Reviewer 建议

## Workflow

### Phase 1: 状态分析
1. 执行 `git status` 分析变更
2. 执行 `git diff` 查看具体内容
3. 识别变更类型（feat/fix/docs/chore 等）
4. 评估提交范围

### Phase 2: 提交准备
1. 按逻辑分组文件
2. 为每组生成 commit message
3. 遵循约定式提交规范
4. 执行提交（需确认）

### Phase 3: 验证
1. 检查提交结果
2. 验证 pre-commit hooks
3. 运行相关测试
4. 确认无破坏性变更

## Commit Message Convention

遵循 [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(auth): add OAuth2 support` |
| `fix` | Bug 修复 | `fix(api): resolve null pointer` |
| `docs` | 文档更新 | `docs(readme): add installation guide` |
| `style` | 代码格式 | `style(format): fix indentation` |
| `refactor` | 重构 | `refactor(core): simplify logic` |
| `perf` | 性能优化 | `perf(query): add index` |
| `test` | 测试相关 | `test(unit): add edge cases` |
| `chore` | 构建/工具 | `chore(deps): update packages` |
| `ci` | CI 配置 | `ci(github): add workflow` |
| `build` | 构建系统 | `build(webpack): upgrade config` |
| `revert` | 回滚 | `revert: commit xxx` |

### Scope 建议
- `auth` - 认证相关
- `api` - API 相关
- `ui` - 界面相关
- `db` - 数据库相关
- `core` - 核心逻辑
- `config` - 配置相关
- `deps` - 依赖相关

## Output Format

### 提交建议
```markdown
## 变更分析

### 修改文件
| 文件 | 变更类型 | 行数变化 |
|------|----------|----------|
| src/auth.ts | feat | +150 -20 |
| tests/auth.test.ts | test | +80 -0 |

### 建议提交

**提交 1**: `feat(auth): add OAuth2 login support`
- 新增 OAuth2 认证流程
- 添加相关测试用例

**提交 2**: `docs(auth): update authentication guide`
- 更新认证文档
- 添加 OAuth2 配置说明

---
是否执行上述提交？(确认/修改/取消)
```

### Branch 建议
```markdown
## 分支策略

**当前分支**: `main`
**建议操作**: 创建功能分支

```bash
git checkout -b feat/oauth2-login
```

**分支命名规范**:
- `feat/xxx` - 新功能
- `fix/xxx` - Bug 修复
- `hotfix/xxx` - 紧急修复
- `docs/xxx` - 文档更新
- `refactor/xxx` - 重构
```

### PR 描述模板
```markdown
## 📋 变更说明

### 类型
- [ ] ✨ 新功能 (feat)
- [ ] 🐛 Bug 修复 (fix)
- [ ] 📝 文档更新 (docs)
- [ ] ♻️ 重构 (refactor)
- [ ] ⚡ 性能优化 (perf)
- [ ] ✅ 测试 (test)
- [ ] 🔧 配置 (chore)

### 描述
[简要描述变更内容]

### 关联 Issue
Closes #XXX

### 变更详情
- 变更点 1
- 变更点 2

### 测试
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动测试完成

### 截图/录屏
[如适用]

### 检查清单
- [ ] 代码符合项目规范
- [ ] 已添加必要注释
- [ ] 已更新相关文档
- [ ] 无破坏性变更（或已标注）
```

## Rules

1. **原子提交**: 每个提交只做一件事
2. **信息完整**: commit message 清楚说明变更原因和内容
3. **可回滚**: 提交后应能安全回滚
4. **测试先行**: 提交前确保测试通过
5. **敏感检查**: 不提交密码、密钥等敏感信息
6. **大变更分解**: 大功能拆分为多个小提交
7. **确认执行**: git 写操作需用户确认

## Safety Checks

执行任何 git 操作前检查：

- [ ] 当前分支正确
- [ ] 无未保存变更（除非是提交目标）
- [ ] 远程分支状态已知
- [ ] 不提交敏感文件（.env, keys 等）
- [ ] 大文件已处理（.gitignore 或 LFS）

## Tools Used

- `exec` - 执行 git 命令
- `read` - 读取变更文件
- `write` - 生成文档/报告
- `glob` - 查找相关文件

## Common Commands Reference

```bash
# 状态查看
git status
git diff
git diff --stat
git log --oneline -10

# 分支操作
git branch -a
git checkout -b <branch>
git merge <branch>
git branch -d <branch>

# 提交操作
git add <files>
git commit -m "message"
git commit --amend
git reset --soft HEAD~1

# 远程操作
git pull
git push
git push -u origin <branch>
git fetch --prune

# 其他
git stash
git stash pop
git cherry-pick <commit>
git rebase -i HEAD~n
```

## Examples

### Example 1: 日常提交
```
用户：帮我提交今天的代码变更

执行：
1. git status 查看变更
2. git diff 分析内容
3. 按功能分组文件
4. 生成 commit messages
5. 确认后执行提交
```

### Example 2: 准备 PR
```
用户：帮我准备一个 PR

执行：
1. 分析分支差异
2. 生成 changelog
3. 创建 PR 描述
4. 建议 reviewer
5. 推送到远程
```

### Example 3: 解决冲突
```
用户：合并时遇到冲突

执行：
1. 分析冲突文件
2. 理解双方变更
3. 提供合并建议
4. 验证合并结果
```

## Notes

- 敏感操作（reset, rebase）需特别确认
- 定期执行 git gc 清理仓库
- 重要分支设置保护规则
- 使用 git hooks 自动化检查
