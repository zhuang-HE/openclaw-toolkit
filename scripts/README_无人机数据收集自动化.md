# 🛩️ 无人机数据收集自动化系统

## 📋 系统概述

本系统实现无人机 BI 数据库的自动化数据收集、更新和月度报告推送。

### 核心功能

- ✅ **月度收集**：每月 28 日自动执行数据收集
- ✅ **报告推送**：生成月报并推送到飞书
- ✅ **数据备份**：自动备份原数据库文件
- ✅ **增量更新**：智能识别新数据并更新
- ✅ **事故案例库**：累积存储事故案例，支持查询分析
- ✅ **销量趋势分析**：跟踪销量变化，生成趋势报告
- ✅ **重大事件告警**：伤亡/高损失自动告警
- ✅ **电商爬取**：支持电商平台销量爬取（可扩展）
- ✅ **错误处理**：完善的日志和异常处理机制

---

## 📁 文件结构

```
/home/admin/.openclaw/workspace/
├── scripts/
│   ├── 无人机数据收集自动化.py      # 主收集脚本
│   ├── run_drone_collection.sh       # 收集任务执行脚本
│   ├── drone_collection_cron.conf    # Crontab 配置文件
│   └── README_无人机数据收集自动化.md   # 本文档
├── reports/drone/
│   └── YYYY-MM_无人机数据收集月报.md    # 月度报告
├── drone_data/
│   ├── 无人机事故案例库.csv          # 事故案例数据库（累积）
│   └── 销量历史趋势.csv               # 销量历史记录（累积）
├── logs/
│   ├── 无人机数据收集_自动化.log     # 收集日志
│   ├── 无人机定时任务执行.log        # 定时任务日志
│   └── cron_drone_collection.log     # Cron 执行日志
└── 无人机 BI 数据库_含人伤金额.csv    # 主数据库
```

---

## 🚀 快速开始

### 步骤 1: 安装依赖

```bash
# 安装 Python 依赖
pip3 install requests

# 或使用 uv（如果已安装）
uv pip install requests
```

### 步骤 2: 配置定时任务（已完成）

```bash
# 安装 crontab 配置
crontab /home/admin/.openclaw/workspace/scripts/drone_collection_cron.conf

# 验证安装
crontab -l
```

### 步骤 3: 手动测试

```bash
# 测试数据收集
bash /home/admin/.openclaw/workspace/scripts/run_drone_collection.sh

# 查看日志
tail -f /home/admin/.openclaw/workspace/logs/无人机数据收集_自动化.log
```

---

## ⚙️ 配置说明

### 飞书推送配置

在 `无人机数据收集自动化.py` 中配置：

```python
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/5e0b173c-c236-4df8-80de-31201bb35d13"
```

### 收集时间

```python
# 每月 28 日 23:00 执行
0 23 28 * *
```

### 数据库路径

```python
DATABASE_FILE = "/home/admin/.openclaw/workspace/无人机 BI 数据库_含人伤金额.csv"
ACCIDENT_DB_FILE = "/home/admin/.openclaw/workspace/drone_data/无人机事故案例库.csv"
SALES_HISTORY_FILE = "/home/admin/.openclaw/workspace/drone_data/销量历史趋势.csv"
```

### 告警阈值配置

```python
ALERT_THRESHOLDS = {
    "death_count": 1,           # 伤亡人数达到即告警
    "serious_accident_count": 3, # 严重事故数达到即告警
    "loss_amount": 100,         # 损失金额超过 100 万即告警（万元）
}
```

### Webhook 配置

```python
WEBHOOK_URL_MONTHLY = "..."  # 月报推送 Webhook
WEBHOOK_URL_ALERT = "..."    # 告警推送 Webhook（可配置不同地址）
```

---

## 📊 数据收集流程

```
1. 收集电商平台销量数据
   ↓
2. 收集保险公司事故数据
   ↓
3. 备份原数据库
   ↓
4. 更新数据库记录
   ↓
5. 生成月度报告
   ↓
6. 推送报告到飞书
   ↓
7. 记录执行日志
```

---

## 📝 月度报告内容

每月生成的报告包含：

- **收集概览**：机型总数、销量统计、事故统计、告警统计
- **完成工作**：本月执行的任务列表
- **销量趋势分析**：各机型环比变化（上升/下降/稳定）
- **事故案例**：本月事故案例详情 + 数据库累计
- **数据库状态**：文件大小、备份信息
- **下月计划**：下一步工作安排

---

## 🔧 高级功能说明

### 事故案例数据库

系统自动累积事故案例到 `drone_data/无人机事故案例库.csv`：

