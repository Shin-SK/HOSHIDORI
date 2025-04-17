<template>
	<section class="form-update container">
	  <h2>舞台追加・編集</h2>
  
	  <!-- エラー -->
	  <p v-if="error" class="text-red-600">{{ error }}</p>
	  <p v-else-if="loading">Loading…</p>
  
	  <!-- フォーム -->
	  <form
		v-else
		@submit.prevent="submitStage"
		enctype="multipart/form-data"
	  >
		<!-- ── ポスター ───────────────────────────── -->

		<div class="poster-outer">
			<div class="field current-poster">
				<img
					v-if="stage.poster_url"
					:src="stage.poster_url"
					:alt="stage.title"
				/>
			</div>
			<div class="field icon">
				<i class="fas fa-chevron-right"></i>
			</div>
			<div class="field poster">
			<input
				id="poster-upload"
				type="file"
				accept="image/*"
				class="filepond"
			/>
			</div>
		</div>

  
		<!-- ── タイトル ───────────────────────────── -->
		<div class="field stage-title">
		  <input
			v-model="stage.title"
			type="text"
			placeholder="タイトル"
			required
		  />
		</div>
  
		<!-- ── 出演者 ───────────────────────────── -->
		<div class="field cast">
		  <textarea
			v-model="stage.cast"
			rows="3"
			placeholder="キャスト (カンマ区切り)"
		  />
		</div>
  
		<!-- ── スタッフ ───────────────────────────── -->
		<div class="field staff">
		  <textarea
			v-model="stage.staff"
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
  
  /* ------- FilePond ------- */
  import * as FilePond from 'filepond'
  import FilePondPluginImagePreview from 'filepond-plugin-image-preview'
  import 'filepond/dist/filepond.min.css'
  import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css'
  FilePond.registerPlugin(FilePondPluginImagePreview)
  
  /* ------- state / router ------- */
  const route   = useRoute()
  const router  = useRouter()
  const stageId = route.params.id
  
  const stage      = ref({ title: '', cast: '', staff: '' })
  const loading    = ref(true)
  const error      = ref(null)
  const posterFile = ref(null)
  
  /* ------- FilePond 初期化関数 ------- */
  const mountFilePond = () => {
	const el = document.getElementById('poster-upload')
	if (!el) return                        // まだ描画されていない
	if (el._pond) return                   // 2回目以降はスキップ
  
	FilePond.create(el, {
	  allowMultiple : false,
	  storeAsFile   : true,
	  labelIdle     : '<i class="fas fa-plus"></i>',
	  server: {
		process: (field, file, md, load) => { posterFile.value = file; load() },
		revert : (uid,   load)           => { posterFile.value = null; load() }
	  }
	})
  }
  
  /* ------- fetch -------- */
  onMounted(async () => {
	try {
	  stage.value = (await apiClient.get(`/api/stage/${stageId}/`)).data
	} catch (e) {
	  error.value = e.message
	} finally {
	  loading.value = false
	}
  })
  
  /* loading が false になった “次の DOM 更新後” に FilePond を作成 */
  watch(loading, async (val) => {
	if (!val) {
	  await nextTick()
	  mountFilePond()
	}
  })
  
  /* ------- submit -------- */
  const submitStage = async () => {
	try {
	  const fd = new FormData()
	  fd.append('title', stage.value.title)
	  fd.append('cast',  stage.value.cast)
	  fd.append('staff', stage.value.staff)
	  if (posterFile.value) fd.append('poster_file', posterFile.value)
  
	  await apiClient.put(
		`/api/stage/${stageId}/`,
		fd,
		{ headers: { 'Content-Type': 'multipart/form-data' } }
	  )
	  router.push(`/stage/${stageId}`)
	} catch (e) {
	  error.value = e.message
	  console.error('[submit error]', e)
	}
  }
  </script>
  

  

