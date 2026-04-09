# /crawl - 网页爬取命令

## Purpose

使用 Scrapling 进行智能网页爬取，支持：
- 绕过 Cloudflare 等反爬虫
- 自适应网站变化
- 并发爬取
- AI 辅助提取

## Usage

```bash
# 基础爬取
/crawl <url> <selector>

# 绕过 Cloudflare
/crawl <url> <selector> --solve-cloudflare

# 自适应模式
/crawl <url> <selector> --adaptive

# 深度爬取
/crawl <url> --depth 3 --concurrent 10

# AI 辅助提取
/crawl <url> --extract "提取所有产品名称和价格"

# 输出格式
/crawl <url> <selector> --output json
/crawl <url> <selector> --output csv
```

## Examples

### 1. 爬取产品价格

```bash
/crawl https://example.com/products '.product::text'
/crawl https://example.com/products '.price::text' --solve-cloudflare
```

**输出:**
```
找到 50 个产品:
- Product 1: $10.99
- Product 2: $19.99
- Product 3: $29.99
...

Token 节省：45,000 (90%)
```

### 2. 爬取新闻文章

```bash
/crawl https://news-site.com 'article h1' --depth 2
/crawl https://news-site.com 'article .content' --output json
```

### 3. AI 辅助提取

```bash
/crawl https://example.com --extract "提取所有产品的名称、价格、评分"
```

**输出:**
```json
{
  "products": [
    {"name": "Product 1", "price": "$10.99", "rating": "4.5"},
    {"name": "Product 2", "price": "$19.99", "rating": "4.2"}
  ]
}
```

### 4. 深度爬取

```bash
/crawl https://example.com --depth 3 --concurrent 10 --stream
```

**实时输出:**
```
[Page 1/50] https://example.com/page1
[Page 2/50] https://example.com/page2
...
[Page 50/50] https://example.com/page50

完成！共爬取 50 个页面
```

## Options

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--depth` | 爬取深度 | 1 |
| `--concurrent` | 并发数 | 5 |
| `--solve-cloudflare` | 绕过 Cloudflare | false |
| `--adaptive` | 自适应模式 | true |
| `--output` | 输出格式 (json/csv/txt) | txt |
| `--stream` | 流式输出 | false |
| `--cache` | 使用缓存 | true |
| `--extract` | AI 提取查询 | null |

## Integration

### 与 deep-research 配合

```bash
# 爬取数据
/crawl https://example.com '.data' --output json > data.json

# 分析数据
/deep-research "分析以下数据趋势..." --input data.json
```

### 与 documentation-lookup 配合

```bash
# 爬取文档
/crawl https://docs.example.com 'article' --depth 2

# 查找特定内容
/documentation-lookup "API 认证方法"
```

## Token Optimization

**传统方式:**
```python
html = requests.get(url).text
# 发送整个 HTML 给 AI → 50,000 tokens
```

**Scrapling 方式:**
```python
page = StealthyFetcher.fetch(url)
data = page.css('.content').getall()
# 只发送提取的数据 → 5,000 tokens
# 节省 90% Token!
```

## Troubleshooting

### Cloudflare 无法绕过

```bash
# 尝试有头模式
/crawl <url> <selector> --headless false

# 等待网络空闲
/crawl <url> <selector> --network-idle
```

### 元素找不到

```bash
# 使用自适应模式
/crawl <url> <selector> --adaptive true

# 使用更宽泛的选择器
/crawl <url> 'div' --adaptive
```

### Token 消耗高

```bash
# 使用 AI 提取模式
/crawl <url> --extract "只提取产品名称"

# 限制输出长度
/crawl <url> <selector> --limit 100
```

## Performance

| 场景 | 传统方式 | Scrapling | 提升 |
|------|---------|-----------|------|
| Cloudflare 绕过 | ❌ 失败 | ✅ 成功 | - |
| Token 消耗 | 50k | 5k | -90% |
| 网站变化适应 | ❌ 手动修复 | ✅ 自动 | - |
| 并发爬取 | ❌ 手动实现 | ✅ 内置 | - |

## Related Commands

- `/scrape` - 单个页面爬取
- `/deep-research` - 深度研究
- `/documentation-lookup` - 文档查找
