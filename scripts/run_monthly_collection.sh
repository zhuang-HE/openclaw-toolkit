#!/bin/bash
# 无人机 BI 数据库月度数据收集 - 快速执行脚本
# 用法：./run_monthly_collection.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="/home/admin/.openclaw/workspace"
LOG_DIR="${WORKSPACE_DIR}/logs"
LOG_FILE="${LOG_DIR}/无人机数据收集_$(date +\%Y\%m\%d_\%H\%M\%S).log"

# 创建日志目录
mkdir -p "${LOG_DIR}"

echo "========================================"
echo "无人机 BI 数据库月度数据收集"
echo "========================================"
echo "执行时间：$(date '+\%Y-\%m-\%d \%H:\%M:\%S')"
echo "日志文件：${LOG_FILE}"
echo ""

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到 python3，请先安装 Python 3"
    exit 1
fi

echo "✓ Python 环境检查通过"

# 检查依赖
echo ""
echo "检查依赖..."
python3 -c "import requests" 2>/dev/null && echo "✓ requests 已安装" || echo "⚠ requests 未安装，请运行：pip3 install requests"
python3 -c "import json" 2>/dev/null && echo "✓ json 已安装" || echo "✗ json 未安装"
python3 -c "import csv" 2>/dev/null && echo "✓ csv 已安装" || echo "✗ csv 未安装"
python3 -c "import logging" 2>/dev/null && echo "✓ logging 已安装" || echo "✗ logging 未安装"

# 执行数据收集脚本
echo ""
echo "开始执行数据收集脚本..."
echo ""

python3 "${SCRIPT_DIR}/无人机数据月度收集.py" 2>&1 | tee "${LOG_FILE}"

EXIT_CODE=${PIPESTATUS[0]}

echo ""
echo "========================================"
if [ ${EXIT_CODE} -eq 0 ]; then
    echo "✓ 数据收集任务执行成功"
else
    echo "✗ 数据收集任务执行失败（退出码：${EXIT_CODE}）"
fi
echo "========================================"
echo "日志文件：${LOG_FILE}"
echo ""

# 显示最新日志
echo "最新日志（最后 20 行）："
echo "----------------------------------------"
tail -n 20 "${LOG_FILE}"
echo "----------------------------------------"

exit ${EXIT_CODE}
