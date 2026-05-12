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

# 启动后端（端口8003）
uvicorn src.main:app --reload --port 8003

# 启动前端（端口3000，自动代理/api到后端8003）
# 注意：npm命令需在用户终端执行，Claude Code bash子进程找不到node
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
HTTP_PROXY=http://127.0.0.1:7890
```

## 当前状态

- Phase 1 ✅ 文档转换 + 知识库生成
- Phase 2 Stage A-E ✅ 后端核心 + AI集成 + 前端框架 + 完善步骤 + 导出功能
- Phase 2 Stage F ✅ DeepSeek API接入修复（代理、模型名、SSE）
- Phase 2 Stage G ✅ ChatPanel Markdown渲染优化
- 前端UI优化 ⏳ 下一阶段

详细进度和待办事项见 `docs/PROJECT_KNOWLEDGE.md`

## 经验文档

`docs/troubleshooting.md` — 已解决问题的排查记录，包含：
- DeepSeek API 连接问题（代理配置、base_url、openai SDK用法）
- DeepSeek 模型名称（v4-flash/v4-pro，旧名废弃时间）
- SSE 流式输出 + Markdown 渲染问题（token含\n导致截流、表格压缩、white-space冲突）
- System Prompt 规范输出格式的最佳实践

**遇到 AI 对话、SSE、Markdown 渲染相关问题时，优先查阅此文档。**

## 开发规范

- Python: ruff格式化，行宽100，类型注解
- TypeScript: strict模式
- Vue: Composition API + `<script setup>`
- JSON知识库: UTF-8编码，缩进2空格
- Git: 功能分支，commit message中文+英文混合
- 所有脚本从项目根目录运行
- markitdown通过pip install使用，不修改其源码
- 前端通过vite proxy代理API请求到后端，无需处理CORS
