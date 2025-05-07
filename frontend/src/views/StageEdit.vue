<!-- StageEdit.vue -->
<template>
	<section class="form-update">

	<h2>{{ isCreate ? '新規追加' : '編集' }}</h2>
  
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
		<div class="field poster">
		  <!-- 旧ポスター -->

			<div v-if="!isCreate" class="item current-poster">
					<img
					v-if="stage.poster_url"
					:src="stage.poster_url"
					:alt="stage.title"
					/>
			</div>

			<div v-if="!isCreate" class="arrow"><i class="fas fa-chevron-right" /></div>

			<!-- 新ポスター upload -->
			<div class="item new-poster">
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

		<div class="field">
			<input v-model="keyword" placeholder="劇場名を入力" />
			<ul v-if="options.length || showNew">
				<li
					v-for="t in options"
					:key="t.id"
					@click="theaterId = t.id; keyword = t.name"
				>
					{{ t.name }}
				</li>

				<!-- 候補に同名が無いときだけ ↓ が出る -->
				<li v-if="showNew" @click="openModal" class="new">
				「{{ keyword }}」を新規追加
				</li>
			</ul>
		</div>

		<button type="submit">保存</button>
	  </form>
	</section>

	<!-- ---------- 新規劇場モーダル ---------- -->
	<div v-if="showModal" class="modal-backdrop">
	<div class="modal">
		<h3>劇場を新規追加</h3>

		<input
		v-model="theaterInput"
		placeholder="劇場名を入力"
		@keyup.enter="saveTheater"
		/>

		<div class="modal-buttons">
		<button @click="saveTheater" :disabled="!theaterInput">追加</button>
		<button @click="showModal = false">キャンセル</button>
		</div>
	</div>
	</div>

</template>

  <script setup>
  import { ref, onMounted, nextTick, watch, computed } from 'vue'
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
  const stageId = route.params.id // null のときは “新規”

  const isCreate = computed(() => !stageId) // ★ ここだけで判定 OK

  const stage       = ref({ title: '', poster_url: '' })
  const castText    = ref('') // textarea 用
  const staffText   = ref('')
  const posterFile  = ref(null)
  
  const loading = ref(true)
  const error   = ref(null)
  
  const keyword   = ref('')
  const options   = ref([])    // サジェスト用
  const theaterId = ref(null)  // 選択済み ID
  
  const showModal      = ref(false)   // モーダル開閉
  const theaterInput   = ref('')      // モーダル内テキストボックス


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

/* ---------- オートサジェスト ---------- */
watch(keyword, async (v) => {
  if (!v) { options.value = []; return }
  const { data } = await apiClient.get('/api/theater/', { params: { q: v } })
  options.value = data             // [{ id, name }, ...]
})

/* ---------- 新規追加 ---------- */
const showNew = computed(() => {
  const k = keyword.value.trim()
  if (!k) return false
  return !options.value.some(t =>
    t.name.toLowerCase() === k.toLowerCase()
  )
})

function openModal () {
  theaterInput.value = ''           // 毎回空にする（初期値入れたければ keyword.value）
  showModal.value    = true
}

async function saveTheater () {
  const name = theaterInput.value.trim()
  if (!name) return

  try {
    const { data } = await apiClient.post('/api/theater/', { name })
    options.value.unshift(data)   // 新規を候補の先頭へ
    theaterId.value = data.id
    keyword.value   = data.name   // 検索窓にも反映
    showModal.value = false       // モーダル閉じる
  } catch (e) {
    console.error(e)
    alert('登録に失敗しました')
  }
}

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

    const url   = stageId ? `/api/stage/${stageId}/` : '/api/stage/'
    const verb = stageId ? apiClient.patch : apiClient.post
    await verb(url, fd, { headers: { 'Content-Type': 'multipart/form-data' } })

    // ③ 完了 → 詳細へ遷移
	const destId = stageId || data.id          // ← 新規時だけ API 返却 id
    router.push({ name:'stage-detail', params:{ id: destId } })
  } catch (e) {
	console.log('server response', e.response?.data)
    error.value = e.message
    console.error('[submit error]', e)
  }
}

  </script>
  
<style>
.modal-backdrop{position:fixed;inset:0;background:#0006;display:flex;justify-content:center;align-items:center;z-index:999}
.modal{background:#fff;padding:24px;border-radius:6px;width:90%;max-width:360px}
.modal-buttons{display:flex;gap:8px;margin-top:16px;justify-content:flex-end}
</style>