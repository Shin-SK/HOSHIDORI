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
      <router-link to="/stage/running" class="trend"><i class="fas fa-rss"></i></router-link>
      <button  class="search" @click="openSearch"><i class="fas fa-search"></i></button>      <router-link to="/news" class="news"><i class="far fa-newspaper"></i></router-link>
      <router-link to="/mypage" class="mypage"><i class="fas fa-user"></i></router-link>
    </div>
  </footer>
  <SearchModal ref="searchModal" />
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth }  from '@/services/useAuth.js'
import SearchModal  from '@/components/SearchModal.vue'

const route        = useRoute()
const { isLoggedIn, logout } = useAuth()

/* ::: 検索モーダル ::: */
const searchModal = ref(null)
function openSearch () {
  searchModal.value?.open()
}
</script>