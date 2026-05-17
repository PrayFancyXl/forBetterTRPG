<script setup lang="ts">
import { useCharacterStore } from '../stores/character'

defineProps<{
  currentStep: number
  completedSteps: number[]
}>()

const store = useCharacterStore()

const steps = [
  { num: 1, label: '灵能力' },
  { num: 2, label: '羁绊' },
  { num: 3, label: '角色信息' },
  { num: 4, label: '属性' },
  { num: 5, label: '技能' },
  { num: 6, label: '能力选择' },
]

function navigate(step: number) {
  store.goToStep(step)
}
</script>

<template>
  <nav class="step-nav">
    <button
      v-for="step in steps"
      :key="step.num"
      class="step-tab"
      :class="{
        active: currentStep === step.num,
        completed: completedSteps.includes(step.num),
      }"
      @click="navigate(step.num)"
    >
      <span class="step-indicator">
        <svg v-if="completedSteps.includes(step.num)" width="12" height="12" viewBox="0 0 12 12" fill="none">
          <path d="M2 6l3 3 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span v-else>{{ step.num }}</span>
      </span>
      <span class="step-label">{{ step.label }}</span>
      <span class="step-glow" v-if="currentStep === step.num"></span>
    </button>
  </nav>
</template>

<style scoped>
.step-nav {
  display: flex;
  justify-content: center;
  gap: 2px;
  background: rgba(15, 25, 35, 0.4);
  border-radius: var(--radius-lg);
  padding: var(--space-xs);
  border: 1px solid var(--border-subtle);
}

.step-tab {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  border: none;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-muted);
  font-family: var(--font-body);
  font-size: 0.85rem;
  cursor: pointer;
  transition: all var(--transition-normal);
  overflow: hidden;
}

.step-tab:hover {
  color: var(--text-secondary);
  background: rgba(209, 196, 233, 0.03);
}

.step-tab.active {
  color: var(--accent-primary);
  background: rgba(209, 196, 233, 0.08);
}

.step-tab.completed:not(.active) {
  color: var(--success);
}

.step-indicator {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 600;
  background: rgba(209, 196, 233, 0.06);
  flex-shrink: 0;
  transition: all var(--transition-normal);
}

.step-tab.active .step-indicator {
  background: rgba(209, 196, 233, 0.15);
  color: var(--accent-primary);
}

.step-tab.completed .step-indicator {
  background: var(--success-bg);
  color: var(--success);
}

.step-label {
  white-space: nowrap;
}

.step-glow {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
  border-radius: 1px;
}

@media (max-width: 700px) {
  .step-nav {
    overflow-x: auto;
    justify-content: flex-start;
  }
  .step-label {
    display: none;
  }
  .step-tab {
    padding: var(--space-sm);
  }
}
</style>
