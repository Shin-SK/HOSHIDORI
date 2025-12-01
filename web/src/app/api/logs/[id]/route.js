// src/app/api/logs/[id]/route.js
import prisma from '@/lib/prisma'
import { getCurrentDbUser } from '@/lib/getCurrentDbUser'

// OPTIONS /api/logs/:id (CORS preflight)
export async function OPTIONS() {
  return new Response(null, { status: 204 })
}

// DELETE /api/logs/:id
export async function DELETE(req, { params }) {
  const dbUser = await getCurrentDbUser(req)
  if (!dbUser) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { id: paramId } = await params
  const id = Number(paramId)
  if (Number.isNaN(id)) {
    return Response.json({ error: 'Invalid id' }, { status: 400 })
  }

  // ログを取得して所有権チェック
  const log = await prisma.viewingLog.findUnique({ where: { id } })
  if (!log) {
    return Response.json({ error: 'Not found' }, { status: 404 })
  }
  if (log.userId !== dbUser.id) {
    return Response.json({ error: 'Forbidden' }, { status: 403 })
  }

  await prisma.viewingLog.delete({ where: { id } })

  return new Response(null, { status: 204 })
}

// PATCH /api/logs/:id
export async function PATCH(req, { params }) {
  const dbUser = await getCurrentDbUser(req)
  if (!dbUser) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { id: paramId } = await params
  const id = Number(paramId)
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

  // ログを取得して所有権チェック
  const existingLog = await prisma.viewingLog.findUnique({ where: { id } })
  if (!existingLog) {
    return Response.json({ error: 'Not found' }, { status: 404 })
  }
  if (existingLog.userId !== dbUser.id) {
    return Response.json({ error: 'Forbidden' }, { status: 403 })
  }

  const log = await prisma.viewingLog.update({
    where: { id },
    data: cleaned,
  })

  return Response.json(log)
}