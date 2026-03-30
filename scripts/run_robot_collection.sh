#!/bin/bash
# 机器人数据收集 - 定时任务执行脚本
# 每天 9:00 执行数据收集

set -e

# 配置
WORKSPACE="/home/admin/.openclaw/workspace"
SCRIPT="$WORKSPACE/scripts/机器人数据收集自动化.py"
LOG_DIR="$WORKSPACE/logs"
PYTHON="python3"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 记录执行开始
echo "=========================================" >> "$LOG_DIR/定时任务执行.log"
echo "执行时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_DIR/定时任务执行.log"
echo "任务：机器人数据收集" >> "$LOG_DIR/定时任务执行.log"

# 执行收集脚本
cd "$WORKSPACE"
$PYTHON "$SCRIPT" 2>&1 | tee -a "$LOG_DIR/机器人数据收集_$(date '+%Y%m%d').log"

# 记录执行结果
if [ $? -eq 0 ]; then
    echo "执行状态：成功" >> "$LOG_DIR/定时任务执行.log"
else
    echo "执行状态：失败" >> "$LOG_DIR/定时任务执行.log"
fi

echo "" >> "$LOG_DIR/定时任务执行.log"
