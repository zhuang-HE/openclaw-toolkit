# 贡献指南 🤝

感谢你对 OpenClaw Toolkit 的兴趣！欢迎各种形式的贡献。

---

## 🐛 报告问题

遇到 Bug 或有功能建议？请先搜索 [已有的 Issue](https://github.com/zhuang-HE/openclaw-toolkit/issues)，避免重复。

- 🐛 Bug 报告 → 使用 [Bug Report 模板](.github/ISSUE_TEMPLATE/bug_report.md)
- 💡 功能请求 → 使用 [Feature Request 模板](.github/ISSUE_TEMPLATE/feature_request.md)
- 📝 使用反馈 → 使用 [Feedback 模板](.github/ISSUE_TEMPLATE/feedback.md)

---

## 🔧 提交代码（Pull Request）

### 开发流程

1. **Fork 仓库**
   点击 GitHub 页面右上角 **Fork** 按钮，将仓库复制到你的账号下。

2. **克隆本地**
   ```bash
   git clone https://github.com/YOUR_USERNAME/openclaw-toolkit.git
   cd openclaw-toolkit
   ```

3. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或修复 bug
   git checkout -b fix/describe-the-bug
   ```

4. **安装依赖并验证**
   ```bash
   # 检查格式
   npm install  # 如果有 package.json

   # 验证 skill 格式
   # 确保每个 SKILL.md 包含有效的 frontmatter
   ```

5. **编写代码并测试**
   - 新增 Skill：确保 `SKILL.md` 包含 `name`、`description`（含中文触发词）
   - 新增 Command/Agent：参考现有文件的格式
   - 不要破坏现有功能

6. **提交代码**
   ```bash
   git add .
   git commit -m "feat(scope): add something useful"
   ```

   **提交信息格式**（参考 [Conventional Commits](https://www.conventionalcommits.org/)）：
   - `feat:` 新功能
   - `fix:` 修复 Bug
   - `docs:` 文档更新
   - `refactor:` 重构（无功能变化）
   - `test:` 测试相关
   - `chore:` 构建/工具变更

7. **推送到你的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **开启 Pull Request**
   - 标题格式：`[TYPE] 简短描述`
   - 内容说明：
     - 解决了什么问题？
     - 做了哪些改动？
     - 如何测试？

---

## 📝 Skill 开发规范

新增 Skill 时，请确保：

### 文件结构
```
skills/your-skill-name/
├── SKILL.md          # 必须包含 frontmatter
└── (可选) scripts/   # 支持脚本放这里
    └── your-script.js
```

### SKILL.md 格式

```markdown
---
name: your-skill-name
description: >
  简洁描述功能。触发词：关键词1、关键词2、关键词3
---

# Your Skill Name

name: your-skill-name

## 功能说明
...

## 工作流程
...
```

### 命名规范
- Skill 目录：`kebab-case`（如 `web-research`）
- `name`：与目录名一致
- `description`：中文 + 英文触发词，方便 AI 自动识别

---

## 🧪 测试规范

- 代码改动后，在本地测试对应功能是否正常
- 确保不破坏已有 Skill 的 `SKILL.md` 结构
- 新增的脚本建议添加基本错误处理

---

## 📄 提交规范

所有贡献的代码将遵循 MIT 许可证。

如有任何疑问，欢迎：
- 在 [GitHub Discussions](https://github.com/zhuang-HE/openclaw-toolkit/discussions) 中提问
- 提交 Issue 描述你的想法

---

> 📌 **提示**：提交前请确保 `git status` 只包含你想提交的改动，避免混入无关文件。
