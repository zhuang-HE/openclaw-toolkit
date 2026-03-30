#!/bin/bash
# 临床试验数据库 - 数据收集执行脚本
# 每月 1 日 02:00 执行

set -e

WORKSPACE="/home/admin/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs"
SCRIPT_DIR="$WORKSPACE/scripts"

mkdir -p "$LOG_DIR"

echo "=========================================" >> "$LOG_DIR/临床试验定时任务执行.log"
echo "执行时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_DIR/临床试验定时任务执行.log"

# 执行数据收集脚本
cd "$WORKSPACE"
python3 "$SCRIPT_DIR/临床试验数据收集自动化.py" >> "$LOG_DIR/临床试验数据收集_自动化.log" 2>&1

echo "执行状态：完成" >> "$LOG_DIR/临床试验定时任务执行.log"
echo "" >> "$LOG_DIR/临床试验定时任务执行.log"
