# ClawHub 发布检查清单

## 发布前准备

### ✅ 文件完整性检查

```bash
cd /home/admin/.openclaw/workspace/openclaw-openclaw-toolkit

# 检查必需文件
ls -la clawhub.json        # ✅ ClawHub 配置
ls -la README.md           # ✅ 项目说明
ls -la LICENSE             # ✅ 许可证
ls -la commands/           # ✅ 命令定义
ls -la agents/             # ✅ 代理定义
ls -la skills/             # ✅ 技能模块
ls -la docs/               # ✅ 文档
ls -la examples/           # ✅ 示例
```

### ✅ clawhub.json 验证

```json
{
  "name": "openclaw-toolkit",         ✅
  "displayName": "OpenClaw Toolkit",  ✅
  "version": "1.0.0",                    ✅
  "description": "...",                  ✅
  "author": "OpenClaw Community",        ✅
  "license": "MIT",                      ✅
  "keywords": [...]                      ✅
}
```

---

## 发布步骤

### 步骤 1: 登录 ClawHub

```bash
cd /home/admin/.openclaw/workspace/openclaw-openclaw-toolkit

# 登录（会打开浏览器）
clawhub login
```

**登录流程**：
1. 执行命令后，系统会自动打开浏览器
2. 使用 GitHub 或 Google 账号登录 ClawHub
3. 授权 CLI 访问
4. 登录成功后返回终端

**如无法打开浏览器**：
```bash
# 手动获取 token（访问 ClawHub 网站）
# 然后使用 token 登录
clawhub login --token YOUR_TOKEN_HERE
```

### 步骤 2: 验证登录状态

```bash
# 查看当前用户
clawhub whoami

# 应显示类似：
# Logged in as: your-username
```

### 步骤 3: 预览发布内容

```bash
# 检查将要发布的文件
clawhub publish . --dry-run
# 或
clawhub inspect openclaw-toolkit
```

### 步骤 4: 正式发布

```bash
# 发布到 ClawHub
clawhub publish .
```

**发布成功后会显示**：
```
✅ Published openclaw-toolkit@1.0.0
🔗 https://clawhub.com/skills/openclaw-toolkit
```

### 步骤 5: 验证发布

1. 访问 ClawHub: https://clawhub.com
2. 搜索：`openclaw-toolkit`
3. 查看技能包详情页

---

## 安装测试

### 测试安装

```bash
# 卸载（如已安装）
clawhub uninstall openclaw-toolkit

# 重新安装
clawhub install openclaw-toolkit

# 验证安装
clawhub list
ls ~/.openclaw/workspace/commands/
ls ~/.openclaw/workspace/agents/
ls ~/.openclaw/workspace/skills/
```

### 功能测试

在 OpenClaw 会话中测试各命令：

```bash
# 测试研究命令
/research AI Agent 框架

# 测试代码审查
/review src/auth.ts

# 测试文档生成
/docs src/api/

# 测试 Git 命令
/git status

# 测试记忆命令
/memory status

# 测试连接命令
/connect status
```

---

## 发布后推广

### 1. 分享链接

```
https://clawhub.com/skills/openclaw-toolkit
```

### 2. 添加到项目 README

```markdown
[![ClawHub](https://img.shields.io/badge/ClawHub-openclaw--toolkit-green)](https://clawhub.com/skills/openclaw-toolkit)
```

### 3. 社区推广

- OpenClaw Discord 社区
- GitHub Discussions
- 社交媒体（Twitter/X, LinkedIn）

---

## 更新流程

### 修改代码后

```bash
# 1. 更新版本号
# 编辑 clawhub.json: "version": "1.0.1"

# 2. 提交更改
git add .
git commit -m "feat: 添加新功能"

# 3. 发布新版本
clawhub publish .
```

### 版本命名规范

- **Patch** (1.0.0 → 1.0.1): Bug 修复
- **Minor** (1.0.0 → 1.1.0): 新功能
- **Major** (1.0.0 → 2.0.0): 破坏性变更

---

## 故障排除

### 问题 1: 登录失败

```
Error: Not logged in
```

**解决**：
```bash
clawhub logout
clawhub login
```

### 问题 2: 名称冲突

```
Error: Skill name 'openclaw-toolkit' already exists
```

**解决**：
- 修改 `clawhub.json` 中的 `name` 字段
- 或使用自己的命名空间：`yourname/openclaw-toolkit`

### 问题 3: 文件过大

```
Error: Package size exceeds limit (10MB)
```

**解决**：
```bash
# 检查文件大小
du -sh *

# 移除大文件
# 更新 .clawhubignore
```

### 问题 4: 验证失败

```
Validation failed: missing required fields
```

**解决**：
检查 `clawhub.json` 必填字段：
- name
- displayName
- version
- description
- author

---

## 统计数据

发布后可查看：

```bash
# 查看技能包信息
clawhub inspect openclaw-toolkit

# 查看安装量（需要权限）
# 访问 ClawHub 网站查看统计面板
```

---

## 快速发布命令

```bash
# 一键发布（如已登录）
cd /home/admin/.openclaw/workspace/openclaw-openclaw-toolkit
clawhub login && clawhub publish .
```

---

## 联系支持

遇到问题？

- ClawHub 文档：https://docs.clawhub.com
- GitHub Issues: https://github.com/clawhub/cli/issues
- Discord 社区：https://discord.gg/clawd

---

**准备就绪？开始发布！**

```bash
cd /home/admin/.openclaw/workspace/openclaw-openclaw-toolkit
clawhub login
clawhub publish .
```
