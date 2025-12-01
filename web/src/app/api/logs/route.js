// src/app/api/logs/route.js
import prisma from '@/lib/prisma'
import { getCurrentDbUser } from '@/lib/getCurrentDbUser'

// OPTIONS /api/logs (CORS preflight)
export async function OPTIONS() {
  return new Response(null, { status: 204 })
}

// GET /api/logs
export async function GET(req) {
  const dbUser = await getCurrentDbUser(req)
  if (!dbUser) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const logs = await prisma.viewingLog.findMany({
    where: { userId: dbUser.id },  // 自分のログだけ
    orderBy: { watchedDate: 'desc' },
    include: {
      user: true,
      work: { include: { theater: true } },
    },
  })

  return Response.json(logs)
}

// POST /api/logs
export async function POST(req) {
  const dbUser = await getCurrentDbUser(req)
  if (!dbUser) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const body = await req.json()

  const workId = Number(body.workId)
  const watchedDate = body.watchedDate
    ? new Date(body.watchedDate)
    : new Date()

  const rating = body.rating ? Number(body.rating) : null
  const tags = Array.isArray(body.tags) ? body.tags : []

  const log = await prisma.viewingLog.create({
    data: {
      userId: dbUser.id,          // ← ここで本物のユーザーID
      workId,
      watchedDate,
      seat: body.seat || null,
      memo: body.memo || null,
      rating,
      tags,
    },
    include: {
      user: true,
      work: { include: { theater: true } },
    },
  })

  return Response.json(log, { status: 201 })
}