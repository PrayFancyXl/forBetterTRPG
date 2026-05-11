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

### Git 初始化

```bash
cd D:\pythonProject\forBetterTRPG
git init
# 首次提交: 4cfb22c
# 状态: 仅本地，未配置remote，未push
```

**注意**: 目前 git 仓库仅存在于本地 `D:\pythonProject\forBetterTRPG\.git\`，尚未推送到 GitHub 或 GitLab。推送时需要：
```bash
git remote add origin <仓库URL>
git push -u origin master
```

### markitdown 安装

markitdown 已通过 pip 安装到全局 Python 环境（需要代理关闭后手动安装）：
```bash
pip install "markitdown[all]"
```

同时项目内 `markitdown/` 子文件夹保留了完整源码（独立 git 仓库），被 `.gitignore` 排除。

### 依赖说明

Python 3.10.3 环境，核心依赖：
- `markitdown[all]` — 文档转换
- `openpyxl` — Excel 解析
- `anthropic` — Claude API（Phase 2 知识库增强）
- `langgraph` + `langchain` — 多Agent框架（Phase 2）

---

## 技术决策

| 决策 | 选择 | 原因 |
|------|------|------|
| 知识库数据源 | Excel优先，PDF补充 | Excel有精确结构化数据，PDF有水印和排版噪音 |
| AI架构 | 分层：Claude(高层) + DeepSeek(执行层) | 高性能AI生成规则，平价AI执行问答，控制成本 |
| Agent框架 | LangGraph | 原生支持supervisor/worker模式，多LLM后端 |
| 前端 | Vue 3 + Vite | 轻量、响应式数据绑定适合表单联动 |
| markitdown处理 | 作为子文件夹保留源码 | 方便调试，.gitignore排除避免污染主仓库 |
