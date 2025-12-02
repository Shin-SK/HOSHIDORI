<!-- src/pages/LogNewPage.vue -->
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { request } from '@/apiClient'
import Multiselect from '@vueform/multiselect'

const router = useRouter()

const works = ref([])
const runs = ref([])
const todayTimes = ref([])
const loading = ref(true)
const error = ref(null)

const form = ref({
  workId: '',
  runId: '',
  watchedDate: '',
  watchedTime: '',
  seat: '',
  memo: '',
  rating: '',
})

// 簡易登録用フォーム
const showQuickForm = ref(false)
const quickForm = ref({
  title: '',
  troupe: '',
  theater: ''
})

async function fetchWorks() {
  loading.value = true
  try {
    const data = await request('/api/works/')
    works.value = data
    // 初期選択はしない
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function fetchRunsAndTimes(workId) {
  try {
    // Runs取得
    const workDetail = await request(`/api/works/${workId}/`)
    runs.value = workDetail.runs || []
    // 今日の公演時間候補取得
    const timesData = await request(`/api/works/${workId}/today_times/`)
    todayTimes.value = timesData.times || []
  } catch (e) {
    console.error('Failed to fetch runs/times:', e)
  }
}

async function onWorkChange() {
  if (form.value.workId) {
    await fetchRunsAndTimes(form.value.workId)
    form.value.runId = ''
    form.value.watchedTime = ''
  } else {
    // 作品が未選択の場合はRunsをクリア
    runs.value = []
    todayTimes.value = []
  }
}

// 簡易登録
async function handleQuickCreate() {
  if (!quickForm.value.title) {
    alert('タイトルは必須です')
    return
  }
  
  try {
    const newWork = await request('/api/works/create_or_get/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: quickForm.value.title,
        troupe_name: quickForm.value.troupe || null,
        theater_name: quickForm.value.theater || null,
        status: 'DRAFT'
      })
    })
    
    // 作品リストに追加して選択
    works.value.push(newWork)
    form.value.workId = newWork.id
    await fetchRunsAndTimes(newWork.id)
    
    // フォームをリセット
    showQuickForm.value = false
    quickForm.value = { title: '', troupe: '', theater: '' }
  } catch (e) {
    alert('作品の登録に失敗しました: ' + e.message)
  }
}

// マルチセレクト用のオプション
const workOptions = computed(() => 
  works.value.map(w => ({
    value: w.id,
    label: `${w.title}（${w.main_theater?.name || w.theater?.name || ''}）`
  }))
)

// 時間候補ボタンをクリックした時
function setTimeCandidate(time) {
  // 今日の日付と候補時間を結合
  const today = new Date().toISOString().split('T')[0]
  form.value.watchedDate = `${today}T${time}`
}

onMounted(fetchWorks)

async function handleSubmit(e) {
  e.preventDefault()

  // watched_atを日付+時間で構築
  let watchedAt = null
  if (form.value.watchedDate) {
    // datetime-localの形式はすでに "YYYY-MM-DDTHH:mm" なので秒を追加するだけ
    watchedAt = `${form.value.watchedDate}:00`
  }

  await request('/api/logs/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      work: Number(form.value.workId),
      run: form.value.runId ? Number(form.value.runId) : null,
      watched_at: watchedAt,
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
    <h1 class="mb-3">観劇ログを追加</h1>

    <p v-if="loading">作品一覧を読み込み中...</p>
    <p v-else-if="error">エラー: {{ error }}</p>

    <form v-else @submit="handleSubmit" class="mb-4">
      <div class="mb-3">
        <label class="form-label">作品</label>
        <Multiselect
          v-model="form.workId"
          :options="workOptions"
          :searchable="true"
          :close-on-select="true"
          placeholder="作品を検索..."
          :no-options-text="'見つかりません'"
          @select="onWorkChange"
        />
        
        <!-- 見つからない場合の2つのオプション -->
        <div class="mt-3 p-3 border rounded bg-light">
          <p class="mb-2 small text-muted">作品が見つからない場合:</p>
          
          <!-- オプション1: 詳細登録ページへ -->
          <button
            type="button"
            class="btn btn-sm btn-outline-primary me-2 mb-2"
            @click="router.push('/works/new')"
          >
            詳細登録ページで新規登録
          </button>
          
          <!-- オプション2: 簡易登録フォーム表示 -->
          <button
            type="button"
            class="btn btn-sm btn-outline-secondary mb-2"
            @click="showQuickForm = !showQuickForm"
          >
            {{ showQuickForm ? '簡易登録を閉じる' : 'ここで簡易登録' }}
          </button>
          
          <!-- 簡易登録フォーム -->
          <div v-if="showQuickForm" class="mt-3 p-3 border rounded bg-white">
            <h6 class="mb-3">簡易登録（DRAFT）</h6>
            <div class="mb-2">
              <label class="form-label small">タイトル *</label>
              <input
                type="text"
                class="form-control form-control-sm"
                v-model="quickForm.title"
                placeholder="作品名"
              />
            </div>
            <div class="mb-2">
              <label class="form-label small">劇団</label>
              <input
                type="text"
                class="form-control form-control-sm"
                v-model="quickForm.troupe"
                placeholder="劇団名"
              />
            </div>
            <div class="mb-2">
              <label class="form-label small">劇場</label>
              <input
                type="text"
                class="form-control form-control-sm"
                v-model="quickForm.theater"
                placeholder="劇場名"
              />
            </div>
            <button
              type="button"
              class="btn btn-sm btn-success"
              @click="handleQuickCreate"
            >
              登録して選択
            </button>
          </div>
        </div>
      </div>

      <div class="mb-3" v-if="form.workId && runs.length > 0">
        <label class="form-label">公演ブロック（任意）</label>
        <select class="form-select" v-model="form.runId">
          <option value="">選択なし</option>
          <option
            v-for="run in runs"
            :key="run.id"
            :value="run.id"
          >
            {{ run.label }}（{{ run.area }}）
          </option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label">観た日時</label>
        <input
          type="datetime-local"
          class="form-control"
          v-model="form.watchedDate"
        />
        <div v-if="todayTimes.length > 0" class="mt-2">
          <small class="text-muted">今日の公演候補:</small>
          <div class="d-flex gap-2 mt-1">
            <button
              v-for="time in todayTimes"
              :key="time"
              type="button"
              class="btn btn-sm btn-outline-secondary"
              @click="setTimeCandidate(time)"
            >
              {{ time }}
            </button>
          </div>
        </div>
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
        <label class="form-label">
          評価（1～5）
          <span v-if="form.rating" class="ms-2 badge bg-primary">
            {{ Number(form.rating).toFixed(1) }}
          </span>
        </label>
        <input
          type="range"
          min="1"
          max="5"
          step="0.1"
          class="form-range"
          v-model="form.rating"
        />
        <div class="d-flex justify-content-between text-muted small">
          <span>1.0</span>
          <span>3.0</span>
          <span>5.0</span>
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label">感想</label>
        <textarea
          class="form-control"
          rows="3"
          v-model="form.memo"
          style="min-height: 200px;"
        />
      </div>

      <button type="submit" class="btn btn-primary">
        保存
      </button>
    </form>
  </main>
</template><style src="@vueform/multiselect/themes/default.css"></style>
