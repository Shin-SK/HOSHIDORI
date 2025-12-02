<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { currentUser } from '@/authState'

const router = useRouter()
const route = useRoute()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)
const message = ref('')

const redirectTo = route.query.redirect || '/logs'

async function handleLogin(e) {
  e.preventDefault()
  loading.value = true
  error.value = null
  message.value = ''

  try {
    const baseUrl = import.meta.env.VITE_API_BASE_URL || ''
    const res = await fetch(`${baseUrl}/api/auth/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        // Djangoデフォルトは username フィールド
        username: username.value,
        password: password.value,
      }),
    })

    if (!res.ok) {
      const text = await res.text()
      throw new Error(text || `Login failed: ${res.status}`)
    }

    const data = await res.json()
    // { access, refresh }
    localStorage.setItem('hoshidori_token', data.access)
    localStorage.setItem('hoshidori_refresh', data.refresh)

    // 簡易的に currentUser をtruthyにする
    currentUser.value = { token: data.access }
    message.value = 'ログインしました'
    router.push(redirectTo)
  } catch (e) {
    console.error(e)
    error.value = e.message || 'ログインに失敗しました'
  } finally {
    loading.value = false
  }
}

// サインアップは別ページに移動
</script>

<template>
  <main class="container py-5" style="max-width: 480px">
    <h1 class="mb-4">HOSHIDORI ログイン</h1>

    <form @submit="handleLogin" class="mb-3">
      <div class="mb-3">
        <label class="form-label">ユーザー名</label>
        <input
          v-model="username"
          type="text"
          class="form-control"
          autocomplete="username"
          required
        />
      </div>

      <div class="mb-3">
        <label class="form-label">パスワード</label>
        <input
          v-model="password"
          type="password"
          class="form-control"
          autocomplete="current-password"
          required
        />
      </div>

      <button type="submit" class="btn btn-primary w-100" :disabled="loading">
        {{ loading ? '処理中...' : 'ログイン' }}
      </button>
    </form>

    <router-link
      class="btn btn-outline-secondary w-100 mb-2"
      :class="{ disabled: loading }"
      to="/signup"
    >
      初めての方はこちら（サインアップ）
    </router-link>

    <p v-if="error" class="text-danger mt-2">{{ error }}</p>
    <p v-if="message" class="text-success mt-2">{{ message }}</p>
  </main>
</template>