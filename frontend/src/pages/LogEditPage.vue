<!-- src/pages/LogEditPage.vue -->
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authorizedFetch } from '@/apiClient'

const route = useRoute()
const router = useRouter()
const id = computed(() => Number(route.params.id))

const loading = ref(true)
const error = ref(null)
const works = ref([])

const form = ref({
  workId: '',
  watchedDate: '',
  seat: '',
  memo: '',
  rating: '',
})

function formatDateInput(val) {
  if (!val) return ''
  const d = new Date(val)
  if (Number.isNaN(d.getTime())) return ''
  return d.toISOString().slice(0, 10)
}

async function fetchData() {
  loading.value = true
  try {
    // 作品一覧
    const resWorks = await authorizedFetch('/api/works')
    if (!resWorks.ok) throw new Error('works API error')
    works.value = await resWorks.json()

    // ログ一覧から該当の1件を引っこ抜く
    const resLogs = await authorizedFetch('/api/logs')
    if (!resLogs.ok) throw new Error('logs API error')
    const all = await resLogs.json()
    const log = all.find((l) => l.id === id.value)
    if (!log) {
      throw new Error('ログが見つかりません')
    }

    form.value = {
      workId: log.workId,
      watchedDate: formatDateInput(log.watchedDate),
      seat: log.seat || '',
      memo: log.memo || '',
      rating: log.rating?.toString() || '',
    }
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)

async function handleSubmit(e) {
  e.preventDefault()

  await authorizedFetch(`/api/logs/${id.value}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      workId: Number(form.value.workId),
      watchedDate: form.value.watchedDate || undefined,
      seat: form.value.seat || null,
      memo: form.value.memo || null,
      rating: form.value.rating ? Number(form.value.rating) : null,
      tags: [],
    }),
  })

  router.push('/logs')
}
</script>

<template>
  <main class="container py-4">
    <h1 class="mb-3">観劇ログを編集（Vue版）</h1>

    <p v-if="loading">読み込み中...</p>
    <p v-else-if="error">エラー: {{ error }}</p>

    <form v-else @submit="handleSubmit" class="mb-4">
      <div class="mb-3">
        <label class="form-label">作品</label>
        <select
          class="form-select"
          v-model="form.workId"
        >
          <option
            v-for="work in works"
            :key="work.id"
            :value="work.id"
          >
            {{ work.title }}（{{ work.theater?.name }}）
          </option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label">観た日</label>
        <input
          type="date"
          class="form-control"
          v-model="form.watchedDate"
        />
      </div>

      <div class="mb-3">
        <label class="form-label">座席</label>
        <input
          type="text"
          class="form-control"
          v-model="form.seat"
        />
      </div>

      <div class="mb-3">
        <label class="form-label">メモ</label>
        <textarea
          class="form-control"
          rows="3"
          v-model="form.memo"
        />
      </div>

      <div class="mb-3">
        <label class="form-label">評価（1〜5）</label>
        <input
          type="number"
          min="1"
          max="5"
          class="form-control"
          v-model="form.rating"
        />
      </div>

      <button type="submit" class="btn btn-primary">更新</button>
    </form>
  </main>
</template>