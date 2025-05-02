// src/services/api.js
import axios  from 'axios'
import router from '@/router'
import { useToast } from 'vue-toastification'

/* ---------------- base ---------------- */
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  withCredentials: false          // JWT だけなら false
})

/* ---------------- toast ----------------
   composable は setup() の外だと直接呼べないので
   “遅延生成” パターンを取る                      */
let toast
function notify (msg) {
  if (!toast) toast = useToast()
  toast.error(msg)
}

/* ---------------- Request --------------- */
api.interceptors.request.use(cfg => {
  // accessToken があれば付与
  const token = localStorage.getItem('accessToken')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

/* =============== Response (error) ========= */
let isRefreshing = false
let queue = []

api.interceptors.response.use(
  res => res,                                 // ← 成功時は手を触れない
  async err => {
    /* ---------- 共通エラー表示 ---------- */
    const data = err.response?.data
    const msg =
      data?.detail ||                          // DRF の detail
      Object.values(data || {})?.[0]?.[0] ||   // password1 など field error
      'エラーが発生しました。運営にお問い合わせください。'
    notify(msg)

    /* ---------- JWT が無い or 401 以外 ---------- */
    const { config, response } = err
    const hasToken = !!localStorage.getItem('accessToken')
    if (!hasToken || !response || response.status !== 401) {
      return Promise.reject(err)               // ここで打ち止め
    }

    /* ---------- 2 回目も 401 → ログアウト ---------- */
    if (config._retry) {
      cleanupAndLogout()
      return Promise.reject(err)
    }
    config._retry = true                       // 1 回だけ再挑戦許可

    /* ---------- 刷新処理が同時に走ったらキュー ---------- */
    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        queue.push({ resolve, reject, config })
      })
    }
    isRefreshing = true

    try {
      /* ---------- リフレッシュ ---------- */
      const refresh = localStorage.getItem('refreshToken')
      if (!refresh) throw new Error('no-refresh-token')

      const { data: refData } = await axios.post(
        `${API_BASE}/dj-rest-auth/jwt/refresh/`,
        { refresh }
      )

      const newAccess = refData.access
      localStorage.setItem('accessToken', newAccess)

      /* ---------- キュー再送 ---------- */
      queue.forEach(p => {
        p.config.headers.Authorization = `Bearer ${newAccess}`
        api.request(p.config).then(p.resolve).catch(p.reject)
      })
      queue = []

      /* ---------- 自分のリトライ ---------- */
      config.headers.Authorization = `Bearer ${newAccess}`
      return api.request(config)

    } catch (e) {
      cleanupAndLogout()
      return Promise.reject(e)                 // ← 失敗は上に伝える
    } finally {
      isRefreshing = false
    }
  }
)

/* ============ util ============ */
function cleanupAndLogout () {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  router.push('/login')
}

export default api

/* ---------- 便利ラッパー（例） ---------- */
export const getPublicProfile = username =>
  api.get(`/api/profile/${username}/`).then(r => r.data)
