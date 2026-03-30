# 🚀 机器人数据收集自动化 - 安装指南

## 📋 前置检查

### 1. 检查 Python 环境

```bash
python3 --version
# 需要 Python 3.8+
```

### 2. 检查必要目录

```bash
ls -la /home/admin/.openclaw/workspace/
# 确认 workspace 存在
```

---

## 🔧 安装步骤

### 步骤 1: 安装 Python 依赖

```bash
# 方法 A: 使用 pip
pip3 install requests beautifulsoup4

# 方法 B: 使用 uv（推荐）
uv pip install requests beautifulsoup4

# 方法 C: 系统级安装
sudo apt-get update
sudo apt-get install -y python3-pip python3-bs4
pip3 install requests beautifulsoup4
```

### 步骤 2: 验证脚本文件

```bash
cd /home/admin/.openclaw/workspace/scripts

# 检查文件是否存在
ls -la 机器人数据收集自动化.py
ls -la run_robot_collection.sh
ls -la push_daily_report.sh
ls -la robot_collection_cron.conf

# 检查执行权限
chmod +x run_robot_collection.sh push_daily_report.sh
```

### 步骤 3: 测试运行

```bash
# 手动执行一次数据收集
cd /home/admin/.openclaw/workspace
python3 scripts/机器人数据收集自动化.py

# 查看输出
tail -f logs/机器人数据收集_*.log
```

### 步骤 4: 配置定时任务

```bash
# 安装 crontab 配置
crontab /home/admin/.openclaw/workspace/scripts/robot_collection_cron.conf

# 验证安装
crontab -l

# 应该看到类似内容：
# 0 9 * * * cd /home/admin/.openclaw/workspace && bash /home/admin/.openclaw/workspace/scripts/run_robot_collection.sh
# 0 20 * * * cd /home/admin/.openclaw/workspace && bash /home/admin/.openclaw/workspace/scripts/push_daily_report.sh
```

### 步骤 5: 检查 cron 服务

```bash
# 检查服务状态
systemctl status cron

# 如果未运行，启动服务
sudo systemctl start cron
sudo systemctl enable cron
```

---

## ✅ 验证安装

### 验证 1: 检查定时任务

```bash
crontab -l
# 应该显示两条定时任务
```

### 验证 2: 手动触发测试

```bash
# 测试数据收集
bash /home/admin/.openclaw/workspace/scripts/run_robot_collection.sh

# 检查日志
cat logs/定时任务执行.log
```

### 验证 3: 检查文件创建

```bash
# 检查日志文件
ls -la logs/机器人数据收集_*.log

# 检查报告目录
ls -la reports/
```

### 验证 4: Token 统计

```bash
# 查看 Token 使用统计
cat logs/token_stats.json

# 应该显示类似：
# {
#   "date": "2026-03-25",
#   "used": 0,
#   "limit": 1000000
# }
```

---

## 🔔 配置消息推送（可选）

### 飞书机器人推送

1. **创建飞书群机器人**
   - 在飞书中创建群聊
   - 添加群机器人 → 自定义机器人
   - 复制 Webhook 地址

2. **配置 Webhook**
   
   编辑 `push_daily_report.sh`，取消注释并配置：
   
   ```bash
   WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK"
   
   curl -X POST -H "Content-Type: application/json" \
        -d "{
          \"msg_type\":\"text\",
          \"content\":{
            \"text\":\"📊 机器人数据收集日报已生成：${TODAY}\\n查看报告：${REPORT_FILE}\"
          }
        }" \
        "$WEBHOOK_URL"
   ```

3. **测试推送**
   
   ```bash
   bash /home/admin/.openclaw/workspace/scripts/push_daily_report.sh
   ```

### 钉钉机器人推送

1. **创建钉钉群机器人**
   - 在钉钉群设置中添加机器人
   - 选择「自定义」
   - 复制 Webhook 地址

