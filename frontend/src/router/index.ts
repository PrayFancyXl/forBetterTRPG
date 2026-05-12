import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/create/1' },
  { path: '/create/:step', name: 'create', component: () => import('../App.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
