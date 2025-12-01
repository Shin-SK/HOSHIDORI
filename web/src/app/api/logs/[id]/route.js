// src/app/api/logs/[id]/route.js
import prisma from '@/lib/prisma'

const CURRENT_USER_ID = 1

// DELETE /api/logs/:id
export async function DELETE(_req, { params }) {
  const id = Number(params.id)
  if (Number.isNaN(id)) {
    return Response.json({ error: 'Invalid id' }, { status: 400 })
  }

  await prisma.viewingLog.delete({
    where: {
      // 自分のログだけ消せるようにする
      id_userId: { id, userId: CURRENT_USER_ID },
    },
  })

  return new Response(null, { status: 204 })
}

// PATCH /api/logs/:id
export async function PATCH(req, { params }) {
  const id = Number(params.id)
  if (Number.isNaN(id)) {
    return Response.json({ error: 'Invalid id' }, { status: 400 })
  }

  const body = await req.json()

  const watchedDate = body.watchedDate
    ? new Date(body.watchedDate)
    : undefined

  const rating =
    body.rating === '' || body.rating === null || body.rating === undefined
      ? null
      : Number(body.rating)

  const tags = Array.isArray(body.tags) ? body.tags : undefined

  const data = {
    workId: body.workId ? Number(body.workId) : undefined,
    // userId は変えさせない（常に CURRENT_USER_ID）
    watchedDate,
    seat: body.seat ?? undefined,
    memo: body.memo ?? undefined,
    rating,
    tags,
  }

  const cleaned = Object.fromEntries(
    Object.entries(data).filter(([, v]) => v !== undefined),
  )

  const log = await prisma.viewingLog.update({
    where: {
      // 自分のログだけ更新
      id_userId: { id, userId: CURRENT_USER_ID },
    },
    data: cleaned,
  })

  return Response.json(log)
}