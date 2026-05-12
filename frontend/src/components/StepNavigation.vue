<script setup lang="ts">
defineProps<{
  currentStep: number
  completedSteps: number[]
}>()

const steps = [
  { num: 1, label: '灵能力' },
  { num: 2, label: '羁绊' },
  { num: 3, label: '角色信息' },
  { num: 4, label: '属性' },
  { num: 5, label: '技能' },
  { num: 6, label: '能力选择' },
]
</script>

<template>
  <nav class="step-nav">
    <div
      v-for="step in steps"
      :key="step.num"
      class="step-item"
      :class="{
        active: currentStep === step.num,
        completed: completedSteps.includes(step.num),
      }"
    >
      <div class="step-circle">{{ step.num }}</div>
      <span class="step-label">{{ step.label }}</span>
    </div>
  </nav>
</template>

<style scoped>
.step-nav {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 20px;
  background: #2a2a4a;
  transition: all 0.2s;
}

.step-item.active {
  background: #a855f7;
  color: white;
}

.step-item.completed {
  background: #065f46;
  color: #6ee7b7;
}

.step-circle {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: bold;
  background: rgba(255, 255, 255, 0.1);
}

.step-label {
  font-size: 0.85rem;
}
</style>
