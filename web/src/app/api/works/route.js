// src/app/api/works/route.js
import prisma from '@/lib/prisma'

const CURRENT_USER_ID = 1 // ローカル用：「自分のログ」判定用

// OPTIONS /api/works (CORS preflight)
export async function OPTIONS() {
  return new Response(null, { status: 204 })
}

export async function GET(req) {
  const { searchParams } = new URL(req.url)
  const qRaw = searchParams.get('q')
  const q = qRaw?.trim()

  let whereWork = {}

  if (q && q.length > 0) {
    where = {
      OR: [
        // タイトル
        {
          title: {
            contains: q,
            mode: 'insensitive',
          },
        },
        // 劇場名
        {
          theater: {
            name: {
              contains: q,
              mode: 'insensitive',
            },
          },
        },
        // 劇団名
        {
          troupe: {
            contains: q,
            mode: 'insensitive',
          },
        },
        // タグ（String[] に q が含まれる）
        {
          tags: {
            hasSome: [q],
          },
        },
        // 俳優名（String[] に q が含まれる）
        {
          actors: {
            hasSome: [q],
          },
        },
      ],
    }
  }

  // 作品本体（劇場付き）
  const works = await prisma.work.findMany({
    where: whereWork,
    include: {
      theater: true,
    },
    orderBy: {
      createdAt: 'desc',
    },
  })

  const workIds = works.map((w) => w.id)
  if (workIds.length === 0) {
    return Response.json([])
  }

  // 全体の平均レーティング
  const allAgg = await prisma.viewingLog.groupBy({
    by: ['workId'],
    _avg: { rating: true },
    where: {
      workId: { in: workIds },
      rating: { not: null },
    },
  })

  // 自分の平均レーティング（ローカルでは userId=1 固定）
  const myAgg = await prisma.viewingLog.groupBy({
    by: ['workId'],
    _avg: { rating: true },
    where: {
      workId: { in: workIds },
      userId: CURRENT_USER_ID,
      rating: { not: null },
    },
  })

  // workId → 平均値 のマップを作る
  const allMap = Object.fromEntries(
    allAgg.map((row) => [row.workId, row._avg.rating]),
  )

  const myMap = Object.fromEntries(
    myAgg.map((row) => [row.workId, row._avg.rating]),
  )

  // works に avgRatingAll / avgRatingMine をくっつける
  const enriched = works.map((w) => ({
    ...w,
    avgRatingAll: allMap[w.id] ?? null,
    avgRatingMine: myMap[w.id] ?? null,
  }))

  return Response.json(enriched)
}

// POST は今のままでOK（作品登録）
export async function POST(req) {
  const body = await req.json()

  const work = await prisma.work.create({
    data: {
      title: body.title,
      troupe: body.troupe || null,
      theaterId: Number(body.theaterId),
      startDate: body.startDate ? new Date(body.startDate) : null,
      endDate: body.endDate ? new Date(body.endDate) : null,
      imageUrl: body.imageUrl || null,
      tags: body.tags ?? [],
    },
  })

  return Response.json(work, { status: 201 })
}