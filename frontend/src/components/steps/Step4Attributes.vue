<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useCharacterStore } from '../../stores/character'
import { useChatStore } from '../../stores/chat'

const store = useCharacterStore()
const chatStore = useChatStore()

const levels = ['E', 'D', 'C', 'B', 'A', 'S', 'SS', 'SSS', 'SSS+']
const physique = ref(store.character?.attributes.physique || 'E')
const wisdom = ref(store.character?.attributes.wisdom || 'E')
const spirit = ref(store.character?.attributes.spirit || 'E')

const lastValidation = ref<any>(null)

async function submit() {
  const result = await store.submitStep(4, {
    physique: physique.value,
    wisdom: wisdom.value,
    spirit: spirit.value,
  })
  lastValidation.value = result
  await chatStore.loadTip(5)
}

const unlocked = computed(() => lastValidation.value?.unlocked ?? null)
</script>

<template>
  <div class="step-container">
    <h2>第四步：属性分配</h2>
    <p class="desc">为你的狩魂者分配三大基础属性等级。属性等级决定了战斗强度和可学习的技能数量。</p>

    <div class="attributes-grid">
      <div class="attr-card">
        <label>体魄</label>
        <p class="attr-hint">影响：武技强度、生命值、可学武技数量</p>
        <select v-model="physique">
          <option v-for="l in levels" :key="l" :value="l">{{ l }}</option>
        </select>
      </div>

      <div class="attr-card">
        <label>智慧</label>
        <p class="attr-hint">影响：术法强度、技能点、可学术法数量</p>
        <select v-model="wisdom">
          <option v-for="l in levels" :key="l" :value="l">{{ l }}</option>
        </select>
      </div>

      <div class="attr-card">
        <label>心魂</label>
        <p class="attr-hint">影响：灵能力强度、灵能印记数量</p>
        <select v-model="spirit">
          <option v-for="l in levels" :key="l" :value="l">{{ l }}</option>
        </select>
      </div>
    </div>

    <div v-if="unlocked" class="unlocked-info">
      <h3>解锁信息</h3>
      <div class="info-grid">
        <div class="info-item">
          <span class="info-label">可学武技</span>
          <span class="info-value">{{ unlocked.martial_arts_count }} 个</span>
        </div>
        <div class="info-item">
          <span class="info-label">秘传武技</span>
          <span class="info-value">{{ unlocked.can_learn_secret_martial ? '已解锁' : '未解锁' }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">可学术法</span>
          <span class="info-value">{{ unlocked.spell_count }} 个</span>
        </div>
        <div class="info-item">
          <span class="info-label">秘传术法</span>
          <span class="info-value">{{ unlocked.can_learn_secret_spells ? '已解锁' : '未解锁' }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">技能点</span>
          <span class="info-value">{{ unlocked.skill_points }} 点</span>
        </div>
        <div class="info-item">
          <span class="info-label">灵能印记</span>
          <span class="info-value">{{ unlocked.spirit_mark_count }} 个</span>
        </div>
      </div>
    </div>

    <button class="submit-btn" @click="submit" :disabled="store.loading">
      {{ store.loading ? '提交中...' : '确认属性' }}
    </button>
  </div>
</template>

<style scoped>
.step-container { max-width: 700px; }

h2 { color: #a855f7; margin-bottom: 8px; }

.desc { color: #999; margin-bottom: 20px; font-size: 0.9rem; }

.attributes-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.attr-card {
  background: #1a1a2e;
  border: 1px solid #2a2a4a;
  border-radius: 10px;
  padding: 16px;
}

.attr-card label {
  font-size: 1.1rem;
  font-weight: bold;
  color: #a855f7;
}

.attr-hint {
  font-size: 0.75rem;
  color: #888;
  margin: 6px 0 10px;
}

.attr-card select {
  width: 100%;
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #2a2a4a;
  background: #16213e;
  color: #e0e0e0;
  font-size: 1rem;
}

.unlocked-info {
  background: #0f3460;
  border: 1px solid #3b82f6;
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 20px;
}

.unlocked-info h3 {
  color: #93c5fd;
  margin-bottom: 12px;
  font-size: 0.95rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.info-label { font-size: 0.8rem; color: #888; }
.info-value { font-size: 1rem; font-weight: bold; color: #e0e0e0; }

.submit-btn {
  padding: 12px 32px;
  border-radius: 8px;
  border: none;
  background: #a855f7;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.2s;
}

.submit-btn:hover { opacity: 0.9; }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
