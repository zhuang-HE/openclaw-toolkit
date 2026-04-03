# 📝 ClawHub 手动登录指南

---

## ⚠️ 当前状态

ClawHub 需要使用 GitHub OAuth 登录，不支持直接使用 GitHub Token。

---

## 🚀 登录步骤

### 方式 1: 使用 clawhub login（推荐）

1. **确保 FastGitHub 运行**（如需要）

2. **执行登录命令**：
   ```bash
   cd /home/admin/.openclaw/workspace/openclaw-toolkit
   clawhub login
   ```

3. **在浏览器中**：
   - 点击 "Login with GitHub"
   - 授权 ClawHub 访问
   - 登录成功后返回终端

4. **验证登录**：
   ```bash
   clawhub whoami
   ```

5. **发布**：
   ```bash
   clawhub publish .
   ```

---

### 方式 2: 手动获取 Token

1. **访问 ClawHub 网站**：
   ```
   https://clawhub.ai
   ```

2. **使用 GitHub 登录**

3. **进入设置页面**：
   - 点击右上角头像
   - Settings → API Tokens
   - Generate New Token

4. **复制 Token**

5. **使用 Token 登录**：
   ```bash
   clawhub login --token YOUR_TOKEN_HERE
   ```

6. **发布**：
   ```bash
   clawhub publish .
   ```

---

## 📦 项目配置

### clawhub.json

```json
{
  "name": "openclaw-toolkit",
  "displayName": "OpenClaw Toolkit",
  "version": "1.0.0",
  "description": "AI 助手最佳实践集成到 OpenClaw 框架",
  "author": "OpenClaw Community",
  "license": "MIT"
}
```

---

## ✅ 发布后验证

### 访问 ClawHub 页面

```
https://clawhub.com/skills/openclaw-toolkit
```

### 测试安装

```bash
clawhub install openclaw-toolkit
clawhub list
```

---

## 🔧 常见问题

### 问题 1: 登录超时

**原因**: 网络问题或 FastGitHub 未运行

**解决**: 
- 确保 FastGitHub 运行
- 或等待网络恢复

### 问题 2: 认证失败

**原因**: Token 无效或过期

**解决**: 重新登录获取新 token

---

## 📖 参考链接

- **ClawHub**: https://clawhub.ai
- **GitHub**: https://github.com/zhuang-HE/openclaw-toolkit

---

**请使用 `clawhub login` 命令在浏览器中完成登录！** 🚀
