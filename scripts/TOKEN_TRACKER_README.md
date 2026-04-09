# Token 统计与日报系统

## 📊 功能

1. **每次对话后自动统计** Token 消耗
2. **每天 0 点自动发送** 前一天的消耗总额
3. **生成详细报告** 包含成本分析

---

## 🚀 快速开始

### 1. 安装 Cron 定时任务

```bash
crontab /home/admin/.openclaw/workspace/scripts/token_cron.conf
```

### 2. 验证安装

```bash
crontab -l
# 应显示：0 0 * * * ... token_tracker.py send
```

### 3. 测试

```bash
# 查看当前统计
python3 /home/admin/.openclaw/workspace/scripts/token_tracker.py show

# 手动发送日报
python3 /home/admin/.openclaw/workspace/scripts/token_tracker.py send
```

---

## 📝 使用方法

### 每次对话后更新统计

**自动调用（推荐）：**
在应用代码中调用：
```python
import subprocess

# 对话结束后调用
subprocess.run([
    'python3', '/home/admin/.openclaw/workspace/scripts/token_tracker.py',
    'update', str(input_tokens), str(output_tokens)
])
```

**手动调用：**
```bash
python3 scripts/token_tracker.py update 574000 574
```

### 查看当前统计

```bash
python3 scripts/token_tracker.py show
```

输出示例：
```
============================================================
📊 Token 消耗统计
============================================================
日期：2026-04-09
输入 Token: 574,000
输出 Token: 574
总消耗：574,574
对话次数：1
总成本：$0.004890
============================================================
```

### 生成日报

```bash
# 生成昨天的报告
python3 scripts/token_tracker.py report

# 生成指定日期的报告
python3 scripts/token_tracker.py report 2026-04-08
```

### 发送日报

```bash
# 自动发送（每天 0 点）
# cron 会自动执行

# 手动发送
python3 scripts/token_tracker.py send
```

---

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `scripts/token_tracker.py` | 主程序 |
| `scripts/token_cron.conf` | Cron 配置 |
| `logs/token_stats.json` | 当前统计 |
| `logs/token_history.csv` | 历史记录 |
| `logs/token_daily_report.md` | 日报文件 |
| `logs/cron_token_report.log` | Cron 日志 |

---

## 📊 日报格式

```markdown
# Token 消耗日报

**日期：** 2026-04-09

## 📊 消耗统计

| 指标 | 数值 |
|------|------|
| **输入 Token** | 574,000 |
| **输出 Token** | 574 |
| **总消耗** | 574,574 |
| **对话次数** | 1 |
| **总成本** | $0.004890 |

## 📈 平均统计

**平均每次对话：**
- Token: 574,574 tokens
- 成本：$0.004890

## 💡 Token 优化建议

1. **使用知识图谱查询** - 71.5 倍 Token 节省
2. **选择合适的模式** - L1/L2/L3
3. **避免重复查询** - 使用缓存
```

---

## 🔧 配置

### 修改模型价格

编辑 `scripts/token_tracker.py`：

```python
MODEL_PRICES = {
    'dashscope/qwen3.5-plus': {'input': 0.002, 'output': 0.006},
    'dashscope/qwen3-max': {'input': 0.02, 'output': 0.06},
    # 添加更多模型...
}
```

### 修改报告发送方式

编辑 `scripts/token_tracker.py` 的 `send_daily_report()` 函数：

```python
def send_daily_report():
    # 生成报告
    report, stats = generate_daily_report(yesterday)
    
    # 集成飞书/邮件等
    # 示例：飞书 Webhook
    # requests.post(WEBHOOK_URL, json={'text': report})
    
    return report, stats
```

---

## 📈 查看历史

### CSV 历史记录

```bash
cat logs/token_history.csv
```

### 历史日报

```bash
ls -lh logs/token_daily_report*.md
```

---

## ⚠️ 注意事项

1. **Cron 权限** - 确保 cron 服务运行
2. **文件权限** - 确保脚本可执行
3. **Python 路径** - 确认 `/usr/bin/python3` 存在
4. **日志轮转** - 定期清理旧日志

---

## 🔍 故障排查

### Cron 不执行

```bash
# 检查 cron 服务
systemctl status cron

# 查看 cron 日志
tail -f /var/log/cron

# 测试脚本
python3 scripts/token_tracker.py show
```

### 统计不准确

```bash
# 重置统计
rm logs/token_stats.json
python3 scripts/token_tracker.py show
```

### 报告未生成

```bash
# 手动生成
python3 scripts/token_tracker.py report

# 检查日志
cat logs/cron_token_report.log
```

---

## 📞 集成示例

### OpenClaw 集成

在 OpenClaw 会话结束时自动调用：

```python
# 在会话结束 hook 中
import subprocess

def on_session_end(input_tokens, output_tokens):
    subprocess.run([
        'python3', 'scripts/token_tracker.py',
        'update', str(input_tokens), str(output_tokens)
    ])
```

### Feishu 通知

```python
import requests

def send_feishu_report(report):
    webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/XXX"
    requests.post(webhook, json={'text': report})
```

---

**创建时间：** 2026-04-09  
**版本：** v1.0
