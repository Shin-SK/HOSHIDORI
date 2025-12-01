// src/app/logs/[id]/edit/page.jsx
import prisma from '@/lib/prisma'
import EditLogForm from './EditLogForm'

export const dynamic = 'force-dynamic'

export default async function EditLogPage({ params }) {
  const { id } = await params                 // ← ここを直す
  const numericId = Number(id)

  if (Number.isNaN(numericId)) {
    return (
      <main className="container py-4">
        <p>不正なIDです。</p>
      </main>
    )
  }

  const log = await prisma.viewingLog.findUnique({
    where: { id: numericId },
    include: {
      user: true,
      work: { include: { theater: true } },
    },
  })

  const works = await prisma.work.findMany({
    include: { theater: true },
    orderBy: { id: 'asc' },
  })

  const users = await prisma.user.findMany({
    orderBy: { id: 'asc' },
  })

  if (!log) {
    return (
      <main className="container py-4">
        <p>このログは存在しません。</p>
      </main>
    )
  }

  return (
    <main className="container py-4">
      <h1 className="mb-3">観劇ログを編集</h1>
      <EditLogForm log={log} works={works} users={users} />
    </main>
  )
}