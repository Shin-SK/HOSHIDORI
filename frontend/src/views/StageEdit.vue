<!-- StageEdit.vue -->
<template>
	<section class="form-update container">
	  <h2>舞台追加・編集</h2>
  
	  <!-- エラー／ローディング -->
	  <p v-if="error" class="text-red-600">{{ error }}</p>
	  <p v-else-if="loading">Loading…</p>
  
	  <!-- ───────── フォーム ───────── -->
	  <form
		v-else
		@submit.prevent="submitStage"
		enctype="multipart/form-data"
	  >
		<!-- ポスター -->
		<div class="poster-outer">
		  <!-- 旧ポスター -->
		  <div class="field current-poster">
			<img
			  v-if="stage.poster_url"
			  :src="stage.poster_url"
			  :alt="stage.title"
			/>
		  </div>
		  <div class="field icon"><i class="fas fa-chevron-right" /></div>
  
		  <!-- 新ポスター upload -->
		  <div class="field poster">
			<input
			  id="poster-upload"
			  type="file"
			  accept="image/*"
			  class="filepond"
			/>
		  </div>
		</div>
  
		<!-- タイトル -->
		<div class="field stage-title">
		  <input
			v-model="stage.title"
			type="text"
			placeholder="タイトル"
			required
		  />
		</div>
  
		<!-- キャスト (カンマ区切り) -->
		<div class="field cast">
		  <textarea
			v-model="castText"
			rows="3"
			placeholder="キャスト (カンマ区切り)"
		  />
		</div>
  
		<!-- スタッフ (カンマ区切り) -->
		<div class="field staff">
		  <textarea
			v-model="staffText"
			rows="3"
			placeholder="スタッフ (カンマ区切り)"
		  />
		</div>
  
		<button type="submit">保存</button>
	  </form>
	</section>
  </template>
  
  <script setup>
  import { ref, onMounted, nextTick, watch } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import apiClient from '@/services/api.js'
  
  /* ---------- FilePond ---------- */
  import * as FilePond from 'filepond'
  import FilePondPluginImagePreview from 'filepond-plugin-image-preview'
  import 'filepond/dist/filepond.min.css'
  import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css'
  FilePond.registerPlugin(FilePondPluginImagePreview)
  
  /* ---------- route / state ---------- */
  const route   = useRoute()
  const router  = useRouter()
  const stageId = route.params.id                // null のときは “新規”
  
  const stage       = ref({ title: '', poster_url: '' })
  const castText    = ref('')                    // textarea 用
  const staffText   = ref('')
  const posterFile  = ref(null)
  
  const loading = ref(true)
  const error   = ref(null)
  
  /* ---------- FilePond ---------- */
  const mountFilePond = () => {
	const el = document.getElementById('poster-upload')
	if (!el || el._pond) return
  
	FilePond.create(el, {
	  allowMultiple : false,
	  storeAsFile   : true,
	  labelIdle     : '<i class="fas fa-plus"></i>',
	  server: {
		process: (_field, file, _meta, load) => { posterFile.value = file; load() },
		revert : (_uid,   load)              => { posterFile.value = null; load() }
	  }
	})
  }
  
  /* ---------- helpers ---------- */
  const splitNames = (str) =>
	str ? str.split(/[,、]/).map(s => s.trim()).filter(Boolean) : []
  
  /* ---------- fetch ---------- */
  onMounted(async () => {
	try {
	  if (stageId) {
		const res = await apiClient.get(`/api/stage/${stageId}/`)
		stage.value = res.data
  
		// credits → textarea 表示用文字列へ
		const credits = res.data.credits || []
		castText.value  = credits
		  .filter(c => c.role === 'cast')
		  .map(c => c.person.name).join(', ')
		staffText.value = credits
		  .filter(c => c.role === 'staff')
		  .map(c => c.person.name).join(', ')
	  }
	} catch (e) {
	// ★ ここを強化
	console.error('AXIOS ERROR →', {
		message : e.message,
		status  : e.response?.status,
		data    : e.response?.data,
		config  : e.config
	})
	} finally {
	  loading.value = false
	  await nextTick()
	  mountFilePond()
	}
  })
  
  /* ---------- submit ---------- */
  const submitStage = async () => {
  try {
    // ① credits を一次元配列で組み立て
    const credits = [
	  ...splitNames(castText.value).map(n => ({ person_name: n, role: 'cast' })),
	  ...splitNames(staffText.value).map(n => ({ person_name: n, role: 'staff' }))
    ]

    // ② multipart で送信
    const fd = new FormData()
    fd.append('title', stage.value.title)
    fd.append('credits_raw', JSON.stringify(credits))   // ★ 文字列で送信
	if (posterFile.value) fd.append('poster_file', posterFile.value)

    const url  = stageId ? `/api/stage/${stageId}/` : '/api/stage/'
    const verb = stageId ? apiClient.patch : apiClient.post
    await verb(url, fd, { headers: { 'Content-Type': 'multipart/form-data' } })

    // ③ 完了 → 詳細へ遷移
    router.push({ name: 'stage-detail', params: { id: stageId || 'new' } })
  } catch (e) {
	console.log('server response', e.response?.data)
    error.value = e.message
    console.error('[submit error]', e)
  }
}

  </script>
  