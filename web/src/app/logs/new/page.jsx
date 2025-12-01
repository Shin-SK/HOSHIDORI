// src/app/logs/new/page.jsx
import prisma from '@/lib/prisma'
import LogForm from './LogForm'

export const dynamic = 'force-dynamic'

export default async function NewLogPage() {
  const works = await prisma.work.findMany({
    include: { theater: true },
    orderBy: { id: 'asc' },
  })

  const users = await prisma.user.findMany({
    orderBy: { id: 'asc' },
  })

  return (
    <main className="container py-4">
      <h1 className="mb-3">観劇ログを追加</h1>
      {works.length === 0 || users.length === 0 ? (
        <p>先に User と Work を作成してください。</p>
      ) : (
        <LogForm works={works} users={users} />
      )}
    </main>
  )
}