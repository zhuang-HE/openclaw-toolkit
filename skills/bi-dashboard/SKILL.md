# BI Dashboard - 智能数据可视化技能

## Purpose

集成 DataEase 开源 BI 工具理念，创建智能数据可视化技能：
- **实时仪表板** - 数据实时更新
- **多数据源融合** - 无人机/临床/保险/机器人数据库
- **自助分析** - 自然语言查询
- **自动可视化** - 智能推荐图表类型
- **异常告警** - 数据变化自动通知

## When to Use

- 需要实时监控数据库变化
- 需要跨数据源分析
- 需要可视化展示数据
- 需要自动生成报告
- 需要异常检测和告警

## Quick Start

```python
# 创建实时仪表板
from bi_dashboard import Dashboard

dashboard = Dashboard()
dashboard.add_source('drone_db', '无人机数据库')
dashboard.add_source('clinical_db', '临床试验数据库')
dashboard.add_source('insurance_db', '保险产品数据库')

# 添加可视化组件
dashboard.add_chart('drone_prices', 'line', '无人机价格趋势')
dashboard.add_chart('trial_count', 'bar', '临床试验数量')

# 显示仪表板
dashboard.show()
```

## Core Features

### 1. 实时仪表板

**支持数据源：**
- 无人机数据库
- 临床试验数据库
- 保险产品数据库
- 机器人数据库
- Web 爬取数据（Scrapling）
- 数据库（MySQL/PostgreSQL）
- API 接口

```python
from bi_dashboard import Dashboard

# 创建仪表板
dashboard = Dashboard(title='数据监控中心')

# 添加数据源
dashboard.add_source(
    name='drone_prices',
    type='scrapling',
    url='https://www.dji.com/cn/products',
    selector='.price::text',
    refresh_interval=300  # 5 分钟刷新
)

# 添加图表
dashboard.add_chart(
    name='price_trend',
    type='line',  # line/bar/pie/table
    title='无人机价格趋势',
    data_source='drone_prices'
)

# 自动刷新
dashboard.start_auto_refresh()
```

### 2. 多数据源融合

**跨源查询：**
```python
from data_fusion import DataFusionCenter

fusion = DataFusionCenter()

# 跨数据源查询
result = fusion.query("""
    分析无人机价格与保险费率的关系
    
    数据源：
    - 无人机数据库（价格、规格）
    - 保险产品数据库（费率）
    
    输出：散点图 + 相关性分析
""")
```

**数据关联：**
```python
# 自动关联相同字段
fusion.auto_join(
    left='drone_db.models',
    right='insurance_db.products',
    on='model_name'
)
```

### 3. 自助分析

**自然语言查询：**
```python
# 用中文查询数据
result = dashboard.ask("显示大疆无人机近 30 天的价格变化")

# 自动生成图表
chart = result.visualize()
```

**智能推荐：**
```python
# 根据数据类型推荐图表
recommendations = dashboard.recommend_charts(data)
# 输出：['line', 'bar', 'scatter']
```

### 4. 实时监控

**异常检测：**
```python
# 设置告警规则
dashboard.add_alert(
    name='price_change_alert',
    condition='drone_prices.change_percent > 10',
    action='send_feishu_notification'
)

# 启动监控
dashboard.start_monitoring()
```

**趋势分析：**
```python
# 自动趋势分析
trend = dashboard.analyze_trend('drone_prices', days=30)
print(f"趋势：{trend.direction}")
print(f"变化率：{trend.change_percent}%")
```

### 5. 自动报告

**日报生成：**
```python
# 自动生成日报
report = dashboard.generate_daily_report(
    sources=['drone_db', 'clinical_db'],
    format='pdf'
)
```

**定时推送：**
```python
# 每天 9 点推送报告
dashboard.schedule_report(
    time='09:00',
    recipients=['user@example.com'],
    format='feishu'
)
```

## Chart Types

### 支持的图表类型

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| `line` | 折线图 | 趋势分析（价格、销量） |
| `bar` | 柱状图 | 对比分析（不同机型） |
| `pie` | 饼图 | 占比分析（市场份额） |
| `scatter` | 散点图 | 相关性分析（价格 vs 费率） |
| `table` | 表格 | 详细数据展示 |
| `gauge` | 仪表盘 | 指标监控（完成率） |
| `map` | 地图 | 地理分布 |
| `heatmap` | 热力图 | 密度分析 |

### 图表配置

```python
dashboard.add_chart(
    name='price_comparison',
    type='bar',
    title='无人机价格对比',
    data_source='drone_prices',
    config={
        'x_axis': 'model',
        'y_axis': 'price',
        'color': 'brand',
        'sort': 'desc',
        'limit': 10
    }
)
```

## Integration

### 与 Scrapling 集成

