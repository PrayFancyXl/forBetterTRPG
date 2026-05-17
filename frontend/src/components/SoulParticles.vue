<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref<HTMLCanvasElement | null>(null)
let animationId = 0
let inkClouds: InkCloud[] = []
let particles: Particle[] = []
let time = 0

interface InkCloud {
  x: number
  y: number
  baseSize: number
  speedX: number
  speedY: number
  opacity: number
  phase: number
  phaseSpeed: number
  color: string
}

interface Particle {
  x: number
  y: number
  size: number
  speedX: number
  speedY: number
  opacity: number
  opacityDir: number
  color: string
}

const CLOUD_COUNT = 6
const PARTICLE_COUNT = 15

const CLOUD_COLORS = [
  'rgba(26, 42, 58,',
  'rgba(30, 52, 72,',
  'rgba(44, 62, 80,',
  'rgba(40, 30, 60,',
  'rgba(25, 35, 55,',
]

const PARTICLE_COLORS = [
  'rgba(209, 196, 233,',
  'rgba(179, 157, 219,',
  'rgba(240, 235, 255,',
]

function createCloud(w: number, h: number): InkCloud {
  return {
    x: Math.random() * w,
    y: Math.random() * h,
    baseSize: Math.random() * 250 + 150,
    speedX: (Math.random() - 0.5) * 0.15,
    speedY: (Math.random() - 0.5) * 0.1,
    opacity: Math.random() * 0.25 + 0.1,
    phase: Math.random() * Math.PI * 2,
    phaseSpeed: Math.random() * 0.003 + 0.001,
    color: CLOUD_COLORS[Math.floor(Math.random() * CLOUD_COLORS.length)],
  }
}

function createParticle(w: number, h: number): Particle {
  return {
    x: Math.random() * w,
    y: Math.random() * h,
    size: Math.random() * 2 + 0.8,
    speedX: (Math.random() - 0.5) * 0.2,
    speedY: (Math.random() - 0.5) * 0.15 - 0.05,
    opacity: Math.random() * 0.4 + 0.1,
    opacityDir: (Math.random() - 0.5) * 0.004,
    color: PARTICLE_COLORS[Math.floor(Math.random() * PARTICLE_COLORS.length)],
  }
}

function animate() {
  const cvs = canvas.value
  if (!cvs) return
  const ctx = cvs.getContext('2d')
  if (!ctx) return

  const w = cvs.width
  const h = cvs.height
  time++

  ctx.clearRect(0, 0, w, h)

  // 绘制墨云
  for (const cloud of inkClouds) {
    cloud.x += cloud.speedX
    cloud.y += cloud.speedY
    cloud.phase += cloud.phaseSpeed

    // 缓慢边界回弹
    if (cloud.x < -cloud.baseSize) cloud.x = w + cloud.baseSize * 0.5
    if (cloud.x > w + cloud.baseSize) cloud.x = -cloud.baseSize * 0.5
    if (cloud.y < -cloud.baseSize) cloud.y = h + cloud.baseSize * 0.5
    if (cloud.y > h + cloud.baseSize) cloud.y = -cloud.baseSize * 0.5

    const sizePulse = Math.sin(cloud.phase) * 30
    const currentSize = cloud.baseSize + sizePulse
    const opacityPulse = Math.sin(cloud.phase * 0.7) * 0.05
    const currentOpacity = cloud.opacity + opacityPulse

    const gradient = ctx.createRadialGradient(
      cloud.x, cloud.y, 0,
      cloud.x, cloud.y, currentSize
    )
    gradient.addColorStop(0, `${cloud.color} ${currentOpacity})`)
    gradient.addColorStop(0.4, `${cloud.color} ${currentOpacity * 0.6})`)
    gradient.addColorStop(0.7, `${cloud.color} ${currentOpacity * 0.2})`)
    gradient.addColorStop(1, `${cloud.color} 0)`)

    ctx.beginPath()
    ctx.arc(cloud.x, cloud.y, currentSize, 0, Math.PI * 2)
    ctx.fillStyle = gradient
    ctx.fill()
  }

  // 绘制灵魂粒子
  for (const p of particles) {
    p.x += p.speedX
    p.y += p.speedY
    p.opacity += p.opacityDir

    if (p.opacity <= 0.05 || p.opacity >= 0.5) {
      p.opacityDir = -p.opacityDir
    }

    if (p.x < -10) p.x = w + 10
    if (p.x > w + 10) p.x = -10
    if (p.y < -10) p.y = h + 10
    if (p.y > h + 10) p.y = -10

    // 粒子本体
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2)
    ctx.fillStyle = `${p.color} ${p.opacity})`
    ctx.fill()

    // 光晕
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.size * 3, 0, Math.PI * 2)
    ctx.fillStyle = `${p.color} ${p.opacity * 0.12})`
    ctx.fill()
  }

  animationId = requestAnimationFrame(animate)
}

function resize() {
  const cvs = canvas.value
  if (!cvs) return
  cvs.width = window.innerWidth
  cvs.height = window.innerHeight
}

onMounted(() => {
  resize()
  const cvs = canvas.value!
  inkClouds = Array.from({ length: CLOUD_COUNT }, () =>
    createCloud(cvs.width, cvs.height)
  )
  particles = Array.from({ length: PARTICLE_COUNT }, () =>
    createParticle(cvs.width, cvs.height)
  )
  animate()
  window.addEventListener('resize', resize)
})

onUnmounted(() => {
  cancelAnimationFrame(animationId)
  window.removeEventListener('resize', resize)
})
</script>

<template>
  <canvas ref="canvas" class="soul-particles"></canvas>
</template>

<style scoped>
.soul-particles {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}
</style>
