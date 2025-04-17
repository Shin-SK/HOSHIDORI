<template>
	<div>
	  <h1>Login with JWT</h1>
	  <div v-if="error">{{ error }}</div>
	  <form @submit.prevent="loginUser">
		<input v-model="form.username" placeholder="Username">
		<input v-model="form.password" type="password" placeholder="Password">
		<button type="submit">Login</button>
	  </form>
	</div>
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
  