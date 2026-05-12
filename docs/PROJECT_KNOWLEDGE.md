# 项目知识库说明文档

本文档记录 forBetterTRPG 项目中各阶段产出的文件、核心操作流程和关键决策，方便后续快速了解项目上下文。

---

## Phase 1: 文档转换与知识库生成

### 1.1 数据来源

| 文件 | 类型 | 大小 | 说明 |
|------|------|------|------|
| 狩魂者TRPG核心规则-电子版（资源部分二三四章）.pdf | PDF | 48MB | 核心规则书，包含建卡流程、战斗规则、世界观 |
| 狩魂者车卡教学v1.pdf | PDF | 8MB | 建卡教学（扫描版，无文字层） |
| 狩魂者可填写卡（正式版）.pdf | PDF | 2.3MB | 可填写角色卡（扫描版，无文字层） |
| 狩魂者空白卡正式版V1.4.xlsx | Excel | 150KB | 角色卡模板，11个sheet，包含所有规则数据 |

### 1.2 转换工具

使用微软 [markitdown](https://github.com/microsoft/markitdown) 将源文件转为 Markdown：

```bash
python scripts/convert_docs.py
```

转换结果存放在 `data/markdown/`：
- `core_rules.md` (465.9 KB) — 规则书全文，有水印噪音但内容完整
- `blank_card.md` (171.5 KB) — Excel 转出的表格 markdown
- `card_tutorial.md` (0 KB) — 扫描版PDF，无法提取文字
- `fillable_card.md` (0 KB) — 扫描版PDF，无法提取文字

### 1.3 知识库生成

```bash
python scripts/generate_knowledge.py
```

该脚本从 Excel 直接提取结构化数据（比 PDF 更精确），输出到 `data/knowledge/`：

| 文件 | 内容 | 用途 |
|------|------|------|
| `attributes.json` | 属性等级表（E→SSS+），每级的属性值、属性强度、三属性成长奖励 | 建卡时属性分配的核心参考 |
| `skills.json` | 7项技能定义及分配规则 | 技能点分配逻辑 |
| `martial_arts.json` | 20+条武技（名称、消耗、目标、效果、风味描述） | 武技选择列表 |
| `spells.json` | 30+条术法（名称、消耗、类别、类型、效果） | 术法选择列表 |
| `spirit_marks.json` | 25种灵能印记类型及描述 | 灵能印记选择 |
| `feats.json` | 20条专长及详细效果描述 | 专长选择 |
| `ultimates.json` | 10条绝技（一挡7个+二挡3个），含对应魂魄和效果 | 绝技选择 |
| `stylish_moves.json` | 7种时髦风格，每种5档消耗对应动作 | 时髦动作选择 |
| `effects.json` | 15种通用效果（恢复、伤害、强化等） | 效果速查参考 |
| `card_template.json` | 角色卡字段定义、约束、建卡步骤 | 前端表单结构定义 |
| `rules_graph.json` | 规则关联关系图（属性→解锁→能力池） | AI分析规则依赖 |
| `core_rules_cleaned.md` | 清洗后的规则书文本（去除水印） | AI上下文补充 |

### 1.4 核心规则摘要

#### 属性系统

三大属性：体魄、智慧、心魂，等级 E(1) → SSS+(9)

| 等级 | 属性值 | 属性强度 | 说明 |
|------|--------|----------|------|
| E | 1 | 0 | 初始，习得基础武技/术法 |
| D | 2 | 1 | 解锁普通武技/术法学习 |
| C | 3 | 1 | 额外习得 |
| B | 4 | 2 | - |
| A | 5 | 2 | 心魂A级觉醒额外灵能印记 |
| S | 6 | 3 | - |
| SS | 7 | 3 | 解锁秘传武技/术法 |
| SSS | 8 | 4 | - |
| SSS+ | 9 | 4 | - |

#### 灵识成长

| 灵识等级 | 获得 |
|----------|------|
| 10 | 第一个专长 |
| 12 | 灵魂武器 |
| 14 | 一挡绝技 |
| 16 | 第二个专长 |
| 18 | 二挡绝技 |

#### 建卡流程（规则书定义）

1. 创建灵能力（概念→标签→描述，≤80字，≤3个标签）
2. 选择狩魂者羁绊
3. 构建角色信息（代号、真名、外貌、性格、背景故事）
4. 分配三大属性等级
5. 分配技能等级
6. 选择武技、术法、专长、灵魂武器、绝技

---

## 核心操作记录

### Git 信息

- 仓库地址: https://github.com/PrayFancyXl/forBetterTRPG.git
- 分支: master
- 提交历史:
  - `4cfb22c` — Phase 1 初始化
  - `2fb4dac` — 项目知识库文档
  - `c4c65dc` — Phase 2 全栈建卡器（后端+前端+AI）

### 环境配置

- Python 3.10.3，虚拟环境位于 `.venv/`（项目根目录下）
- Node.js 22.18.0 + npm 10.9.3
- pip 安装有 SSL 问题，需开启 Clash 代理（127.0.0.1:7890）或手动安装
- npm install 需在用户终端执行（Claude Code 的 bash 子进程 PATH 找不到 node）

### 启动命令

```bash
# 后端（终端1）
cd D:\pythonProject\forBetterTRPG
.venv\Scripts\activate
uvicorn src.main:app --reload --port 8000

# 前端（终端2）
cd D:\pythonProject\forBetterTRPG\frontend
npm run dev
# 访问 http://localhost:3000
```

### DeepSeek API

- 配置文件: `.env`（项目根目录，已在.gitignore中）
- 格式: `DEEPSEEK_API_KEY=sk-xxxxx`
- 模型: deepseek-chat
- 接入方式: langchain_openai.ChatOpenAI (base_url=https://api.deepseek.com)

---

## Phase 2: 全栈建卡器

### 2.1 后端架构 (src/)

```
src/
├── main.py              # FastAPI入口，CORS，路由注册，知识库启动加载
├── config.py            # pydantic-settings，读取.env
├── models/
│   ├── enums.py         # AttributeLevel(E-SSS+), CreationStep(1-6), ATTRIBUTE_TABLE
│   ├── character.py     # CharacterCard完整Pydantic模型（12个子模型）
│   └── creation_state.py # CreationSession, ValidationResult
├── rule_engine/
│   ├── engine.py        # validate_step()调度器，按步骤分发校验
│   ├── attribute_rules.py # 属性→武技数/术法数/技能点/灵能印记数/强度
│   ├── spirit_growth.py # 灵识等级→专长/武器/绝技解锁
│   └── skill_rules.py  # 技能点预算和分配约束
├── services/
│   ├── knowledge_loader.py # KnowledgeBase单例，加载12个JSON
│   └── ai_service.py   # DeepSeek对话，步骤感知上下文注入，SSE流式
└── routes/
    ├── character.py     # POST/GET/PUT 会话和步骤提交
    ├── validation.py    # 校验端点
    ├── knowledge.py     # 知识库查询（武技/术法/专长等，支持过滤）
    └── chat.py          # AI对话SSE端点 + 步骤提示 + 历史清除
```

**API端点（20个）：**
- `POST /api/sessions` — 创建建卡会话
- `GET /api/sessions/{id}` — 获取会话
- `PUT /api/sessions/{id}/steps/{step}` — 提交步骤数据+自动校验
- `POST /api/validation/{session_id}` — 手动校验
- `GET /api/knowledge/{type}` — 查询知识库（martial-arts/spells/feats/ultimates/spirit-marks/stylish-moves/effects/attributes）
- `POST /api/chat` — AI对话（SSE流式）
- `GET /api/chat/tip/{step}` — 获取步骤提示
- `DELETE /api/chat/history/{session_id}` — 清除对话历史
- `GET /api/health` — 健康检查

**规则引擎核心逻辑：**
- 属性等级→解锁信息：`compute_unlocked_info(physique, wisdom, spirit)` 返回武技数/术法数/技能点/印记数/是否秘传
- 灵识成长：`compute_spirit_unlocks(spirit_awareness)` 返回专长数/武器/绝技解锁状态
- 技能校验：`validate_skill_allocation(free_points, wisdom)` 检查预算和上限

### 2.2 前端架构 (frontend/)

```
frontend/src/
├── main.ts              # Vue app入口，Pinia + Router
├── App.vue              # 主布局（步骤导航 + 内容区 + AI侧边栏）
├── router/index.ts      # 路由（/create/:step）
├── stores/
│   ├── character.ts     # Pinia: 会话状态、submitStep()
│   └── chat.ts          # Pinia: 消息列表、sendMessage()流式
├── api/client.ts        # fetch封装 + SSE流式消费
├── types/character.ts   # TypeScript接口（镜像后端模型）
└── components/
    ├── StepNavigation.vue      # 步骤指示器（6步，高亮当前/已完成）
    ├── ValidationFeedback.vue  # 错误/警告显示
    ├── ChatPanel.vue           # AI对话侧边栏（输入+消息列表+流式渲染）
    └── steps/
        ├── Step1SpiritPower.vue  # 灵能力创建（名称/描述/标签/弱点）
        ├── Step2Bond.vue         # 羁绊选择（预设+自定义）
        ├── Step3CharacterInfo.vue # 角色信息表单
        ├── Step4Attributes.vue   # 属性分配（3个选择器+解锁信息面板）
        ├── Step5Skills.vue       # 技能分配（占位，Stage D完善）
        └── Step6Abilities.vue    # 能力选择（占位，Stage D完善）
```

**UI设计：** 暗色主题（#1a1a2e背景），紫色主色调（#a855f7），左侧内容区+右侧AI对话栏

### 2.3 当前进度

| Stage | 状态 | 说明 |
|-------|------|------|
| A 后端核心 | ✅ 完成 | 数据模型+规则引擎+API路由，已验证 |
| B AI集成 | ✅ 完成 | DeepSeek对话服务+SSE+步骤上下文注入 |
| C 前端框架 | ✅ 完成 | Vue 3脚手架+核心组件+Pinia状态管理 |
| D 完善步骤 | ⏳ 待做 | Step5技能滑块、Step6能力选择列表、CardPreview |
| E 导出功能 | ⏳ 待做 | JSON导出/导入 + Excel模板填充导出 |
| 前端优化 | ⏳ 待做 | UI美化、响应式、动画、无障碍（D/E完成后统一优化） |

### 2.4 待完善事项（Stage D）

**Step5Skills 需要实现：**
- 7个技能滑块（运动/操作/隐秘/调查/洞察/说服/狩魂学识）
- 技能点预算显示（由智慧等级决定）
- 属性附加自动计算
- 实时校验（不超预算、单项不超5）

**Step6Abilities 需要实现：**
- 分Tab展示：武技 | 术法 | 专长 | 灵魂武器 | 绝技 | 时髦动作
- 从 `/api/knowledge/{type}` 加载可选列表
- 根据属性等级过滤（秘传需SS+）
- 数量限制校验
- 选中项管理

**CardPreview 需要实现：**
- 右侧或底部实时预览角色卡摘要
- 显示已填写的所有信息

### 2.5 待完善事项（Stage E）

**导出功能：**
- JSON导出：序列化CharacterCard为JSON文件下载
- JSON导入：上传JSON恢复会话
- Excel导出：用openpyxl打开原始模板xlsx，按映射填充单元格，返回下载
  - 需要建立字段→(sheet, cell)的映射关系
  - 原始模板在 `originData/狩魂者空白卡正式版V1.4.xlsx`

---

## 技术决策

| 决策 | 选择 | 原因 |
|------|------|------|
| 知识库数据源 | Excel优先，PDF补充 | Excel有精确结构化数据，PDF有水印和排版噪音 |
| AI架构 | 分层：Claude(高层) + DeepSeek(执行层) | 高性能AI生成规则，平价AI执行问答，控制成本 |
| Agent框架 | LangGraph | 原生支持supervisor/worker模式，多LLM后端 |
| 前端 | Vue 3 + Vite | 轻量、响应式数据绑定适合表单联动 |
| markitdown处理 | 作为子文件夹保留源码 | 方便调试，.gitignore排除避免污染主仓库 |
