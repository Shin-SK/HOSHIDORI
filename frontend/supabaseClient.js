const baseUrl = import.meta.env.VITE_API_BASE_URL || ''

export async function authorizedFetch(path, init = {}) {
  const { data } = await supabase.auth.getSession()
  const token = data.session?.access_token

  if (!token) throw new Error('No auth session')

  const headers = new Headers(init.headers || {})
  headers.set('Authorization', `Bearer ${token}`)

  const url = `${baseUrl}${path}`  // ここで常に backend ドメインに向ける

  return fetch(url, { ...init, headers })
}