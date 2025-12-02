// src/authState.js
import { ref } from 'vue'

export const currentUser = ref(null)
export const authReady = ref(false)

export async function initAuth() {
  // ローカルにJWTがあれば簡易的にログイン状態とみなす
  const token = localStorage.getItem('hoshidori_token')
  if (token) {
    currentUser.value = { token }
  } else {
    currentUser.value = null
  }
  authReady.value = true
}