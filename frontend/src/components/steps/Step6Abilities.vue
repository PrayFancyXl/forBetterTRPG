<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useCharacterStore } from '../../stores/character'
import { useChatStore } from '../../stores/chat'
import { api } from '../../api/client'

const store = useCharacterStore()
const chatStore = useChatStore()

const activeTab = ref('martial_arts')
const tabs = [
  { key: 'martial_arts', label: '武技' },
  { key: 'spells', label: '术法' },
  { key: 'feats', label: '专长' },
  { key: 'spirit_marks', label: '灵能印记' },
  { key: 'ultimates', label: '绝技' },
  { key: 'stylish_moves', label: '时髦动作' },
]

const martialArts = ref<any[]>([])
const spells = ref<any[]>([])
const feats = ref<any[]>([])
const spiritMarks = ref<any[]>([])
const ultimates = ref<any[]>([])
const stylishMoves = ref<any>({})

const selectedMartialArts = ref<string[]>([])
const selectedSpells = ref<string[]>([])
const selectedFeats = ref<string[]>([])
const selectedMarks = ref<string[]>([])
const selectedUltimates = ref<string[]>([])
const selectedStyle = ref('')

const unlocked = computed(() => {
  if (!store.session) return null
  return store.session.validation_results[4]?.unlocked ?? null
})

const maxMartial = computed(() => unlocked.value?.martial_arts_count ?? 0)
const canSecret = computed(() => unlocked.value?.can_learn_secret_martial ?? false)
const maxSpells = computed(() => unlocked.value?.spell_count ?? 0)
const canSecretSpells = computed(() => unlocked.value?.can_learn_secret_spells ?? false)
const maxMarks = computed(() => unlocked.value?.spirit_mark_count ?? 0)

onMounted(async () => {
  try {
    martialArts.value = await api.getKnowledge('martial-arts', { secret: String(canSecret.value) })
    spells.value = await api.getKnowledge('spells', { secret: String(canSecretSpells.value) })
    feats.value = await api.getKnowledge('feats')
    spiritMarks.value = await api.getKnowledge('spirit-marks')
    ultimates.value = await api.getKnowledge('ultimates')
    stylishMoves.value = await api.getKnowledge('stylish-moves')
  } catch (e) {
    console.error('Failed to load knowledge:', e)
  }
})

function toggleSelection(list: string[], item: string, max: number) {
  const idx = list.indexOf(item)
  if (idx >= 0) {
    list.splice(idx, 1)
  } else if (list.length < max) {
    list.push(item)
  }
}

async function submit() {
  const data: any = {
    martial_arts: selectedMartialArts.value.map(name => {
      const art = martialArts.value.find(a => a.name === name)
      return art ? { name: art.name, cost: art.cost, target: art.target, assist: art.assist, secret: art.secret, effect: art.effect, flavor: art.flavor } : { name }
    }),
    spells: selectedSpells.value.map(name => {
      const spell = spells.value.find(s => s.name === name)
      return spell ? { name: spell.name, cost: spell.cost, target: spell.target, category: spell.category, secret: spell.secret, spell_type: spell.type, effect: spell.effect, flavor: spell.flavor } : { name }
    }),
    feats: selectedFeats.value.map(name => {
      const feat = feats.value.find(f => f.name === name)
      return feat ? { name: feat.name, description: feat.description } : { name }
    }),
    spirit_marks: selectedMarks.value.map(t => ({ mark_type: t, corresponding_soul: '' })),
  }
  if (selectedUltimates.value.length > 0) {
    data.ultimates = selectedUltimates.value.map(name => {
      const ult = ultimates.value.find(u => u.name === name)
      return ult ? { name: ult.name, soul: ult.soul, domain: ult.domain, effect: ult.effect, description: ult.description, tier: ult.tier } : { name }
    })
  }
  if (selectedStyle.value && stylishMoves.value[selectedStyle.value]) {
    data.stylish_moves = stylishMoves.value[selectedStyle.value].map((m: any) => ({
      style: selectedStyle.value, cost: m.cost, action: m.action,
    }))
  }
  await store.submitStep(6, data)
}
</script>

