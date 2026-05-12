import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '../api/client'

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  streaming?: boolean
}

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([])
  const streaming = ref(false)
  const tip = ref('')
  const selectedModel = ref('deepseek-v4-flash')

  async function sendMessage(sessionId: string, message: string, step: number) {
    messages.value.push({ role: 'user', content: message })
    messages.value.push({ role: 'assistant', content: '', streaming: true })
    streaming.value = true

    try {
      const lastIdx = messages.value.length - 1
      for await (const token of api.chatStream(sessionId, message, step, selectedModel.value)) {
        messages.value[lastIdx].content += token
      }
      messages.value[lastIdx].streaming = false
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

  return { messages, streaming, tip, selectedModel, sendMessage, loadTip, clearMessages }
})
