<!-- src/views/HomeView.vue -->
<template>
	<div>
	  <h1>Home</h1>
	  <p>This is the home page.</p>
	  <router-link to="/stage">Go to Stage List</router-link>
	</div>
  </template>
  
  <script>
  export default {
	name: "HomeView",
  };
  </script>
  
  <style scoped>
  /* 必要があればスタイルを追加 */
  </style>
  