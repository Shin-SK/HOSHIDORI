<template>
  <!-- header / footer は meta.hideLayout が無い時だけ描画 -->
  <header v-if="!route.meta.hideLayout" class="header">
    <div class="header__wrap">
      <router-link to="/stage" class="logo"><img src="/img/logo.svg" /></router-link>
    </div>
  </header>

  <!-- main -->
  <main :class="route.meta.hideHeader ? '' : 'container'">
    <router-view />
  </main>

  <footer v-if="!route.meta.hideFooter" class="footer">
    <div class="footer__wrap">
      <router-link to="/stage" class="home"><i class="fas fa-home"></i></router-link>
      <router-link to="/stage" class="trend"><i class="fas fa-rss"></i></router-link>
      <router-link to="/stage" class="search"><i class="fas fa-search"></i></router-link>
      <router-link to="/stage" class="news"><i class="far fa-newspaper"></i></router-link>
      <router-link to="/mypage" class="mypage"><i class="fas fa-user"></i></router-link>
    </div>
  </footer>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useAuth }  from '@/services/useAuth.js'
const route = useRoute()
const { isLoggedIn, logout } = useAuth()
</script>
