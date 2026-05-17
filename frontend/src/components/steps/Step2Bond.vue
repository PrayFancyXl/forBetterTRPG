<script setup lang="ts">
import { ref } from 'vue'
import { useCharacterStore } from '../../stores/character'
import { useChatStore } from '../../stores/chat'

const store = useCharacterStore()
const chatStore = useChatStore()
const bond = ref('')

const bonds = [
  '复仇', '守护', '探索', '救赎', '荣耀', '自由', '责任', '好奇'
]

async function submit() {
  await store.submitStep(2, { bond: bond.value })
  await chatStore.loadTip(3)
}
</script>

<template>
  <div class="step-container">
    <h2>第二步：选择狩魂者羁绊</h2>
    <p class="desc">狩魂者羁绊是促使你加入狩魂活动的基本动机。</p>

    <div class="bond-grid">
      <div
        v-for="b in bonds" :key="b"
        class="bond-card"
        :class="{ selected: bond === b }"
        @click="bond = b"
      >
        {{ b }}
      </div>
    </div>

    <div class="form-group">
      <label>或自定义羁绊</label>
      <input v-model="bond" placeholder="输入自定义羁绊..." />
    </div>

    <button class="submit-btn" @click="submit" :disabled="store.loading || !bond">
      {{ store.loading ? '提交中...' : '确认羁绊' }}
    </button>
  </div>
</template>

<style scoped>
.step-container { max-width: 600px; }
h2 {
  font-family: var(--font-title);
  color: var(--accent-primary);
  margin-bottom: var(--space-sm);
}
.desc {
  color: var(--text-secondary);
  margin-bottom: var(--space-lg);
  font-size: 0.9rem;
}
.bond-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-sm);
  margin-bottom: var(--space-md);
}
.bond-card {
  padding: var(--space-md);
  text-align: center;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
  background: rgba(15, 25, 35, 0.4);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-normal);
}
.bond-card:hover {
  border-color: var(--border-glow);
  color: var(--text-primary);
  box-shadow: 0 0 12px rgba(209, 196, 233, 0.06);
  transform: translateY(-1px);
}
.bond-card.selected {
  border-color: var(--accent-muted);
  background: rgba(209, 196, 233, 0.08);
  color: var(--accent-primary);
  box-shadow: var(--shadow-glow-active);
}
.form-group { margin-bottom: var(--space-md); }
.form-group label {
  display: block;
  margin-bottom: var(--space-xs);
  font-size: 0.85rem;
  color: var(--text-secondary);
}
.form-group input {
  width: 100%;
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
  border: none;
  border-bottom: 1px solid var(--border-glow);
  background: rgba(15, 25, 35, 0.5);
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: 0.9rem;
  outline: none;
  transition: all var(--transition-normal);
}
.form-group input::placeholder { color: var(--text-muted); }
.form-group input:focus {
  border-bottom-color: var(--accent-primary);
  box-shadow: 0 1px 0 0 var(--accent-primary);
}
.submit-btn {
  padding: var(--space-sm) var(--space-xl);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-glow);
  background: transparent;
  color: var(--accent-primary);
  font-family: var(--font-body);
  font-size: 0.9rem;
  cursor: pointer;
  box-shadow: var(--shadow-glow);
  transition: all var(--transition-normal);
}
.submit-btn:hover {
  background: rgba(209, 196, 233, 0.08);
  border-color: var(--accent-muted);
  box-shadow: var(--shadow-glow-active);
}
.submit-btn:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
