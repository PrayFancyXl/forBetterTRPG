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
  border-radius: var(--radius-md);
  padding: var(--space-sm) var(--space-md);
  margin-bottom: var(--space-sm);
}

.errors {
  background: var(--error-bg);
  border: 1px solid rgba(229, 115, 115, 0.2);
}

.warnings {
  background: var(--warning-bg);
  border: 1px solid rgba(255, 183, 77, 0.2);
}

.feedback-item {
  font-size: 0.85rem;
  padding: 2px 0;
  color: var(--text-primary);
}

.errors .icon { color: var(--error); }
.warnings .icon { color: var(--warning); }
</style>
