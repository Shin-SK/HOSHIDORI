// web/src/app/api/works/route.js
import prisma from '@/lib/prisma'

export async function GET() {
  const works = await prisma.work.findMany({
    include: {
      theater: true,
    },
    orderBy: {
      id: 'asc',
    },
  })

  return Response.json(works)
}