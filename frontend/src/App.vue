<script setup>
import { IconSearch } from '@tabler/icons-vue'
</script>

<template>
  <div style="padding-bottom: 80px;">
    <router-view />
  </div>
  <footer class="position-fixed bottom-0 w-100 bg-white border-top">
    <div class="d-flex justify-content-between p-2">
      <router-link to="/logs" class="btn btn-sm">
        <img src="/icon.svg" height="40" alt="">
      </router-link>
      <router-link to="/works" class="btn btn-sm df-center">
        <IconSearch />
      </router-link>
    </div>
  </footer>
</template>

<style>
/* 全体共通のスタイルがあればここに */
</style>