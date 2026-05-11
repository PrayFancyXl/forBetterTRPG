# forBetterTRPG - 狩魂者TRPG交互式建卡器

## 项目架构

```
forBetterTRPG/
├── scripts/          # 构建阶段脚本（文档转换、知识库生成）
├── data/
│   ├── markdown/     # markitdown转换输出
│   └── knowledge/    # AI生成的结构化知识库JSON
├── originData/       # 原始TRPG规则书PDF和Excel模板
├── markitdown/       # 微软markitdown工具（子文件夹，独立git）
├── src/              # 后端源码（Phase 2+）
└── frontend/         # Vue 3 + Vite 前端（Phase 2+）
```

## 技术栈

- **文档转换**: markitdown (PDF/Excel → Markdown)
- **AI框架**: LangGraph + LangChain（分层多Agent架构）
- **高层AI**: Claude (Anthropic) — 规则分析、知识库生成
- **执行AI**: DeepSeek — 建卡问答、实时交互
- **前端**: Vue 3 + Vite
- **后端**: FastAPI (Phase 2+)

## 开发命令

```bash
# 安装依赖
pip install -e ".[dev]"

# 文档转换（将originData转为markdown）
python scripts/convert_docs.py

# 生成知识库（需要ANTHROPIC_API_KEY环境变量）
python scripts/generate_knowledge.py

# 代码检查
ruff check .
ruff format .
```

## 环境变量

需要在 `.env` 文件中配置：
```
ANTHROPIC_API_KEY=your_key_here
DEEPSEEK_API_KEY=your_key_here  # Phase 2+
```

## 分层AI架构

1. **构建阶段**（离线）: Claude Opus 分析规则书 → 生成结构化知识库JSON + 建卡流程规则
2. **运行阶段**（在线）: DeepSeek 基于知识库 → 引导用户建卡、回答规则问题

## 开发规范

- Python 代码使用 ruff 格式化，行宽 100
- JSON 知识库文件使用 UTF-8 编码，缩进 2 空格
- 所有脚本从项目根目录运行
- markitdown 通过 pip install 使用，不修改其源码
