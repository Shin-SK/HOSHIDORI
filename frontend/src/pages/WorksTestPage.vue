<!-- frontend/src/pages/WorksSearchPage.vue -->
<script setup>
import { ref } from 'vue'
import { fetchWorks } from '@/apiClient'

const q = ref('')
const works = ref([])
const loading = ref(false)
const error = ref(null)

async function search() {
  loading.value = true
  error.value = null
  works.value = []
  try {
    const data = await fetchWorks(q.value ? { search: q.value } : {})
    works.value = data
  } catch (e) {
    console.error(e)
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="container py-4">
    <h1 class="mb-3">作品を探す</h1>

    <form class="row g-2 mb-4" @submit.prevent="search">
      <div class="col-sm-9">
        <input
          v-model="q"
          type="search"
          class="form-control"
          placeholder="作品名・劇団名・俳優名など"
        />
      </div>
      <div class="col-sm-3 d-grid">
        <button type="submit" class="btn btn-primary">
          検索
        </button>
      </div>
    </form>

    <p v-if="loading">検索中...</p>
    <p v-else-if="error">エラー: {{ error }}</p>
    <p v-else-if="works.length === 0">該当する作品がありません。</p>

    <ul v-else class="list-group">
      <li
        v-for="w in works"
        :key="w.id"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <div>
          <div class="fw-bold">{{ w.title }}</div>
          <div class="small text-muted">
            {{ w.troupe || '劇団不明' }} /
            {{ w.main_theater?.name || '劇場不明' }}
          </div>
        </div>
        <router-link
          :to="`/logs/new?work=${w.id}`"
          class="btn btn-sm btn-outline-primary"
        >
          この作品でログを書く
        </router-link>
      </li>
    </ul>
  </main>
</template>