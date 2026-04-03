# /connect - 外部连接命令

trigger: /connect [service] [--action=list|query|exec]

## Description
连接和管理外部服务（类似 MCP 协议），支持 GitHub、数据库、Docker 等。

## Services

| 服务 | 说明 | 前置条件 |
|------|------|----------|
| `github` | GitHub API | GITHUB_TOKEN |
| `database` | 数据库连接 | DATABASE_URL |
| `docker` | Docker 管理 | Docker 安装 |
| `k8s` | Kubernetes | kubectl 配置 |
| `aws` | AWS 服务 | AWS CLI + 凭证 |
| `status` | 连接状态 | - |

## Examples

### 查看连接状态
```bash
/connect status
```

输出：
```markdown
## 可用连接

| 服务 | 类型 | 状态 | 说明 |
|------|------|------|------|
| GitHub | API | ✅ 就绪 | GITHUB_TOKEN 已配置 |
| PostgreSQL | CLI | ✅ 就绪 | DATABASE_URL 已配置 |
| Docker | CLI | ⚠️ 警告 | 需要 sudo 权限 |
| Kubernetes | CLI | ❌ 未配置 | kubectl 未安装 |
| AWS | CLI | ❌ 未配置 | AWS CLI 未安装 |

### 建议
- 配置 Docker 用户组以避免 sudo
- 安装 AWS CLI 以启用 AWS 集成
```

### GitHub 操作
```bash
/connect github --action=list
```

输出：
```markdown
## GitHub Issues (Open: 3)

1. **#42 - Bug: Login fails**
   - 状态：Open
   - 标签：bug, auth
   - 创建：2026-04-01

2. **#41 - Feature: Add dark mode**
   - 状态：Open
   - 标签：enhancement
   - 创建：2026-03-30

3. **#40 - Docs: Update README**
   - 状态：Open
   - 标签：documentation
   - 创建：2026-03-28

---
操作建议：
- `/connect github --action=query 42` 查看详情
- `/connect github --action=exec "issue create ..."` 创建 issue
```

### 数据库查询
```bash
/connect database --action=query "SELECT * FROM users LIMIT 5"
```

输出：
```markdown
## 查询结果

```
| id | email | created_at |
|----|-------|------------|
| 1  | user1@example.com | 2026-01-15 |
| 2  | user2@example.com | 2026-02-20 |
| 3  | user3@example.com | 2026-03-10 |
| 4  | user4@example.com | 2026-03-25 |
| 5  | user5@example.com | 2026-04-01 |
```

5 rows returned.
```

### Docker 管理
```bash
/connect docker --action=list
```

输出：
```markdown
## Docker 容器

| 容器名 | 镜像 | 状态 | 端口 |
|--------|------|------|------|
| web-app | node:18 | Up 2 days | 3000:3000 |
| db | postgres:15 | Up 5 days | 5432:5432 |
| redis | redis:7 | Up 5 days | 6379:6379 |

---
操作建议：
- `/connect docker --action=logs web-app` 查看日志
- `/connect docker --action=exec "docker restart web-app"` 重启
```

## Configuration

### 环境变量
```bash
# GitHub
export GITHUB_TOKEN=ghp_xxx

# 数据库
export DATABASE_URL=postgresql://user:pass@host:5432/db

# AWS
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
export AWS_REGION=us-east-1
```

### 权限说明
| 服务 | 推荐权限 | 说明 |
|------|----------|------|
| GitHub | repo:read | 只读访问，除非需要创建 issue |
| 数据库 | SELECT | 默认只读，写操作需确认 |
| Docker | 用户组 | 加入 docker 组避免 sudo |
| AWS | ReadOnlyAccess | 最小权限原则 |

## Related
- skill: mcp-connector
- command: /status

## Notes
- 敏感操作需要确认
- 使用只读凭证优先
- 记录所有外部调用
