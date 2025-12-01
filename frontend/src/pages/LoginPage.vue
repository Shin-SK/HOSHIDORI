<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { supabase } from '@/supabaseClient'
import { currentUser } from '@/authState'

const router = useRouter()
const route = useRoute()

const email = ref('')
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
    const { data, error: loginError } = await supabase.auth.signInWithPassword({
      email: email.value,
      password: password.value,
    })

    if (loginError) throw loginError

    currentUser.value = data.user
    message.value = 'ログインしました'
    router.push(redirectTo)
  } catch (e) {
    console.error(e)
    error.value = e.message || 'ログインに失敗しました'
  } finally {
    loading.value = false
  }
}

async function handleSignup(e) {
  e.preventDefault()
  loading.value = true
  error.value = null
  message.value = ''

  try {
    const { data, error: signupError } = await supabase.auth.signUp({
      email: email.value,
      password: password.value,
    })

    if (signupError) throw signupError

    message.value = 'サインアップしました。メール確認が必要な場合はメールを確認してください。'
    // そのままログイン or 手動ログインでもOK
  } catch (e) {
    console.error(e)
    error.value = e.message || 'サインアップに失敗しました'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="container py-5" style="max-width: 480px">
    <h1 class="mb-4">HOSHIDORI ログイン</h1>

    <form @submit="handleLogin" class="mb-3">
      <div class="mb-3">
        <label class="form-label">メールアドレス</label>
        <input
          v-model="email"
          type="email"
          class="form-control"
          required
        />
      </div>

      <div class="mb-3">
        <label class="form-label">パスワード</label>
        <input
          v-model="password"
          type="password"
          class="form-control"
          required
        />
      </div>

      <button type="submit" class="btn btn-primary w-100" :disabled="loading">
        {{ loading ? '処理中...' : 'ログイン' }}
      </button>
    </form>

    <button
      class="btn btn-outline-secondary w-100 mb-2"
      :disabled="loading"
      @click="handleSignup"
    >
      初めての方はこちら（サインアップ）
    </button>

    <p v-if="error" class="text-danger mt-2">{{ error }}</p>
    <p v-if="message" class="text-success mt-2">{{ message }}</p>
  </main>
</template>