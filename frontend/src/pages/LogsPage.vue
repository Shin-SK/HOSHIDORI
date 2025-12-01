<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { IconCirclePlus, IconStar, IconBinoculars } from '@tabler/icons-vue'

const logs = ref([])
const loading = ref(true)
const error = ref(null)
const router = useRouter()

async function fetchLogs() {
  loading.value = true
  try {
    const res = await fetch('/api/logs')
    if (!res.ok) throw new Error('API error')
    logs.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchLogs)

function formatDate(val) {
  if (!val) return ''
  const d = new Date(val)
  if (Number.isNaN(d.getTime())) return ''
  return d.toISOString().slice(0, 10)
}

async function deleteLog(id) {
  const ok = window.confirm('この観劇ログを削除しますか？')
  if (!ok) return

  await fetch(`/api/logs/${id}`, {
    method: 'DELETE',
  })

  // 再取得
  await fetchLogs()
}
</script>

<template>
  <main class="container py-4">
    <h1 class="mb-3 df-center">
      <img 
        src="/icon.svg"
        style="width: 80px;"
        alt="">
    </h1>

    <router-link to="/logs/new" class="btn text-dark df-center my-5">
      <IconCirclePlus :size="40"/>
    </router-link>

    <p v-if="loading">読み込み中...</p>
    <p v-else-if="error">エラー: {{ error }}</p>
    <p v-else-if="logs.length === 0">まだ観劇ログがありません。</p>

    <div v-else class="row g-1">
      <div v-for="log in logs" :key="log.id" class="col-6 col-md-3 col-lg-2">
        <div class="poster position-relative">
          <router-link :to="`/logs/${log.id}/detail`">
            <img 
              v-if="log.work?.imageUrl" 
              :src="log.work.imageUrl" 
              class="poster-img w-100"
              :alt="log.work.title"
              style="aspect-ratio: 1/1.414; object-fit: cover; cursor: pointer;"
            >
            <div 
              v-else 
              class="poster-img bg-secondary d-flex align-items-center justify-content-center text-white"
              style="aspect-ratio: 1/1.414; cursor: pointer;"
            >
              画像なし
            </div>
          </router-link>
          <div class="poster-body df-center gap-2 bg-light p-1">
            <div class="star df-center text-muted gap-1">
              <IconStar :size="16" />
              <div>{{ log.rating }}</div>
            </div>
            <div class="date df-center"><IconBinoculars :size="20" /><small>{{ formatDate(log.watchedDate) }}</small></div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>