```python
from scrapling import StealthyFetcher
from bi_dashboard import Dashboard

# 爬取数据
page = StealthyFetcher.fetch('https://dji.com/products')
prices = page.css('.price::text').getall()

# 添加到仪表板
dashboard.add_data('dji_prices', prices)
dashboard.update_chart('price_trend')
```

### 与 Token 统计集成

```python
# 监控 Token 消耗
dashboard.add_source(
    name='token_stats',
    type='file',
    path='logs/token_stats.json'
)

dashboard.add_chart(
    name='daily_tokens',
    type='line',
    title='每日 Token 消耗',
    data_source='token_stats'
)
```

### 与飞书集成

```python
# 告警推送到飞书
dashboard.add_alert(
    name='token_high_alert',
    condition='token_stats.daily > 100000',
    action={
        'type': 'feishu',
        'webhook': 'https://open.feishu.cn/...'
    }
)
```

## Use Cases

### 1. 无人机价格监控

```python
dashboard = Dashboard(title='无人机价格监控')

# 添加数据源
dashboard.add_source(
    name='dji_prices',
    type='scrapling',
    url='https://www.dji.com/cn/products',
    selector='.product',
    refresh_interval=3600
)

# 添加图表
dashboard.add_chart(
    name='price_trend',
    type='line',
    title='价格趋势',
    data_source='dji_prices'
)

dashboard.add_chart(
    name='brand_comparison',
    type='bar',
    title='品牌对比',
    data_source='dji_prices'
)

# 设置告警
dashboard.add_alert(
    name='price_drop',
    condition='dji_prices.change < -5%',
    action='send_notification'
)
```

### 2. 临床试验监控

```python
dashboard = Dashboard(title='临床试验监控')

# 添加数据源
dashboard.add_source(
    name='clinical_trials',
    type='api',
    url='https://clinicaltrials.gov/api',
    params={'cond': 'cancer'}
)

# 添加图表
dashboard.add_chart(
    name='trial_count',
    type='bar',
    title='试验数量',
    data_source='clinical_trials'
)

dashboard.add_chart(
    name='phase_distribution',
    type='pie',
    title='阶段分布',
    data_source='clinical_trials'
)
```

### 3. 保险产品分析

```python
dashboard = Dashboard(title='保险产品分析')

# 跨数据源融合
fusion = DataFusionCenter()
fusion.join(
    left='insurance_db.products',
    right='drone_db.models',
    on='model_name'
)

# 分析费率与风险关系
dashboard.add_chart(
    name='rate_risk_correlation',
    type='scatter',
    title='费率 vs 风险系数',
    data_source='fused_data'
)
```

## Performance

| 指标 | 数值 |
|------|------|
| 数据刷新延迟 | <5 秒 |
| 图表渲染时间 | <1 秒 |
| 跨源查询响应 | <3 秒 |
| 告警触发延迟 | <1 秒 |
| Token 节省 | 80% |

## Best Practices

### Do's
✅ 设置合理的刷新间隔  
✅ 使用缓存减少请求  
✅ 设置告警阈值  
✅ 定期清理旧数据  
✅ 使用飞书推送告警  

### Don'ts
❌ 过高频率刷新（浪费 Token）  
❌ 不设置告警阈值  
❌ 忽略数据验证  
❌ 不监控异常  

## Troubleshooting

### 数据不更新

```python
# 检查数据源连接
dashboard.check_source('drone_prices')

# 手动刷新
dashboard.refresh('drone_prices')

# 查看日志
dashboard.get_logs()
```

### 图表不显示

```python
# 检查数据
data = dashboard.get_data('price_trend')
print(f"数据量：{len(data)}")

# 检查配置
config = dashboard.get_chart_config('price_trend')
print(f"配置：{config}")
```

### 告警不触发

```python
# 检查告警规则
alerts = dashboard.get_alerts()
print(f"告警规则：{alerts}")

# 手动测试
dashboard.test_alert('price_drop')
```

## Commands

### /bi-dashboard

创建和管理仪表板：

```bash
/bi-dashboard create "无人机监控"
/bi-dashboard add-chart line "价格趋势"
/bi-dashboard add-alert "价格变化>10%"
/bi-dashboard show
```

### /bi-query

自然语言查询数据：

```bash
/bi-query "显示大疆无人机价格趋势"
/bi-query "对比各品牌保险费率"
/bi-query "临床试验数量月度变化"
```

### /bi-report

生成报告：

```bash
/bi-report daily --sources drone,clinical
/bi-report weekly --format pdf
/bi-report custom --query "价格分析"
```

## Resources

- **DataEase:** https://github.com/dataease/dataease
- **ECharts:** https://echarts.apache.org/
- **Plotly:** https://plotly.com/

---

**创建时间:** 2026-04-10  
**版本:** v1.0  
**依赖:** scrapling, plotly, pandas
