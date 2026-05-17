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

.attributes-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-md);
  margin-bottom: var(--space-lg);
}

.attr-card {
  background: rgba(15, 25, 35, 0.4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-md);
  transition: all var(--transition-normal);
}

.attr-card:hover {
  border-color: var(--border-glow);
  box-shadow: 0 0 12px rgba(209, 196, 233, 0.06);
}

.attr-card label {
  font-family: var(--font-title);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--accent-primary);
}

.attr-hint {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin: var(--space-xs) 0 var(--space-sm);
}

.attr-card select {
  width: 100%;
  padding: var(--space-sm);
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
  border: none;
  border-bottom: 1px solid var(--border-glow);
  background: rgba(15, 25, 35, 0.5);
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: 1rem;
  outline: none;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23A0A0B8' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 8px center;
  padding-right: 28px;
  transition: all var(--transition-normal);
}

.attr-card select:focus {
  border-bottom-color: var(--accent-primary);
  box-shadow: 0 1px 0 0 var(--accent-primary);
}

.unlocked-info {
  background: var(--info-bg);
  border: 1px solid rgba(129, 212, 250, 0.2);
  border-radius: var(--radius-md);
  padding: var(--space-md);
  margin-bottom: var(--space-lg);
}

.unlocked-info h3 {
  color: var(--info);
  margin-bottom: var(--space-sm);
  font-size: 0.95rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-sm);
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.info-label { font-size: 0.8rem; color: var(--text-muted); }
.info-value { font-size: 1rem; font-weight: 600; color: var(--text-primary); }

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
