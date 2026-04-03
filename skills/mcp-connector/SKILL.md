# MCP Connector Skill

name: mcp-connector

## Task
连接外部服务和 API，实现类似 Claude Code MCP 协议的集成能力。

## Overview

MCP (Model Context Protocol) 是 Anthropic 推出的标准协议，用于 AI 模型安全地连接外部数据源和工具。

本 Skill 在 OpenClaw 中实现类似的连接能力，通过：
1. **Stdio 连接器**: 通过 exec 调用外部 CLI 工具
2. **HTTP 连接器**: 通过 web_fetch 调用 REST API
3. **自定义连接器**: 针对特定服务定制集成

## Supported Connections

### 1. 文件系统 (Filesystem)
```javascript
// 内置支持，无需额外配置
read({path: "./file.txt"})
write({path: "./output.md", content: "..."})
```

### 2. GitHub API
```javascript
// 通过 exec 调用 GitHub CLI
exec({command: "gh issue create --title 'Bug' --body 'Description'"})
exec({command: "gh pr list --state open"})
```

### 3. 数据库 (Database)
```javascript
// PostgreSQL
exec({command: "psql $DATABASE_URL -c 'SELECT * FROM users'"})

// MySQL
exec({command: "mysql -u user -p -e 'SELECT * FROM table'"})

// SQLite
exec({command: "sqlite3 database.db 'SELECT * FROM table'"})
```

### 4. Docker
```javascript
exec({command: "docker ps -a"})
exec({command: "docker logs container_id"})
exec({command: "docker-compose up -d"})
```

### 5. Kubernetes
```javascript
exec({command: "kubectl get pods"})
exec({command: "kubectl logs pod_name"})
exec({command: "kubectl apply -f deployment.yaml"})
```

### 6. Cloud Providers
```javascript
// AWS
exec({command: "aws s3 ls"})
exec({command: "aws ec2 describe-instances"})

// GCP
exec({command: "gcloud compute instances list"})

// Azure
exec({command: "az vm list"})
```

### 7. Web Services
```javascript
// 通过 HTTP API
web_fetch({url: "https://api.github.com/repos/xxx/xxx"})

// 需要认证的 API
exec({command: "curl -H 'Authorization: Bearer $TOKEN' https://api.service.com"})
```

## Configuration

### 环境变量配置
在 Gateway 环境或系统环境中配置：

```bash
# GitHub
export GITHUB_TOKEN=ghp_xxx

# 数据库
export DATABASE_URL=postgresql://user:pass@host:5432/db

# AWS
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
export AWS_REGION=us-east-1

# Docker
export DOCKER_HOST=unix:///var/run/docker.sock
```

### 配置文件（可选）
```json
// ~/.openclaw/workspace/mcp-config.json
{
  "connections": {
    "github": {
      "type": "cli",
      "command": "gh",
      "auth": "GITHUB_TOKEN"
    },
    "database": {
      "type": "cli",
      "command": "psql",
      "env": "DATABASE_URL"
    },
    "docker": {
      "type": "cli",
      "command": "docker"
    }
  }
}
```

## Workflow

### Phase 1: 连接发现
1. 检查可用 CLI 工具
2. 验证环境变量配置
3. 测试连接可用性
4. 报告可用服务列表

### Phase 2: 请求路由
1. 解析用户意图
2. 选择合适连接器
3. 构建命令/API 调用
4. 执行并获取结果

### Phase 3: 结果处理
1. 解析原始输出
2. 格式化为可读内容
3. 提取关键信息
4. 生成响应

### Phase 4: 错误处理
1. 捕获执行错误
2. 分类错误类型
3. 提供修复建议
4. 记录错误日志

## Output Format

### 连接状态报告
```markdown
## 可用连接

| 服务 | 类型 | 状态 | 说明 |
|------|------|------|------|
| GitHub | CLI | ✅ 就绪 | gh CLI 已安装 |
| PostgreSQL | CLI | ✅ 就绪 | DATABASE_URL 已配置 |
| Docker | CLI | ⚠️ 警告 | 需要 sudo 权限 |
| AWS | CLI | ❌ 未配置 | 缺少 AWS CLI |

## 建议
- 安装 AWS CLI 以启用 AWS 集成
- 配置 Docker 用户组以避免 sudo
```

### API 调用结果
```markdown
## GitHub Issues

### 打开的问题 (3)

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
```

## Security Considerations

### 权限控制
1. **最小权限**: 使用只读 token 除非需要写操作
2. **环境变量**: 敏感信息通过环境变量传递
3. **命令白名单**: 限制可执行的命令类型
4. **审计日志**: 记录所有外部调用

### 安全最佳实践
```bash
# ✅ 好的做法
export GITHUB_TOKEN=ghp_xxx  # 只读 token
exec({command: "gh issue list"})  # 只读操作

# ❌ 避免的做法
exec({command: "rm -rf /"})  # 危险命令
write({path: "/etc/passwd"})  # 敏感文件
```

## Tools Used

- `exec` - 执行 CLI 工具
- `web_fetch` - HTTP API 调用
- `read`/`write` - 文件操作
- `browser` - Web 服务交互（如需要）

## Example Connections

### GitHub Integration
```javascript
// 列出 open issues
exec({
  command: "gh issue list --state open --json number,title,labels"
})

// 创建 issue
exec({
  command: "gh issue create --title 'Bug' --body 'Description'"
})

// 获取 PR 详情
exec({
  command: "gh pr view 123 --json files,commits"
})
```

### Database Integration
```javascript
// 查询数据
exec({
  command: "psql $DATABASE_URL -c 'SELECT * FROM users LIMIT 10' --csv"
})

// 导出备份
exec({
  command: "pg_dump $DATABASE_URL > backup.sql"
})
```

### Docker Integration
```javascript
// 容器状态
exec({command: "docker ps -a --format 'table {{.Names}}\\t{{.Status}}'"})

// 查看日志
exec({command: "docker logs app-container --tail 50"})

// 重启服务
exec({command: "docker-compose restart web"})
```

## Troubleshooting

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Command not found | CLI 未安装 | 安装对应 CLI 工具 |
| Permission denied | 权限不足 | 配置 sudo 或用户组 |
| Connection refused | 服务未运行 | 启动对应服务 |
| Auth failed | 认证失败 | 检查 token/密码 |
| Timeout | 网络问题 | 检查网络和防火墙 |

### 诊断命令
```bash
# 检查 CLI 工具
which gh
which docker
which kubectl

# 检查环境变量
echo $GITHUB_TOKEN
echo $DATABASE_URL

# 测试连接
gh auth status
docker info
kubectl cluster-info
```

## Notes

- 优先使用官方 CLI 工具（gh, aws, gcloud 等）
- 敏感操作需要用户确认
- 记录所有外部调用便于审计
- 定期更新 CLI 工具版本
