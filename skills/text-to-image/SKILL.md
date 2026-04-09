# Text-to-Image - 文生图技能

## Purpose

集成 AI 文生图能力，将文字描述转换为高质量图像：
- **Stable Diffusion** - 开源文生图模型
- **DALL-E 3** - OpenAI 文生图 API
- **Midjourney** - 高质量艺术生成
- **Flux** - 最新高分辨率模型
- **控制网 (ControlNet)** - 精确控制构图

## When to Use

- 需要生成产品效果图
- 需要创建营销素材
- 需要设计概念图
- 需要可视化创意
- 需要批量生成变体

## Quick Start

```python
# 基础文生图
from text_to_image import ImageGenerator

generator = ImageGenerator(provider='stable_diffusion')

# 生成图像
image = generator.generate(
    prompt="一个现代化的无人机产品图，白色背景，专业摄影，4K",
    negative_prompt="模糊，低质量，变形",
    width=1024,
    height=1024,
    steps=30
)

# 保存
image.save("drone_product.png")
```

## Providers

### 1. Stable Diffusion (推荐)

**优势：**
- 开源免费
- 可本地部署
- 支持 ControlNet
- 社区模型丰富

```python
generator = ImageGenerator(
    provider='stable_diffusion',
    model='sd-xl-base-1.0',
    device='cuda'  # 或'cpu'
)

image = generator.generate(
    prompt="专业产品摄影，无人机，白色背景，演播室灯光",
    negative_prompt="模糊，暗，低质量",
    width=1024,
    height=1024,
    steps=30,
    guidance_scale=7.5
)
```

### 2. DALL-E 3

**优势：**
- 高质量输出
- 理解能力强
- API 简单

```python
generator = ImageGenerator(
    provider='dalle3',
    api_key='your-api-key'
)

image = generator.generate(
    prompt="A professional product photo of a drone",
    size="1024x1024",
    quality="hd"
)
```

### 3. Midjourney

**优势：**
- 艺术质量最高
- 风格多样
- 适合创意设计

```python
generator = ImageGenerator(
    provider='midjourney',
    discord_channel='your-channel'
)

image = generator.generate(
    prompt="drone product photography, studio lighting, white background --ar 1:1 --v 6"
)
```

### 4. Flux

**优势：**
- 最新模型
- 超高分辨率
- 细节丰富

```python
generator = ImageGenerator(
    provider='flux',
    model='flux-pro-1.1'
)

image = generator.generate(
    prompt="Ultra-detailed drone product shot, 8K resolution",
    width=1536,
    height=1536
)
```

## Prompt Engineering

### 基础结构

```
[主体描述] + [环境/背景] + [风格] + [灯光] + [构图] + [质量参数]
```

### 示例模板

#### 产品摄影
```
专业产品摄影，[产品名称]，白色背景，演播室灯光，45 度角，超细节，8K 分辨率，商业级质量
```

#### 概念艺术
```
概念艺术，[主题]，赛博朋克风格，霓虹灯光，未来感，数字绘画，ArtStation 趋势
```

#### 包装设计
```
产品包装设计，[产品类型]，极简主义，现代风格，品牌视觉，矢量图，高质量渲染
```

### 负面提示词 (Negative Prompt)

```
模糊，低质量，变形，多余，水印，文字，签名，暗，过曝，噪点
```

## Advanced Features

### ControlNet 控制

**精确控制构图：**

```python
# 使用边缘检测
generator.add_controlnet(
    type='canny',
    image='reference_edge.png',
    strength=0.8
)

# 使用深度图
generator.add_controlnet(
    type='depth',
    image='depth_map.png',
    strength=0.6
)

# 使用姿势控制
generator.add_controlnet(
    type='openpose',
    image='pose_reference.png',
    strength=0.9
)
```

### 图像变体

```python
# 生成多个变体
variants = generator.generate_variants(
    prompt="无人机产品图",
    count=9,
    variation_strength=0.3
)

# 保存变体网格
generator.save_grid(variants, "variants_grid.png")
```

### 高清放大

```python
# 先生成低分辨率
low_res = generator.generate(prompt, width=512, height=512)

# 然后放大
high_res = generator.upscale(
    image=low_res,
    scale=4,
    model='realesrgan-x4plus'
)
```

### 风格迁移

