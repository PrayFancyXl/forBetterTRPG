# forBetterTRPG — 狩魂者TRPG AI建卡器

一个基于AI的交互式TRPG角色卡构建工具，旨在降低《狩魂者TRPG》新手玩家的建卡学习成本。

## 特性

- 将规则书PDF自动转换为结构化知识库
- AI辅助的分步建卡引导
- 实时规则校验与建议
- 角色发展方向预测

## 快速开始

```bash
# 安装依赖
pip install -e ".[dev]"

# 转换规则书文档
python scripts/convert_docs.py

# 生成知识库
python scripts/generate_knowledge.py
```

## 项目状态

- [x] Phase 1: 文档转换 + 知识库生成
- [ ] Phase 2: 前端建卡器 + 后端API
- [ ] Phase 3: 多Agent协同建卡
- [ ] Phase 4: 角色发展建议

## 技术栈

| 层级 | 技术 |
|------|------|
| 文档转换 | markitdown |
| AI编排 | LangGraph |
| 高层AI | Claude (Anthropic) |
| 执行AI | DeepSeek |
| 前端 | Vue 3 + Vite |
| 后端 | FastAPI |
