// src/app/api/logs/route.js
import prisma from '@/lib/prisma'

const CURRENT_USER_ID = 1 // ✨ ローカル用の「自分」

// GET /api/logs
export async function GET() {
  const logs = await prisma.viewingLog.findMany({
    where: { userId: CURRENT_USER_ID },      // ← 自分のログだけ
    orderBy: { watchedDate: 'desc' },
    include: {
      user: true,
      work: {
        include: {
          theater: true,
        },
      },
    },
  })

  return Response.json(logs)
}

// POST /api/logs
export async function POST(req) {
  const body = await req.json()

  const workId = Number(body.workId)
  const watchedDate = body.watchedDate
    ? new Date(body.watchedDate)
    : new Date()

  const rating = body.rating ? Number(body.rating) : null
  const tags = Array.isArray(body.tags) ? body.tags : []

  const log = await prisma.viewingLog.create({
    data: {
      userId: CURRENT_USER_ID,  // ← フロントから userId は受け取らない
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