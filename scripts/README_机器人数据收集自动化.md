# 🤖 机器人数据收集自动化系统

## 📋 系统概述

本系统实现机器人数据库的自动化数据收集、更新和日报推送。

### 核心功能

- ✅ **定时收集**：每天 9:00 自动执行数据收集
- ✅ **日报推送**：每天 20:00 生成并推送日报
- ✅ **Token 控制**：每日消耗不超过 100 万 token
- ✅ **多渠道收集**：官方渠道 + 行业平台 + 公开数据
- ✅ **增量更新**：智能识别新产品和价格更新
- ✅ **错误处理**：完善的日志和异常处理机制

---

## 📁 文件结构

```
/home/admin/.openclaw/workspace/
├── scripts/
│   ├── 机器人数据收集自动化.py      # 主收集脚本
│   ├── run_robot_collection.sh       # 收集任务执行脚本
│   ├── push_daily_report.sh          # 日报推送脚本
│   ├── robot_collection_cron.conf    # Crontab 配置文件
│   └── README_机器人数据收集自动化.md   # 本文档
├── reports/
│   └── YYYY-MM-DD_机器人数据收集日报.md  # 每日报告
├── logs/
│   ├── 机器人数据收集_YYYYMMDD_HHMMSS.log  # 收集日志
│   ├── 定时任务执行.log              # 定时任务日志
│   ├── 日报推送.log                  # 推送日志
│   └── token_stats.json              # Token 使用统计
└── 机器人数据库_核心版.csv            # 主数据库
```

---

## 🚀 快速开始

### 步骤 1: 安装依赖

```bash
# 安装 Python 依赖
pip3 install requests beautifulsoup4

# 或使用 uv（如果已安装）
uv pip install requests beautifulsoup4
```

### 步骤 2: 配置定时任务

```bash
# 安装 crontab 配置
crontab /home/admin/.openclaw/workspace/scripts/robot_collection_cron.conf

# 验证安装
crontab -l
```

### 步骤 3: 手动测试

```bash
# 测试数据收集
bash /home/admin/.openclaw/workspace/scripts/run_robot_collection.sh

# 测试日报推送
bash /home/admin/.openclaw/workspace/scripts/push_daily_report.sh

# 查看日志
tail -f /home/admin/.openclaw/workspace/logs/机器人数据收集_*.log
```

---

## ⚙️ 配置说明

### Token 控制

在 `机器人数据收集自动化.py` 中配置：

```python
DAILY_TOKEN_LIMIT: int = 1_000_000  # 每日 100 万 token
TOKEN_COST_PER_REQUEST: int = 100   # 估算每次请求 token 消耗
```

### 收集时间

```python
COLLECTION_TIME: str = "09:00"  # 收集时间
REPORT_TIME: str = "20:00"      # 报告时间
```

### 收集渠道

```python
CHANNELS = {
    "official": {   # 官方渠道（第一优先级）
        "enabled": True,
        "sources": ["company_website", "official_store"]
    },
    "industry": {   # 行业平台（第二优先级）
        "enabled": True,
        "sources": ["ggrobot.com", "robotchina.com"]
    },
    "public": {     # 公开数据（第三优先级）
        "enabled": True,
        "sources": ["gov_procurement", "bidding_platform"]
    }
}
```

---

## 📊 数据收集流程

```
1. 加载现有数据库
   ↓
2. 检查 Token 余额
   ↓
3. 收集官方渠道数据（公司官网、官方商城）
   ↓
4. 收集行业平台数据（高工机器人、中国机器人网）
   ↓
5. 检查产品价格更新
   ↓
6. 收集事故数据
   ↓
7. 数据去重和合并
   ↓
8. 保存数据库
   ↓
9. 生成统计报告
   ↓
10. 记录 Token 使用情况
```

---

## 📝 日报内容

每日 20:00 生成的日报包含：

