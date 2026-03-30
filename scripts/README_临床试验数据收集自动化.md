# 🏥 临床试验数据收集自动化系统

## 📋 系统概述

本系统实现药物/医疗器械临床试验数据库的自动化数据收集、更新和月度报告推送。

### 核心功能

- ✅ **月度收集**：每月 1 日自动执行数据收集
- ✅ **报告推送**：生成月报并推送到飞书
- ✅ **多渠道数据**：CDE、NMPA、临床试验登记平台、保险公司
- ✅ **事故案例库**：累积存储事故案例，支持查询分析
- ✅ **费率趋势分析**：跟踪保险费率变化，生成趋势报告
- ✅ **重大事件告警**：死亡案例/高赔偿自动告警
- ✅ **真实数据源**：支持 CDE/NMPA 网站爬取（可扩展）
- ✅ **错误处理**：完善的日志和异常处理机制

---

## 📁 文件结构

```
/home/admin/.openclaw/workspace/
├── scripts/
│   ├── 临床试验数据收集自动化.py    # 主收集脚本
│   ├── run_clinical_trial_collection.sh  # 收集任务执行脚本
│   ├── clinical_trial_cron.conf     # Crontab 配置文件
│   └── README_临床试验数据收集自动化.md  # 本文档
├── reports/clinical_trial/
│   └── YYYY-MM_临床试验数据收集月报.md  # 月度报告
├── clinical_trial_data/
│   ├── YYYY-MM_月度汇总.json        # 月度汇总数据
│   ├── 临床试验事故案例库.csv       # 事故案例数据库（累积）
│   └── 保险费率历史趋势.csv          # 费率历史记录（累积）
├── logs/
│   ├── 临床试验数据收集_自动化.log   # 收集日志
│   ├── 临床试验定时任务执行.log      # 定时任务日志
│   └── cron_clinical_trial_collection.log  # Cron 执行日志
└── 临床试验相关报告文件
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
crontab /home/admin/.openclaw/workspace/scripts/clinical_trial_cron.conf

# 验证安装
crontab -l
```

### 步骤 3: 手动测试

```bash
# 测试数据收集
bash /home/admin/.openclaw/workspace/scripts/run_clinical_trial_collection.sh

# 查看日志
tail -f /home/admin/.openclaw/workspace/logs/临床试验数据收集_自动化.log
```

---

## ⚙️ 配置说明

### 飞书推送配置

在 `临床试验数据收集自动化.py` 中配置：

```python
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/031785aa-83b0-4e5a-bbe9-187fd69f9e23"
```

### 收集时间

```python
# 每月 1 日 02:00 执行
0 2 1 * *
```

### 数据源配置

```python
DATA_SOURCES = {
    "cde": {"name": "国家药监局药品审评中心", "url": "https://www.cde.org.cn"},
    "nmpa": {"name": "国家药品监督管理局", "url": "https://www.nmpa.gov.cn"},
    "chinadrugtrials": {"name": "药物临床试验登记平台", "url": "https://www.chinadrugtrials.org.cn"},
    "chictr": {"name": "中国临床试验注册中心", "url": "http://www.chictr.org.cn"}
}
```

### 告警阈值配置

```python
ALERT_THRESHOLDS = {
    "death_count": 1,           # 死亡案例数达到即告警
    "serious_ae_count": 5,      # 严重不良事件达到即告警
    "compensation_amount": 200, # 赔偿金额超过 200 万即告警
}
```

### Webhook 配置

```python
WEBHOOK_URL_MONTHLY = "..."  # 月报推送 Webhook
WEBHOOK_URL_ALERT = "..."    # 告警推送 Webhook（可配置不同地址）
```
```

---

## 📊 数据收集流程

```
1. 收集 CDE 数据（药品审评、批准通知、安全警示）
   ↓
2. 收集 NMPA 数据（不良反应报告、安全警告）
   ↓
3. 收集临床试验登记数据（新增试验、分期分布）
   ↓
4. 收集保险费率数据（保险公司报价）
   ↓
5. 收集事故数据（公开文献、监管公告）
   ↓
6. 保存月度汇总数据
   ↓
7. 生成月度报告
   ↓
8. 推送报告到飞书
   ↓
