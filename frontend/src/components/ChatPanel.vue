<script setup lang="ts">
import { ref } from 'vue'
import { useCharacterStore } from '../stores/character'
import { useChatStore } from '../stores/chat'

const store = useCharacterStore()
const chatStore = useChatStore()
const input = ref('')

async function send() {
  if (!input.value.trim() || !store.session) return
  const msg = input.value.trim()
  input.value = ''
  await chatStore.sendMessage(store.session.id, msg, store.currentStep)
}
</script>

<template>
  <div class="chat-panel">
    <div class="chat-header">AI 建卡助手</div>
    <div class="chat-messages">
      <div
        v-for="(msg, i) in chatStore.messages"
        :key="i"
        class="message"
        :class="msg.role"
      >
        <div class="message-content">{{ msg.content }}</div>
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
  max-width: 90%;
  padding: 8px 12px;
  border-radius: 10px;
  font-size: 0.9rem;
  line-height: 1.5;
  white-space: pre-wrap;
}

.message.user {
  align-self: flex-end;
  background: #a855f7;
  color: white;
}

.message.assistant {
  align-self: flex-start;
  background: #2a2a4a;
  color: #e0e0e0;
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
