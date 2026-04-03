# 🚀 发布到 ClawHub 指南

---

## ⚠️ 当前状态

**需要登录 ClawHub 后才能发布**

---

## 📋 发布步骤

### 步骤 1: 登录 ClawHub

```bash
cd /home/admin/.openclaw/workspace/openclaw-toolkit
clawhub login
```

**登录流程**：
1. 执行 `clawhub login`
2. 浏览器自动打开 ClawHub 网站
3. 使用 GitHub/Google 账号登录
4. 授权 CLI 访问
5. 登录成功后返回终端

### 步骤 2: 验证登录

```bash
clawhub whoami
```

应显示当前登录用户。

### 步骤 3: 发布到 ClawHub

```bash
clawhub publish .
```

**发布成功后会显示**：
```
✅ Published openclaw-toolkit@1.0.0
🔗 https://clawhub.com/skills/openclaw-toolkit
```

### 步骤 4: 验证发布

访问 ClawHub 查看已发布的技能包：
```
https://clawhub.com/skills/openclaw-toolkit
```

---

## 📦 项目配置

### clawhub.json

```json
{
  "name": "openclaw-toolkit",
  "displayName": "OpenClaw Toolkit",
  "version": "1.0.0",
  "description": "AI 助手最佳实践集成到 OpenClaw 框架 - 包含 Commands/Agents/Skills 完整工具集",
  "author": "OpenClaw Community",
  "license": "MIT",
  "keywords": ["openclaw", "commands", "agents", "skills", "productivity", "workflow", "ai-assistant", "automation"],
  ...
}
```

### 发布内容

- ✅ 6 个 Commands
- ✅ 3 个 Agents
- ✅ 6 个 Skills
- ✅ 完整文档

---

## 🔧 常见问题

### 问题 1: 未登录

```
Error: Not logged in. Run: clawhub login
```

**解决**: 执行 `clawhub login`

### 问题 2: 名称冲突

```
Error: Skill name already exists
```

**解决**: 
- 修改 `clawhub.json` 中的 `name` 字段
- 或使用不同的命名空间

### 问题 3: 验证失败

```
Validation failed: missing required fields
```

**解决**: 检查 `clawhub.json` 必填字段：
- name
- displayName
- version
- description
- author

---

## 📊 发布后

### 安装测试

```bash
# 卸载（如已安装）
clawhub uninstall openclaw-toolkit

# 重新安装
clawhub install openclaw-toolkit

# 验证
clawhub list
```

### 更新版本

```bash
# 1. 更新版本号
# 编辑 clawhub.json: "version": "1.0.1"

# 2. 提交更改
git add .
git commit -m "chore: bump version to 1.0.1"

# 3. 发布新版本
clawhub publish .
```

---

## 🎯 快速发布

```bash
cd /home/admin/.openclaw/workspace/openclaw-toolkit
clawhub login      # 登录
clawhub publish .  # 发布
```

---

## 📖 参考文档

- [ClawHub 文档](https://docs.clawhub.com)
- [PUBLISH_TO_CLAWHUB.md](PUBLISH_TO_CLAWHUB.md)
- [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)

---

**准备就绪后执行发布命令！** 🚀
