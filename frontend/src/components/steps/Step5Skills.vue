<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useCharacterStore } from '../../stores/character'
import { useChatStore } from '../../stores/chat'

const store = useCharacterStore()
const chatStore = useChatStore()

const SKILL_NAMES: Record<string, string> = {
  athletics: '运动',
  operation: '操作',
  stealth: '隐秘',
  investigation: '调查',
  insight: '洞察',
  persuasion: '说服',
  hunter_lore: '狩魂学识',
}

const SKILL_ATTRS: Record<string, string> = {
  athletics: '体魄',
  operation: '体魄',
  stealth: '智慧',
  investigation: '智慧',
  insight: '心魂',
  persuasion: '心魂',
  hunter_lore: '特殊',
}

const skills = ref<Record<string, number>>({
  athletics: 0,
  operation: 0,
  stealth: 0,
  investigation: 0,
  insight: 0,
  persuasion: 0,
  hunter_lore: 0,
})

const lastValidation = computed(() => {
  if (!store.session) return null
  return store.session.validation_results[4]?.unlocked ?? null
})

const totalBudget = computed(() => lastValidation.value?.skill_points ?? 0)
const totalUsed = computed(() => Object.values(skills.value).reduce((a, b) => a + b, 0))
const remaining = computed(() => totalBudget.value - totalUsed.value)

function increment(key: string) {
  if (skills.value[key] < 5 && remaining.value > 0) {
    skills.value[key]++
  }
}

function decrement(key: string) {
  if (skills.value[key] > 0) {
    skills.value[key]--
  }
}

async function submit() {
  await store.submitStep(5, { skills: skills.value })
  await chatStore.loadTip(6)
}
</script>

<template>
  <div class="step-container">
    <h2>第五步：技能分配</h2>
    <p class="desc">将技能点分配到7项技能中。每项技能最高5点。</p>

    <div class="budget-bar">
      <span>技能点预算：</span>
      <span class="budget-value" :class="{ over: remaining < 0 }">
        {{ totalUsed }} / {{ totalBudget }}
      </span>
      <span class="remaining">（剩余 {{ remaining }} 点）</span>
    </div>

    <div v-if="totalBudget === 0" class="warning-box">
      请先完成第四步（属性分配）以获得技能点预算
    </div>

    <div class="skills-list">
      <div v-for="(label, key) in SKILL_NAMES" :key="key" class="skill-row">
        <div class="skill-info">
          <span class="skill-name">{{ label }}</span>
          <span class="skill-attr">{{ SKILL_ATTRS[key] }}</span>
        </div>
        <div class="skill-control">
          <button class="ctrl-btn" @click="decrement(key)" :disabled="skills[key] <= 0">-</button>
          <span class="skill-value">{{ skills[key] }}</span>
          <button class="ctrl-btn" @click="increment(key)" :disabled="skills[key] >= 5 || remaining <= 0">+</button>
          <div class="skill-bar">
            <div class="skill-fill" :style="{ width: (skills[key] / 5 * 100) + '%' }"></div>
          </div>
        </div>
      </div>
    </div>

    <button class="submit-btn" @click="submit" :disabled="store.loading || remaining < 0">
      {{ store.loading ? '提交中...' : '确认技能分配' }}
    </button>
  </div>
</template>

<style scoped>
.step-container { max-width: 650px; }
h2 { color: #a855f7; margin-bottom: 8px; }
.desc { color: #999; margin-bottom: 16px; font-size: 0.9rem; }

.budget-bar {
  background: #1a1a2e;
  border: 1px solid #2a2a4a;
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 16px;
  font-size: 0.95rem;
}

.budget-value { font-weight: bold; color: #a855f7; }
.budget-value.over { color: #ef4444; }
.remaining { color: #888; font-size: 0.85rem; margin-left: 8px; }

.warning-box {
  background: #3b2f11;
  border: 1px solid #f59e0b;
  border-radius: 8px;
  padding: 10px 14px;
  margin-bottom: 16px;
  color: #fbbf24;
  font-size: 0.9rem;
}

.skills-list { display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px; }

.skill-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #1a1a2e;
  border: 1px solid #2a2a4a;
  border-radius: 8px;
  padding: 12px 16px;
}

.skill-info { display: flex; flex-direction: column; min-width: 80px; }
.skill-name { font-weight: bold; font-size: 0.95rem; }
.skill-attr { font-size: 0.75rem; color: #888; }

.skill-control { display: flex; align-items: center; gap: 10px; }

.ctrl-btn {
  width: 28px; height: 28px; border-radius: 50%;
  border: 1px solid #2a2a4a; background: #16213e;
  color: #e0e0e0; font-size: 1.1rem; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
}
.ctrl-btn:hover:not(:disabled) { border-color: #a855f7; color: #a855f7; }
.ctrl-btn:disabled { opacity: 0.3; cursor: not-allowed; }

.skill-value { font-size: 1.1rem; font-weight: bold; width: 20px; text-align: center; }

.skill-bar {
  width: 80px; height: 6px; background: #2a2a4a; border-radius: 3px; overflow: hidden;
}
.skill-fill {
  height: 100%; background: #a855f7; border-radius: 3px; transition: width 0.2s;
}

.submit-btn {
  padding: 12px 32px; border-radius: 8px; border: none;
  background: #a855f7; color: white; font-size: 1rem; cursor: pointer;
}
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
