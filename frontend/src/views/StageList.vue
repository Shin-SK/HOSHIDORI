<!-- src/views/StageList.vue -->
<template>
	<section class="stage mb-footer">
	  <!-- ■ 検索フォーム -->
	  <div class="search-form">
		<form @submit.prevent="doSearch">
		  <div class="input-wrap">
			<input
			  v-model="searchTerm"
			  type="text"
			  placeholder="舞台タイトル・出演者・スタッフで検索"
			/>
			<button type="submit">
			  <i class="fas fa-search" />
			</button>
		  </div>
		</form>
	  </div>
  
	  <div class="mainTitle">舞台一覧</div>
  
	  <!-- ■ 状態表示 -->
	  <p v-if="error" class="text-red-600">{{ error }}</p>
	  <p v-else-if="loading">Loading…</p>
  
	  <!-- ■ ステージ一覧 -->
	  <div v-else class="stagelist lists">
		<!-- ── ループ ─────────────────────────── -->
		<div
		  v-for="stage in stages"
		  :key="stage.id"
		  class="lists__wrap"
		>
		  <!-- ポスター -->
		  <div class="poster">
			<router-link :to="{ name: 'stage-detail', params: { id: stage.id } }">
			  <img
				v-if="stage.poster_url"
				:src="stage.poster_url"
				:alt="stage.title"
			  />
			  <span v-else class="noimage">No&nbsp;Poster</span>
			</router-link>
		  </div>
  
		  <!-- タイトル + Cast / Staff -->
		  <div class="text-area">
			<div class="title">
			  <router-link :to="{ name: 'stage-detail', params: { id: stage.id } }">
				{{ stage.title }}
			  </router-link>
			</div>
  
			<div class="wrap">
			  <ul>
				<!-- Cast -->
				<li
				  v-for="(person, idx) in splitNames(stage.cast)"
				  :key="'cast-' + idx"
				>
				  <router-link
					:to="{ name: 'stage-list', query: { search: person } }"
				  >
					{{ person }}
				  </router-link>
				</li>
  
				<li v-if="splitNames(stage.staff).length"> / </li>
  
				<!-- Staff -->
				<li
				  v-for="(staff, idx2) in splitNames(stage.staff)"
				  :key="'staff-' + idx2"
				>
				  <router-link
					:to="{ name: 'stage-list', query: { search: staff } }"
				  >
					{{ staff }}
				  </router-link>
				</li>
			  </ul>
			</div>
		  </div>
		</div>
  
		<!-- ステージが 0 件のとき -->
		<p v-if="stages.length === 0">舞台情報がありません</p>
  
		<!-- 新規作成ボタン -->
		<div class="stage__wrap stage-create">
		  <div class="box">
			<router-link to="/stage/create">
			  <i class="fas fa-plus" />
			</router-link>
		  </div>
		</div>
	  </div>
	</section>
  </template>
  
<script>
  import { watch, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import apiClient from '@/services/api.js'
  
  export default {
	name: 'StageList',
	setup () {
	  const route = useRoute()
	  const router = useRouter()
  
	  /* ---------- state ---------- */
	  const stages = ref([])
	  const loading = ref(true)
	  const error = ref(null)
	  const searchTerm = ref(route.query.search || '')
  
	  /* ---------- fetch ---------- */
	  const fetchStages = async () => {
		try {
		  loading.value = true
		  error.value = null
		  const res = await apiClient.get('/api/stage/', {
			params: { search: searchTerm.value || undefined }
		  })
		  stages.value = res.data
		} catch (e) {
		  error.value = e.message
		} finally {
		  loading.value = false
		}
	  }
  
	  /* ---------- handlers ---------- */
	  const doSearch = () => {
		router.push({ name: 'stage-list', query: { search: searchTerm.value } })
	  }
  
	  /* ---------- utilities ---------- */
		/** キャスト／スタッフの文字列を配列に変換 */
		const splitNames = (str) => {
		if (!str) return []
		return str
			.split(/[,、]/)            // 半角・全角カンマどちらも区切り文字
			.map(s => s.trim())
			.filter(Boolean)
		}
  
	  /* ---------- effects ---------- */
	  // 初回 & クエリ変更時に再取得
	  fetchStages()
	  watch(() => route.query.search, (newVal) => {
		searchTerm.value = newVal || ''
		fetchStages()
	  })
  
	  return {
		stages,
		loading,
		error,
		searchTerm,
		doSearch,
		splitNames
	  }
	}
  }
</script>
  