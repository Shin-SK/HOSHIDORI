<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '@/supabaseClient'

const router = useRouter()

const form = ref({
  title: '',
  theaterId: '',   // ひとまず数値入力。後でセレクトにしてもOK
  troupe: '',
  startDate: '',
  endDate: '',
  imageFile: null,
  tags: '',        // カンマ区切りで入力
  actors: '',      // カンマ区切りで入力
})

const uploading = ref(false)
const error = ref(null)
const uploadedUrl = ref('')

function onFileChange(e) {
  const file = e.target.files?.[0] || null
  form.value.imageFile = file
}

async function uploadImageIfNeeded() {
  if (!form.value.imageFile) return null

  const file = form.value.imageFile
  const ext = file.name.split('.').pop()
  const fileName = `${crypto.randomUUID()}.${ext}`
  const filePath = `main/${fileName}`

  const { error: uploadError } = await supabase.storage
    .from('works')
    .upload(filePath, file)

  if (uploadError) {
    console.error('upload error', uploadError)
    throw uploadError
  }

  const { data } = supabase.storage.from('works').getPublicUrl(filePath)
  return data.publicUrl
}

async function handleSubmit(e) {
  e.preventDefault()
  error.value = null
  uploadedUrl.value = ''
  uploading.value = true

  try {
    const imageUrl = await uploadImageIfNeeded()

    // Nextの /api/works に作品を登録
    const tags = form.value.tags
      ? form.value.tags.split(',').map(t => t.trim()).filter(Boolean)
      : []
    const actors = form.value.actors
      ? form.value.actors.split(',').map(a => a.trim()).filter(Boolean)
      : []

    await fetch('/api/works', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: form.value.title,
        theaterId: Number(form.value.theaterId),
        troupe: form.value.troupe || null,
        startDate: form.value.startDate || null,
        endDate: form.value.endDate || null,
        imageUrl,
        tags,
        actors,
      }),
    })

    // 作品作成 → ログ新規作成画面へ
    router.push('/logs/new')
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

    <form @submit="handleSubmit" class="mb-4">
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
        <label class="form-label">劇場ID（仮）</label>
        <input
          type="number"
          class="form-control"
          v-model="form.theaterId"
          placeholder="1 など"
          required
        />
        <!-- 本当は /api/theaters から劇場一覧を取ってセレクトにする -->
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
        <label class="form-label">公演開始日</label>
        <input
          type="date"
          class="form-control"
          v-model="form.startDate"
        />
      </div>

      <div class="mb-3">
        <label class="form-label">公演終了日</label>
        <input
          type="date"
          class="form-control"
          v-model="form.endDate"
        />
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
        <label class="form-label">出演者（任意・カンマ区切り）</label>
        <input
          type="text"
          class="form-control"
          v-model="form.actors"
          placeholder="例: 山田太郎, 佐藤花子"
        />
        <small class="text-muted">複数の出演者をカンマで区切って入力</small>
      </div>

      <button type="submit" class="btn btn-primary" :disabled="uploading">
        {{ uploading ? '保存中…' : '作品を保存してログ追加へ' }}
      </button>
    </form>

    <p v-if="error" class="text-danger">エラー: {{ error }}</p>
  </main>
</template>