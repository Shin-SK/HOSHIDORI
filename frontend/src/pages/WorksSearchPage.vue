<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import WorksBody from '@/components/WorksBody.vue'

const route = useRoute()
const q = ref(route.query.q || '')
const works = ref([])
const loading = ref(false)
const error = ref(null)

async function search() {
  loading.value = true
  error.value = null
  works.value = []

  try {
    const params = new URLSearchParams()
    if (q.value.trim()) params.set('q', q.value.trim())

    const res = await fetch(`/api/works?${params.toString()}`)
    if (!res.ok) throw new Error('API error')

    works.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

// 初期表示：クエリパラメータがあれば自動検索
onMounted(() => {
  if (q.value) {
    search()
  }
})
</script>

<template>
  <main class="container py-4">
    <h1 class="mb-3">作品検索</h1>

    <form class="row g-2 mb-4" @submit.prevent="search">
      <div class="col-sm-9">
        <input
          v-model="q"
          type="search"
          class="form-control"
          placeholder="タイトル・劇場名・タグ・俳優名などで検索"
        />
      </div>
      <div class="col-sm-3 d-grid">
        <button type="submit" class="btn btn-primary">
          検索
        </button>
      </div>
    </form>

    <p v-if="loading">検索中...</p>
    <p v-else-if="error" class="text-danger">エラー: {{ error }}</p>
    <p v-else-if="works.length === 0 && q">該当する作品がありません。</p>

    <div v-if="works.length > 0" class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3">
      <div v-for="work in works" :key="work.id" class="col">
        <div class="card h-100">
          <img
            v-if="work.imageUrl"
            :src="work.imageUrl"
            class="card-img-top"
            :alt="work.title"
            style="height: 250px; object-fit: cover;"
          />
          <div 
            v-else 
            class="card-img-top bg-secondary d-flex align-items-center justify-content-center text-white"
            style="height: 250px;"
          >
            画像なし
          </div>
          <WorksBody :work="work" />
        </div>
      </div>
    </div>
  </main>
</template>
