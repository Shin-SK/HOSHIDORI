<!-- src/views/LogEdit.vue -->
<template>
	<section class="form-update log-form container">
	  <h2>{{ mode === 'create' ? 'ログ追加' : 'ログ編集' }}</h2>
  
	  <p v-if="error" class="text-red-600">{{ error }}</p>
	  <p v-else-if="loading">Loading…</p>
  
	  <form v-else @submit.prevent="handleSubmit">
		<!-- ステータス -->
		<div class="field radio" style="display: none;">
			<div
				class="radio__wrap"
				v-for="opt in statusOptions"
				:key="opt.value"
			>
				<input
				type="radio"
				name="status"
				:id="`status_${opt.value}`"
				:value="opt.value"
				v-model="form.status"
				required
				/>
				<label :for="`status_${opt.value}`">
				<i :class="opt.icon"></i>
				{{ opt.label }}
				</label>
			</div>
		</div>

  
		<!-- 観劇回数 -->
		<div class="field">
		<label for="times-input">観劇回数</label>
		<input
			id="times-input"
			v-model.number="form.times"
			type="number"
			min="1"
		/>
		</div>

		<!-- レビュー評価（クリックで 1〜5 を選択） -->
		<div class="field star-rating">
		<label>レビュー評価</label><br />

		<!-- ☆ここiconをfontawsomeからさっき作ったscssのオリジナルに変更したい。
		選択されてないやつはicon-star-line 選択されてるやつはicon-star -->
		<i
			v-for="n in 5"
			:key="n"
			:class="['', n <= form.rating ? 'icon-star' : 'icon-star-line']"
			:data-value="n"
			@click="form.rating = n"
		/>

		<!-- 送信用の hidden input。必要なら name を付けても OK -->
		<input type="hidden" id="rating-input" :value="form.rating" />
		</div>

		<!-- コメント -->
		<div class="field">
		<label for="comment-input">コメント</label>
		<textarea
			id="comment-input"
			v-model="form.comment"
			rows="4"
			placeholder="コメント"
		/>
		</div>

  
		<button type="submit">{{ mode === 'create' ? '作成' : '更新' }}</button>
	  </form>
	</section>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import apiClient from '@/services/api.js'
  
  /* ---------- props ---------- */
  const props = defineProps({
	mode: { type: String,  required: true },  // 'create' | 'edit'
	id  : { type: [String, Number], default: null } // ← 編集時の logId
  })
  
  const mode   = props.mode
  const logId  = props.id           // create 時は null
  
  /* ---------- router / route ---------- */
  const route  = useRoute()
  const router = useRouter()
  
	/* ★ 追記: クエリから初期 status を拾う（無ければ null） ★ */
	const initStatus = route.query.toStatus || null

  /* route から取れる stageId (create 時のみ入っている) */
  const stageIdFromRoute = Number(route.params.stageId) || null
  
  /* ---------- state ---------- */
  const loading = ref(mode === 'edit')
  const error   = ref(null)
  
  const form = ref({
	status : initStatus || 'watched',
	times  : 1,
	rating : 0,
	comment: '',
	// edit 時は後で API から上書きされる
	stage  : stageIdFromRoute        // create 時はここに数値 id を保持
  })
  
  /* ---------- util: 最終的な stageId を計算 ---------- */
  const stageId = computed(() => {
	// ⚫︎ create ルート: route.params.stageId がある
	if (stageIdFromRoute) return stageIdFromRoute
	// ⚫︎ edit ルート: form.stage は {id:…} か 数値 のどちらか
	const s = form.value.stage
	return typeof s === 'object' ? s.id : Number(s)
  })
  
  /* ---------- status ラジオ用オプション ---------- */
  const statusOptions = [
	{ value: 'watched', label: '観た',     icon: 'fas fa-eye'       },
	{ value: 'want',    label: '観たい',   icon: 'fas fa-heart'     },
	{ value: 'cannot',  label: '観れない', icon: 'fas fa-eye-slash' }
  ]
  
  /* ---------- 既存ログ取得 (edit) ---------- */
  onMounted(async () => {
	if (mode !== 'edit') return
	try {
	  const res = await apiClient.get(`/api/log/${logId}/`)
	  form.value = { ...form.value, ...res.data }   // ← stage も入る
	  if (initStatus) form.value.status = initStatus
	} catch (e) {
	  error.value = e.message
	} finally {
	  loading.value = false
	}
  })
  
  /* ---------- submit ---------- */
  const handleSubmit = async () => {
	try {
	  if (mode === 'create') {
		/* ------ 新規作成 ------ */
		await apiClient.post('/api/log/', {
		  stage_id: stageId.value,     
		  status  : form.value.status,
		  times   : form.value.times,
		  rating  : form.value.rating,
		  comment : form.value.comment
		})
	  } else {
		/* ------ 編集更新 ------ */
		await apiClient.put(`/api/log/${logId}/`, {
		  stage_id: stageId.value,
		  status : form.value.status,
		  times  : form.value.times,
		  rating : form.value.rating,
		  comment: form.value.comment
		})
	  }
	  /* 共通: 完了後にステージ詳細へ遷移 */
	  router.push({ name: 'stage-detail', params: { id: stageId.value } })
	} catch (e) {
		console.error(e.response?.data || e.message)        // ← ここで詳細を確認
		error.value = JSON.stringify(e.response?.data)      // ← 画面にも表示
		|| e.message
	}
  }
  </script>
  

  