```python
# 应用艺术风格
styled = generator.apply_style(
    image=base_image,
    style='cyberpunk',
    strength=0.7
)

# 或使用参考图
styled = generator.apply_style(
    image=base_image,
    style_image='reference_style.png',
    strength=0.5
)
```

## Use Cases

### 1. 无人机产品效果图

```python
generator = ImageGenerator(provider='stable_diffusion')

# 生成产品图
product_image = generator.generate(
    prompt="专业无人机产品摄影，DJI 风格，白色背景，演播室灯光，4K 超细节",
    negative_prompt="模糊，暗，低质量，文字，水印",
    width=1024,
    height=1024
)

# 生成使用场景
scene_image = generator.generate(
    prompt="无人机在山地飞行，航拍视角，日出时分，电影感，8K",
    width=1536,
    height=1024
)
```

### 2. 保险产品可视化

```python
# 生成保险概念图
insurance_image = generator.generate(
    prompt="保险保护概念，盾牌图标，蓝色主题，3D 渲染，专业商务风格",
    width=1024,
    height=1024
)

# 生成理赔流程图
flowchart = generator.generate(
    prompt="保险理赔流程图，简洁信息图，蓝色和白色，矢量风格",
    width=1920,
    height=1080
)
```

### 3. 营销素材

```python
# 生成社交媒体图片
social_media = generator.generate(
    prompt="社交媒体营销图，无人机产品，促销标签，红色和黑色，吸引眼球",
    width=1080,
    height=1080
)

# 生成海报
poster = generator.generate(
    prompt="产品发布海报，无人机，科技感，渐变背景，大标题空间",
    width=1080,
    height=1920
)
```

### 4. 包装设计

```python
# 生成包装概念
package = generator.generate(
    prompt="产品包装设计，无人机，极简主义，白色和蓝色，高端质感",
    width=1024,
    height=1024
)

# 生成多个方案
options = generator.generate_variants(
    prompt="产品包装盒设计，正面视图",
    count=6,
    variation_strength=0.4
)
```

## Commands

### /text-to-image

```bash
# 基础生成
/text-to-image "一个现代化的无人机产品图"

# 指定参数
/text-to-image "产品摄影" --size 1024x1024 --steps 30

# 指定提供商
/text-to-image "艺术图" --provider midjourney

# 生成变体
/text-to-image "概念图" --variants 9
```

### /image-variants

```bash
# 基于现有图像生成变体
/image-variants input.png --count 9 --strength 0.3
```

### /upscale-image

```bash
# 放大图像
/upscale-image input.png --scale 4 --model realesrgan
```

## Integration

### 与 BI 仪表板集成

```python
# 为数据报告生成可视化图
dashboard.add_custom_image(
    generator.generate("数据增长趋势，上升箭头，蓝色主题")
)
```

### 与 Scrapling 集成

```python
# 爬取产品数据后生成效果图
products = scraper.collect(url, '.product')
for product in products:
    image = generator.generate(f"{product['name']} 产品图")
    product['image'] = image
```

### 与飞书集成

```python
# 生成并推送到飞书
image = generator.generate(prompt)
feishu_bot.send_image(image, webhook=WEBHOOK)
```

## Best Practices

### Do's
✅ 使用详细的提示词  
✅ 添加负面提示词  
✅ 使用合适的分辨率  
✅ 多次生成选择最佳  
✅ 使用 ControlNet 精确控制  

### Don'ts
❌ 提示词过于简单  
❌ 忽略负面提示词  
❌ 使用过低分辨率  
❌ 期望一次完美  

## Performance

| 提供商 | 生成时间 | 质量 | 成本 |
|--------|---------|------|------|
| Stable Diffusion | 5-10 秒 | ⭐⭐⭐⭐ | 免费 |
| DALL-E 3 | 10-20 秒 | ⭐⭐⭐⭐⭐ | $0.04/张 |
| Midjourney | 30-60 秒 | ⭐⭐⭐⭐⭐ | $10/月 |
| Flux | 10-15 秒 | ⭐⭐⭐⭐⭐ | 免费 |

## Resources

- **Stable Diffusion:** https://github.com/Stability-AI/stablediffusion
- **ControlNet:** https://github.com/lllyasviel/ControlNet
- **DALL-E 3:** https://platform.openai.com/docs/guides/images
- **Midjourney:** https://midjourney.com
- **Flux:** https://blackforestlabs.ai/flux/

---

**创建时间:** 2026-04-10  
**版本:** v1.0  
**依赖:** diffusers, transformers, pillow, torch
