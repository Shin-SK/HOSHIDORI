<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import WorksBody from '@/components/WorksBody.vue'
import { authorizedFetch } from '@/apiClient'

const props = defineProps(['id'])
const work = ref(null)
const loading = ref(true)
const error = ref(null)
const route = useRoute()

async function fetchWork() {
  loading.value = true
  try {
    const workId = props.id || route.params.id
    const res = await authorizedFetch(`/api/works`)
    if (!res.ok) throw new Error('API error')
    const works = await res.json()
    work.value = works.find(w => w.id === Number(workId))
    if (!work.value) {
      error.value = '作品が見つかりません'
    }
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchWork)
</script>

<template>
  <main class="container py-4">
    <p v-if="loading">読み込み中...</p>
    <p v-else-if="error">エラー: {{ error }}</p>
    <p v-else-if="!work">作品が見つかりません。</p>

    <div v-else class="wrap">
      <div class="h-100">
        <img 
          v-if="work.imageUrl" 
          :src="work.imageUrl" 
          class="w-100"
          :alt="work.title"
          style="object-fit: cover;"
        >
        <div 
          v-else 
          class="bg-secondary d-flex align-items-center justify-content-center text-white"
          style="aspect-ratio: 1/1.414;"
        >
          画像なし
        </div>
        
        <WorksBody :work="work" />
      </div>
    </div>
  </main>
</template>
