# 推送到 GitHub 指南

由于 GitHub CLI (`gh`) 未安装，请使用以下方法手动推送到 GitHub。

---

## 方法一：使用 GitHub CLI（推荐）

### 安装 gh

```bash
# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# macOS
brew install gh
```

### 认证并推送

```bash
# 登录 GitHub
gh auth login

# 创建仓库并推送
cd /home/admin/.openclaw/workspace/openclaw-claude-code-toolkit
gh repo create openclaw-claude-code-toolkit --public --source=. --remote=origin --push
```

---

## 方法二：使用 Git + GitHub 网页

### 步骤 1: 在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 仓库名：`openclaw-claude-code-toolkit`
3. 描述：`Claude Code best practices migrated to OpenClaw framework`
4. 选择 **Public**
5. **不要** 勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

### 步骤 2: 添加远程仓库并推送

```bash
cd /home/admin/.openclaw/workspace/openclaw-claude-code-toolkit

# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/openclaw-claude-code-toolkit.git

# 或者使用 SSH（如配置了 SSH key）
# git remote add origin git@github.com:YOUR_USERNAME/openclaw-claude-code-toolkit.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

---

## 方法三：使用 Git 凭证存储

### 配置凭证存储

```bash
# 启用凭证存储
git config --global credential.helper store

# 推送时会提示输入用户名和密码
git push -u origin main
```

### 使用 Personal Access Token

GitHub 密码登录已弃用，需使用 Personal Access Token：

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择 scopes: `repo`, `workflow`
4. 生成 token
5. 推送时使用 token 作为密码

```bash
git push -u origin main
# Username: YOUR_USERNAME
# Password: YOUR_PERSONAL_ACCESS_TOKEN
```

---

## 验证推送

推送完成后，访问：

```
https://github.com/YOUR_USERNAME/openclaw-claude-code-toolkit
```

确认文件已上传：
- ✅ README.md
- ✅ LICENSE
- ✅ commands/
- ✅ agents/
- ✅ skills/
- ✅ docs/
- ✅ examples/

---

## 后续更新

```bash
# 日常提交和推送
cd /home/admin/.openclaw/workspace/openclaw-claude-code-toolkit
git add .
git commit -m "feat: 添加新功能"
git push
```

---

## 添加协作者（可选）

1. 访问仓库 Settings → Collaborators
2. 点击 "Add people"
3. 输入协作者的 GitHub 用户名
4. 选择权限级别

---

## 启用 Issues 和 Projects（可选）

1. Settings → Features
2. 启用 Issues, Projects, Wiki 等功能

---

## 添加 GitHub Actions（可选）

创建 `.github/workflows/ci.yml` 添加 CI/CD 流程。

---

**推送完成后，记得更新 README.md 中的链接！**

```markdown
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/YOUR_USERNAME/openclaw-claude-code-toolkit)
```
