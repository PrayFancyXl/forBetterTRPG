<script setup lang="ts">
import { ref } from 'vue'
import { useCharacterStore } from '../../stores/character'
import { useChatStore } from '../../stores/chat'

const store = useCharacterStore()
const chatStore = useChatStore()

const name = ref('')
const description = ref('')
const tags = ref('')
const weaknessTag = ref('')

async function submit() {
  const tagList = tags.value.split(/[,，、]/).map(t => t.trim()).filter(Boolean)
  await store.submitStep(1, {
    name: name.value,
    description: description.value,
    tags: tagList,
    weakness_tag: weaknessTag.value,
  })
  await chatStore.loadTip(2)
}
</script>

<template>
  <div class="step-container">
    <h2>第一步：创建灵能力</h2>
    <p class="desc">灵能力是你角色的核心特色。先想一个概念，再用不超过80字描述。</p>

    <div class="form-group">
      <label>灵能力名称</label>
      <input v-model="name" placeholder="例如：烈焰操控、时间静止..." />
    </div>

    <div class="form-group">
      <label>灵能力描述 <span class="char-count">{{ description.length }}/80</span></label>
      <textarea v-model="description" maxlength="80" rows="3" placeholder="描述你的灵能力..."></textarea>
    </div>

    <div class="form-group">
      <label>灵能力标签（最多3个，用逗号分隔）</label>
      <input v-model="tags" placeholder="例如：火焰，远程，范围" />
    </div>

    <div class="form-group">
      <label>灵能力弱点标签</label>
      <input v-model="weaknessTag" placeholder="例如：怕水" />
    </div>

    <button class="submit-btn" @click="submit" :disabled="store.loading">
      {{ store.loading ? '提交中...' : '确认灵能力' }}
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
.form-group { margin-bottom: var(--space-md); }
.form-group label {
  display: block;
  margin-bottom: var(--space-xs);
  font-size: 0.85rem;
  color: var(--text-secondary);
}
.char-count { color: var(--text-muted); font-size: 0.8rem; }
.form-group input, .form-group textarea {
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
.form-group input::placeholder, .form-group textarea::placeholder {
  color: var(--text-muted);
}
.form-group input:focus, .form-group textarea:focus {
  border-bottom-color: var(--accent-primary);
  box-shadow: 0 1px 0 0 var(--accent-primary);
}
.form-group textarea {
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  border-bottom: 1px solid var(--border-glow);
  resize: vertical;
}
.form-group textarea:focus {
  border-color: var(--accent-muted);
  box-shadow: 0 0 0 1px var(--accent-dim);
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
