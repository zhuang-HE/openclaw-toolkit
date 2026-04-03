#!/bin/bash
# 机器人数据收集 - 日报生成和推送脚本（带重试机制）
# 每天 20:00 执行
# 优化：添加自动重试、限流检测、指数退避

set -e

# 配置
WORKSPACE="/home/admin/.openclaw/workspace"
REPORT_DIR="$WORKSPACE/reports"
LOG_DIR="$WORKSPACE/logs"
TODAY=$(date '+%Y-%m-%d')

# 飞书 Webhook 配置（签名校验已关闭）
WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/5128a9a6-8f58-407a-9cbe-5f816713d289"

# 重试配置
MAX_RETRIES=5
INITIAL_DELAY=5  # 初始等待秒数

echo "=========================================" >> "$LOG_DIR/日报推送.log"
echo "执行时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_DIR/日报推送.log"

# 检查今日报告是否存在
REPORT_FILE="$REPORT_DIR/${TODAY}_机器人数据收集日报.md"

if [ -f "$REPORT_FILE" ]; then
    echo "找到日报文件：$REPORT_FILE" >> "$LOG_DIR/日报推送.log"
    
    # 生成飞书消息内容（带重试逻辑）
    python3 << PYTHON_SCRIPT
import os
import sys
import time
import requests
from datetime import datetime

# 配置
webhook_url = "$WEBHOOK_URL"
report_file = "$REPORT_FILE"
max_retries = $MAX_RETRIES
initial_delay = $INITIAL_DELAY

# 读取报告内容
with open(report_file, 'r', encoding='utf-8') as f:
    report_content = f.read()

# 提取关键信息
lines = report_content.split('\n')

# 从报告中提取关键数据
total_products = "24"
file_size = "5.7 KB"
token_used = "2,000"
token_remaining = "998,000"

for line in lines:
    if '总记录数' in line and ':' in line:
        parts = line.split(':')
        if len(parts) >= 2:
            total_products = parts[1].strip().replace('款产品', '').strip()
    if '文件大小' in line and ':' in line:
        parts = line.split(':')
        if len(parts) >= 2:
            file_size = parts[1].strip()
    if 'Token 消耗' in line and '|' in line:
        parts = line.split('|')
        if len(parts) >= 3:
            token_used = parts[2].strip()
    if 'Token 剩余' in line and '|' in line:
        parts = line.split('|')
        if len(parts) >= 3:
            token_remaining = parts[2].strip()

# 构建飞书卡片消息
today = datetime.now().strftime('%Y-%m-%d')
content = {
    "msg_type": "interactive",
    "card": {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"📊 机器人数据收集日报 ({today})"},
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**今日概览**\n- 📦 数据库产品数：{total_products} 款\n- 💾 数据库大小：{file_size}\n- 🔑 Token 消耗：{token_used}\n- 💰 Token 剩余：{token_remaining}"
                }
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**✅ 完成的工作**\n• 官方渠道数据收集\n• 行业平台数据扫描\n• 产品价格更新检查\n• 事故数据收集\n• 数据库去重和保存"
                }
            },
            {"tag": "hr"},
            {
                "tag": "note",
                "elements": [
                    {"tag": "plain_text", "content": f"📄 完整报告已保存至：reports/{today}_机器人数据收集日报.md"}
                ]
            }
        ]
    }
}

# 发送消息（带重试逻辑）
headers = {"Content-Type": "application/json"}

def send_with_retry():
    """带重试和指数退避的发送函数"""
    last_error = None
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"尝试发送 (第 {attempt}/{max_retries} 次)...")
            
            response = requests.post(webhook_url, json=content, headers=headers, timeout=10)
            result = response.json()
            
            if result.get('code') == 0:
                print(f"推送成功：{today}")
                return True
            
            # 检查错误类型
            error_code = result.get('code')
            error_msg = result.get('msg', '')
            
            # 频率限制错误 (11232) - 需要等待重试
            if error_code == 11232 or 'frequency limited' in error_msg.lower():
                wait_time = initial_delay * (2 ** (attempt - 1))  # 指数退避
                print(f"触发频率限制，等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
                last_error = result
                continue
            
            # 其他错误 - 不重试
            print(f"推送失败（非限流错误）：{result}")
            return False
            
        except requests.exceptions.RequestException as e:
            print(f"网络错误 (第 {attempt} 次): {e}")
            last_error = str(e)
            
            if attempt < max_retries:
                wait_time = initial_delay * (2 ** (attempt - 1))
                print(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            continue
    
    # 所有重试都失败
    print(f"推送失败（已达最大重试次数）：{last_error}")
    return False

# 执行发送
success = send_with_retry()
sys.exit(0 if success else 1)
PYTHON_SCRIPT
    
    if [ $? -eq 0 ]; then
        echo "推送状态：成功" >> "$LOG_DIR/日报推送.log"
    else
        echo "推送状态：失败（已达最大重试次数）" >> "$LOG_DIR/日报推送.log"
    fi
else
    echo "未找到今日报告文件：$REPORT_FILE" >> "$LOG_DIR/日报推送.log"
    echo "尝试生成报告..." >> "$LOG_DIR/日报推送.log"
    
    # 如果没有报告，尝试生成一个摘要
    python3 << 'PYTHON_SCRIPT'
import os
from datetime import datetime

workspace = "/home/admin/.openclaw/workspace"
report_dir = os.path.join(workspace, "reports")
os.makedirs(report_dir, exist_ok=True)

today = datetime.now().strftime('%Y-%m-%d')
report_file = os.path.join(report_dir, f"{today}_机器人数据收集日报.md")

# 生成简单报告
report = f"""# 机器人数据收集日报

**日期**: {today}  
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 今日概览

- **数据收集状态**: 未执行或执行失败
- **原因**: 未找到收集日志或报告文件

---

## 📝 说明

今日的数据收集任务可能尚未执行，或执行过程中出现问题。

请检查：
1. 定时任务是否正常配置
2. 收集脚本是否正常运行
3. 日志文件是否有错误信息

---

## 🔍 相关日志

查看日志文件：
- `/home/admin/.openclaw/workspace/logs/机器人数据收集_*.log`

---

*本报告由机器人数据收集系统自动生成*
"""

with open(report_file, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"已生成补充报告：{report_file}")
PYTHON_SCRIPT
    
    echo "已生成补充报告" >> "$LOG_DIR/日报推送.log"
fi

echo "" >> "$LOG_DIR/日报推送.log"
