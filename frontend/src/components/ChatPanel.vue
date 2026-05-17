<script setup lang="ts">
import { ref } from 'vue'
import { marked } from 'marked'
import { useCharacterStore } from '../stores/character'
import { useChatStore } from '../stores/chat'

const store = useCharacterStore()
const chatStore = useChatStore()
const input = ref('')

const MODELS = [
  { value: 'deepseek-v4-flash', label: 'V4 Flash（快速）' },
  { value: 'deepseek-v4-pro', label: 'V4 Pro（旗舰）' },
]

marked.setOptions({ breaks: false })

const renderer = new marked.Renderer()
marked.use({ renderer, gfm: true, breaks: false })

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>')
}

function normalizeMarkdown(content: string): string {
  // 先把单行压缩表格展开：| cell | | cell | → | cell |\n| cell |
  let result = content.replace(/\|\s*\|/g, '|\n|')

  return result
    // 把非表格行的单个\n替换为空格，保留\n\n和表格行的\n
    .replace(/([^\n|])\n([^\n|])/g, '$1 $2')
    // 行首 * 列表符转为 -
    .replace(/^(\s*)\* /gm, '$1- ')
    // 修复 ** 加粗两侧多余空格
    .replace(/\*\*\s+/g, '**')
    .replace(/\s+\*\*/g, '**')
    // 修复有序列表序号：1 . → 1.
    .replace(/(\d+)\s+\.\s+/g, '$1. ')
}

function renderMarkdown(content: string): string {
  return marked.parse(normalizeMarkdown(content)) as string
}

async function send() {
  if (!input.value.trim() || !store.session) return
  const msg = input.value.trim()
  input.value = ''
  await chatStore.sendMessage(store.session.id, msg, store.currentStep)
}
</script>

<template>
  <div class="chat-panel">
    <div class="chat-header">
      <span>AI 建卡助手</span>
      <select v-model="chatStore.selectedModel" class="model-select" :disabled="chatStore.streaming">
        <option v-for="m in MODELS" :key="m.value" :value="m.value">{{ m.label }}</option>
      </select>
    </div>
    <div class="chat-messages">
      <div
        v-for="(msg, i) in chatStore.messages"
        :key="i"
        class="message"
        :class="msg.role"
      >
        <div
          v-if="msg.role === 'assistant'"
          class="message-content"
          :class="{ 'markdown-body': !msg.streaming, 'streaming-text': msg.streaming }"
          v-html="msg.streaming ? escapeHtml(msg.content) : renderMarkdown(msg.content)"
        />
        <div v-else class="message-content">{{ msg.content }}</div>
      </div>
      <div v-if="chatStore.messages.length === 0" class="empty-hint">
        有任何关于建卡的问题，都可以在这里提问
      </div>
    </div>
    <div class="chat-input">
      <input
        v-model="input"
        @keyup.enter="send"
        placeholder="输入问题..."
        :disabled="chatStore.streaming"
      />
      <button @click="send" :disabled="chatStore.streaming || !input.trim()">发送</button>
    </div>
  </div>
</template>

<style scoped>
.chat-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  padding: var(--space-md);
  font-family: var(--font-title);
  font-weight: 700;
  border-bottom: 1px solid var(--border-subtle);
  color: var(--accent-primary);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.model-select {
  font-family: var(--font-body);
  font-size: 0.75rem;
  padding: 3px 6px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-glow);
  background: rgba(15, 25, 35, 0.5);
  color: var(--text-secondary);
  cursor: pointer;
  outline: none;
  transition: all var(--transition-normal);
}

.model-select:focus { border-color: var(--accent-muted); }
.model-select:disabled { opacity: 0.4; }

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-sm);
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.message {
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  line-height: 1.5;
}

.message.user {
  align-self: flex-end;
  max-width: 85%;
  background: rgba(209, 196, 233, 0.12);
  border: 1px solid var(--border-glow);
  color: var(--accent-primary);
  white-space: pre-wrap;
  word-break: break-word;
}

.message.assistant {
  align-self: stretch;
  background: rgba(15, 25, 35, 0.4);
  border: 1px solid var(--border-subtle);
  color: var(--text-primary);
  word-break: break-word;
  overflow-wrap: break-word;
}

.markdown-body {
  line-height: 1.6;
  font-size: 0.85rem;
}

.streaming-text {
  line-height: 1.6;
  font-size: 0.85rem;
  white-space: pre-wrap;
  word-break: break-word;
}

.markdown-body :deep(p) {
  margin: 0 0 8px;
}

.markdown-body :deep(p:last-child) {
  margin-bottom: 0;
}

.markdown-body :deep(strong) {
  color: var(--accent-bright);
  font-weight: 600;
}

.markdown-body :deep(em) {
  color: var(--info);
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  color: var(--accent-primary);
  margin: 10px 0 6px;
  font-size: 1em;
  font-family: var(--font-title);
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 18px;
  margin: 4px 0 8px;
}

.markdown-body :deep(li) {
  margin-bottom: 3px;
}

.markdown-body :deep(code) {
  background: rgba(15, 25, 35, 0.6);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 1px 5px;
  font-size: 0.85em;
  font-family: var(--font-mono);
  color: var(--accent-bright);
}

.markdown-body :deep(pre) {
  background: rgba(15, 25, 35, 0.6);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-sm) var(--space-md);
  overflow-x: auto;
  margin: 6px 0;
}

.markdown-body :deep(pre code) {
  background: none;
  border: none;
  padding: 0;
  color: var(--text-primary);
}

.markdown-body :deep(blockquote) {
  border-left: 3px solid var(--accent-muted);
  margin: 6px 0;
  padding-left: 10px;
  color: var(--text-secondary);
}

.markdown-body :deep(hr) {
  border: none;
  border-top: 1px solid var(--border-subtle);
  margin: 8px 0;
}

.markdown-body :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 8px 0;
  font-size: 0.8rem;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid var(--border-subtle);
  padding: 6px 10px;
  text-align: left;
}

.markdown-body :deep(th) {
  background: rgba(15, 25, 35, 0.6);
  color: var(--accent-primary);
  font-weight: 600;
}

.markdown-body :deep(tr:nth-child(even)) {
  background: rgba(15, 25, 35, 0.3);
}

.empty-hint {
  text-align: center;
  color: var(--text-muted);
  margin-top: 40px;
  font-size: 0.85rem;
}

.chat-input {
  display: flex;
  gap: var(--space-sm);
  padding: var(--space-sm);
  border-top: 1px solid var(--border-subtle);
}

.chat-input input {
  flex: 1;
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-glow);
  background: rgba(15, 25, 35, 0.5);
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: 0.85rem;
  outline: none;
  transition: all var(--transition-normal);
}

.chat-input input::placeholder { color: var(--text-muted); }
.chat-input input:focus {
  border-color: var(--accent-muted);
  box-shadow: 0 0 8px rgba(209, 196, 233, 0.08);
}

.chat-input button {
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-glow);
  background: transparent;
  color: var(--accent-primary);
  font-family: var(--font-body);
  font-size: 0.85rem;
  cursor: pointer;
  transition: all var(--transition-normal);
}

.chat-input button:hover {
  background: rgba(209, 196, 233, 0.08);
  border-color: var(--accent-muted);
}

.chat-input button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
