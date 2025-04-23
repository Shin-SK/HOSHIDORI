<!-- src/views/LoginView.vue -->
<template>
	<section class="login allauth form-update">
	  <!-- エラーメッセージ -->
	  <div v-if="error" class="text-red-600">{{ error }}</div>
  
	  <form @submit.prevent="loginUser">
		<div class="logo">
		  <img src="/img/logo.svg" alt="">
		</div>
  
		<div class="field">
		  <label>メールアドレスまたはユーザー名</label>
		  <input v-model="form.username" />
		</div>
  
		<div class="field">
		  <label>パスワード</label>
		  <input v-model="form.password" type="password" />
		</div>
  
		<div class="field create-account">
		  <p>アカウントをお持ちでない方は<br />
			<router-link to="/signup">新規登録</router-link>
		  </p>
		</div>
  
		<div class="field submit-button">
		  <button type="submit">ログイン</button>
		</div>
	  </form>
	</section>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import apiClient from '@/services/api.js'
  import { useAuth } from '@/services/useAuth.js'
  
  const router = useRouter()
  
  // v-model で使うデータは reactive() でも OK
  const form  = ref({ username: '', password: '' })
  const error = ref(null)
  const { setTokens } = useAuth()
  
  // ★ テンプレートと同じ名前にする
  const loginUser = async () => {
	error.value = null
	try {
	  const body = {
		username: form.value.username,
		password: form.value.password
	  }
	  const { data } = await apiClient.post('/dj-rest-auth/jwt/create/', body)
	  setTokens(data.access, data.refresh)
	  router.push('/stage')           // 任意の遷移先
	} catch (e) {
	  error.value = 'ログイン失敗：' +
		(e.response?.data?.detail || e.message)
	}
  }
  </script>
  