2. **配置推送**
   
   编辑 `push_daily_report.sh`：
   
   ```bash
   WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
   
   curl -X POST -H "Content-Type: application/json" \
        -d "{
          \"msgtype\":\"markdown\",
          \"markdown\":{
            \"title\":\"机器人数据收集日报\",
            \"text\":\"#### 📊 机器人数据收集日报\\n- 日期：${TODAY}\\n- 报告已生成，请查看\"
          }
        }" \
        "$WEBHOOK_URL"
   ```

### Telegram 推送

1. **创建 Telegram Bot**
   - 联系 @BotFather 创建机器人
   - 获取 Bot Token
   - 获取 Chat ID

2. **配置推送**
   
   ```bash
   BOT_TOKEN="YOUR_BOT_TOKEN"
   CHAT_ID="YOUR_CHAT_ID"
   
   curl -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
        -d "chat_id=$CHAT_ID&text=📊 机器人数据收集日报已生成：${TODAY}"
   ```

---

## 🛠️ 故障排查

### 问题 1: Python 依赖缺失

```bash
# 错误：ModuleNotFoundError: No module named 'requests'

# 解决：
pip3 install requests beautifulsoup4

# 或检查 Python 路径
which python3
python3 -m pip install requests beautifulsoup4
```

### 问题 2: 定时任务不执行

```bash
# 检查 cron 服务
sudo systemctl status cron

# 查看 cron 日志
grep CRON /var/log/syslog | tail -20

# 或
journalctl -u cron -f

# 重启 cron 服务
sudo systemctl restart cron
```

### 问题 3: 权限问题

```bash
# 错误：Permission denied

# 解决：
chmod +x /home/admin/.openclaw/workspace/scripts/*.sh
chmod 644 /home/admin/.openclaw/workspace/scripts/*.py
```

### 问题 4: 路径问题

```bash
# 错误：文件不存在

# 解决：使用绝对路径
cd /home/admin/.openclaw/workspace
pwd
```

### 问题 5: 编码问题

```bash
# 错误：UnicodeDecodeError

# 解决：确保文件使用 UTF-8 编码
file scripts/机器人数据收集自动化.py
# 应该显示：UTF-8 Unicode text
```

---

## 📊 日常运维

### 查看执行情况

```bash
# 查看最新日志
tail -100 logs/机器人数据收集_*.log

# 查看定时任务日志
tail -50 logs/定时任务执行.log

# 查看 Token 使用
cat logs/token_stats.json | python3 -m json.tool
```

### 清理旧日志

```bash
# 保留最近 30 天的日志
find logs/ -name "机器人数据收集_*.log" -mtime +30 -delete

# 保留最近 30 天的报告
find reports/ -name "*.md" -mtime +30 -delete
```

### 备份数据库

```bash
# 每日备份
cp /home/admin/.openclaw/workspace/机器人数据库_核心版.csv \
   /home/admin/.openclaw/workspace/backup/机器人数据库_$(date +%Y%m%d).csv

# 或使用 cron 自动备份
echo "0 21 * * * cp /home/admin/.openclaw/workspace/机器人数据库_核心版.csv /home/admin/.openclaw/workspace/backup/机器人数据库_\$(date +\\%Y\\%m\\%d).csv" | crontab -
```

---

## 📞 获取帮助

### 查看文档

```bash
cat /home/admin/.openclaw/workspace/scripts/README_机器人数据收集自动化.md
```

### 测试模式

```bash
# 启用调试模式（在脚本中添加）
python3 -c "
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/scripts')
from 机器人数据收集自动化 import *
# 手动测试各个函数
"
```

---

## ✅ 安装完成检查清单

- [ ] Python 依赖已安装
- [ ] 脚本文件存在且有执行权限
- [ ] 手动测试运行成功
- [ ] Crontab 已安装
- [ ] Cron 服务正在运行
- [ ] 日志目录可写
- [ ] （可选）消息推送已配置
- [ ] （可选）备份策略已配置

---

*安装指南版本：1.0*  
*更新时间：2026-03-25*
