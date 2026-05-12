# forBetterTRPG — 狩魂者TRPG AI建卡器

一个基于AI的交互式TRPG角色卡构建工具，旨在降低《狩魂者TRPG》新手玩家的建卡学习成本。

## 特性

- 将规则书PDF自动转换为结构化知识库
- AI辅助的分步建卡引导（DeepSeek对话）
- 实时规则校验与建议
- 角色卡导出（JSON + Excel原始模板格式）
- 角色卡导入（JSON）

## 快速开始

### 环境准备

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# 安装Python依赖
pip install fastapi uvicorn pydantic-settings python-dotenv sse-starlette langchain-openai openpyxl python-multipart

# 安装前端依赖
cd frontend && npm install && cd ..
```

### 配置环境变量

在项目根目录创建 `.env` 文件：
```
DEEPSEEK_API_KEY=sk-你的DeepSeek_API_Key
```

### 生成知识库（首次运行）

```bash
# 转换规则书文档为Markdown
python scripts/convert_docs.py

# 从Excel提取结构化知识库
python scripts/generate_knowledge.py
```

### 启动项目

```bash
# 终端1：启动后端（端口8003）
.venv\Scripts\activate
uvicorn src.main:app --reload --port 8003

# 终端2：启动前端（端口3000）
cd frontend
npm run dev
```

浏览器访问 http://localhost:3000

## 项目状态

- [x] Phase 1: 文档转换 + 知识库生成
- [x] Phase 2: 前端建卡器 + 后端API + AI集成 + 导出功能
- [ ] Phase 3: 多Agent协同建卡
- [ ] Phase 4: 角色发展建议
- [ ] 前端UI优化

## 技术栈

| 层级 | 技术 |
|------|------|
| 文档转换 | markitdown |
| AI编排 | LangGraph + LangChain |
| 高层AI | Claude (Anthropic) — 规则分析 |
| 执行AI | DeepSeek — 建卡问答 |
| 前端 | Vue 3 + Vite + Pinia + TypeScript |
| 后端 | FastAPI + Pydantic v2 |
| 导出 | openpyxl (Excel模板填充) |

## 项目文档

详细的项目知识库、架构说明和待办事项见 [docs/PROJECT_KNOWLEDGE.md](docs/PROJECT_KNOWLEDGE.md)
