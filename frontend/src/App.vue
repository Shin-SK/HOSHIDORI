<!-- src/App.vue ----------------------------------------------- -->
<template>
  <!-- header / footer は meta.hideLayout が無い時だけ描画 -->
  <header v-if="!route.meta.hideLayout" class="header">
    <div class="header__wrap">
      <router-link to="/stage" class="logo"><img src="/img/logo.svg" /></router-link>
    </div>
  </header>

  <!-- main -->
  <main :class="route.meta.hideLayout ? '' : 'container'">
    <router-view />
  </main>

  <footer v-if="!route.meta.hideLayout" class="footer">
    <div class="footer__wrap">
      <router-link to="/mypage" class="mypage"><img src="/img/icon_user.svg" /></router-link>      <router-link to="/stage" class="logo"><img src="/img/logo.svg" /></router-link>
      <!-- ☆ ここを出し分ける -->
      <!-- 未ログイン → “ログイン” アイコン -->
      <router-link v-if="!isLoggedIn" to="/login" class="login">
        <img src="/img/icon_login.svg" />
      </router-link>

      <!-- ログイン中 → “ログアウト” アイコン -->
      <a v-else href="#" class="login" @click.prevent="logout">
        <img src="/img/icon_logout.svg" />
      </a>
    </div>
  </footer>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useAuth }  from '@/services/useAuth.js'
const route = useRoute()
const { isLoggedIn, logout } = useAuth()
</script>
