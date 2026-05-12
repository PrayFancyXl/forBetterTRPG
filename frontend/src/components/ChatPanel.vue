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
  padding: 14px;
  font-weight: bold;
  border-bottom: 1px solid #2a2a4a;
  color: #a855f7;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.model-select {
  font-size: 0.8rem;
  padding: 3px 6px;
  border-radius: 6px;
  border: 1px solid #2a2a4a;
  background: #1a1a2e;
  color: #e0e0e0;
  cursor: pointer;
  outline: none;
}

.model-select:disabled {
  opacity: 0.5;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message {
  padding: 8px 12px;
  border-radius: 10px;
  font-size: 0.9rem;
  line-height: 1.5;
}

.message.user {
  align-self: flex-end;
  max-width: 85%;
  background: #a855f7;
  color: white;
  white-space: pre-wrap;
  word-break: break-word;
}

.message.assistant {
  align-self: stretch;
  background: #2a2a4a;
  color: #e0e0e0;
  word-break: break-word;
  overflow-wrap: break-word;
}

.markdown-body {
  line-height: 1.6;
  font-size: 0.9rem;
}

.streaming-text {
  line-height: 1.6;
  font-size: 0.9rem;
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
  color: #c084fc;
  font-weight: 600;
}

.markdown-body :deep(em) {
  color: #a5b4fc;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  color: #a855f7;
  margin: 10px 0 6px;
  font-size: 1em;
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
  background: #1a1a2e;
  border: 1px solid #3a3a5a;
  border-radius: 4px;
  padding: 1px 5px;
  font-size: 0.85em;
  color: #c084fc;
}

.markdown-body :deep(pre) {
  background: #1a1a2e;
  border: 1px solid #3a3a5a;
  border-radius: 6px;
  padding: 10px 12px;
  overflow-x: auto;
  margin: 6px 0;
}

.markdown-body :deep(pre code) {
  background: none;
  border: none;
  padding: 0;
  color: #e0e0e0;
}

.markdown-body :deep(blockquote) {
  border-left: 3px solid #a855f7;
  margin: 6px 0;
  padding-left: 10px;
  color: #aaa;
}

.markdown-body :deep(hr) {
  border: none;
  border-top: 1px solid #3a3a5a;
  margin: 8px 0;
}

.markdown-body :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 8px 0;
  font-size: 0.85rem;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid #3a3a5a;
  padding: 6px 10px;
  text-align: left;
}

.markdown-body :deep(th) {
  background: #1a1a2e;
  color: #a855f7;
  font-weight: 600;
}

.markdown-body :deep(tr:nth-child(even)) {
  background: #1e1e3a;
}

.empty-hint {
  text-align: center;
  color: #666;
  margin-top: 40px;
  font-size: 0.9rem;
}

.chat-input {
  display: flex;
  gap: 8px;
  padding: 12px;
  border-top: 1px solid #2a2a4a;
}

.chat-input input {
  flex: 1;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #2a2a4a;
  background: #1a1a2e;
  color: #e0e0e0;
  outline: none;
}

.chat-input input:focus {
  border-color: #a855f7;
}

.chat-input button {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  background: #a855f7;
  color: white;
  cursor: pointer;
}

.chat-input button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
