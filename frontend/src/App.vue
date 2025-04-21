<!-- src/App.vue -->
<template>
  <header class="header">
      <div class="header__wrap">
        <router-link to="/stage" class="logo">
          <img src="/img/logo.svg" alt="">
        </router-link>
      </div>
  </header>
  <div class="container">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
/* 全体スタイルはお好みで */
</style>
