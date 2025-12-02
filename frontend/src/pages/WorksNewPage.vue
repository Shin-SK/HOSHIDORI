<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { request } from '@/apiClient'
import Multiselect from '@vueform/multiselect'

const router = useRouter()

const theaters = ref([])
const actors = ref([])
const loading = ref(true)

const form = ref({
  title: '',
  theaterId: '',
  troupe: '',
  description: '',
  imageFile: null,
  tags: '',
  actorIds: [],  // 選択された俳優ID配列
  actorNames: [], // 新規入力された俳優名配列
})

const uploading = ref(false)
const error = ref(null)

// 劇場オプション
const theaterOptions = computed(() =>
  theaters.value.map(t => ({
    value: t.id,
    label: `${t.name}（${t.area || ''}）`
  }))
)

// 俳優オプション（既存 + 新規入力可能）
const actorOptions = computed(() =>
  actors.value.map(a => ({
    value: a.id,
    label: a.name
  }))
)

async function fetchData() {
  loading.value = true
  try {
    const [theatersData, actorsData] = await Promise.all([
      request('/api/theaters/'),
      request('/api/actors/')
    ])
    theaters.value = theatersData
    actors.value = actorsData
  } catch (e) {
    console.error('Failed to fetch data:', e)
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)

function onFileChange(e) {
  const file = e.target.files?.[0] || null
  form.value.imageFile = file
}

async function handleSubmit(e) {
  e.preventDefault()
  error.value = null
  uploading.value = true

  try {
    // 選択された俳優IDと新規入力された名前を処理
    const selectedActorIds = form.value.actorIds.filter(id => typeof id === 'number')
    const newActorNames = form.value.actorIds.filter(id => typeof id === 'string')
    
    // 新規俳優を作成
    const createdActors = await Promise.all(
      newActorNames.map(name =>
        request('/api/actors/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name })
        }).catch(() => null) // 重複エラーは無視
      )
    )
    
    // 作成された俳優のIDを追加
    const allActorIds = [
      ...selectedActorIds,
      ...createdActors.filter(a => a?.id).map(a => a.id)
    ]

    // まずcreate_or_get APIで作品を作成または取得
    const payload = {
      title: form.value.title,
      troupe: form.value.troupe || '',
      main_theater_id: form.value.theaterId ? Number(form.value.theaterId) : null,
    }

    const created = await request('/api/works/create_or_get/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    // 画像と俳優がある場合は別途PATCH
    if (created?.id) {
      const fd = new FormData()
      if (form.value.imageFile) {
        fd.append('main_image', form.value.imageFile)
      }
      if (allActorIds.length > 0) {
        allActorIds.forEach(id => fd.append('actors', id))
      }
      
      if (form.value.imageFile || allActorIds.length > 0) {
        await request(`/api/works/${created.id}/`, {
          method: 'PATCH',
          body: fd,
        })
      }
    }

    // 作品作成 → ログ新規作成画面へ
    const workId = created?.id
    if (workId) {
      router.push(`/logs/new?work=${workId}`)
    } else {
      router.push('/logs/new')
    }
  } catch (e) {
    console.error(e)
    error.value = e.message
  } finally {
    uploading.value = false
  }
}
</script>

<template>
  <main class="container py-4">
    <h1 class="mb-3">作品を追加（画像付き）</h1>

    <p v-if="loading">データ読み込み中...</p>

    <form v-else @submit="handleSubmit" class="mb-4">
      <div class="mb-3">
        <label class="form-label">タイトル</label>
        <input
          type="text"
          class="form-control"
          v-model="form.title"
          required
        />
      </div>

      <div class="mb-3">
        <label class="form-label">劇場</label>
        <Multiselect
          v-model="form.theaterId"
          :options="theaterOptions"
          :searchable="true"
          :close-on-select="true"
          placeholder="劇場を検索..."
          :no-options-text="'見つかりません'"
        />
      </div>

      <div class="mb-3">
        <label class="form-label">劇団名（任意）</label>
        <input
          type="text"
          class="form-control"
          v-model="form.troupe"
        />
      </div>

      <div class="mb-3">
        <label class="form-label">作品説明（任意）</label>
        <textarea class="form-control" rows="4" v-model="form.description" />
      </div>

      <div class="mb-3">
        <label class="form-label">作品画像</label>
        <input
          type="file"
          class="form-control"
          accept="image/*"
          @change="onFileChange"
        />
      </div>

      <div class="mb-3">
        <label class="form-label">タグ（任意・カンマ区切り）</label>
        <input
          type="text"
          class="form-control"
          v-model="form.tags"
          placeholder="例: 会話劇, コメディ, 一人芝居"
        />
        <small class="text-muted">複数のタグをカンマで区切って入力</small>
      </div>

      <div class="mb-3">
        <label class="form-label">出演者（複数選択可・新規入力可）</label>
        <Multiselect
          v-model="form.actorIds"
          :options="actorOptions"
          mode="tags"
          :searchable="true"
          :create-option="true"
          placeholder="出演者を選択または入力..."
          :no-options-text="'見つかりません'"
        />
        <small class="text-muted">
          既存の出演者から選択、または新しい名前を入力してEnterで追加
        </small>
      </div>

      <button type="submit" class="btn btn-primary" :disabled="uploading">
        {{ uploading ? '保存中…' : '作品を保存してログ追加へ' }}
      </button>
    </form>

    <p v-if="error" class="text-danger">エラー: {{ error }}</p>
  </main>
</template>

<style src="@vueform/multiselect/themes/default.css"></style>