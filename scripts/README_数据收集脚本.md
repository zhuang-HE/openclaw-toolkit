# 无人机 BI 数据库 - 月度数据收集脚本配置指南

## 📋 目录结构

```
/home/admin/.openclaw/workspace/
├── scripts/
│   ├── 无人机数据月度收集.py          # 完整版（需要 Feishu API 配置）
│   ├── 无人机数据月度收集_简化版.py    # 简化版（推荐使用）
│   ├── run_monthly_collection.sh       # 快速执行脚本
│   └── drone_data_cron.conf            # Cron 定时任务配置
├── logs/
│   └── 无人机数据收集.log              # 执行日志
└── 无人机 BI 数据库_*.csv              # 导出的数据文件
```

---

## 🚀 快速开始

### 1. 手动执行测试

```bash
# 进入脚本目录
cd /home/admin/.openclaw/workspace/scripts

# 执行简化版脚本（推荐）
python3 无人机数据月度收集_简化版.py

# 或使用快速执行脚本
bash run_monthly_collection.sh
```

### 2. 查看执行日志

```bash
# 查看最新日志
tail -f /home/admin/.openclaw/workspace/logs/无人机数据收集.log

# 查看历史日志
ls -la /home/admin/.openclaw/workspace/logs/
```

---

## ⏰ 设置定时任务

### 方法一：使用 crontab（推荐）

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每月最后一天 23:00 执行）
0 23 28-31 * * [ "$(date -d tomorrow +\%d)" = "01" ] && /usr/bin/python3 /home/admin/.openclaw/workspace/scripts/无人机数据月度收集_简化版.py >> /home/admin/.openclaw/workspace/logs/无人机数据收集.log 2>&1

# 或者每月 1 日凌晨 1:00 执行（备用）
0 1 1 * * /usr/bin/python3 /home/admin/.openclaw/workspace/scripts/无人机数据月度收集_简化版.py >> /home/admin/.openclaw/workspace/logs/无人机数据收集.log 2>&1

# 保存后验证
crontab -l
```

### 方法二：使用系统定时器（systemd）

创建服务文件 `/etc/systemd/system/drone-data-collector.service`：

```ini
[Unit]
Description=无人机 BI 数据库月度数据收集
After=network.target

[Service]
Type=oneshot
User=admin
ExecStart=/usr/bin/python3 /home/admin/.openclaw/workspace/scripts/无人机数据月度收集_简化版.py
WorkingDirectory=/home/admin/.openclaw/workspace/scripts
StandardOutput=append:/home/admin/.openclaw/workspace/logs/无人机数据收集.log
StandardError=append:/home/admin/.openclaw/workspace/logs/无人机数据收集.log
```

创建定时器文件 `/etc/systemd/system/drone-data-collector.timer`：

```ini
[Unit]
Description=每月执行无人机数据收集
Requires=drone-data-collector.service

[Timer]
OnCalendar=*-*-28,29,30,31 23:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

启用定时器：

```bash
sudo systemctl daemon-reload
sudo systemctl enable drone-data-collector.timer
sudo systemctl start drone-data-collector.timer
sudo systemctl list-timers  # 查看定时器状态
```

---

## 🔧 Feishu API 配置（完整版需要）

如果使用完整版脚本（`无人机数据月度收集.py`），需要配置 Feishu API：

### 1. 创建 Feishu 应用

1. 访问 https://open.feishu.cn/app
2. 创建企业内部应用
3. 获取 App ID 和 App Secret

### 2. 配置脚本

编辑 `无人机数据月度收集.py`，修改以下配置：

```python
# 数据库配置
DRONE_BI_APP_TOKEN = "HYYgbijbZazt4PsLT6MclOXkn4c"
DRONE_BI_TABLE_ID = "tblJAciMAjql32wu"
DRONE_ACCIDENT_APP_TOKEN = "CRZnbAd7eakijQswHsAc4F8mnqd"
DRONE_ACCIDENT_TABLE_ID = "tbl6IzOz1vsbI3Cb"

# Feishu API 配置
app_id = "cli_xxxxxxxxxxxxx"  # 替换为你的 App ID
app_secret = "xxxxxxxxxxxxx"  # 替换为你的 App Secret
```

### 3. 添加应用权限

在 Feishu 开放平台添加以下权限：
- 多维表格读取权限
- 多维表格写入权限

---

## 📊 数据收集内容

### 无人机 BI 数据库

| 字段 | 数据来源 | 更新频率 |
|------|----------|----------|
| 销量数据 | 电商平台、行业报告 | 月度 |
| 事故数据 | 保险公司、民航局 | 月度 |
| 损失金额 | 保险公司理赔数据 | 月度 |

### 事故数据库

| 字段 | 数据来源 | 更新频率 |
|------|----------|----------|
| 案件信息 | 保险公司理赔系统 | 实时/月度 |
| 损失金额 | 保险公司理赔数据 | 实时/月度 |
| 事故类型 | 案件报告 | 实时/月度 |

---

## 🔍 故障排查

### 常见问题

#### 1. 脚本执行失败

```bash
# 检查 Python 环境
python3 --version

# 检查依赖
pip3 list | grep requests

# 安装依赖
pip3 install requests
```

#### 2. 日志文件不存在

```bash
# 创建日志目录
mkdir -p /home/admin/.openclaw/workspace/logs

# 检查权限
ls -la /home/admin/.openclaw/workspace/
```

#### 3. Cron 任务不执行

```bash
# 检查 cron 服务状态
sudo systemctl status cron

# 查看 cron 日志
grep CRON /var/log/syslog

# 验证 crontab 语法
crontab -l
```

---

## 📈 监控与告警

### 添加邮件告警

在脚本末尾添加邮件通知：

```python
import smtplib
from email.mime.text import MIMEText

def send_email_alert(success, summary):
    """发送邮件告警"""
    msg = MIMEText(f"""
    无人机数据收集任务执行完成
    
    执行结果：{'成功' if success else '失败'}
    {summary}
    """)
    
    msg['Subject'] = '无人机数据收集任务通知'
    msg['From'] = 'alert@example.com'
    msg['To'] = 'admin@example.com'
    
    # 发送邮件
    # ...
```

---

## 📝 维护说明

### 定期维护

1. **每周**：检查日志文件，确认任务正常执行
2. **每月**：验证导出数据完整性
3. **每季度**：清理旧日志文件（保留最近 3 个月）

### 日志清理

```bash
# 清理 3 个月前的日志
find /home/admin/.openclaw/workspace/logs/ -name "*.log" -mtime +90 -delete
```

---

## 📞 技术支持

如遇到问题，请检查：
1. 日志文件：`/home/admin/.openclaw/workspace/logs/无人机数据收集.log`
2. Cron 日志：`/var/log/syslog` (grep CRON)
3. 系统时间：`date` (确保时区正确)

---

**最后更新：** 2026-03-18  
**版本：** v1.0
