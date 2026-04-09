# 视觉设计技能使用指南

## 📦 已安装技能

### 1. Text-to-Image (文生图)
**位置:** `skills/text-to-image/SKILL.md`

**功能:**
- Stable Diffusion/DALL-E 3/Midjourney/Flux
- ControlNet 精确控制
- Prompt 工程模板

**使用:**
```bash
/text-to-image "一个现代化的无人机产品图，白色背景，专业摄影，4K"
/text-to-image "产品摄影" --size 1024x1024 --steps 30
/text-to-image "艺术图" --provider midjourney
```

---

### 2. Image-to-Image (图生图)
**位置:** `skills/image-to-image/SKILL.md`

**功能:**
- 风格转换 (10+ 预设风格)
- 图像修复 (老照片/去水印)
- 图像扩展 (Outpainting)
- 局部重绘 (Inpainting)
- 超分辨率 (2x/4x 放大)

**使用:**
```bash
/image-to-image input.png --style cyberpunk --strength 0.7
/image-to-image damaged.png --action inpaint
/image-to-image input.png --action outpaint --direction right --pixels 512
/image-to-image low_res.png --action upscale --scale 4
```

---

### 3. Design-Style (设计风格)
**位置:** `skills/design-style/SKILL.md`

**功能:**
- 4 种主要风格指南
- 智能配色生成
- 字体搭配推荐
- 版式设计建议

**使用:**
```bash
/design-style "科技公司官网" --industry tech
/design-style --color --base #0066FF --scheme complementary
/design-style --typography --usage website --style modern
/color-palette --base #0066FF --count 5
/font-pairing --primary Montserrat --usage presentation
```

---

### 4. Visual-Effects (视觉效果)
**位置:** `skills/visual-effects/SKILL.md`

**功能:**
- 粒子系统
- 光效 (发光/光晕)
- 过渡动画
- 动态图形
- 特效合成

**使用:**
```bash
/visual-effects particles --count 1000 --color orange
/visual-effects glow --position 512,512 --color blue
/visual-effects transition --type fade --duration 1.0
/visual-effects mograph --text "Hello" --animation typewriter
```

---

### 5. Generative-Media (生成媒体)
**位置:** `skills/generative-media/`

**功能:**
- Nano-Banana (Gemini 3 风格)
- Cinema Director (电影级视频)
- Seedance 2 (文生视频/图生视频)
- UI Designer (界面设计)
- Logo Creator (Logo 设计)

**使用:**
```bash
# Nano-Banana 图像生成
cd skills/generative-media/library/visual/nano-banana
bash scripts/generate-nano-art.sh --subject "玻璃蜂鸟" --style "微距摄影"

# Cinema Director 视频生成
cd skills/generative-media/library/motion/cinema-director
bash scripts/generate-film.sh --subject "赛博机械龙" --intent "史诗" --duration 10

# Seedance 2 图生视频
cd skills/generative-media/library/motion/seedance-2
bash scripts/generate-seedance.sh --mode i2v --file ./concept.jpg
```

---

## 🎯 使用场景

### 1. 无人机产品图生成

```bash
# 文生图
/text-to-image "专业无人机产品摄影，DJI 风格，白色背景，演播室灯光，4K 超细节"

# 图生图 (风格转换)
/image-to-image drone_photo.png --style professional --strength 0.6

# 高清放大
/image-to-image low_res.png --action upscale --scale 4

# 背景移除
cd skills/generative-media
muapi enhance remove-bg ./drone.png --download ./outputs
```

---

### 2. 保险产品可视化

```bash
# 生成保险概念图
/text-to-image "保险保护概念，盾牌图标，蓝色主题，3D 渲染，专业商务风格"

# 生成理赔流程图
/text-to-image "保险理赔流程图，简洁信息图，蓝色和白色，矢量风格"

# 设计风格建议
/design-style --color --emotion trust --industry finance
```

---

