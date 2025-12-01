// src/router.js
import { createRouter, createWebHistory } from 'vue-router'
import LogsPage from '@/pages/LogsPage.vue'
import LogNewPage from '@/pages/LogNewPage.vue'
import LogEditPage from '@/pages/LogEditPage.vue'
import LogsDetailPage from '@/pages/LogsDetailPage.vue'
import WorksList from '@/pages/WorksList.vue'
import WorksDetailPage from '@/pages/WorksDetailPage.vue'
import WorksNewPage from '@/pages/WorksNewPage.vue'

const routes = [
  { path: '/', redirect: '/logs' },
  { path: '/logs', name: 'logs', component: LogsPage },
  { path: '/logs/new', name: 'log-new', component: LogNewPage },
  {
    path: '/logs/:id/detail',
    name: 'log-detail',
    component: LogsDetailPage,
    props: true,
  },
  {
    path: '/logs/:id/edit',
    name: 'log-edit',
    component: LogEditPage,
    props: true,
  },
  { path: '/works', name: 'works', component: WorksList },
  {
    path: '/works/:id/detail',
    name: 'work-detail',
    component: WorksDetailPage,
    props: true,
  },
  { path: '/works/new', name: 'work-new', component: WorksNewPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router