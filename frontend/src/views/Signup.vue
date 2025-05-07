<!-- src/views/Signup.vue -->
<template>
	<section class="form auth-form container signup">
	  <h1>新規登録</h1>
  
	  <!-- ▼ サーバー共通エラー -->
	  <p v-if="nonFieldError" class="text-red-600">{{ nonFieldError }}</p>
  
	  <form @submit.prevent="handleSubmit" enctype="multipart/form-data">
		<!-- メール -->
		<div class="field">
		  <label for="email">メールアドレス</label>
		  <input id="email" v-model.trim="form.email" type="email" required />
		  <p v-if="errors.email" class="error">{{ errors.email }}</p>
		</div>
  
		<!-- パスワード -->
		<div class="field">
		  <label for="pw1">パスワード</label>
		  <input id="pw1" v-model.trim="form.password1" type="password" required />
		  <p v-if="errors.password1" class="error">{{ errors.password1 }}</p>
		</div>
  
		<!-- パスワード確認 -->
		<div class="field">
		  <label for="pw2">パスワード（確認）</label>
		  <input id="pw2" v-model.trim="form.password2" type="password" required />
		  <p v-if="errors.password2" class="error">{{ errors.password2 }}</p>
		</div>

  		<!-- ユーザーネーム -->
		  <div class="field">
		  <label for="username">ユーザーID(英数字6〜20字/あとで変更できます)</label>
			<input id="username" v-model.trim="form.username" pattern="[A-Za-z0-9_]{6,20}" required />
		  <p v-if="errors.username" class="error">{{ errors.usernam }}</p>
		</div>

		<!-- ニックネーム -->
		<div class="field">
		  <label for="nickname">ユーザーネーム(あとで変更できます)</label>
		  <input id="nickname" v-model.trim="form.nickname" required />
		  <p v-if="errors.nickname" class="error">{{ errors.nickname }}</p>
		</div>
  
		<!-- アイコン画像を使うなら
		<div class="field">
		  <label for="icon">アイコン画像（任意）</label>
		  <input id="icon" type="file" @change="onFileChange" accept="image/*" />
		  <p v-if="errors.icon" class="error">{{ errors.icon }}</p>
		</div>
		-->
  
		<button type="submit" :disabled="loading">
		  {{ loading ? '送信中…' : '登録する' }}
		</button>
	  </form>
  
	  <div class="login">
		<p>すでにアカウントをお持ちの方は</p>
		<router-link :to="{ name: 'login' }">ログイン</router-link>
	  </div>
	</section>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import apiClient from '@/services/api.js'      // axios ラッパー
  
  const router        = useRouter()
  const loading       = ref(false)
  const nonFieldError = ref('')
  const errors        = ref({})                 // 各フィールドのエラー
  
  // フォーム state
  const form = ref({
	email: '',
	password1: '',
	password2: '',
	username: '',
	nickname: '',
	// icon: null,
  })
  
  const onFileChange = e => {
	form.value.icon = e.target.files[0] ?? null
  }
  
  /* ---------- submit ---------- */
  const handleSubmit = async () => {
	loading.value = true
	nonFieldError.value = ''
	errors.value = {}
  
	try {
	  // FormData にして multipart 送信（画像を使わないなら普通の JSON で OK）
	  const fd = new FormData()
	  Object.entries(form.value).forEach(([k, v]) => {
		if (v !== null && v !== '') fd.append(k, v)
	  })
  
	  await apiClient.post('/dj-rest-auth/registration/', fd, {
		headers: { 'Content-Type': 'multipart/form-data' },
	  })
  
	  alert('登録が完了しました！')
	  router.push('/login')
	} catch (e) {
	  const data = e.response?.data || {}
	  nonFieldError.value = data.detail || ''
	  errors.value = { ...data }                 // そのまま突っ込む（key は field 名）
	} finally {
	  loading.value = false
	}
  }
  </script>
  
  <style scoped>
  .field { margin-bottom: 1rem; }
  .error { color: #e11d48; font-size: .875rem; }
  button { width: 100%; }
  </style>
  