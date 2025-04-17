// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import StageList from '../views/StageList.vue'
import StageDetail from '../views/StageDetail.vue'
import StageEdit from '../views/StageEdit.vue'
import StageCreate from '../views/StageCreate.vue'
import MyPage from '../views/MyPage.vue'
import LogEdit from '../views/LogEdit.vue'

// ★ ログインページをインポート
import LoginView from '../views/LoginView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/stage', name: 'stage-list', component: StageList },
  { path: '/stage/create', name: 'stage-create', component: StageCreate },
  { path: '/stage/:id', name: 'stage-detail', component: StageDetail },
  { path: '/stage/:id/edit', name: 'stage-edit', component: StageEdit },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/mypage', name: 'mypage', component: MyPage },
  { path  : '/log/create/:stageId', name  : 'log-create', component: LogEdit, props: route => ({ mode: 'create', stageId: Number(route.params.stageId) })},
  { path: '/log/:id/edit', name: 'log-edit', component: LogEdit, props: route => ({ mode: 'edit', id: route.params.id }) },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