<template>
  <div class="step-container">
    <h2>第六步：能力选择</h2>
    <p class="desc">根据属性等级选择武技、术法、专长等能力。</p>

    <div v-if="!unlocked" class="warning-box">
      请先完成第四步（属性分配）以确定可选能力数量
    </div>

    <div v-else>
      <div class="tab-bar">
        <button
          v-for="tab in tabs" :key="tab.key"
          class="tab-btn" :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key"
        >{{ tab.label }}</button>
      </div>

      <!-- 武技 -->
      <div v-if="activeTab === 'martial_arts'" class="tab-content">
        <p class="limit-info">已选 {{ selectedMartialArts.length }} / {{ maxMartial }} 个武技</p>
        <div class="card-grid">
          <div
            v-for="art in martialArts" :key="art.name"
            class="ability-card" :class="{ selected: selectedMartialArts.includes(art.name), secret: art.secret }"
            @click="toggleSelection(selectedMartialArts, art.name, maxMartial)"
          >
            <div class="card-header">
              <span class="card-name">{{ art.name }}</span>
              <span v-if="art.secret" class="secret-badge">秘传</span>
            </div>
            <div class="card-cost">{{ art.cost }}</div>
            <div class="card-effect">{{ art.effect }}</div>
          </div>
        </div>
      </div>

      <!-- 术法 -->
      <div v-if="activeTab === 'spells'" class="tab-content">
        <p class="limit-info">已选 {{ selectedSpells.length }} / {{ maxSpells }} 个术法</p>
        <div class="card-grid">
          <div
            v-for="spell in spells" :key="spell.name"
            class="ability-card" :class="{ selected: selectedSpells.includes(spell.name), secret: spell.secret }"
            @click="toggleSelection(selectedSpells, spell.name, maxSpells)"
          >
            <div class="card-header">
              <span class="card-name">{{ spell.name }}</span>
              <span v-if="spell.secret" class="secret-badge">秘传</span>
              <span class="card-category">{{ spell.category }}</span>
            </div>
            <div class="card-cost">{{ spell.cost }}</div>
            <div class="card-effect">{{ spell.effect }}</div>
          </div>
        </div>
      </div>

      <!-- 专长 -->
      <div v-if="activeTab === 'feats'" class="tab-content">
        <p class="limit-info">已选 {{ selectedFeats.length }} / 2 个专长</p>
        <div class="card-grid">
          <div
            v-for="feat in feats" :key="feat.name"
            class="ability-card" :class="{ selected: selectedFeats.includes(feat.name) }"
            @click="toggleSelection(selectedFeats, feat.name, 2)"
          >
            <div class="card-header">
              <span class="card-name">{{ feat.name }}</span>
            </div>
            <div class="card-effect">{{ feat.description }}</div>
          </div>
        </div>
      </div>

      <!-- 灵能印记 -->
      <div v-if="activeTab === 'spirit_marks'" class="tab-content">
        <p class="limit-info">已选 {{ selectedMarks.length }} / {{ maxMarks }} 个灵能印记</p>
        <div class="card-grid">
          <div
            v-for="mark in spiritMarks" :key="mark.type"
            class="ability-card" :class="{ selected: selectedMarks.includes(mark.type) }"
            @click="toggleSelection(selectedMarks, mark.type, maxMarks)"
          >
            <div class="card-header">
              <span class="card-name">{{ mark.type }}</span>
            </div>
            <div class="card-effect">{{ mark.description }}</div>
          </div>
        </div>
      </div>

      <!-- 绝技 -->
      <div v-if="activeTab === 'ultimates'" class="tab-content">
        <p class="limit-info">选择绝技（需灵识14级以上）</p>
        <div class="card-grid">
          <div
            v-for="ult in ultimates" :key="ult.name"
            class="ability-card" :class="{ selected: selectedUltimates.includes(ult.name) }"
            @click="toggleSelection(selectedUltimates, ult.name, 2)"
          >
            <div class="card-header">
              <span class="card-name">{{ ult.name }}</span>
              <span class="tier-badge">{{ ult.tier }}</span>
            </div>
            <div class="card-cost">{{ ult.soul }} · {{ ult.domain }}</div>
            <div class="card-effect">{{ ult.effect }}</div>
          </div>
        </div>
      </div>

      <!-- 时髦动作 -->
      <div v-if="activeTab === 'stylish_moves'" class="tab-content">
        <p class="limit-info">选择一种时髦风格</p>
        <div class="style-grid">
          <div
            v-for="(moves, style) in stylishMoves" :key="style"
            class="style-card" :class="{ selected: selectedStyle === style }"
            @click="selectedStyle = String(style)"
          >
            <div class="style-name">{{ style }}</div>
            <div class="style-moves">
              <div v-for="move in (moves as any[])" :key="move.cost" class="move-item">
                <span class="move-cost">{{ move.cost }}</span>
                <span class="move-action">{{ move.action }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <button class="submit-btn" @click="submit" :disabled="store.loading">
      {{ store.loading ? '提交中...' : '确认能力选择' }}
    </button>
  </div>
</template>

<style scoped>
.step-container { max-width: 900px; }
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

.warning-box {
  background: var(--warning-bg);
  border: 1px solid rgba(255, 183, 77, 0.2);
  border-radius: var(--radius-md);
  padding: var(--space-sm) var(--space-md);
  margin-bottom: var(--space-md);
  color: var(--warning);
  font-size: 0.9rem;
}

.tab-bar {
  display: flex;
  gap: 2px;
  margin-bottom: var(--space-md);
  flex-wrap: wrap;
  background: rgba(15, 25, 35, 0.4);
  border-radius: var(--radius-md);
  padding: var(--space-xs);
  border: 1px solid var(--border-subtle);
}
.tab-btn {
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-sm);
  border: none;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  font-family: var(--font-body);
  font-size: 0.85rem;
  transition: all var(--transition-normal);
}
.tab-btn:hover { color: var(--text-secondary); background: rgba(209, 196, 233, 0.03); }
.tab-btn.active {
  color: var(--accent-primary);
  background: rgba(209, 196, 233, 0.08);
}

