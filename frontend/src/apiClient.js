// src/apiClient.js
import { supabase } from '@/supabaseClient'

export async function authorizedFetch(input, init = {}) {
  const { data } = await supabase.auth.getSession()
  const token = data.session?.access_token

  if (!token) {
    throw new Error('No auth session')
  }

  const headers = new Headers(init.headers || {})
  headers.set('Authorization', `Bearer ${token}`)

  return fetch(input, {
    ...init,
    headers,
  })
}