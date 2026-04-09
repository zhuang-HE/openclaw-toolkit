# /bi-query - BI 数据查询命令

## Purpose

使用自然语言查询数据，自动生成可视化图表。

## Usage

```bash
# 基础查询
/bi-query "<自然语言查询>"

# 指定数据源
/bi-query "<查询>" --sources drone,clinical

# 指定图表类型
/bi-query "<查询>" --chart line

# 导出结果
/bi-query "<查询>" --output csv

# 趋势分析
/bi-query "<查询>" --trend 30
```

## Examples

### 1. 无人机数据查询

```bash
# 价格趋势
/bi-query "显示大疆无人机近 30 天的价格变化"

# 品牌对比
/bi-query "对比各品牌无人机的平均价格"

# 规格分析
/bi-query "分析无人机载重与价格的关系"
```

**输出:**
```
📊 图表类型：折线图

数据预览:
日期       | 品牌  | 型号        | 价格
2026-04-01 | 大疆  | Mini 4 Pro  | 7499
2026-04-02 | 大疆  | Mini 4 Pro  | 7499
...

趋势分析:
- 方向：稳定
- 变化率：0%
- 平均值：7499 元
```

### 2. 临床试验查询

```bash
# 试验数量
/bi-query "显示癌症临床试验的数量趋势"

# 阶段分布
/bi-query "显示临床试验各阶段的占比"

# 最新试验
/bi-query "显示最近新增的临床试验"
```

### 3. 保险产品查询

```bash
# 费率对比
/bi-query "对比各保险公司的费率"

# 相关性分析
/bi-query "分析风险系数与费率的关系"

# 产品统计
/bi-query "统计各类保险产品的数量"
```

### 4. 跨数据源查询

```bash
# 融合分析
/bi-query "分析无人机价格与保险费率的关系" --sources drone,insurance

# 综合报告
/bi-query "生成综合数据分析报告" --sources all --output pdf
```

## Options

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--sources` | 数据源（逗号分隔） | all |
| `--chart` | 图表类型（line/bar/pie/scatter/table） | auto |
| `--output` | 输出格式（csv/json/pdf） | table |
| `--trend` | 趋势分析天数 | 0 |
| `--limit` | 结果数量限制 | 100 |

## Chart Types

### 自动推荐逻辑

| 查询关键词 | 推荐图表 |
|-----------|---------|
| 趋势/变化 | line（折线图） |
| 对比/比较 | bar（柱状图） |
| 占比/分布 | pie（饼图） |
| 关系/相关 | scatter（散点图） |
| 详细/列表 | table（表格） |

### 手动指定

```bash
/bi-query "价格趋势" --chart line
/bi-query "品牌对比" --chart bar
/bi-query "市场占比" --chart pie
/bi-query "相关性分析" --chart scatter
```

## Data Sources

### 可用数据源

| 名称 | 说明 | 记录数 |
|------|------|--------|
| `drone` | 无人机数据库 | 25 款机型 |
| `clinical` | 临床试验数据库 | 动态更新 |
| `insurance` | 保险产品数据库 | 动态更新 |
| `robot` | 机器人数据库 | 动态更新 |
| `token` | Token 统计 | 每日更新 |

### 使用示例

```bash
# 单个数据源
/bi-query "无人机价格" --sources drone

# 多个数据源
/bi-query "价格与费率关系" --sources drone,insurance

# 所有数据源
/bi-query "综合分析" --sources all
```

## Output Formats

### 表格输出（默认）

```bash
/bi-query "价格对比"
```

**输出:**
```
品牌  | 型号        | 价格   | 变化
-----|------------|-------|------
大疆  | Mini 4 Pro | 7499  | 0%
大疆  | Air 3      | 12499 | 0%
...
```

### CSV 导出

```bash
/bi-query "价格对比" --output csv
```

**输出:** 保存到 `collected_data/query_result.csv`

### JSON 导出

```bash
/bi-query "价格对比" --output json
```

**输出:** 保存到 `collected_data/query_result.json`

### PDF 报告

```bash
/bi-query "综合分析" --output pdf
```

**输出:** 生成包含图表的 PDF 报告

## Advanced Features

### 趋势分析

```bash
# 分析近 30 天趋势
/bi-query "价格变化" --trend 30

# 分析近 7 天趋势
/bi-query "销量变化" --trend 7
```

**输出:**
```
📈 趋势分析

方向：上升 ⬆️
变化率：+5.2%
平均值：8500 元
波动率：2.3%
```

### 异常检测

```bash
# 自动检测异常
/bi-query "检测价格异常"

# 设置阈值
/bi-query "检测价格异常" --threshold 10
```

**输出:**
```
🚨 异常检测

发现 2 个异常:
1. 大疆 Mavic 3 Pro: 价格下降 15%
2. 极飞 P150: 价格上涨 12%
```

### 智能推荐

```bash
# 获取图表推荐
/bi-query "数据分析" --recommend
```

**输出:**
```
💡 图表推荐

基于数据特征，推荐:
1. 折线图 - 显示趋势
2. 柱状图 - 对比分析
3. 散点图 - 相关性分析
```

## Integration

### 与 Scrapling 集成

```bash
# 爬取并分析
/crawl https://dji.com '.price' --output bi
/bi-query "分析爬取的价格数据"
```

### 与 Token 统计集成

```bash
# 监控 Token 消耗
/bi-query "显示今日 Token 消耗趋势" --sources token
```

### 与飞书集成

```bash
# 推送到飞书
/bi-query "生成日报" --output feishu
```

## Performance

| 指标 | 目标值 |
|------|--------|
| 查询响应时间 | <3 秒 |
| 图表渲染时间 | <1 秒 |
| 跨源查询响应 | <5 秒 |
| 大数据集（10 万 +） | <10 秒 |

## Troubleshooting

### 查询无结果

```bash
# 检查数据源
/bi-sources

# 检查数据量
/bi-query "统计数量" --chart table
```

### 图表不显示

```bash
# 检查数据格式
/bi-query "原始数据" --output json

# 更换图表类型
/bi-query "查询" --chart table
```

### 性能慢

```bash
# 限制结果数量
/bi-query "查询" --limit 50

# 使用缓存
/bi-query "查询" --cache
```

## Related Commands

- `/bi-dashboard` - 创建和管理仪表板
- `/bi-report` - 生成报告
- `/crawl` - 网页爬取
- `/scrape` - 数据提取
