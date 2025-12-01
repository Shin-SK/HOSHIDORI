// src/router.js
import { createRouter, createWebHistory } from 'vue-router'
import LogsPage from '@/pages/LogsPage.vue'
import LogNewPage from '@/pages/LogNewPage.vue'
import LogEditPage from '@/pages/LogEditPage.vue'

const routes = [
  { path: '/', redirect: '/logs' },
  { path: '/logs', name: 'logs', component: LogsPage },
  { path: '/logs/new', name: 'log-new', component: LogNewPage },
  {
    path: '/logs/:id/edit',
    name: 'log-edit',
    component: LogEditPage,
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router