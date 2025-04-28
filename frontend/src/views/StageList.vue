<!-- src/views/StageList.vue -->
<template>
	<section class="stage mb-footer">
	  <!-- ■ 検索フォーム -->
	   <div class="header-stage">
			<div class="logo">
				<router-link to="/stage" class="logo"><img src="/img/logo.svg" /></router-link>
			</div>
			<div class="search-form">
				<form @submit.prevent="doSearch">
				<div class="input-wrap">
					<input
					v-model="searchTerm"
					type="text"
					placeholder="検索"
					/>
					<button type="submit">
					<i class="fas fa-search" />
					</button>
				</div>
				</form>
			</div>
	   </div>

  
	  <!-- ■ ローディング / エラー -->
	  <p v-if="error" class="text-red-600">{{ error }}</p>
	  <p v-else-if="loading">Loading…</p>
  
	  <!-- ■ ステージ一覧 -->
	  <div v-else class="stagelist lists">
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
  
			<div class="wrap" style="display: none;">
			  <ul>
				<!-- Cast -->
				<li
				  v-for="(c, idx) in stage.credits.filter(cr => cr.role === 'cast')"
				  :key="'cast-' + idx"
				>
				  <router-link
					:to="{ name: 'stage-list', query: { search: c.person.name } }"
				  >
					{{ c.person.name }}
				  </router-link>
				</li>
  
				<!-- スタッフがあれば区切り -->
				<li
				  v-if="stage.credits.some(cr => cr.role === 'cast') &&
						 stage.credits.some(cr => cr.role === 'staff')"
				>
				  /
				</li>
  
				<!-- Staff -->
				<li
				  v-for="(s, idx) in stage.credits.filter(cr => cr.role === 'staff')"
				  :key="'staff-' + idx"
				>
				  <router-link
					:to="{ name: 'stage-list', query: { search: s.person.name } }"
				  >
					{{ s.person.name }}
				  </router-link>
				</li>
			  </ul>
			</div>
		  </div>
		</div>
  
		<p v-if="stages.length === 0">舞台情報がありません</p>
  
		<!-- 新規作成ボタン -->
		<div class="stage__wrap stage-create">
		  <div class="box">
			<router-link to="/stage/create/">
			  <i class="fas fa-plus" />
			</router-link>
		  </div>
		</div>
	  </div>
	</section>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import apiClient from '@/services/api.js'
  
  const route       = useRoute()
  const router      = useRouter()
  
  /* ---------- state ---------- */
  const stages     = ref([])
  const loading    = ref(true)
  const error      = ref(null)
  const searchTerm = ref(route.query.search || '')
  
  /* ---------- fetch ---------- */
  const fetchStages = async () => {
	try {
	  loading.value = true
	// ▼ URL のクエリをそのまま API に流す（search も上書き）
	const res = await apiClient.get('/api/stage/', {
	params: { ...route.query, search: searchTerm.value || undefined }
	})
	  stages.value = res.data        // credits 配列込みで返ってくる
	} catch (e) {
	  error.value = e.message
	} finally {
	  loading.value = false
	}
  }
  
  /* ---------- handlers ---------- */
  const doSearch = () => {
	router.push({
	name : 'stage-list',
	query: { ...route.query, search: searchTerm.value || undefined }
	})
  }
  
  /* ---------- effects ---------- */
  fetchStages()                                  // 初回
  watch(() => route.query, () => fetchStages(), { deep: true })
  </script>
  