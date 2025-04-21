<template>
	<section class="login allauth form-update">
	  <div v-if="error">{{ error }}</div>
	  <form @submit.prevent="loginUser">
		<div class="logo">
			<img src="/img/logo.svg" alt="">
		</div>
		<div class="field">
			<label for="">メールアドレスまたはユーザー名</label>
			<input v-model="form.username">
		</div>
		<div class="field">
			<label for="">パスワード</label>
			<input v-model="form.password" type="password">
		</div>

		<div class="field create-account">
			<p>アカウントをお持ちでない方は<br>
				<router-link to="">新規登録</router-link>
			</p>
		</div>
		<div class="field submit-button">
			<button type="submit">ログイン</button>
		</div>

	  </form>
	</section>

  </template>
  
  <script>
  import apiClient from '@/services/api.js'
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  
  export default {
	name: 'LoginView',
	setup() {
	  const router = useRouter()
	  const form = ref({ username: '', password: '' })
	  const error = ref(null)
  
	  const login = async () => {
		try {
			const body = { username: form.username, password: form.password }
			const res = await api.post('/dj-rest-auth/jwt/create/', body)
			localStorage.setItem('accessToken',  res.data.access)
			localStorage.setItem('refreshToken', res.data.refresh)
			router.push('/stage')           // 任意ページへ
		} catch(e){ err.value = 'ログイン失敗' }
		}
  
	  return { form, error, login }
	}
  }
  </script>
  