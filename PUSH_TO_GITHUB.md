# 推送到 GitHub 指南

由于 GitHub 需要认证，请选择以下任一方式推送。

---

## 方式一：使用 GitHub 网页（最简单）

### 步骤 1: 在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 填写以下信息：
   - **Repository name**: `openclaw-toolkit`
   - **Description**: `AI 助手最佳实践集成到 OpenClaw 框架 - 包含 Commands/Agents/Skills 完整工具集`
   - **Visibility**: Public（公开）或 Private（私有）
   - **不要勾选** "Initialize this repository with a README"
3. 点击 "Create repository"

### 步骤 2: 添加远程仓库并推送

```bash
cd /home/admin/.openclaw/workspace/openclaw-toolkit

# 替换 YOUR_GITHUB_USERNAME 为你的 GitHub 用户名
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/openclaw-toolkit.git

# 或使用 SSH（如配置了 SSH key）
# git remote add origin git@github.com:YOUR_GITHUB_USERNAME/openclaw-toolkit.git

# 推送
git branch -M main
git push -u origin main
```

### 步骤 3: 验证

访问你的仓库：
```
https://github.com/YOUR_GITHUB_USERNAME/openclaw-toolkit
```

---

## 方式二：安装并使用 GitHub CLI

### 安装 gh

```bash
# Linux (Ubuntu/Debian)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# macOS
brew install gh
```

### 登录并推送

```bash
cd /home/admin/.openclaw/workspace/openclaw-toolkit

# 登录（会打开浏览器）
gh auth login

# 选择：
# - GitHub.com
# - HTTPS
# - Login with a web browser
# - 按提示完成认证

# 创建仓库并推送
gh repo create openclaw-toolkit --public --source=. --remote=origin --push
```

---

## 方式三：使用 Git + Personal Access Token

### 步骤 1: 创建 Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写：
   - **Note**: `openclaw-toolkit push`
   - **Expiration**: 90 days 或 No expiration
   - **Scopes**: 勾选 `repo` (Full control of private repositories)
4. 点击 "Generate token"
5. **复制并保存 token**（只显示一次！）

### 步骤 2: 创建仓库并推送

```bash
cd /home/admin/.openclaw/workspace/openclaw-toolkit

# 1. 在 GitHub 网页创建仓库（同方式一）
# https://github.com/new

# 2. 添加远程仓库
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/openclaw-toolkit.git

# 3. 推送（会提示输入密码）
git push -u origin main

# Username: YOUR_GITHUB_USERNAME
# Password: 粘贴你的 Personal Access Token（不会显示）
```

---

## 方式四：配置 SSH Key（推荐长期使用）

### 步骤 1: 生成 SSH Key

```bash
# 生成新 key
ssh-keygen -t ed25519 -C "your_email@example.com"

# 或（如系统不支持 ed25519）
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

### 步骤 2: 添加 SSH Key 到 GitHub

1. 查看公钥：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
2. 复制输出内容
3. 访问 https://github.com/settings/keys
4. 点击 "New SSH key"
5. 粘贴公钥内容
6. 点击 "Add SSH key"

### 步骤 3: 推送

```bash
cd /home/admin/.openclaw/workspace/openclaw-toolkit

# 使用 SSH 远程
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/openclaw-toolkit.git
git push -u origin main
```

---

## 推送后配置

### 1. 更新 README 中的链接

编辑 `README.md`，将：
```markdown
https://github.com/openclaw/openclaw-toolkit
```

改为你的实际仓库地址：
```markdown
https://github.com/YOUR_GITHUB_USERNAME/openclaw-toolkit
```

### 2. 添加 Topics

在仓库页面：
1. 点击 "Manage topics"
2. 添加：
   - `openclaw`
   - `ai-assistant`
   - `productivity`
   - `automation`
   - `workflow`
   - `cli`

### 3. 启用 Issues（可选）

在仓库 Settings → Features 中启用 Issues。

---

## 常见问题

### Q1: 推送失败 - Authentication failed

**原因**: 认证信息错误

**解决**:
- 使用 Personal Access Token 代替密码
- 或配置 SSH key

### Q2: 推送失败 - Repository not found

**原因**: 仓库不存在或权限不足

**解决**:
- 确认已在 GitHub 创建仓库
- 检查用户名是否正确
- 检查 token 权限

### Q3: 推送失败 - Permission denied

**原因**: SSH key 未配置

**解决**:
```bash
# 测试 SSH 连接
ssh -T git@github.com

# 如失败，重新配置 SSH key
```

### Q4: 仓库已存在

**原因**: 同名的仓库已存在

**解决**:
- 使用不同的仓库名
- 或删除已存在的仓库

---

## 快速命令参考

```bash
# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin https://github.com/USER/openclaw-toolkit.git

# 推送
git push -u origin main

# 查看状态
git status

# 查看提交历史
git log --oneline
```

---

## 推送成功后

1. ✅ 验证 GitHub 仓库页面
2. ✅ 更新 README 中的链接
3. ✅ 添加仓库描述和 topics
4. ✅ 分享到社区

---

**选择一种方式开始推送吧！** 🚀

推荐顺序：
1. 方式一（GitHub 网页）- 最简单
2. 方式四（SSH Key）- 长期使用最方便
3. 方式二（GitHub CLI）- 功能最强大
4. 方式三（Personal Access Token）- 备用方案