- **收集概览**：开始/结束时间、新增/更新数量
- **Token 使用**：消耗量、剩余量、使用百分比
- **完成工作**：今日执行的任务列表
- **遇到问题**：错误和异常记录
- **数据库状态**：总记录数、文件大小
- **明日计划**：下一步工作安排

---

## 🔧 自定义开发

### 添加新的收集渠道

在 `RobotDataCollector` 类中添加新方法：

```python
def collect_from_new_source(self) -> List[Dict]:
    """从新渠道收集数据"""
    if not self.token_manager.can_use(estimated_cost):
        return []
    
    try:
        # 实现收集逻辑
        response = self.session.get(url)
        data = self.parse_response(response)
        
        self.token_manager.use(estimated_cost)
        return data
    except Exception as e:
        self.logger.error(f"收集失败：{e}")
        return []
```

### 定制解析逻辑

针对不同网站实现解析器：

```python
def parse_company_website(self, html: str) -> Dict:
    """解析公司官网 HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    
    # 提取产品信息
    product = {
        '公司全称': self.extract_text(soup, '.company-name'),
        '型号': self.extract_text(soup, '.product-model'),
        '价格': self.extract_price(soup, '.price'),
        # ...
    }
    
    return product
```

---

## 🛡️ 安全和最佳实践

### Token 管理

- ✅ 每次请求前检查余额
- ✅ 实时统计使用情况
- ✅ 达到上限自动停止
- ✅ 每日重置计数器

### 错误处理

- ✅ 捕获所有异常
- ✅ 记录详细错误信息
- ✅ 不影响其他渠道收集
- ✅ 支持重试机制

### 数据质量

- ✅ 去重处理
- ✅ 格式验证
- ✅ 必填字段检查
- ✅ 异常值检测

---

## 📈 监控和维护

### 查看日志

```bash
# 查看最新日志
tail -f /home/admin/.openclaw/workspace/logs/机器人数据收集_*.log

# 查看 Token 统计
cat /home/admin/.openclaw/workspace/logs/token_stats.json

# 查看定时任务日志
tail -f /home/admin/.openclaw/workspace/logs/定时任务执行.log
```

### 检查定时任务

```bash
# 查看已安装的定时任务
crontab -l

# 查看 cron 服务状态
systemctl status cron

# 手动触发一次收集（测试用）
bash /home/admin/.openclaw/workspace/scripts/run_robot_collection.sh
```

### 常见问题

**Q: 定时任务不执行？**
```bash
# 检查 cron 服务
sudo systemctl status cron
sudo systemctl restart cron

# 检查 crontab 语法
crontab -l
```

**Q: Token 消耗过快？**
- 调整 `TOKEN_COST_PER_REQUEST` 估算值
- 减少收集渠道优先级
- 增加缓存机制

**Q: 数据收集失败？**
- 检查网络连接
- 查看日志文件错误信息
- 验证目标网站是否可访问

---

## 📞 推送配置

### 飞书推送

```bash
# 在 push_daily_report.sh 中配置
WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK"

curl -X POST -H "Content-Type: application/json" \
     -d "{\"msg_type\":\"text\",\"content\":{\"text\":\"📊 机器人数据收集日报已生成\"}}" \
     "$WEBHOOK_URL"
```

### 钉钉推送

```bash
WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"

curl -X POST -H "Content-Type: application/json" \
     -d "{\"msgtype\":\"text\",\"text\":{\"content\":\"📊 机器人数据收集日报已生成\"}}" \
     "$WEBHOOK_URL"
```

### Telegram 推送

```bash
BOT_TOKEN="YOUR_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"

curl -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
     -d "chat_id=$CHAT_ID&text=📊 机器人数据收集日报已生成"
```

---

## 🎯 下一步优化

1. **智能解析**：针对不同网站实现定制解析器
2. **数据验证**：增加数据质量检查规则
3. **缓存机制**：减少重复请求，提高效率
4. **告警系统**：异常情况实时通知
5. **可视化**：数据趋势图表和仪表板
6. **API 集成**：支持从 API 直接获取数据

---

*文档更新时间：2026-03-25*
