<script setup lang="ts">
import { computed } from 'vue'
import { useCharacterStore } from '../stores/character'

const store = useCharacterStore()
const char = computed(() => store.character)
</script>

<template>
  <div class="card-preview" v-if="char">
    <h3>角色卡预览</h3>

    <div class="preview-section" v-if="char.spirit_power.name">
      <div class="section-title">灵能力</div>
      <div class="field"><span class="label">名称：</span>{{ char.spirit_power.name }}</div>
      <div class="field" v-if="char.spirit_power.tags.length">
        <span class="label">标签：</span>
        <span class="tag" v-for="t in char.spirit_power.tags" :key="t">{{ t }}</span>
      </div>
    </div>

    <div class="preview-section" v-if="char.basic_info.bond">
      <div class="section-title">羁绊</div>
      <div class="field">{{ char.basic_info.bond }}</div>
    </div>

    <div class="preview-section" v-if="char.basic_info.name || char.basic_info.codename">
      <div class="section-title">角色信息</div>
      <div class="field" v-if="char.basic_info.codename">
        <span class="label">代号：</span>{{ char.basic_info.codename }}
      </div>
      <div class="field" v-if="char.basic_info.name">
        <span class="label">姓名：</span>{{ char.basic_info.name }}
      </div>
      <div class="field" v-if="char.basic_info.gender">
        <span class="label">性别：</span>{{ char.basic_info.gender }}
      </div>
      <div class="field" v-if="char.basic_info.age">
        <span class="label">年龄：</span>{{ char.basic_info.age }}
      </div>
    </div>

    <div class="preview-section" v-if="char.attributes.physique !== 'E' || char.attributes.wisdom !== 'E' || char.attributes.spirit !== 'E'">
      <div class="section-title">属性</div>
      <div class="attr-row">
        <div class="attr-item">
          <span class="attr-label">体魄</span>
          <span class="attr-value">{{ char.attributes.physique }}</span>
        </div>
        <div class="attr-item">
          <span class="attr-label">智慧</span>
          <span class="attr-value">{{ char.attributes.wisdom }}</span>
        </div>
        <div class="attr-item">
          <span class="attr-label">心魂</span>
          <span class="attr-value">{{ char.attributes.spirit }}</span>
        </div>
      </div>
    </div>

    <div class="preview-section" v-if="char.martial_arts.length">
      <div class="section-title">武技 ({{ char.martial_arts.length }})</div>
      <div class="chip-list">
        <span class="chip" v-for="a in char.martial_arts" :key="a.name">{{ a.name }}</span>
      </div>
    </div>

    <div class="preview-section" v-if="char.spells.length">
      <div class="section-title">术法 ({{ char.spells.length }})</div>
      <div class="chip-list">
        <span class="chip" v-for="s in char.spells" :key="s.name">{{ s.name }}</span>
      </div>
    </div>

    <div class="preview-section" v-if="char.feats.length">
      <div class="section-title">专长</div>
      <div class="chip-list">
        <span class="chip" v-for="f in char.feats" :key="f.name">{{ f.name }}</span>
      </div>
    </div>

    <div class="preview-section" v-if="char.spirit_marks.length">
      <div class="section-title">灵能印记</div>
      <div class="chip-list">
        <span class="chip" v-for="m in char.spirit_marks" :key="m.mark_type">{{ m.mark_type }}</span>
      </div>
    </div>

    <div v-if="!char.spirit_power.name && !char.basic_info.name" class="empty-state">
      开始建卡后这里会显示角色卡预览
    </div>
  </div>
</template>

<style scoped>
.card-preview {
  padding: var(--space-md);
}

h3 {
  font-family: var(--font-title);
  color: var(--accent-primary);
  font-size: 1rem;
  margin-bottom: var(--space-sm);
  padding-bottom: var(--space-sm);
  border-bottom: 1px solid var(--border-subtle);
}

.preview-section {
  margin-bottom: var(--space-md);
  padding-bottom: var(--space-sm);
  border-bottom: 1px solid var(--border-subtle);
}

.section-title {
  font-size: 0.75rem;
  color: var(--accent-secondary);
  font-weight: 500;
  margin-bottom: var(--space-xs);
  letter-spacing: 0.05em;
}

.field {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 2px;
}

.label {
  color: var(--text-muted);
}

.tag {
  display: inline-block;
  background: var(--accent-dim);
  color: var(--accent-primary);
  padding: 1px 8px;
  border-radius: 10px;
  font-size: 0.75rem;
  margin-right: 4px;
}

.attr-row {
  display: flex;
  gap: var(--space-sm);
}

.attr-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(15, 25, 35, 0.4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: var(--space-xs) var(--space-sm);
}

.attr-label { font-size: 0.7rem; color: var(--text-muted); }
.attr-value { font-size: 1.1rem; font-weight: 600; color: var(--text-primary); }

.chip-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-xs);
}

.chip {
  background: rgba(15, 25, 35, 0.4);
  border: 1px solid var(--border-subtle);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.empty-state {
  text-align: center;
  color: var(--text-muted);
  font-size: 0.85rem;
  margin-top: 30px;
}
</style>
