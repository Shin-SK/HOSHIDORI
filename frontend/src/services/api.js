// src/services/api.js
import axios from 'axios'
import router from '@/router'

// ◇ 1. 基本設定
const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: false            // JWT はヘッダだけで送る
})

// ◇ 2. リクエスト前: accessToken があれば必ず付ける
api.interceptors.request.use(cfg => {
  const token = localStorage.getItem('accessToken')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

// ◇ 3. レスポンス後: 401 が来たら自動リフレッシュ＆リトライ
let isRefreshing = false
let queued = []   // リフレッシュ中のリクエストをキューに貯める

api.interceptors.response.use(
  res => res,     // 200 系はそのまま返す
  async err => {
    const { config, response } = err
    if (!response || response.status !== 401) throw err       // 401 以外はただ投げる

    // ----- ここから 401 対応 -----
    // ① すでにリフレッシュ試したリクエストなら諦めてログインへ
    if (config._retry) {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      router.push('/login')
      throw err
    }
    config._retry = true

    // ② 同時に 401 が複数来る場合のロック
    if (isRefreshing) {
      return new Promise((resolve, reject) => queued.push({ resolve, reject, config }))
    }
    isRefreshing = true

    try {
      // ③ refresh トークンで新しい access を取得
      const refresh = localStorage.getItem('refreshToken')
      const res = await axios.post('http://localhost:8000/dj-rest-auth/jwt/refresh/', {
        refresh
      })
      const newAccess = res.data.access
      localStorage.setItem('accessToken', newAccess)

      // ④ 今のリクエスト & 待機列を再送
      config.headers.Authorization = `Bearer ${newAccess}`
      queued.forEach(p => {
        p.config.headers.Authorization = `Bearer ${newAccess}`
        api.request(p.config).then(p.resolve).catch(p.reject)
      })
      queued = []
      return api.request(config)

    } catch (refreshErr) {
      // ⑤ refresh 失敗 → ログアウト
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      router.push('/login')
      throw refreshErr
    } finally {
      isRefreshing = false
    }
  }
)

export default api