.tab-content { min-height: 200px; }
.limit-info { color: var(--info); font-size: 0.85rem; margin-bottom: var(--space-sm); }

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: var(--space-sm);
  max-height: 400px;
  overflow-y: auto;
}

.ability-card {
  background: rgba(15, 25, 35, 0.4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-sm) var(--space-md);
  cursor: pointer;
  transition: all var(--transition-normal);
}
.ability-card:hover {
  border-color: var(--border-glow);
  box-shadow: 0 0 12px rgba(209, 196, 233, 0.06);
}
.ability-card.selected {
  border-color: var(--accent-muted);
  background: rgba(209, 196, 233, 0.05);
  box-shadow: var(--shadow-glow-active);
}
.ability-card.secret { border-left: 3px solid var(--warning); }

.card-header { display: flex; align-items: center; gap: var(--space-sm); margin-bottom: var(--space-xs); }
.card-name { font-weight: 500; font-size: 0.9rem; color: var(--text-primary); }
.secret-badge {
  font-size: 0.7rem;
  background: var(--warning-bg);
  color: var(--warning);
  padding: 1px 6px;
  border-radius: var(--radius-sm);
}
.tier-badge {
  font-size: 0.7rem;
  background: var(--accent-dim);
  color: var(--accent-primary);
  padding: 1px 6px;
  border-radius: var(--radius-sm);
}
.card-category { font-size: 0.7rem; color: var(--text-muted); }
.card-cost { font-size: 0.8rem; color: var(--info); margin-bottom: var(--space-xs); }
.card-effect {
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.4;
  max-height: 60px;
  overflow: hidden;
}

.style-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-sm);
}
.style-card {
  background: rgba(15, 25, 35, 0.4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-md);
  cursor: pointer;
  transition: all var(--transition-normal);
}
.style-card:hover {
  border-color: var(--border-glow);
}
.style-card.selected {
  border-color: var(--accent-muted);
  background: rgba(209, 196, 233, 0.05);
  box-shadow: var(--shadow-glow-active);
}
.style-name {
  font-weight: 500;
  color: var(--accent-primary);
  margin-bottom: var(--space-sm);
}
.style-moves { display: flex; flex-direction: column; gap: var(--space-xs); }
.move-item { display: flex; gap: var(--space-sm); font-size: 0.8rem; }
.move-cost { color: var(--info); min-width: 60px; }
.move-action { color: var(--text-secondary); }

.submit-btn {
  margin-top: var(--space-lg);
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
