<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

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
    <h1 class="mb-3">観劇ログ一覧（Vue版）</h1>

    <router-link to="/logs/new" class="btn btn-primary mb-3">
      新規ログ追加
    </router-link>

    <p v-if="loading">読み込み中...</p>
    <p v-else-if="error">エラー: {{ error }}</p>
    <p v-else-if="logs.length === 0">まだ観劇ログがありません。</p>

    <table v-else class="table table-striped">
      <thead>
        <tr>
          <th>日付</th>
          <th>タイトル</th>
          <th>劇場</th>
          <th>ユーザー</th>
          <th>メモ</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in logs" :key="log.id">
          <td>{{ formatDate(log.watchedDate) }}</td>
          <td>{{ log.work?.title }}</td>
          <td>{{ log.work?.theater?.name }}</td>
          <td>{{ log.user?.name }}</td>
          <td>{{ log.memo }}</td>
          <td>
            <router-link
              :to="`/logs/${log.id}/edit`"
              class="btn btn-sm btn-outline-primary me-2"
            >
              編集
            </router-link>
            <button
              type="button"
              class="btn btn-sm btn-outline-danger"
              @click="deleteLog(log.id)"
            >
              削除
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </main>
</template>