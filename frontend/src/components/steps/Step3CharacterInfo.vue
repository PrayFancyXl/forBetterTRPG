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
h2 { color: #a855f7; margin-bottom: 8px; }
.desc { color: #999; margin-bottom: 20px; font-size: 0.9rem; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 6px; font-size: 0.9rem; color: #ccc; }
.form-group input, .form-group textarea {
  width: 100%; padding: 10px 12px; border-radius: 8px;
  border: 1px solid #2a2a4a; background: #1a1a2e; color: #e0e0e0; outline: none; font-size: 0.95rem;
}
.form-group input:focus, .form-group textarea:focus { border-color: #a855f7; }
.submit-btn {
  padding: 12px 32px; border-radius: 8px; border: none;
  background: #a855f7; color: white; font-size: 1rem; cursor: pointer;
}
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
