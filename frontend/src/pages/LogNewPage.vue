<!-- src/pages/LogNewPage.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const works = ref([])
const loading = ref(true)
const error = ref(null)

const form = ref({
  workId: '',
  watchedDate: '',
  seat: '',
  memo: '',
  rating: '',
})

// ローカルでは全部「自分=1」でOK、API側で userId=1 をセットする想定
// → フロントで userId は扱わない

async function fetchWorks() {
  loading.value = true
  try {
    const res = await fetch('/api/works')
    if (!res.ok) throw new Error('API error')
    const data = await res.json()
    works.value = data
    if (data.length > 0) {
      form.value.workId = data[0].id
    }
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchWorks)

async function handleSubmit(e) {
  e.preventDefault()

  await fetch('/api/logs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      // userId は送らない。API側で1固定にする
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
    <h1 class="mb-3">観劇ログを追加（Vue版）</h1>

    <p v-if="loading">作品一覧を読み込み中...</p>
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
          placeholder="A列12番 など"
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

      <button type="submit" class="btn btn-primary">
        保存
      </button>
    </form>
  </main>
</template>