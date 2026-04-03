#!/bin/bash

# GitHub 推送脚本
# 用法：./push-to-github.sh

set -e

echo "🚀 GitHub 推送脚本"
echo "=================="
echo ""

# 检查是否在项目目录
if [ ! -f "README.md" ]; then
    echo "❌ 错误：请在项目根目录执行此脚本"
    exit 1
fi

# 获取 GitHub 用户名
echo "请输入你的 GitHub 用户名:"
read -p "> " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ 错误：GitHub 用户名不能为空"
    exit 1
fi

echo ""
echo "📦 将推送到：https://github.com/$GITHUB_USERNAME/openclaw-toolkit"
echo ""

# 检查是否已配置远程
if git remote | grep -q "origin"; then
    echo "⚠️  已存在 remote origin"
    read -p "是否覆盖？(y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote remove origin
    else
        echo "❌ 推送已取消"
        exit 0
    fi
fi

# 选择协议
echo ""
echo "选择连接方式:"
echo "1) HTTPS (需要密码或 token)"
echo "2) SSH (需要配置 SSH key)"
read -p "> " PROTOCOL

if [ "$PROTOCOL" = "1" ]; then
    REMOTE_URL="https://github.com/$GITHUB_USERNAME/openclaw-toolkit.git"
elif [ "$PROTOCOL" = "2" ]; then
    REMOTE_URL="git@github.com:$GITHUB_USERNAME/openclaw-toolkit.git"
else
    echo "❌ 无效选择"
    exit 1
fi

echo ""
echo "🔗 远程地址：$REMOTE_URL"
echo ""

# 添加远程仓库
echo "➕ 添加远程仓库..."
git remote add origin $REMOTE_URL

# 确保分支名为 main
git branch -M main

# 确认推送
read -p "确认推送到 GitHub？(y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 推送已取消"
    exit 0
fi

# 推送
echo ""
echo "🚀 开始推送..."
echo "   如提示密码，请使用 Personal Access Token（不是 GitHub 密码）"
echo ""

if git push -u origin main; then
    echo ""
    echo "✅ 推送成功！"
    echo ""
    echo "📦 仓库地址:"
    echo "   https://github.com/$GITHUB_USERNAME/openclaw-toolkit"
    echo ""
    echo "🎉 完成！"
    echo ""
    echo "下一步:"
    echo "1. 访问仓库页面"
    echo "2. 更新 README 中的链接"
    echo "3. 添加 topics: openclaw, ai-assistant, productivity, etc."
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "可能的原因:"
    echo "- 认证失败：使用 Personal Access Token 代替密码"
    echo "- 仓库不存在：先在 GitHub 创建仓库"
    echo "- SSH key 未配置：运行 ssh-keygen 并添加到 GitHub"
    echo ""
    echo "详细指南请查看：PUSH_TO_GITHUB.md"
    exit 1
fi
