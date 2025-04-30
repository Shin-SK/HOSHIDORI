// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView      from '@/views/HomeView.vue'
import StageList     from '@/views/StageList.vue'
import StageListRun  from '@/views/StageListRun.vue'
import StageDetail   from '@/views/StageDetail.vue'
import StageEdit     from '@/views/StageEdit.vue'
import StageCreate   from '@/views/StageCreate.vue'
import MyPage        from '@/views/MyPage.vue'
import LogEdit       from '@/views/LogEdit.vue'
import ProfileEdit   from '@/views/ProfileEdit.vue'
import Signup        from '@/views/Signup.vue'
import PublicProfile from '@/views/PublicProfile.vue'
import LoginView     from '@/views/LoginView.vue'
import NewsList     from '@/views/NewsList.vue'

const routes = [
  // トップ → ログイン済みなら /stage
  {
    path: '/',
    name: 'home',
    component: HomeView,
    beforeEnter: (_to, _from, next) =>
      localStorage.getItem('accessToken')
        ? next({ name: 'stage-list' })
        : next()
  },

  /* ─────── 公開ページ ─────── */
  { path: '/stage',name: 'stage-list',component: StageList, meta: { hideLayout: true }},
  { path: '/stage/running',name: 'stage-list-run',component: StageListRun, meta: { hideLayout: true }},
  { path: '/stage/:id',name: 'stage-detail', component: StageDetail },
  { path: '/login',name: 'login',component: LoginView },
  { path: '/signup',name: 'signup',component: Signup },
  { path: '/profile/:username', name: 'public-profile', component: PublicProfile, props: true },
  { path: '/news',name: 'news',component: NewsList },

  /* ─────── 要ログインページ ─────── */
  { path: '/mypage', name: 'mypage',component: MyPage,meta: { requiresAuth: true } },
  { path: '/profile/edit',name: 'profile-edit',  component: ProfileEdit,meta: { requiresAuth: true } },
  { path: '/stage/create',name: 'stage-create',  component: StageCreate,meta: { requiresAuth: true } },
  { path: '/stage/:id/edit',name: 'stage-edit',component: StageEdit,meta: { requiresAuth: true } },
  { path: '/log/create/:stageId', name: 'log-create',component: LogEdit,props: r => ({ mode:'create', stageId:+r.params.stageId }), meta: { requiresAuth: true } },
  { path: '/log/:id/edit',name: 'log-edit',component: LogEdit,props: r => ({ mode:'edit',  id:r.params.id }),meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

/* ─────── 共通ガード ─────── */
router.beforeEach((to, _from, next) => {
  if (to.meta.requiresAuth && !localStorage.getItem('accessToken')) {
    next({ name: 'login', query: { next: to.fullPath } })
  } else {
    next()
  }
})

export default router
