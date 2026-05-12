# 开发经验沉淀 - 问题排查与解决方案

本文档记录项目开发中遇到的典型问题及解决方案，供后续 AI 对话快速参考。

---

## 1. DeepSeek API 连接问题

### 症状
`httpx.ConnectError` 或 `openai.APIConnectionError`，无法连接 `api.deepseek.com`。

### 根本原因
- 国内直连 `api.deepseek.com` 需要代理
- `langchain_openai.ChatOpenAI` 不支持透传 httpx 代理客户端，兼容性差

### 解决方案
1. 弃用 `langchain_openai`，改用 `openai.AsyncOpenAI` 直接调用
2. `base_url` 必须加 `/v1` 后缀：`https://api.deepseek.com/v1`
3. 通过 `.env` 配置 `HTTP_PROXY=http://127.0.0.1:7890`（Clash 代理）
4. 创建 `httpx.AsyncClient(proxy=...)` 传入 `openai.AsyncOpenAI`

### 关键代码（`src/services/ai_service.py`）
```python
def _get_client() -> openai.AsyncOpenAI:
    import httpx
    http_client = httpx.AsyncClient(proxy=settings.HTTP_PROXY) if settings.HTTP_PROXY else None
    return openai.AsyncOpenAI(
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_BASE_URL,  # https://api.deepseek.com/v1
        http_client=http_client,
    )
```

### 环境变量（`.env`）
```
DEEPSEEK_API_KEY=sk-xxxxx
HTTP_PROXY=http://127.0.0.1:7890
```

---

## 2. DeepSeek 模型名称

### 当前有效模型（截至2026-05）
| 模型 ID | 说明 |
|---|---|
| `deepseek-v4-flash` | 快速轻量版，原 `deepseek-chat` 的新名称 |
| `deepseek-v4-pro` | 旗舰版，1.6T参数 |
| `deepseek-chat` | 旧名，2026-07-24 废弃，现指向 v4-flash |

默认使用 `deepseek-v4-flash`，前端 ChatPanel 支持切换。

---

## 3. SSE 流式输出 + Markdown 渲染问题

### 症状
- AI 回复每个字之间有换行，文字极窄
- `**加粗**` 显示为原始星号
- 表格无法渲染

### 根本原因链

**问题1：token 含 `\n` 导致 SSE 拆行**

DeepSeek 流式输出的 token 可能包含 `\n`（如 `**\n`）。`sse-starlette` 按 SSE 规范把含换行的 data 拆成多行：
```
data: **
data:        ← 空行
```
前端收到空 `data:` 行后，原代码 `if (data === '[DONE]') return` 触发 `return`，**截断整个流**。

**解决方案：后端 JSON 序列化 token**
```python
# src/routes/chat.py
import json
yield {"data": json.dumps(token, ensure_ascii=False)}
```
```typescript
// frontend/src/api/client.ts
const raw = line.slice(6).trim()
if (!raw) continue          // 跳过空行，不要 return
if (raw === '[DONE]') return
yield JSON.parse(raw)
```

**问题2：流式拼接时 markdown 语法被破坏**

流式输出时逐 token 追加，`marked` 对不完整的 markdown 解析错误（`** 文字 **` 有空格、`* 列表` 用星号等）。

**解决方案：流式时显示纯文本，流结束后渲染 markdown**
```typescript
// stores/chat.ts - 流式时标记 streaming: true
messages.value[lastIdx].streaming = false  // 流结束后置 false

// ChatPanel.vue - 根据 streaming 状态切换渲染方式
v-html="msg.streaming ? escapeHtml(msg.content) : renderMarkdown(msg.content)"
```

**问题3：单行压缩表格无法渲染**

模型有时把表格压缩成单行：`| A | B | | :--- | :--- | | val | val |`

**解决方案：normalizeMarkdown 预处理**
```typescript
function normalizeMarkdown(content: string): string {
  // 展开压缩表格
  let result = content.replace(/\|\s*\|/g, '|\n|')
  return result
    // 非表格行的单\n替换为空格
    .replace(/([^\n|])\n([^\n|])/g, '$1 $2')
    // * 列表转 - 列表
    .replace(/^(\s*)\* /gm, '$1- ')
    // 修复加粗两侧空格
    .replace(/\*\*\s+/g, '**').replace(/\s+\*\*/g, '**')
}
```

**问题4：`white-space: pre-wrap` 阻止 HTML 渲染**

`.message` 上的 `white-space: pre-wrap` 会让 `v-html` 渲染的 HTML 标签失效。

**解决方案：assistant 消息单独设置 `white-space: normal`**

---

## 4. System Prompt 规范输出格式

在 `SYSTEM_PROMPT_BASE` 中明确要求模型输出格式，避免前端解析问题：

```python
# src/services/ai_service.py
"""
...
5. 输出列表时使用 `-` 作为列表符号，不要使用 `*`
6. 输出表格时，每行必须独立换行，使用标准 Markdown 表格格式，分隔行（`:---`）必须单独占一行
"""
```

---

## 5. 前端宽度问题

### 症状
assistant 消息气泡很窄，只有内容宽度。

### 原因
`.message` 在 flex 容器中，`max-width: 90%` + `align-self: flex-start` 会收缩到内容宽度。

### 解决方案
```css
.message.assistant {
  align-self: stretch;   /* 撑满父容器宽度 */
  white-space: normal;   /* 允许 HTML 渲染 */
}
```
