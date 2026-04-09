#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token 消耗统计与日报系统
功能：
1. 每次对话后统计 token 花费
2. 每天 0 点发送前一天的消耗总额
3. 自动生成 Token 消耗报告
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import csv
import requests

# 配置
WORKSPACE = "/home/admin/.openclaw/workspace"
LOG_DIR = f"{WORKSPACE}/logs"
TOKEN_STATS_FILE = f"{LOG_DIR}/token_stats.json"
TOKEN_HISTORY_FILE = f"{LOG_DIR}/token_history.csv"
DAILY_REPORT_FILE = f"{LOG_DIR}/token_daily_report.md"

# 飞书 Webhook
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/587f3c74-4345-4fc6-98b3-b2a935f6787e"

# 模型价格（每 1000 tokens）
MODEL_PRICES = {
    'dashscope/qwen3.5-plus': {'input': 0.002, 'output': 0.006},
    'dashscope/qwen3-max': {'input': 0.02, 'output': 0.06},
    'dashscope/qwen3-vl-plus': {'input': 0.002, 'output': 0.006},
}

def get_current_model():
    """获取当前使用的模型"""
    try:
        # 从 session_status 或配置文件中获取
        return 'dashscope/qwen3.5-plus'  # 默认
    except:
        return 'dashscope/qwen3.5-plus'

def load_token_stats():
    """加载当前 Token 统计"""
    default_stats = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'input_tokens': 0,
        'output_tokens': 0,
        'total_tokens': 0,
        'total_cost': 0.0,
        'session_count': 0,
    }
    
    if os.path.exists(TOKEN_STATS_FILE):
        try:
            with open(TOKEN_STATS_FILE, 'r', encoding='utf-8') as f:
                stats = json.load(f)
                # 确保所有字段存在
                for key in default_stats.keys():
                    if key not in stats:
                        stats[key] = default_stats[key]
                return stats
        except:
            pass
    
    return default_stats

def save_token_stats(stats):
    """保存 Token 统计"""
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(TOKEN_STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def load_token_history():
    """加载历史统计"""
    history = []
    if os.path.exists(TOKEN_HISTORY_FILE):
        with open(TOKEN_HISTORY_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                history.append(row)
    return history

def save_to_history(stats):
    """保存到历史记录"""
    os.makedirs(LOG_DIR, exist_ok=True)
    
    file_exists = os.path.exists(TOKEN_HISTORY_FILE)
    
    with open(TOKEN_HISTORY_FILE, 'a', encoding='utf-8', newline='') as f:
        fieldnames = ['date', 'input_tokens', 'output_tokens', 'total_tokens', 'total_cost', 'session_count']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'date': stats['date'],
            'input_tokens': stats.get('input_tokens', 0),
            'output_tokens': stats.get('output_tokens', 0),
            'total_tokens': stats.get('total_tokens', 0),
            'total_cost': stats.get('total_cost', 0.0),
            'session_count': stats.get('session_count', 0),
        })

def calculate_cost(input_tokens, output_tokens, model=None):
    """计算花费"""
    if model is None:
        model = get_current_model()
    
    prices = MODEL_PRICES.get(model, {'input': 0.002, 'output': 0.006})
    
    cost = (input_tokens / 1000) * prices['input'] + (output_tokens / 1000) * prices['output']
    return round(cost, 6)

def update_token_stats(input_tokens=0, output_tokens=0):
    """更新 Token 统计（每次对话后调用）"""
    stats = load_token_stats()
    
    # 检查是否需要新的一天
    today = datetime.now().strftime('%Y-%m-%d')
    if stats['date'] != today:
        # 保存前一天的统计到历史
        save_to_history(stats)
        # 重置统计
        stats = {
            'date': today,
            'input_tokens': 0,
            'output_tokens': 0,
            'total_tokens': 0,
            'total_cost': 0.0,
            'session_count': 0,
        }
    
    # 更新统计
    stats['input_tokens'] += input_tokens
    stats['output_tokens'] += output_tokens
    stats['total_tokens'] = stats['input_tokens'] + stats['output_tokens']
    stats['total_cost'] = calculate_cost(stats['input_tokens'], stats['output_tokens'])
    stats['session_count'] += 1
    
    # 保存
    save_token_stats(stats)
    
    return stats