9. 记录执行日志
```

---

## 📝 月度报告内容

每月生成的报告包含：

- **收集概览**：新增试验、进行中试验、不良反应报告、事故案例
- **试验分布**：按分期（I/II/III/IV 期）统计
- **保险费率**：各保险公司费率参考 + 趋势分析
- **事故案例**：本月事故案例详情 + 数据库累计
- **费率趋势**：环比变化分析（上升/下降/稳定）
- **下月计划**：下一步工作安排

---

## 🔧 数据源说明

### 官方渠道

| 渠道 | 数据类型 | 更新频率 |
|------|---------|---------|
| CDE（药品审评中心） | 药品审评、批准通知 | 每日 |
| NMPA（药监局） | 不良反应报告、安全警示 | 每周 |
| 药物临床试验登记平台 | 试验登记信息 | 每日 |
| 中国临床试验注册中心 | 试验注册信息 | 每日 |

### 商业数据源（可扩展）

| 渠道 | 数据类型 | 价格 |
|------|---------|------|
| 医药魔方 | 临床试验数据、安全性信息 | 5-20 万/年 |
| 药智网 | 药品和医疗器械信息 | 1-10 万/年 |
| Cortellis | 全球临床试验数据 | 20-50 万/年 |

---

## 🔧 高级功能说明

### 事故案例数据库

系统自动累积事故案例到 `clinical_trial_data/临床试验事故案例库.csv`：

- **自动去重**：基于案例 ID 避免重复入库
- **统一字段**：标准化字段格式，支持药物/器械试验
- **累计统计**：月报中显示累计案例数
- **查询分析**：可用于后续数据分析和趋势研究

### 费率趋势分析

系统自动跟踪保险费率变化：

- **历史记录**：每次收集保存到 `保险费率历史趋势.csv`
- **趋势计算**：环比变化百分比（上升/下降/稳定）
- **可视化**：月报中展示各公司费率趋势
- **决策支持**：帮助评估保险市场走势

### 重大事件告警

自动检测并推送重大安全事件：

**告警触发条件**（可配置）：
- 死亡案例 ≥ 1 例
- 严重不良事件 ≥ 5 例
- 赔偿金额 ≥ 200 万元

**告警方式**：
- 飞书即时消息推送
- 包含事件详情和赔偿信息
- 可与月报推送使用不同 Webhook

---

## 🔧 自定义开发

### 添加新的数据源

在脚本中添加新的收集函数：

```python
def collect_new_source_data():
    """从新渠道收集数据"""
    logger.info("开始收集新渠道数据...")
    
    # 实现收集逻辑
    data = {...}
    
    logger.info(f"收集到 {len(data)} 条数据")
    return data
```

### 修改收集频率

编辑 `clinical_trial_cron.conf`：

```bash
# 每季度执行（1/4/7/10 月 1 日）
0 2 1 1,4,7,10 * * cd $WORKSPACE && bash $WORKSPACE/scripts/run_clinical_trial_collection.sh

# 每半月执行（1 日和 15 日）
0 2 1,15 * * cd $WORKSPACE && bash $WORKSPACE/scripts/run_clinical_trial_collection.sh
```

---

## 🛡️ 最佳实践

### 数据备份

- ✅ 每次收集后自动保存月度汇总
- ✅ JSON 格式存储关键指标
- ✅ CSV 格式存储详细数据

### 错误处理

- ✅ 捕获所有异常
- ✅ 记录详细错误信息
- ✅ 不影响其他数据源收集

### 日志管理

- ✅ 详细的执行日志
- ✅ 时间戳和级别标记
- ✅ 同时输出到文件和控制台

---

## 📈 监控和维护

### 查看日志

```bash
# 查看最新日志
tail -f /home/admin/.openclaw/workspace/logs/临床试验数据收集_自动化.log

# 查看定时任务日志
tail -f /home/admin/.openclaw/workspace/logs/临床试验定时任务执行.log

# 查看月度报告
cat /home/admin/.openclaw/workspace/reports/clinical_trial/2026-03_临床试验数据收集月报.md
```

### 检查定时任务

```bash
# 查看已安装的定时任务
crontab -l

# 查看 cron 服务状态
systemctl status cron

# 手动触发一次收集（测试用）
bash /home/admin/.openclaw/workspace/scripts/run_clinical_trial_collection.sh
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
- 检查网络连接
- 查看日志文件错误信息
- 验证目标网站是否可访问

---

## 📞 推送配置

### 飞书推送（已配置）

```python
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/031785aa-83b0-4e5a-bbe9-187fd69f9e23"
```

推送内容包含：
- 新增试验登记数量
- 进行中试验总数
- NMPA 不良反应报告数
- 事故案例数
- 完成的工作列表

---

## 🎯 下一步优化

1. **真实数据源集成** - 对接 CDE/NMPA API 或实现爬虫
2. **数据验证** - 增加数据质量检查规则
3. **趋势分析** - 试验数量和事故率的同比/环比分析
4. **可视化** - 数据趋势图表和仪表板
5. **告警系统** - 重大安全事件实时通知
6. **商业数据库对接** - 医药魔方、药智网等

---

## 📊 系统状态

| 组件 | 状态 | 说明 |
|------|------|------|
| 定时任务 | ✅ 已安装 | 每月 1 日 02:00 执行 |
| 数据收集 | ✅ 正常运行 | CDE + NMPA + 登记平台 + 保险费率 + 事故数据 |
| 月度报告 | ✅ 自动生成 | 保存到 reports/clinical_trial/ |
| 飞书推送 | ✅ 已配置 | 月报 + 告警双通道 |
| 事故数据库 | ✅ 累积存储 | clinical_trial_data/临床试验事故案例库.csv |
| 费率趋势 | ✅ 自动分析 | 环比变化、趋势判断 |
| 重大告警 | ✅ 实时推送 | 死亡/高赔偿自动告警 |

---

*文档更新时间：2026-03-30*
*系统版本：v1.0*
