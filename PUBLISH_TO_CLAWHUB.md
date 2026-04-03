# 发布到 ClawHub 指南

ClawHub 是 OpenClaw 的技能市场，可以让其他用户轻松发现和安装你的技能包。

---

## 前置条件

### 1. 安装 ClawHub CLI

```bash
# ClawHub CLI 通常随 OpenClaw 一起安装
# 验证安装
clawhub --cli-version
```

### 2. 登录 ClawHub

```bash
# 登录（会打开浏览器）
clawhub login
```

登录流程：
1. 执行 `clawhub login`
2. 浏览器自动打开 ClawHub 网站
3. 使用 GitHub/Google 账号登录
4. 授权后自动返回 CLI

### 3. 验证登录

```bash
# 查看当前用户
clawhub whoami
```

---

## 发布流程

### 步骤 1: 准备 clawhub.json

已创建 `clawhub.json` 文件，包含：

```json
{
  "name": "openclaw-toolkit",
  "displayName": "OpenClaw Toolkit",
  "version": "1.0.0",
  "description": "将 AI 助手 的最佳实践迁移到 OpenClaw 框架",
  "author": "OpenClaw Community",
  "license": "MIT",
  "keywords": [ "openclaw", "commands", "agents", "skills"],
  ...
}
```

### 步骤 2: 验证包结构

```bash
# 检查文件完整性
cd /home/admin/.openclaw/workspace/openclaw-openclaw-toolkit
ls -la
```

确保包含：
- ✅ clawhub.json
- ✅ README.md
- ✅ LICENSE
- ✅ commands/
- ✅ agents/
- ✅ skills/
- ✅ docs/

### 步骤 3: 发布到 ClawHub

```bash
cd /home/admin/.openclaw/workspace/openclaw-openclaw-toolkit

# 发布技能包
clawhub publish .
```

### 步骤 4: 验证发布

访问 ClawHub 网站查看已发布的技能包：
```
https://clawhub.com
```

搜索：`openclaw-toolkit`

---

## 更新技能包

### 修改版本号

编辑 `clawhub.json`：
```json
{
  "version": "1.0.1"  // 更新版本号
}
```

### 发布更新

```bash
# 提交更改
git add .
git commit -m "feat: 添加新功能"

# 发布新版本
clawhub publish .
```

---

## 安装测试

### 本地测试安装

```bash
# 卸载（如已安装）
clawhub uninstall openclaw-toolkit

# 重新安装
clawhub install openclaw-toolkit

# 验证
clawhub list
```

### 验证功能

在 OpenClaw 会话中测试：
```bash
/research AI Agent 框架
/review src/auth.ts
```

---

## 常见问题

### 问题 1: 登录失败

**错误**: `Error: Not logged in`

**解决**:
```bash
# 重新登录
clawhub logout
clawhub login
```

### 问题 2: 发布失败 - 名称冲突

**错误**: `Skill name already exists`

**解决**:
- 修改 `clawhub.json` 中的 `name` 字段
- 或联系 ClawHub 管理员

### 问题 3: 发布失败 - 验证错误

**错误**: `Validation failed: missing required fields`

**解决**:
检查 `clawhub.json` 是否包含必填字段：
- name
- displayName
- version
- description
- author

### 问题 4: 文件过大

ClawHub 对技能包大小有限制（通常 10MB）。

**解决**:
- 移除不必要的大文件
- 使用 `.clawhubignore` 排除文件

---

## .clawhubignore 文件

创建 `.clawhubignore` 排除不需要的文件：

```
# .clawhubignore
.git/
node_modules/
*.log
backup/
*.xlsx
*.csv
```

---

## 技能包最佳实践

### 命名规范

- **name**: 小写，连字符分隔（`my-skill`）
- **displayName**: 可读名称（`My Skill`）
- **version**: 语义化版本（`1.0.0`）

### 目录结构

```
my-skill/
├── clawhub.json       # 必需
├── README.md          # 必需
├── LICENSE            # 推荐
├── SKILL.md           # 技能定义
└── ...
```

### 文档要求

- README.md 必须包含：
  - 功能说明
  - 安装指南
  - 使用示例
  - 配置说明

---

## 推广技能包

### 1. 分享到社区

- OpenClaw Discord
- GitHub Discussions
- 社交媒体

### 2. 添加 Badge

在 README 中添加：

```markdown
[![ClawHub](https://img.shields.io/badge/ClawHub-openclaw--toolkit-green)](https://clawhub.com/skills/openclaw-toolkit)
```

### 3. 收集反馈

- 启用 GitHub Issues
- 收集用户反馈
- 持续改进

---

## 统计数据

查看技能包统计：

```bash
# 查看安装量（需要管理员权限）
clawhub inspect openclaw-toolkit

# 查看评分和评论
# 访问 ClawHub 网站
```

---

## 删除技能包（如需要）

```bash
# 软删除（隐藏）
clawhub hide openclaw-toolkit

# 永久删除（需要管理员权限）
clawhub delete openclaw-toolkit
```

---

## 下一步

1. ✅ 登录 ClawHub
2. ✅ 验证 clawhub.json
3. ✅ 发布技能包
4. ✅ 测试安装
5. ✅ 分享到社区

---

**准备发布？执行：**

```bash
cd /home/admin/.openclaw/workspace/openclaw-openclaw-toolkit
clawhub login      # 如未登录
clawhub publish .  # 发布
```
