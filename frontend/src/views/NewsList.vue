<template>
	<section class="news">
	  <h1 class="page-title">演劇ニュース</h1>
  
	  <ul class="news-list">
		<li v-for="n in itemsWithImage" :key="n.id">
		  <a :href="n.link" target="_blank" rel="noopener">
			<img :src="n.image" alt="" loading="lazy" />
			<div class="body">
			  <h2 class="title">{{ n.title }}</h2>
			  <p class="meta">
				<time :datetime="n.pub_at">{{ formatDate(n.pub_at) }}</time>
				| {{ n.source }}
			  </p>
			</div>
		  </a>
		</li>
	  </ul>
  
	  <p class="powered">Powered by 各メディア RSS</p>
	</section>
  </template>
  
  
  <script setup>
  import { ref, onMounted, computed } from 'vue'
  import apiClient from '@/services/api'
  
  const items = ref([])
  
  onMounted(async () => {
	items.value = (await apiClient.get('/api/news/')).data
  })
  
  /* 画像 URL が入っている記事だけ返す */
  const itemsWithImage = computed(() =>
	items.value.filter(n => n.image && n.image.trim() !== '')
  )
  
  function formatDate(dt) {
	return new Date(dt).toLocaleDateString('ja-JP', {
	  year: 'numeric', month: '2-digit', day: '2-digit'
	})
  }
  </script>
  

  <style scoped>
  .news-list { @apply grid gap-4 sm:grid-cols-2 lg:grid-cols-3; }
  .news-list li { @apply bg-white rounded-xl shadow overflow-hidden; }
  .news-list img { @apply w-full h-40 object-cover; }
  .body { @apply p-3; }
  .title { @apply text-sm font-semibold leading-snug; }
  .meta  { @apply text-xs text-gray-500 mt-1; }
  .powered { @apply text-center text-xs text-gray-400 mt-6; }
  </style>
  