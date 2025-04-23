// src/services/useAuth.js
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

/* ── 状態 ─────────────────────────────── */
const _access = ref(localStorage.getItem('accessToken') || null)

/* ── 公開 API ─────────────────────────── */
export function useAuth () {
  const router = useRouter()

  /** ログイン中判定 (リアクティブ) */
  const isLoggedIn = computed(() => !!_access.value)

  /** ログイン成功時にトークンを保存 & 反映 */
  const setTokens = (access, refresh) => {
    localStorage.setItem('accessToken',  access)
    localStorage.setItem('refreshToken', refresh)
    _access.value = access
  }

  /** ログアウト共通処理 */
  const logout = () => {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    _access.value = null
    router.push('/login')
  }

  return { isLoggedIn, setTokens, logout }
}
