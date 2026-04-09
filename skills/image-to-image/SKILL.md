# Image-to-Image - 图生图技能

## Purpose

基于现有图像进行转换和编辑：
- **风格转换** - 将图像转换为不同艺术风格
- **图像修复** - 修复损坏或缺失部分
- **图像扩展** - 智能扩展画布 (Outpainting)
- **局部重绘** - 修改图像特定区域 (Inpainting)
- **超分辨率** - 提升图像分辨率和质量

## When to Use

- 需要修改现有图片
- 需要转换图片风格
- 需要修复老照片
- 需要扩展图片边界
- 需要提升图片质量

## Quick Start

```python
from image_to_image import ImageEditor

editor = ImageEditor()

# 风格转换
styled = editor.style_transfer(
    image='input.png',
    style='cyberpunk',
    strength=0.7
)

# 图像修复
fixed = editor.inpaint(
    image='damaged.png',
    mask='damage_mask.png'
)

# 图像扩展
extended = editor.outpaint(
    image='input.png',
    direction='right',
    pixels=512
)
```

## Core Features

### 1. 风格转换 (Style Transfer)

**转换到不同艺术风格：**

```python
editor = ImageEditor(provider='stable_diffusion')

# 转换为赛博朋克风格
cyberpunk = editor.style_transfer(
    image='drone_photo.png',
    style='cyberpunk',
    prompt="赛博朋克风格，霓虹灯光，未来感",
    strength=0.7
)

# 转换为油画风格
oil_painting = editor.style_transfer(
    image='product.png',
    style='oil_painting',
    strength=0.6
)

# 使用参考图转换
styled = editor.style_transfer(
    image='input.png',
    style_image='reference_style.png',
    strength=0.5
)
```

**预设风格：**
- `cyberpunk` - 赛博朋克
- `anime` - 动漫风格
- `oil_painting` - 油画
- `watercolor` - 水彩
- `sketch` - 素描
- `pixel_art` - 像素艺术
- `3d_render` - 3D 渲染
- `minimalist` - 极简主义

### 2. 图像修复 (Inpainting)

**修复损坏或缺失部分：**

```python
# 自动检测并修复
fixed = editor.inpaint(
    image='damaged_photo.png',
    prompt="修复损坏区域，保持原样"
)

# 使用蒙版精确修复
fixed = editor.inpaint(
    image='photo.png',
    mask='scratch_mask.png',
    prompt="平滑表面，无划痕"
)

# 移除不需要的物体
removed = editor.inpaint(
    image='product_photo.png',
    mask='object_mask.png',
    prompt="干净背景，无物体"
)
```

**应用场景：**
- 老照片修复
- 移除水印
- 移除路人
- 修复划痕
- 填补缺失

### 3. 图像扩展 (Outpainting)

**智能扩展画布：**

```python
# 向右扩展
extended = editor.outpaint(
    image='input.png',
    direction='right',
    pixels=512,
    prompt="延续图像内容，自然过渡"
)

# 向四周扩展
extended = editor.outpaint(
    image='input.png',
    direction='all',
    pixels=256,
    prompt="扩展背景，保持一致"
)

# 自定义扩展区域
extended = editor.outpaint(
    image='input.png',
    top=100,
    bottom=100,
    left=0,
    right=0
)
```

**应用场景：**
- 扩展照片边界
- 创建宽屏版本
- 适配不同比例
- 补充画面内容

### 4. 局部重绘 (Regional Editing)

**修改图像特定区域：**

```python
# 替换物体
edited = editor.regional_edit(
    image='product.png',
    mask='product_mask.png',
    prompt="红色版本的无人机",
    strength=0.8
)

# 添加元素
edited = editor.regional_edit(
    image='scene.png',
    mask='sky_mask.png',
    prompt="添加彩虹到天空",
    strength=0.6
)

# 修改颜色
edited = editor.regional_edit(
    image='drone.png',
    mask='body_mask.png',
    prompt="蓝色机身",
    strength=0.7
)
```

### 5. 超分辨率 (Super Resolution)

**提升图像质量：**

```python
# 4 倍放大
upscaled = editor.upscale(
    image='low_res.png',
    scale=4,
    model='realesrgan-x4plus'
)

# 人脸增强
enhanced = editor.upscale(
    image='portrait.png',
    scale=2,
    face_enhance=True
)

# 细节增强
enhanced = editor.upscale(
    image='product.png',
    scale=2,
    detail_enhance=True
)
```

## Advanced Features

### ControlNet 精确控制

```python
# 使用边缘控制
editor.add_controlnet(
    type='canny',
    image='edge_map.png',
    strength=0.8
)

# 使用深度控制
editor.add_controlnet(
    type='depth',
    image='depth_map.png',
    strength=0.6
)

# 使用法线贴图
editor.add_controlnet(
    type='normal',
    image='normal_map.png',
    strength=0.5
)
```

