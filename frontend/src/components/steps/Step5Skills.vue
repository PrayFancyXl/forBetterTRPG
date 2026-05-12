<script setup lang="ts">
import { useCharacterStore } from '../../stores/character'

const store = useCharacterStore()
</script>

<template>
  <div class="step-container">
    <h2>第五步：技能分配</h2>
    <p class="desc">根据智慧等级获得的技能点，分配到7项技能中。（开发中）</p>
    <p class="placeholder">此步骤将在 Stage D 中完善</p>
  </div>
</template>

<style scoped>
.step-container { max-width: 600px; }
h2 { color: #a855f7; margin-bottom: 8px; }
.desc { color: #999; margin-bottom: 20px; font-size: 0.9rem; }
.placeholder { color: #666; font-style: italic; }
</style>
