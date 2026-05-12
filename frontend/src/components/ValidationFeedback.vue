<script setup lang="ts">
import { computed } from 'vue'
import { useCharacterStore } from '../stores/character'

const store = useCharacterStore()

const currentValidation = computed(() => {
  if (!store.session) return null
  return store.session.validation_results[store.currentStep] ?? null
})
</script>

<template>
  <div v-if="currentValidation">
    <div v-if="currentValidation.errors.length" class="feedback errors">
      <div v-for="err in currentValidation.errors" :key="err" class="feedback-item">
        <span class="icon">✗</span> {{ err }}
      </div>
    </div>
    <div v-if="currentValidation.warnings.length" class="feedback warnings">
      <div v-for="warn in currentValidation.warnings" :key="warn" class="feedback-item">
        <span class="icon">⚠</span> {{ warn }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.feedback {
  border-radius: 8px;
  padding: 10px 14px;
  margin-bottom: 12px;
}

.errors {
  background: #3b1111;
  border: 1px solid #ef4444;
}

.warnings {
  background: #3b2f11;
  border: 1px solid #f59e0b;
}

.feedback-item {
  font-size: 0.9rem;
  padding: 2px 0;
}

.errors .icon { color: #ef4444; }
.warnings .icon { color: #f59e0b; }
</style>