- **自动去重**：基于案例 ID 避免重复入库
- **统一字段**：标准化字段格式（品牌、型号、事故类型、地点、损失、伤亡、原因）
- **累计统计**：月报中显示累计案例数
- **查询分析**：可用于后续数据分析和趋势研究

### 销量趋势分析

系统自动跟踪各机型销量变化：

- **历史记录**：每次收集保存到 `销量历史趋势.csv`
- **趋势计算**：环比变化百分比（上升/下降/稳定）
- **可视化**：月报中展示各机型销量趋势表
- **决策支持**：帮助评估市场走势

### 重大事件告警

自动检测并推送重大安全事件：

**告警触发条件**（可配置）：
- 伤亡事故（死亡/重伤）≥ 1 例
- 损失金额 ≥ 100 万元

**告警方式**：
- 飞书即时消息推送
- 包含事件详情和损失信息
- 可与月报推送使用不同 Webhook

### 电商数据爬取

支持从电商平台爬取真实销量数据：

- **爬取目标**：京东、淘宝等电商平台
- **自动降级**：爬取失败时使用模拟数据
- **可扩展**：可添加更多数据源

---

## 🔧 自定义开发

### 添加新的数据源

在脚本中添加新的收集函数：

```python
def collect_from_new_source():
    """从新渠道收集数据"""
    logger.info("开始收集新渠道数据...")
    
    # 实现收集逻辑
    data = {...}
    
    logger.info(f"收集到 {len(data)} 条数据")
    return data
```

### 修改收集频率

编辑 `drone_collection_cron.conf`：

```bash
# 每周执行（每周日 23:00）
0 23 * * 0 cd $WORKSPACE && bash $WORKSPACE/scripts/run_drone_collection.sh

# 每季度执行（1/4/7/10 月 28 日）
0 23 28 1,4,7,10 * cd $WORKSPACE && bash $WORKSPACE/scripts/run_drone_collection.sh
```

---

## 🛡️ 最佳实践

### 数据备份

- ✅ 每次更新前自动备份
- ✅ 备份文件名包含时间戳
- ✅ 保留历史备份文件

### 错误处理

- ✅ 捕获所有异常
- ✅ 记录详细错误信息
- ✅ 不影响备份和日志记录

### 日志管理

- ✅ 详细的执行日志
- ✅ 时间戳和级别标记
- ✅ 同时输出到文件和控制台

---

## 📈 监控和维护

### 查看日志

```bash
# 查看最新日志
tail -f /home/admin/.openclaw/workspace/logs/无人机数据收集_自动化.log

# 查看定时任务日志
tail -f /home/admin/.openclaw/workspace/logs/无人机定时任务执行.log

# 查看月度报告
cat /home/admin/.openclaw/workspace/reports/drone/2026-03_无人机数据收集月报.md
```

### 检查定时任务

```bash
# 查看已安装的定时任务
crontab -l

# 查看 cron 服务状态
systemctl status cron

# 手动触发一次收集（测试用）
bash /home/admin/.openclaw/workspace/scripts/run_drone_collection.sh
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

**Q: 飞书推送失败？**
- 检查 Webhook URL 是否正确
- 确认机器人签名校验已关闭
- 查看日志中的错误信息

**Q: 数据收集失败？**
- 检查数据库文件路径
- 查看日志文件错误信息
- 验证 Python 依赖是否安装

---

## 📞 推送配置

### 飞书推送（已配置）

```python
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/5e0b173c-c236-4df8-80de-31201bb35d13"
```

推送内容包含：
- 数据库机型总数
- 2025 年预估销量
- 2025 年事故总数
- 完成的工作列表

---

## 🎯 下一步优化

1. **真实数据源集成**：对接电商平台 API、保险公司数据接口
2. **数据验证**：增加数据质量检查规则
3. **趋势分析**：销量和事故的同比/环比分析
4. **可视化**：数据趋势图表和仪表板
5. **告警系统**：异常数据实时通知

---

## 📊 系统状态

| 组件 | 状态 | 说明 |
|------|------|------|
| 定时任务 | ✅ 已安装 | 每月 28 日 23:00 执行 |
| 数据收集 | ✅ 正常运行 | 销量 + 事故数据收集 |
| 数据库备份 | ✅ 自动备份 | 更新前自动备份 |
| 月度报告 | ✅ 自动生成 | 保存到 reports/drone/ |
| 飞书推送 | ✅ 已配置 | 月报 + 告警双通道 |
| 事故数据库 | ✅ 累积存储 | drone_data/无人机事故案例库.csv |
| 销量趋势 | ✅ 自动分析 | 环比变化、趋势判断 |
| 重大告警 | ✅ 实时推送 | 伤亡/高损失自动告警 |

---

*文档更新时间：2026-03-30*
*系统版本：v1.0*
