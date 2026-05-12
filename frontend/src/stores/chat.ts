import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '../api/client'

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([])
  const streaming = ref(false)
  const tip = ref('')

  async function sendMessage(sessionId: string, message: string, step: number) {
    messages.value.push({ role: 'user', content: message })
    messages.value.push({ role: 'assistant', content: '' })
    streaming.value = true

    try {
      const lastIdx = messages.value.length - 1
      for await (const token of api.chatStream(sessionId, message, step)) {
        messages.value[lastIdx].content += token
      }
    } finally {
      streaming.value = false
    }
  }

  async function loadTip(step: number) {
    const result = await api.getTip(step)
    tip.value = result.tip
  }

  function clearMessages() {
    messages.value = []
  }

  return { messages, streaming, tip, sendMessage, loadTip, clearMessages }
})
