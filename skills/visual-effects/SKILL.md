# Visual Effects - 视觉效果技能

## Purpose

创建专业视觉效果和动画：
- **粒子效果** - 粒子系统动画
- **光效** - 发光、光晕、光线
- **过渡动画** - 场景转换效果
- **动态图形** - Motion Graphics
- **特效合成** - 多层效果合成

## Effect Types

### 1. 粒子效果 (Particle Effects)

```python
from visual_effects import ParticleSystem

# 创建粒子系统
particles = ParticleSystem()

# 添加发射器
particles.add_emitter(
    type='point',
    position=(512, 512),
    rate=100,  # 每秒粒子数
    lifetime=2.0
)

# 配置粒子
particles.configure_particle(
    size=(10, 30),
    color=['#FF6600', '#FFCC00'],
    speed=(50, 100),
    gravity=-50
)

# 渲染
effect = particles.render(
    width=1920,
    height=1080,
    fps=60,
    duration=5
)
```

### 2. 光效 (Light Effects)

```python
from visual_effects import LightEffects

lights = LightEffects()

# 添加光源
lights.add_light(
    type='spotlight',
    position=(512, 256),
    color='#FFFFFF',
    intensity=1.5,
    angle=45
)

# 添加光晕
lights.add_glow(
    position=(512, 512),
    radius=100,
    color='#0066FF',
    intensity=0.8
)

# 渲染光效
effect = lights.render(
    background='drone_image.png',
    output='lighting_effect.mp4'
)
```

### 3. 过渡动画 (Transition Effects)

```python
from visual_effects import Transitions

transitions = Transitions()

# 淡入淡出
fade = transitions.fade(
    duration=1.0,
    direction='in'  # or 'out'
)

# 滑动过渡
slide = transitions.slide(
    duration=0.5,
    direction='left'
)

# 缩放过渡
zoom = transitions.zoom(
    duration=0.8,
    ease='ease_out'
)

# 应用过渡
video = transitions.apply(
    clips=[clip1, clip2],
    transition=fade
)
```

### 4. 动态图形 (Motion Graphics)

```python
from visual_effects import MotionGraphics

mograph = MotionGraphics()

# 创建文字动画
text_anim = mograph.text_animation(
    text="产品发布",
    font="Inter Bold",
    animation='typewriter',
    duration=2.0
)

# 创建形状动画
shape_anim = mograph.shape_animation(
    shape='circle',
    animation='scale_up',
    duration=1.5
)

# 创建图标动画
icon_anim = mograph.icon_animation(
    icon='drone',
    animation='float',
    duration=3.0
)

# 合成
final = mograph.compose([text_anim, shape_anim, icon_anim])
```

### 5. 特效合成 (VFX Compositing)

```python
from visual_effects import VFXCompositor

compositor = VFXCompositor()

# 添加图层
compositor.add_layer(
    image='background.png',
    type='background'
)

compositor.add_layer(
    video='drone_footage.mp4',
    type='video',
    blend_mode='normal'
)

compositor.add_layer(
    effect=particles,
    type='effect',
    blend_mode='screen'
)

# 添加调色
compositor.add_color_grading(
    brightness=1.1,
    contrast=1.2,
    saturation=1.1
)

# 渲染合成
final = compositor.render(
    output='final_composite.mp4',
    resolution='4K'
)
```

## Commands

### /visual-effects

```bash
# 创建粒子效果
/visual-effects particles --count 1000 --color orange

# 创建光效
/visual-effects glow --position 512,512 --color blue

# 创建过渡
/visual-effects transition --type fade --duration 1.0

# 创建动态图形
/visual-effects mograph --text "Hello" --animation typewriter
```

### /compose

```bash
/compose layer1.png layer2.mp4 effect.json --output final.mp4
```

---

**创建时间:** 2026-04-10  
**版本:** v1.0  
**依赖:** moviepy, pillow, numpy, opencv
