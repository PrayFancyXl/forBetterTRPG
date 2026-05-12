# forBetterTRPG - 狩魂者TRPG交互式建卡器

## 项目架构

```
forBetterTRPG/
├── scripts/              # 构建阶段脚本（文档转换、知识库生成）
├── data/
│   ├── markdown/         # markitdown转换输出（.gitignore排除）
│   └── knowledge/        # 结构化知识库JSON（.gitignore排除，可重新生成）
├── originData/           # 原始TRPG规则书PDF和Excel模板
├── markitdown/           # 微软markitdown工具（子文件夹，独立git）
├── src/                  # FastAPI后端
│   ├── main.py           # 入口，CORS，路由注册
│   ├── config.py         # pydantic-settings配置
│   ├── models/           # Pydantic数据模型
│   ├── rule_engine/      # 规则校验引擎
│   ├── services/         # 知识库加载、AI对话、导出
│   └── routes/           # API路由
├── frontend/             # Vue 3 + Vite + TypeScript
│   └── src/
│       ├── components/   # Vue组件（steps/, ChatPanel, StepNavigation等）
│       ├── stores/       # Pinia状态管理
│       ├── api/          # API请求封装
│       └── types/        # TypeScript类型定义
├── docs/                 # 项目文档
│   └── PROJECT_KNOWLEDGE.md  # 详细项目知识库（阶段产出、规则摘要、待办）
└── .venv/                # Python虚拟环境（.gitignore排除）
```

## 技术栈

- **文档转换**: markitdown (PDF/Excel → Markdown)
- **AI框架**: LangGraph + LangChain（分层多Agent架构）
- **高层AI**: Claude (Anthropic) — 规则分析、知识库生成
- **执行AI**: DeepSeek (deepseek-chat) — 建卡问答、实时交互
- **前端**: Vue 3 + Vite + Pinia + Vue Router + TypeScript
- **后端**: FastAPI + Pydantic v2 + uvicorn
- **导出**: openpyxl（Excel模板填充）

## 开发命令

```bash
# 激活虚拟环境
.venv\Scripts\activate  # Windows

# 启动后端（端口8000）
uvicorn src.main:app --reload --port 8000

# 启动前端（端口3000，自动代理/api到后端）
cd frontend && npm run dev

# 文档转换
python scripts/convert_docs.py

# 生成知识库
python scripts/generate_knowledge.py

# 代码检查
ruff check .
ruff format .
```

## 环境变量

`.env` 文件（项目根目录）：
```
DEEPSEEK_API_KEY=sk-xxxxx
```

## 当前状态

- Phase 1 ✅ 文档转换 + 知识库生成
- Phase 2 Stage A-C ✅ 后端核心 + AI集成 + 前端框架
- Phase 2 Stage D ⏳ 完善Step5/Step6/CardPreview
- Phase 2 Stage E ⏳ 导出功能（JSON + Excel）
- 前端UI优化 ⏳ D/E完成后统一优化

详细进度和待办事项见 `docs/PROJECT_KNOWLEDGE.md`

## 开发规范

- Python: ruff格式化，行宽100，类型注解
- TypeScript: strict模式
- Vue: Composition API + `<script setup>`
- JSON知识库: UTF-8编码，缩进2空格
- Git: 功能分支，commit message中文+英文混合
- 所有脚本从项目根目录运行
- markitdown通过pip install使用，不修改其源码
- 前端通过vite proxy代理API请求到后端，无需处理CORS
