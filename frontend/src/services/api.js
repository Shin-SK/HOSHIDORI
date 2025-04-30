// src/services/api.js
import axios  from 'axios'
import router from '@/router'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  withCredentials: false          // JWT だけなら false
})

// ───── リクエスト前 ─────
api.interceptors.request.use(cfg => {
  const token = localStorage.getItem('accessToken')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

// ───── レスポンス後 ─────
let isRefreshing = false
let queue = []

api.interceptors.response.use(
  res => res,
  async err => {
    const { config, response } = err
    
    if (!localStorage.getItem('accessToken')) throw err

    if (!response || response.status !== 401) throw err

    // 1回 retry した物は諦めてログインへ
    if (config._retry) {
      cleanupAndLogout()
      throw err
    }
    config._retry = true

    // refresh 中はキューへ
    if (isRefreshing) {
      return new Promise((resolve, reject) => queue.push({ resolve, reject, config }))
    }
    isRefreshing = true

    try {
      // ── リフレッシュ
      const refresh = localStorage.getItem('refreshToken')
      if (!refresh) throw new Error('no-refresh-token')

        const { data } = await axios.post(`${API_BASE}/dj-rest-auth/jwt/refresh/`,
        { refresh })

      const newAccess = data.access
      localStorage.setItem('accessToken', newAccess)

      // 自分 & キューを再送
      config.headers.Authorization = `Bearer ${newAccess}`
      queue.forEach(p => {
        p.config.headers.Authorization = `Bearer ${newAccess}`
        api.request(p.config).then(p.resolve).catch(p.reject)
      })
      queue = []
      return api.request(config)

    } catch (e) {
      cleanupAndLogout()
      throw e
    } finally {
      isRefreshing = false
    }
  }
)

// ユーティリティ
function cleanupAndLogout () {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  router.push('/login')
}

export default api

// 便利ラッパー（使わなくても OK）
export const getPublicProfile = username =>
  api.get(`/api/profile/${username}/`).then(r => r.data)