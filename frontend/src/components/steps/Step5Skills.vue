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
h2 {
  font-family: var(--font-title);
  color: var(--accent-primary);
  margin-bottom: var(--space-sm);
}
.desc {
  color: var(--text-secondary);
  margin-bottom: var(--space-md);
  font-size: 0.9rem;
}

.budget-bar {
  background: rgba(15, 25, 35, 0.4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-sm) var(--space-md);
  margin-bottom: var(--space-md);
  font-size: 0.9rem;
}

.budget-value { font-weight: 600; color: var(--accent-primary); }
.budget-value.over { color: var(--error); }
.remaining { color: var(--text-muted); font-size: 0.85rem; margin-left: var(--space-sm); }

.warning-box {
  background: var(--warning-bg);
  border: 1px solid rgba(255, 183, 77, 0.2);
  border-radius: var(--radius-md);
  padding: var(--space-sm) var(--space-md);
  margin-bottom: var(--space-md);
  color: var(--warning);
  font-size: 0.9rem;
}

.skills-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  margin-bottom: var(--space-lg);
}

.skill-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(15, 25, 35, 0.4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-sm) var(--space-md);
  transition: all var(--transition-normal);
}

.skill-row:hover {
  border-color: var(--border-glow);
}

.skill-info { display: flex; flex-direction: column; min-width: 80px; }
.skill-name { font-weight: 500; font-size: 0.9rem; color: var(--text-primary); }
.skill-attr { font-size: 0.75rem; color: var(--text-muted); }

.skill-control { display: flex; align-items: center; gap: var(--space-sm); }

.ctrl-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1px solid var(--border-glow);
  background: transparent;
  color: var(--text-secondary);
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}
.ctrl-btn:hover:not(:disabled) {
  border-color: var(--accent-muted);
  color: var(--accent-primary);
  box-shadow: 0 0 8px rgba(209, 196, 233, 0.1);
}
.ctrl-btn:disabled { opacity: 0.3; cursor: not-allowed; }

.skill-value {
  font-size: 1.1rem;
  font-weight: 600;
  width: 20px;
  text-align: center;
  color: var(--text-primary);
}

.skill-bar {
  width: 80px;
  height: 4px;
  background: rgba(209, 196, 233, 0.08);
  border-radius: 2px;
  overflow: hidden;
}
.skill-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent-secondary), var(--accent-bright));
  border-radius: 2px;
  transition: width var(--transition-normal);
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
