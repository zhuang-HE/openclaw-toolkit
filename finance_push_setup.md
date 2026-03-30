# 金融数据推送配置指南

## 📋 推送方案对比

| 方式 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **飞书机器人** | 免费、稳定、富文本 | 需创建群/机器人 | ⭐⭐⭐⭐⭐ |
| 飞书个人消息 | 直接推送到个人 | 需要 API 权限配置 | ⭐⭐⭐⭐ |
| 邮件推送 | 正式、可存档 | 可能进垃圾箱 | ⭐⭐⭐ |
| 微信推送 | 最常用 | 需要企业微信/Server 酱 | ⭐⭐⭐ |

---

## 🚀 方案一：飞书机器人（推荐）

### 第一步：创建飞书机器人

1. 打开飞书，创建一个群（可以只拉你自己）
2. 点击右上角 **群设置** → **机器人** → **添加机器人**
3. 选择 **自定义机器人**
4. 填写机器人名称：`金融数据助手`
5. 勾选 **自定义关键词**（可选，如"金融"）
6. 点击 **完成**
7. **复制 Webhook 地址**（重要！）

### 第二步：配置脚本

编辑 `finance_push_feishu.py`，替换 Webhook：

```python
# 第 17 行，替换为你的 Webhook URL
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/XXXXXXXXX"
```

### 第三步：测试推送

```bash
cd /home/admin/.openclaw/workspace
python finance_push_feishu.py
```

如果收到飞书消息，说明配置成功！

### 第四步：设置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加以下两行（工作日 9:15 和 16:00）
15 9 * * 1-5 cd /home/admin/.openclaw/workspace && python finance_push_feishu.py >> finance_data/push.log 2>&1
0 16 * * 1-5 cd /home/admin/.openclaw/workspace && python finance_push_feishu.py >> finance_data/push.log 2>&1
```

**保存退出**（vim 按 `:wq`）

### 第五步：验证定时任务

```bash
# 查看已配置的定时任务
crontab -l

# 查看 cron 服务状态
systemctl status cron
```

---

## 📧 方案二：飞书个人消息（更私密）

如果需要直接推送到你的飞书私聊（而不是群），需要：

1. 创建飞书应用
2. 获取 App ID 和 App Secret
3. 获取用户 ID
4. 使用飞书 API 发送消息

**需要我帮你配置这个方案吗？**

---

## 📊 推送效果预览

### 盘前推送（9:15）

```
📊 金融数据简报 - 盘前
━━━━━━━━━━━━━━━━━━━━━━
采集时间：2026-03-13 09:15

主要指数
📈 上证指数：3052.45 (+0.85%)
📈 深证成指：9856.32 (+1.12%)
📈 创业板指：2045.67 (+1.58%)
📉 沪深 300：3650.00 (-0.25%)

💰 北向资金：+45.60 亿元
🏆 涨跌停：涨停 52 家 | 跌停 8 家

数据源：AkShare（东方财富、新浪财经等）
```

### 盘后推送（16:00）

```
📊 金融数据简报 - 盘后
━━━━━━━━━━━━━━━━━━━━━━
采集时间：2026-03-13 16:00

主要指数
📈 上证指数：3065.78 (+1.28%)
📈 深证成指：9920.45 (+1.75%)
📈 创业板指：2058.90 (+2.15%)
📈 沪深 300：3680.50 (+0.82%)

💰 北向资金：+52.30 亿元
🏆 涨跌停：涨停 68 家 | 跌停 5 家

数据源：AkShare（东方财富、新浪财经等）
```

---

## 🔧 常见问题

### Q1: 收不到消息？
- 检查 Webhook URL 是否正确
- 检查 cron 服务是否运行：`systemctl status cron`
- 查看日志：`tail -f finance_data/push.log`

### Q2: 节假日也推送？
修改 crontab，排除节假日：
```bash
# 需要配合脚本判断交易日
```

### Q3: 想增加推送内容？
编辑 `finance_push_feishu.py` 中的 `get_market_summary()` 函数

### Q4: 想改推送时间？
修改 crontab 中的时间配置：
```bash
# 格式：分 时 日 月 周
15 9 * * 1-5  # 工作日 9:15
0 16 * * 1-5  # 工作日 16:00
```

---

## 📁 文件清单

```
/home/admin/.openclaw/workspace/
├── finance_data_auto.py          # 数据采集脚本
├── finance_push_feishu.py        # 飞书推送脚本
├── finance_push_setup.md         # 配置指南（本文件）
├── finance_data_template.md      # 数据格式模板
└── finance_data/                 # 数据存储目录
    ├── finance_data_*.json       # 原始数据
    └── push_backup/              # 推送备份
```

---

## ✅ 下一步

1. **创建飞书机器人**（5 分钟）
2. **复制 Webhook 到脚本**
3. **运行测试**：`python finance_push_feishu.py`
4. **配置 cron**：`crontab -e`

需要我帮你：
- 直接配置 cron 定时任务？
- 改用其他推送方式（邮件/微信）？
- 增加更多数据指标？