### 3. 营销素材制作

```bash
# 社交媒体图片
/text-to-image "社交媒体营销图，无人机产品，促销标签，红色和黑色，吸引眼球" --size 1080x1080

# 产品海报
/text-to-image "产品发布海报，无人机，科技感，渐变背景，大标题空间" --size 1080x1920

# 动态图形
/visual-effects mograph --text "新品发布" --animation fade_in
```

---

### 4. Logo 设计

```bash
# 使用 Generative Media
cd skills/generative-media/library/visual/logo-creator
bash scripts/create-logo.sh --company "DJI" --style minimalist --industry tech

# 或使用文生图
/text-to-image "极简科技 Logo，无人机图标，蓝色和白色，矢量风格" --size 1024x1024
```

---

### 5. UI/UX 设计

```bash
# 使用 UI Designer
cd skills/generative-media/library/visual/ui-design
bash scripts/design-ui.sh --type mobile --industry tech --style modern

# 或使用设计风格建议
/design-style --typography --usage mobile_app --style modern
/design-style --layout --content_type product_showcase
```

---

## 🔧 配置 API

### Replicate API (推荐)

```bash
# 获取 Token: https://replicate.com/account/api-tokens
export REPLICATE_API_TOKEN=r8_你的 token

# 使用 Python 脚本
python3 scripts/replicate_generate.py --prompt "无人机产品图"
```

### Fal.ai API

```bash
# 获取 Key: https://fal.ai/dashboard/keys
export FAL_KEY=你的 key

# 使用脚本
python3 scripts/fal_generate.py --prompt "无人机产品图"
```

### Novita AI

```bash
# 获取 Key: https://novita.ai
export NOVITA_KEY=你的 key

# 使用脚本
python3 scripts/novita_generate.py --prompt "无人机产品图"
```

---

## 📁 文件位置

```
/home/admin/.openclaw/workspace/skills/
├── text-to-image/SKILL.md          # 文生图技能
├── image-to-image/SKILL.md         # 图生图技能
├── design-style/SKILL.md           # 设计风格技能
├── visual-effects/SKILL.md         # 视觉效果技能
└── generative-media/               # 生成媒体技能
    ├── library/
    │   ├── visual/
    │   │   ├── nano-banana/
    │   │   ├── ui-design/
    │   │   └── logo-creator/
    │   └── motion/
    │       ├── cinema-director/
    │       └── seedance-2/
    ├── schema_data.json            # 100+ 模型数据
    └── INTEGRATION.md              # 集成指南
```

---

## 💡 最佳实践

### Prompt 编写技巧

```
[主体描述] + [环境/背景] + [风格] + [灯光] + [构图] + [质量参数]

示例:
专业产品摄影，无人机，白色背景，演播室灯光，45 度角，超细节，8K 分辨率，商业级质量
```

### 负面提示词

```
模糊，低质量，变形，多余，水印，文字，签名，暗，过曝，噪点
```

### 参数建议

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| steps | 20-30 | 生成步数 |
| guidance_scale | 7-9 | 提示词相关性 |
| strength | 0.3-0.8 | 图生图强度 |
| width/height | 1024x1024 | 标准分辨率 |

---

## 🚀 快速开始

### 1. 选择 API 服务

**推荐:** Replicate (便宜 + 快速)
- 注册：https://replicate.com
- 获取 Token
- 配置环境变量

### 2. 测试文生图

```bash
/text-to-image "测试图，简单几何图形" --size 512x512
```

### 3. 生成产品图

```bash
/text-to-image "专业无人机产品摄影，白色背景，演播室灯光" --size 1024x1024
```

### 4. 后期处理

```bash
# 放大
/image-to-image output.png --action upscale --scale 2

# 风格调整
/image-to-image output.png --style professional --strength 0.3
```

---

**创建时间:** 2026-04-10  
**版本:** v1.0  
**状态:** ✅ 立即可用
