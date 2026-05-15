# UI 设计进度记录

## 风格方向：Ethereal Ink Wash（以太水墨）

**确定的设计语言：**
- 背景：深青 `#1A2A3A` + 石板灰 `#2C3E50` 流动烟雾
- 面板：毛玻璃 glassmorphism，`backdrop-filter: blur`
- 边框：多层 `box-shadow` 幽光晕染，无实线 border
- 字体：Noto Serif SC（标题）+ Noto Sans SC（正文）
- 粒子：55个灵魂粒子浮动动画（幽灵紫 + 以太白）
- 导航：Tab 式自由切换（非强制顺序）

## 已实现的4个调整方向

| 方向 | 技术 | 状态 |
|------|------|------|
| 1. 毛笔边框 | `BrushBorder.png` 作为 `::after` 叠加层 | ✅ |
| 2. 材质混合 | `background.png` + `mix-blend-mode: screen` + SVG noise | ✅ |
| 3. 幽光晕染边框 | 多层 `box-shadow`，无实线 border | ✅ |
| 4. 不对称设计 | Tab nav `clip-path` 墨迹形状 + 剑痕分割线 | ✅ |

## 生成的资源文件

- `BrushBorder.png` — RGBA 笔触边框叠加图（1200×800，四边笔触，中心透明）
- `PanelMask.png` — 备用遮罩图（白底黑边，safe zone 对齐 padding）
- `ethereal-inkwash-mockup.html` — 完整交互预览（含粒子动画）

## 原始素材（originData/）

- `BrushStrokeMask.png` — 黑底白笔触，RGB，1672×941，笔触集中在图片中央横带
- `background.png` — 深色水墨纹理，RGB，1672×941，最亮像素约 RGB(37,61,79)

## 待实现（下一阶段）

- [ ] 将设计落地到实际 Vue 组件
- [ ] Tab 导航改为可点击自由切换（修改 character store 的 currentStep 逻辑）
- [ ] 全局 CSS 变量化（颜色、间距）
- [ ] 响应式适配
- [ ] Excel 导出字段映射补全