def generate_daily_report(date=None):
    """生成日报"""
    if date is None:
        date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    history = load_token_history()
    
    # 查找指定日期的统计
    day_stats = None
    for record in history:
        if record['date'] == date:
            day_stats = record
            break
    
    # 如果没有历史记录，使用当前统计
    if day_stats is None:
        current = load_token_stats()
        if current['date'] == date:
            day_stats = current
        else:
            day_stats = {
                'date': date,
                'input_tokens': 0,
                'output_tokens': 0,
                'total_tokens': 0,
                'total_cost': 0.0,
                'session_count': 0,
            }
    
    # 生成报告
    report = f"""# Token 消耗日报

**日期：** {day_stats['date']}

## 📊 消耗统计

| 指标 | 数值 |
|------|------|
| **输入 Token** | {int(day_stats.get('input_tokens', 0)):,} |
| **输出 Token** | {int(day_stats.get('output_tokens', 0)):,} |
| **总消耗** | {int(day_stats.get('total_tokens', 0)):,} |
| **对话次数** | {day_stats.get('session_count', 0)} |
| **总成本** | ${float(day_stats.get('total_cost', 0.0)):.6f} |

## 📈 平均统计

**平均每次对话：**
- Token: {int(day_stats.get('total_tokens', 0)) / max(1, int(day_stats.get('session_count', 1))):,.0f} tokens
- 成本：${float(day_stats.get('total_cost', 0.0)) / max(1, int(day_stats.get('session_count', 1))):.6f}

## 💡 Token 优化建议

1. **使用知识图谱查询** - 71.5 倍 Token 节省
   ```bash
   /search "查询" --mode graph  # 500 tokens
   ```

2. **选择合适的模式**
   - 简单查询：L1 (500 tokens)
   - 中等查询：L2 (1,500 tokens)
   - 复杂查询：L3 (5,000 tokens)

3. **避免重复查询** - 使用缓存

---

**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**报告文件：** {DAILY_REPORT_FILE}
"""
    
    # 保存报告
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(DAILY_REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report, day_stats

def format_feishu_message(stats):
    """格式化飞书消息"""
    date = stats.get('date', 'Unknown')
    total_tokens = int(stats.get('total_tokens', 0))
    total_cost = float(stats.get('total_cost', 0.0))
    session_count = int(stats.get('session_count', 0))
    input_tokens = int(stats.get('input_tokens', 0))
    output_tokens = int(stats.get('output_tokens', 0))
    
    # 计算平均
    avg_tokens = total_tokens // max(1, session_count)
    avg_cost = total_cost / max(1, session_count)
    
    message = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": f"📊 Token 消耗日报 - {date}",
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": f"日期：{date}\n\n"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "📈 消耗统计\n"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": f"输入 Token: {input_tokens:,}\n"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": f"输出 Token: {output_tokens:,}\n"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": f"总消耗：{total_tokens:,} tokens\n"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": f"对话次数：{session_count} 次\n"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": f"总成本：${total_cost:.6f}\n\n"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "📉 平均统计\n"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": f"平均每次对话：{avg_tokens:,} tokens\n"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": f"平均成本：${avg_cost:.6f}\n\n"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "💡 Token 优化建议\n"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "1. 使用知识图谱查询 - 71.5 倍节省\n"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "2. 选择合适的模式 (L1/L2/L3)\n"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "3. 避免重复查询 - 使用缓存"
                            }
                        ]
                    ]
                }
            }
        }
    }
    
    return message

def send_feishu_report(stats):
    """发送飞书日报"""
    message = format_feishu_message(stats)
    
    try:
        response = requests.post(FEISHU_WEBHOOK, json=message)
        response.raise_for_status()
        print(f"✅ 飞书日报已发送：{stats.get('date')}")
        print(f"   总消耗：{int(stats.get('total_tokens', 0)):,} tokens")
        print(f"   总成本：${float(stats.get('total_cost', 0.0)):.6f}")
        return True
    except Exception as e:
        print(f"❌ 飞书发送失败：{e}")
        return False

def send_daily_report():
    """发送日报（每天 0 点执行）"""
    # 生成昨天的报告
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    report, stats = generate_daily_report(yesterday)
    
    # 发送到飞书
    print(f"日报已生成：{DAILY_REPORT_FILE}")
    print(f"日期：{yesterday}")
    print(f"总消耗：{int(stats.get('total_tokens', 0)):,} tokens")
    print(f"总成本：${float(stats.get('total_cost', 0.0)):.6f}")
    
    # 飞书推送
    send_feishu_report(stats)
    
    return report, stats

def print_current_stats():
    """打印当前统计"""
    stats = load_token_stats()
    print("\n" + "=" * 60)
    print("📊 Token 消耗统计")
    print("=" * 60)
    print(f"日期：{stats['date']}")
    print(f"输入 Token: {stats.get('input_tokens', 0):,}")
    print(f"输出 Token: {stats.get('output_tokens', 0):,}")
    print(f"总消耗：{stats.get('total_tokens', 0):,}")
    print(f"对话次数：{stats.get('session_count', 0)}")
    print(f"总成本：${stats.get('total_cost', 0.0):.6f}")
    print("=" * 60)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'update':
            # 更新统计
            input_tokens = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            output_tokens = int(sys.argv[3]) if len(sys.argv) > 3 else 0
            stats = update_token_stats(input_tokens, output_tokens)
            print_current_stats()
        
        elif command == 'report':
            # 生成报告
            date = sys.argv[2] if len(sys.argv) > 2 else None
            report, stats = generate_daily_report(date)
            print(report)
        
        elif command == 'send':
            # 发送日报
            send_daily_report()
        
        elif command == 'show':
            # 显示当前统计
            print_current_stats()
    else:
        # 默认显示当前统计
        print_current_stats()
