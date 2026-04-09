# 飞书 Token 日报配置说明

## ✅ 已配置完成

**飞书 Webhook:**
```
https://open.feishu.cn/open-apis/bot/v2/hook/587f3c74-4345-4fc6-98b3-b2a935f6787e
```

**推送时间:** 每天 0:00（北京时间）

**推送内容:** Token 消耗日报

---

## 📊 日报格式

```
📊 Token 消耗日报 - 2026-04-09

📈 消耗统计
输入 Token: 574,000
输出 Token: 574
总消耗：574,574 tokens
对话次数：1 次
总成本：$1.151444

📉 平均统计
平均每次对话：574,574 tokens
平均成本：$1.151444

💡 Token 优化建议
1. 使用知识图谱查询 - 71.5 倍节省
2. 选择合适的模式 (L1/L2/L3)
3. 避免重复查询 - 使用缓存
```

---

## 🔧 配置说明

### 1. Cron 定时任务

**已安装:**
```bash
0 0 * * * python3 /home/admin/.openclaw/workspace/scripts/token_tracker.py send
```

**执行时间:** 每天 0:00 AM

### 2. 飞书 Webhook

**配置文件:** `scripts/token_tracker.py`

**变量:**
```python
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/587f3c74-4345-4fc6-98b3-b2a935f6787e"
```

### 3. 消息格式

**类型:** post（富文本消息）

**语言:** 简体中文 (zh_cn)

**内容:**
- 标题：📊 Token 消耗日报 - 日期
- 消耗统计表格
- 平均统计
- Token 优化建议

---

## 📝 测试方法

### 手动测试推送

```bash
python3 scripts/token_tracker.py send
```

### 发送测试消息

```bash
python3 -c "
import requests
webhook = 'https://open.feishu.cn/open-apis/bot/v2/hook/587f3c74-4345-4fc6-98b3-b2a935f6787e'
message = {'msg_type': 'text', 'content': {'text': '测试消息'}}
requests.post(webhook, json=message)
"
```

### 查看 Cron 日志

```bash
tail -f logs/cron_token_report.log
```

---

## 🎯 功能特性

### 自动统计
- ✅ 每次对话后自动更新统计
- ✅ 自动计算成本（按模型价格）
- ✅ 自动保存到历史记录

### 自动推送
- ✅ 每天 0 点自动推送
- ✅ 飞书富文本消息
- ✅ 包含详细统计和优化建议

### 历史记录
- ✅ CSV 格式历史记录
- ✅ 可查询任意日期的统计
- ✅ 自动生成日报文件

---

## 📊 查看统计

### 当前统计
```bash
python3 scripts/token_tracker.py show
```

### 历史统计
```bash
cat logs/token_history.csv
```

### 日报文件
```bash
cat logs/token_daily_report.md
```

---

## 🔍 故障排查

### 飞书推送失败

**检查:**
1. Webhook URL 是否正确
2. 网络连接是否正常
3. 飞书机器人是否启用

**日志:**
```bash
cat logs/cron_token_report.log
```

### Cron 不执行

**检查:**
```bash
crontab -l
systemctl status cron
```

**测试:**
```bash
python3 scripts/token_tracker.py send
```

---

## 📞 联系人

**配置时间:** 2026-04-09  
**配置者:** AI Agent  
**版本:** v1.0

---

**飞书日报已配置完成，每天 0 点自动推送！** 🎉
