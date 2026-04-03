#!/bin/bash

# ClawHub 发布脚本
# 用法：./release.sh

set -e

echo "🚀 ClawHub 发布脚本"
echo "=================="
echo ""

# 检查是否在项目目录
if [ ! -f "clawhub.json" ]; then
    echo "❌ 错误：请在项目根目录执行此脚本（需要 clawhub.json）"
    exit 1
fi

# 检查 clawhub CLI
if ! command -v clawhub &> /dev/null; then
    echo "❌ 错误：clawhub CLI 未安装"
    exit 1
fi

echo "✅ 预检查通过"
echo ""

# 显示当前版本
VERSION=$(grep '"version"' clawhub.json | cut -d'"' -f4)
echo "📦 当前版本：v$VERSION"
echo ""

# 检查登录状态
echo "🔐 检查登录状态..."
if ! clawhub whoami &> /dev/null; then
    echo "⚠️  未登录，开始登录流程..."
    clawhub login
else
    echo "✅ 已登录"
fi
echo ""

# 预览发布
echo "📋 预览发布内容..."
echo "   将发布到：clawhub.com"
echo "   技能名称：claude-code-toolkit"
echo "   版本号：v$VERSION"
echo ""

# 确认发布
read -p "确认发布？(y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 发布已取消"
    exit 0
fi

# 执行发布
echo ""
echo "🚀 开始发布..."
clawhub publish .

echo ""
echo "✅ 发布成功！"
echo ""
echo "📦 技能包信息:"
echo "   名称：claude-code-toolkit"
echo "   版本：v$VERSION"
echo "   链接：https://clawhub.com/skills/claude-code-toolkit"
echo ""
echo "🎉 完成！"
