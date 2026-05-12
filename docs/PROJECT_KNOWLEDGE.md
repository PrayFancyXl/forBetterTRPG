# 项目知识库说明文档

本文档记录 forBetterTRPG 项目中各阶段产出的文件、核心操作流程和关键决策，方便后续快速了解项目上下文。

---

## 项目概述

《狩魂者TRPG》AI辅助交互式建卡器。将复杂的Excel建卡流程转化为分步引导式网页应用，集成AI问答辅助新手玩家。

- GitHub: https://github.com/PrayFancyXl/forBetterTRPG.git
- 分支: master
- 最新提交: `773506f` (feat: Stage D+E)

---

## 环境配置

- Python 3.10.3，虚拟环境: `.venv/`（项目根目录）
- Node.js 22.18.0 + npm 10.9.3
- pip安装需开启Clash代理（127.0.0.1:7890），否则SSL报错
- npm install需在用户终端执行（Claude Code的bash子进程PATH找不到node）
- 前端端口: 3000（vite proxy代理/api到后端）
- 后端端口: 8003（用户已修改vite.config.ts中的target为8003）

### 启动命令

```bash
# 后端
cd D:\pythonProject\forBetterTRPG
.venv\Scripts\activate
uvicorn src.main:app --reload --port 8003

# 前端
cd D:\pythonProject\forBetterTRPG\frontend
npm run dev
# 浏览器访问 http://localhost:3000
```

### 环境变量

`.env` 文件（项目根目录，已在.gitignore中排除）：
```
DEEPSEEK_API_KEY=sk-xxxxx
```

---

## Phase 1: 文档转换与知识库生成（已完成）

### 数据来源

| 文件 | 类型 | 大小 | 说明 |
|------|------|------|------|
| 狩魂者TRPG核心规则-电子版（资源部分二三四章）.pdf | PDF | 48MB | 核心规则书 |
| 狩魂者车卡教学v1.pdf | PDF | 8MB | 扫描版，无文字层 |
| 狩魂者可填写卡（正式版）.pdf | PDF | 2.3MB | 扫描版，无文字层 |
| 狩魂者空白卡正式版V1.4.xlsx | Excel | 150KB | 角色卡模板，11个sheet |

### 知识库文件（data/knowledge/）

| 文件 | 内容 |
|------|------|
| `attributes.json` | 属性等级表（E→SSS+），属性值/强度/成长奖励 |
| `skills.json` | 7项技能定义及分配规则 |
| `martial_arts.json` | 20+条武技 |
| `spells.json` | 30+条术法 |
| `spirit_marks.json` | 25种灵能印记 |
| `feats.json` | 20条专长 |
| `ultimates.json` | 10条绝技（一挡7+二挡3） |
| `stylish_moves.json` | 7种时髦风格 |
| `effects.json` | 15种通用效果 |
| `card_template.json` | 角色卡字段定义和建卡步骤 |
| `rules_graph.json` | 规则关联关系图 |
| `core_rules_cleaned.md` | 清洗后的规则书文本 |

### 核心规则摘要

**属性系统：** 体魄/智慧/心魂，等级E(1,0)→SSS+(9,4)

**灵识成长：** 10级专长、12级灵魂武器、14级一挡绝技、16级专长、18级二挡绝技

**建卡6步：** 灵能力→羁绊→角色信息→属性→技能→能力选择

---

## Phase 2: 全栈建卡器（已完成）

### 后端架构 (src/)

```
src/
├── main.py              # FastAPI入口，CORS，路由注册，知识库启动加载
├── config.py            # pydantic-settings，读取.env
├── models/
│   ├── enums.py         # AttributeLevel, CreationStep, ATTRIBUTE_TABLE
│   ├── character.py     # CharacterCard完整Pydantic模型（12个子模型）
│   └── creation_state.py # CreationSession, ValidationResult
├── rule_engine/
│   ├── engine.py        # validate_step()调度器
│   ├── attribute_rules.py # 属性→解锁计算
│   ├── spirit_growth.py # 灵识→成长奖励
│   └── skill_rules.py  # 技能点校验
├── services/
│   ├── knowledge_loader.py # KnowledgeBase单例
│   ├── ai_service.py   # DeepSeek对话（SSE流式，步骤感知上下文）
│   └── export_service.py # JSON + Excel导出
└── routes/
    ├── character.py     # 会话CRUD + 步骤提交
    ├── validation.py    # 校验端点
    ├── knowledge.py     # 知识库查询（支持过滤）
    ├── chat.py          # AI对话SSE + 步骤提示
    └── export.py        # 导出/导入端点
```

**API端点（19个）：**
- `POST /api/sessions` — 创建建卡会话
- `GET /api/sessions/{id}` — 获取会话
- `PUT /api/sessions/{id}/steps/{step}` — 提交步骤数据+自动校验
- `POST /api/validation/{session_id}` — 手动校验
- `GET /api/knowledge/{type}` — 查询知识库
- `POST /api/chat` — AI对话（SSE流式）
- `GET /api/chat/tip/{step}` — 步骤提示
- `DELETE /api/chat/history/{session_id}` — 清除历史
- `POST /api/export/json/{session_id}` — 导出JSON
- `POST /api/export/excel/{session_id}` — 导出Excel
- `POST /api/export/import/json` — 导入JSON
- `GET /api/health` — 健康检查

### 前端架构 (frontend/)

```
frontend/src/
├── App.vue              # 主布局（导航+内容+侧边栏+导出按钮）
├── stores/character.ts  # Pinia会话状态
├── stores/chat.ts       # Pinia聊天状态
├── api/client.ts        # API封装+SSE
├── components/
│   ├── StepNavigation.vue
│   ├── ValidationFeedback.vue
│   ├── ChatPanel.vue
│   ├── CardPreview.vue
│   └── steps/Step1-6.vue
└── types/character.ts
```

**UI：** 暗色主题(#1a1a2e)，紫色主色(#a855f7)，左内容+右侧栏(预览+AI对话)

### 进度总览

| Stage | 状态 |
|-------|------|
| A 后端核心 | ✅ |
| B AI集成 | ✅ |
| C 前端框架 | ✅ |
| D 完善步骤 | ✅ |
| E 导出功能 | ✅ |
| 前端UI优化 | ⏳ |

---

## 已知问题

1. **DeepSeek对话报错**: httpx连接异常，可能是代理/网络问题。需确认能访问api.deepseek.com
2. **前端优化待做**: UI美化、响应式、动画、错误处理优化
3. **Excel导出映射不完整**: 当前只映射了部分字段，需扩展完整映射

---

## 技术决策

| 决策 | 选择 | 原因 |
|------|------|------|
| 知识库数据源 | Excel优先 | 精确结构化数据 |
| AI架构 | Claude(高层) + DeepSeek(执行层) | 成本控制 |
| Agent框架 | LangGraph | supervisor/worker模式 |
| 前端 | Vue 3 + Vite + Pinia | 轻量、表单联动好 |
| 后端 | FastAPI + Pydantic v2 | 类型安全、自动文档 |
| 会话存储 | 内存dict | 简单，通过JSON导出持久化 |
| DeepSeek接入 | langchain_openai.ChatOpenAI | OpenAI兼容API |

---

## 依赖清单

**Python (.venv):**
fastapi, uvicorn, pydantic, pydantic-settings, python-dotenv, sse-starlette, langchain-openai, openpyxl, python-multipart, markitdown[all]

**Node (frontend/node_modules):**
vue@3.5, vue-router@4.6, pinia@2.3, vite@6.4, @vitejs/plugin-vue, typescript, vue-tsc
