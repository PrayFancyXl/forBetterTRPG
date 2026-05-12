<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useCharacterStore } from './stores/character'
import { useChatStore } from './stores/chat'
import StepNavigation from './components/StepNavigation.vue'
import Step1SpiritPower from './components/steps/Step1SpiritPower.vue'
import Step2Bond from './components/steps/Step2Bond.vue'
import Step3CharacterInfo from './components/steps/Step3CharacterInfo.vue'
import Step4Attributes from './components/steps/Step4Attributes.vue'
import Step5Skills from './components/steps/Step5Skills.vue'
import Step6Abilities from './components/steps/Step6Abilities.vue'
import ChatPanel from './components/ChatPanel.vue'
import ValidationFeedback from './components/ValidationFeedback.vue'

const store = useCharacterStore()
const chatStore = useChatStore()

const currentStep = computed(() => store.currentStep)

onMounted(async () => {
  await store.createSession()
  await chatStore.loadTip(1)
})
</script>

<template>
  <div class="app-container" v-if="store.session">
    <header class="app-header">
      <h1>狩魂者TRPG 建卡器</h1>
    </header>

    <StepNavigation :current-step="currentStep" :completed-steps="store.completedSteps" />

    <div class="main-layout">
      <main class="content-area">
        <ValidationFeedback />

        <div class="tip-bar" v-if="chatStore.tip">
          <span class="tip-icon">💡</span> {{ chatStore.tip }}
        </div>

        <Step1SpiritPower v-if="currentStep === 1" />
        <Step2Bond v-if="currentStep === 2" />
        <Step3CharacterInfo v-if="currentStep === 3" />
        <Step4Attributes v-if="currentStep === 4" />
        <Step5Skills v-if="currentStep === 5" />
        <Step6Abilities v-if="currentStep === 6" />
      </main>

      <aside class="chat-sidebar">
        <ChatPanel />
      </aside>
    </div>
  </div>
  <div v-else class="loading">加载中...</div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #1a1a2e;
  color: #e0e0e0;
  min-height: 100vh;
}

.app-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.app-header {
  text-align: center;
  margin-bottom: 20px;
}

.app-header h1 {
  color: #a855f7;
  font-size: 1.8rem;
}

.main-layout {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 20px;
  margin-top: 20px;
}

.content-area {
  background: #16213e;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #2a2a4a;
}

.chat-sidebar {
  background: #16213e;
  border-radius: 12px;
  border: 1px solid #2a2a4a;
  display: flex;
  flex-direction: column;
  max-height: 80vh;
}

.tip-bar {
  background: #1e3a5f;
  border: 1px solid #3b82f6;
  border-radius: 8px;
  padding: 10px 14px;
  margin-bottom: 16px;
  font-size: 0.9rem;
  color: #93c5fd;
}

.tip-icon {
  margin-right: 6px;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-size: 1.2rem;
  color: #a855f7;
}

@media (max-width: 900px) {
  .main-layout {
    grid-template-columns: 1fr;
  }
}
</style>
