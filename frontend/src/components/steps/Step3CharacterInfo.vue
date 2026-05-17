<script setup lang="ts">
import { ref } from 'vue'
import { useCharacterStore } from '../../stores/character'
import { useChatStore } from '../../stores/chat'

const store = useCharacterStore()
const chatStore = useChatStore()

const form = ref({
  name: '', codename: '', gender: '', age: '',
  backstory: '', appearance: '',
})

async function submit() {
  await store.submitStep(3, form.value)
  await chatStore.loadTip(4)
}
</script>

<template>
  <div class="step-container">
    <h2>第三步：角色信息</h2>
    <p class="desc">填写你的狩魂者基本信息。姓名和代号为必填项。</p>

    <div class="form-row">
      <div class="form-group">
        <label>姓名 *</label>
        <input v-model="form.name" placeholder="真名" />
      </div>
      <div class="form-group">
        <label>代号 *</label>
        <input v-model="form.codename" placeholder="狩魂者代号" />
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label>性别</label>
        <input v-model="form.gender" placeholder="性别" />
      </div>
      <div class="form-group">
        <label>年龄</label>
        <input v-model="form.age" placeholder="年龄" />
      </div>
    </div>

    <div class="form-group">
      <label>外形描述</label>
      <textarea v-model="form.appearance" rows="2" placeholder="描述外貌特征..."></textarea>
    </div>

    <div class="form-group">
      <label>背景故事</label>
      <textarea v-model="form.backstory" rows="4" placeholder="你的狩魂者有怎样的过去..."></textarea>
    </div>

    <button class="submit-btn" @click="submit" :disabled="store.loading || !form.name || !form.codename">
      {{ store.loading ? '提交中...' : '确认信息' }}
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
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
}
.form-group { margin-bottom: var(--space-md); }
.form-group label {
  display: block;
  margin-bottom: var(--space-xs);
  font-size: 0.85rem;
  color: var(--text-secondary);
}
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
