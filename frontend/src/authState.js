// src/authState.js
import { ref } from 'vue'
import { supabase } from '@/supabaseClient'

export const currentUser = ref(null)
export const authReady = ref(false)

export async function initAuth() {
  // ローカルにSessionがあれば拾う
  const { data } = await supabase.auth.getUser()
  currentUser.value = data.user ?? null
  authReady.value = true

  // これ以降の変化も監視
  supabase.auth.onAuthStateChange((_event, session) => {
    currentUser.value = session?.user ?? null
  })
}