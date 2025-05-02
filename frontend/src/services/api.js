// src/services/api.js
import axios  from 'axios'
import router from '@/router'
import { useToast } from 'vue-toastification'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  withCredentials: false
})

/* ------------ toast ------------ */
let toast
function notify (msg) {
  if (!toast) toast = useToast()
  toast.error(msg)
}

/* ------------ Request ------------ */
api.interceptors.request.use(cfg => {
  const token = localStorage.getItem('accessToken')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

/* ============ Response (error) ============ */
let isRefreshing = false
let queue = []

api.interceptors.response.use(
  res => res,
  async err => {
    /* ① ここで一度だけ展開 --------------- */
    const { response, config } = err

    /* ---------- エラー表示 ---------- */
    if (response) {
      if (response.status !== 401) {            // 401 は黙っておく
        const data = response.data
        const msg =
          Object.values(data || {})?.[0]?.[0] ||
          data?.detail ||
          'エラーが発生しました。運営にお問い合わせください。'
        notify(msg)
      }
    } else {
      notify('通信に失敗しました。電波状況を確認してください。')
    }

    /* ---------- 401 以外 or トークン無し ---------- */
    const hasToken = !!localStorage.getItem('accessToken')
    if (!hasToken || !response || response.status !== 401) {
      return Promise.reject(err)
    }

    /* ---------- リトライは 1 回だけ ---------- */
    if (config._retry) {
      cleanupAndLogout()
      return Promise.reject(err)
    }
    config._retry = true

    /* ---------- 他でリフレッシュ中ならキュー ---------- */
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

      /* ---------- 自分をリトライ ---------- */
      config.headers.Authorization = `Bearer ${newAccess}`
      return api.request(config)

    } catch (e) {
      cleanupAndLogout()
      return Promise.reject(e)
    } finally {
      isRefreshing = false
    }
  }
)

/* ------------ util ------------ */
function cleanupAndLogout () {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  router.push('/login')
}

export default api

export const getPublicProfile = username =>
  api.get(`/api/profile/${username}/`).then(r => r.data)
