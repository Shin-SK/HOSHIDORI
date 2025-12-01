// src/lib/getCurrentDbUser.js
import { supabaseServer } from '@/lib/supabaseServer'
import prisma from '@/lib/prisma'

export async function getCurrentDbUser(req) {
  const auth = req.headers.get('authorization')

  if (!auth || !auth.startsWith('Bearer ')) {
    return null
  }

  const token = auth.slice('Bearer '.length).trim()

  // SupabaseのJWTから user を取得
  const { data, error } = await supabaseServer.auth.getUser(token)

  if (error || !data.user) {
    return null
  }

  const supaUser = data.user

  // PrismaのUserと紐づけ（なければ作る）
  const dbUser = await prisma.user.upsert({
    where: { supabaseUserId: supaUser.id },
    update: {
      email: supaUser.email ?? 'unknown@example.com',
    },
    create: {
      email: supaUser.email ?? 'unknown@example.com',
      username: null, // 初回は null、プロフィール編集で設定可能にする
      supabaseUserId: supaUser.id,
      role: 'USER', // 初回登録は USER、管理者は手動で変更
    },
  })

  return dbUser
}