# Design Style - 设计风格技能

## Purpose

提供专业设计风格指导和自动生成：
- **风格指南** - 各设计风格详细说明
- **配色方案** - 智能配色生成
- **字体搭配** - 字体组合推荐
- **版式设计** - 布局建议
- **品牌视觉** - VI 系统设计

## Style Categories

### 1. 现代极简 (Modern Minimalist)

**特点：**
- 大量留白
- 简洁几何形状
- 有限配色（2-3 色）
- 无衬线字体
- 清晰层次

**适用：** 科技公司、高端品牌、产品展示

**配色方案：**
- 主色：#FFFFFF (白)
- 辅色：#000000 (黑)
- 强调色：#0066FF (蓝)

### 2. 赛博朋克 (Cyberpunk)

**特点：**
- 霓虹色彩
- 高对比度
- 科技感元素
- 网格和线条
- 发光效果

**配色方案：**
- 主色：#0D0D0D (深黑)
- 辅色：#FF00FF (品红), #00FFFF (青)
- 强调色：#FFFF00 (黄)

### 3. 商务专业 (Business Professional)

**特点：**
- 稳重大气
- 传统配色
- 清晰结构
-  serif 字体
- 对称布局

**适用：** 金融、法律、咨询

### 4. 创意艺术 (Creative Artistic)

**特点：**
- 大胆配色
- 不规则布局
- 艺术元素
- 纹理丰富
- 个性化

## Color Tools

### 智能配色

```python
from design_style import ColorGenerator

generator = ColorGenerator()

# 基于主色生成配色
palette = generator.generate_palette(
    base_color='#0066FF',
    scheme='complementary',  # 互补色
    count=5
)

# 基于情感生成
palette = generator.generate_by_emotion(
    emotion='trust',  # trust/energy/calm/luxury
    industry='tech'
)

# 基于品牌生成
palette = generator.generate_by_brand(
    brand_name='DJI',
    industry='drone'
)
```

### 配色检查

```python
# 检查可访问性
accessibility = generator.check_accessibility(
    foreground='#000000',
    background='#FFFFFF'
)
# 输出：WCAG AA Pass, 对比度 21:1

# 检查和谐度
harmony = generator.check_harmony(palette)
# 输出：和谐度评分 92/100
```

## Typography

### 字体推荐

```python
from design_style import TypographyAdvisor

advisor = TypographyAdvisor()

# 基于用途推荐
fonts = advisor.recommend(
    usage='tech_website',  # tech_website/print/social_media
    style='modern'
)
# 输出：
# - 标题：Inter
# - 正文：Roboto
# - 代码：Fira Code

# 字体搭配
pairing = advisor.get_pairing(
    primary_font='Montserrat',
    usage='presentation'
)
```

### 字体层次

```python
hierarchy = advisor.create_hierarchy(
    fonts={
        'heading': 'Inter',
        'body': 'Roboto'
    },
    levels=['h1', 'h2', 'h3', 'body', 'caption']
)
```

## Layout

### 版式建议

```python
from design_style import LayoutAdvisor

advisor = LayoutAdvisor()

# 基于内容推荐布局
layout = advisor.recommend(
    content_type='product_showcase',
    aspect_ratio='16:9'
)

# 网格系统
grid = advisor.create_grid(
    columns=12,
    gutter=24,
    margin=48
)
```

### 响应式设计

```python
breakpoints = advisor.create_responsive(
    base_grid=grid,
    devices=['mobile', 'tablet', 'desktop']
)
```

## Commands

### /design-style

```bash
# 获取风格建议
/design-style "科技公司官网" --industry tech

# 获取配色方案
/design-style --color --base #0066FF --scheme complementary

# 获取字体推荐
/design-style --typography --usage website --style modern
```

### /color-palette

```bash
/color-palette --base #0066FF --count 5
/color-palette --emotion trust --industry finance
```

### /font-pairing

```bash
/font-pairing --primary Montserrat --usage presentation
```

---

**创建时间:** 2026-04-10  
**版本:** v1.0
