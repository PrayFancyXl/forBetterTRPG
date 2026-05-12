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
h2 { color: #a855f7; margin-bottom: 8px; }
.desc { color: #999; margin-bottom: 20px; font-size: 0.9rem; }
.bond-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 16px; }
.bond-card {
  padding: 12px; text-align: center; border-radius: 8px;
  border: 1px solid #2a2a4a; background: #1a1a2e; cursor: pointer; transition: all 0.2s;
}
.bond-card:hover { border-color: #a855f7; }
.bond-card.selected { background: #a855f7; color: white; border-color: #a855f7; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 6px; font-size: 0.9rem; color: #ccc; }
.form-group input {
  width: 100%; padding: 10px 12px; border-radius: 8px;
  border: 1px solid #2a2a4a; background: #1a1a2e; color: #e0e0e0; outline: none;
}
.form-group input:focus { border-color: #a855f7; }
.submit-btn {
  padding: 12px 32px; border-radius: 8px; border: none;
  background: #a855f7; color: white; font-size: 1rem; cursor: pointer;
}
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
