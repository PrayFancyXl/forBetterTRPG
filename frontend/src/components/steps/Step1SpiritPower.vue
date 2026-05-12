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
h2 { color: #a855f7; margin-bottom: 8px; }
.desc { color: #999; margin-bottom: 20px; font-size: 0.9rem; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 6px; font-size: 0.9rem; color: #ccc; }
.char-count { color: #888; font-size: 0.8rem; }
.form-group input, .form-group textarea {
  width: 100%; padding: 10px 12px; border-radius: 8px;
  border: 1px solid #2a2a4a; background: #1a1a2e; color: #e0e0e0;
  font-size: 0.95rem; outline: none;
}
.form-group input:focus, .form-group textarea:focus { border-color: #a855f7; }
.submit-btn {
  padding: 12px 32px; border-radius: 8px; border: none;
  background: #a855f7; color: white; font-size: 1rem; cursor: pointer;
}
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