### 批量处理

```python
# 批量风格转换
images = ['img1.png', 'img2.png', 'img3.png']
results = editor.batch_style_transfer(
    images=images,
    style='cyberpunk',
    strength=0.7,
    workers=4
)

# 批量放大
upscaled = editor.batch_upscale(
    images=images,
    scale=2,
    workers=4
)
```

### 工作流编排

```python
# 创建处理工作流
workflow = editor.create_workflow([
    {'action': 'upscale', 'scale': 2},
    {'action': 'denoise', 'strength': 0.3},
    {'action': 'style_transfer', 'style': 'cinematic'},
    {'action': 'sharpen'}
])

# 执行工作流
result = workflow.execute('input.png')
```

## Use Cases

### 1. 产品图优化

```python
editor = ImageEditor()

# 提升分辨率
product_hd = editor.upscale('product_low.jpg', scale=4)

# 移除背景
product_nobg = editor.remove_background(product_hd)

# 添加新背景
product_new = editor.regional_edit(
    image=product_nobg,
    mask='background_mask.png',
    prompt="白色演播室背景，柔光"
)

# 保存
product_new.save('product_final.png')
```

### 2. 老照片修复

```python
# 完整修复流程
old_photo = load('old_damaged.jpg')

# 1. 放大
upscaled = editor.upscale(old_photo, scale=4)

# 2. 去划痕
fixed = editor.inpaint(
    image=upscaled,
    prompt="修复划痕和损坏"
)

# 3. 上色
colored = editor.style_transfer(
    image=fixed,
    style='colorize',
    strength=0.5
)

# 4. 增强
enhanced = editor.enhance(colored)

enhanced.save('restored_photo.png')
```

### 3. 营销素材制作

```python
# 从产品图创建多种营销素材
base_image = 'product.png'

# 社交媒体方形图
social = editor.crop_and_fill(
    image=base_image,
    target_ratio='1:1',
    prompt="填充背景"
)

# 海报竖版图
poster = editor.outpaint(
    image=base_image,
    direction='top',
    pixels=512,
    prompt="添加标题空间"
)

# 宽屏横幅
banner = editor.outpaint(
    image=base_image,
    direction='right',
    pixels=1024,
    prompt="扩展展示空间"
)
```

### 4. 设计迭代

```python
# 快速生成设计变体
base_design = 'design_v1.png'

# 生成颜色变体
variants = editor.batch_regional_edit(
    image=base_design,
    mask='color_area_mask.png',
    prompts=[
        "蓝色主题",
        "红色主题",
        "绿色主题",
        "黑色主题"
    ]
)

# 保存所有变体
for i, variant in enumerate(variants):
    variant.save(f'design_v2_color_{i+1}.png')
```

## Commands

### /image-to-image

```bash
# 风格转换
/image-to-image input.png --style cyberpunk --strength 0.7

# 图像修复
/image-to-image damaged.png --action inpaint

# 图像扩展
/image-to-image input.png --action outpaint --direction right --pixels 512

# 超分辨率
/image-to-image low_res.png --action upscale --scale 4
```

### /style-transfer

```bash
/style-transfer input.png --style anime --output output.png
```

### /inpaint

```bash
/inpaint image.png --mask mask.png --prompt "修复区域"
```

### /outpaint

```bash
/outpaint image.png --direction all --pixels 256
```

## Performance

| 操作 | 处理时间 | 质量提升 |
|------|---------|---------|
| 风格转换 | 5-10 秒 | ⭐⭐⭐⭐ |
| 图像修复 | 10-20 秒 | ⭐⭐⭐⭐⭐ |
| 图像扩展 | 10-15 秒 | ⭐⭐⭐⭐ |
| 超分辨率 (2x) | 3-5 秒 | ⭐⭐⭐⭐ |
| 超分辨率 (4x) | 10-20 秒 | ⭐⭐⭐⭐⭐ |

## Best Practices

### Do's
✅ 使用合适的强度值 (0.3-0.8)  
✅ 提供清晰的蒙版  
✅ 使用详细的提示词  
✅ 保存中间结果  
✅ 多次尝试取最佳  

### Don'ts
❌ 强度过高导致失真  
❌ 蒙版边界模糊  
❌ 提示词过于简单  
❌ 期望完美一次成功  

## Resources

- **Stable Diffusion Inpaint:** https://github.com/Stability-AI/stablediffusion
- **ControlNet:** https://github.com/lllyasviel/ControlNet
- **Real-ESRGAN:** https://github.com/xinntao/Real-ESRGAN
- **GFPGAN:** https://github.com/TencentARC/GFPGAN

---

**创建时间:** 2026-04-10  
**版本:** v1.0  
**依赖:** diffusers, transformers, pillow, torch, realesrgan
