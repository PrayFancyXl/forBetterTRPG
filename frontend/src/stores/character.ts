import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { CreationSession, ValidationResult } from '../types/character'
import { api } from '../api/client'

export const useCharacterStore = defineStore('character', () => {
  const session = ref<CreationSession | null>(null)
  const loading = ref(false)

  const currentStep = computed(() => session.value?.current_step ?? 1)
  const character = computed(() => session.value?.character)
  const completedSteps = computed(() => session.value?.completed_steps ?? [])

  async function createSession() {
    loading.value = true
    try {
      session.value = await api.createSession()
    } finally {
      loading.value = false
    }
  }

  function goToStep(step: number) {
    if (!session.value) return
    if (step < 1 || step > 6) return
    session.value.current_step = step
  }

  async function submitStep(step: number, data: any): Promise<ValidationResult> {
    if (!session.value) throw new Error('No session')
    loading.value = true
    try {
      const result = await api.submitStep(session.value.id, step, data)
      session.value = result.session
      return result.validation
    } finally {
      loading.value = false
    }
  }

  return { session, loading, currentStep, character, completedSteps, createSession, goToStep, submitStep }
})
