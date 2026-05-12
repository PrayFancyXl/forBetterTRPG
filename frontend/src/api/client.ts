import type { CreationSession, ValidationResult } from '../types/character'

const BASE_URL = '/api'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

export const api = {
  createSession(): Promise<CreationSession> {
    return request('/sessions', { method: 'POST' })
  },

  getSession(id: string): Promise<CreationSession> {
    return request(`/sessions/${id}`)
  },

  submitStep(sessionId: string, step: number, data: any): Promise<{ validation: ValidationResult; session: CreationSession }> {
    return request(`/sessions/${sessionId}/steps/${step}`, {
      method: 'PUT',
      body: JSON.stringify({ data }),
    })
  },

  getKnowledge(type: string, params?: Record<string, string>): Promise<any> {
    const query = params ? '?' + new URLSearchParams(params).toString() : ''
    return request(`/knowledge/${type}${query}`)
  },

  getTip(step: number): Promise<{ tip: string }> {
    return request(`/chat/tip/${step}`)
  },

  async *chatStream(sessionId: string, message: string, step: number): AsyncGenerator<string> {
    const res = await fetch(`${BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, message, step }),
    })
    if (!res.ok) throw new Error(`Chat error: ${res.status}`)
    const reader = res.body!.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          if (data === '[DONE]') return
          yield data
        }
      }
    }
  },
}
