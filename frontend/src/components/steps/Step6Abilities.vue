<script setup lang="ts">
import { useCharacterStore } from '../../stores/character'

const store = useCharacterStore()
</script>

<template>
  <div class="step-container">
    <h2>第六步：能力选择</h2>
    <p class="desc">选择武技、术法、专长、灵魂武器和绝技。（开发中）</p>
    <p class="placeholder">此步骤将在 Stage D 中完善</p>
  </div>
</template>

<style scoped>
.step-container { max-width: 600px; }
h2 { color: #a855f7; margin-bottom: 8px; }
.desc { color: #999; margin-bottom: 20px; font-size: 0.9rem; }
.placeholder { color: #666; font-style: italic; }
</style>
