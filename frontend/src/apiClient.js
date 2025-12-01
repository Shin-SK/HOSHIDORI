// src/apiClient.js
import { supabase } from '@/supabaseClient'

const baseUrl = import.meta.env.VITE_API_BASE_URL || ''

export async function authorizedFetch(path, init = {}) {
  const { data } = await supabase.auth.getSession()
  const token = data.session?.access_token

  if (!token) throw new Error('No auth session')

  const headers = new Headers(init.headers || {})
  headers.set('Authorization', `Bearer ${token}`)

  // path は "/api/logs" みたいに先頭スラッシュ付きで渡す前提
  const url = `${baseUrl}${path}`

  return fetch(url, { ...init, headers })
}