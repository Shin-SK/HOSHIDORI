// src/app/logs/page.jsx
import prisma from '@/lib/prisma'
import DeleteLogButton from './DeleteLogButton'

export const dynamic = 'force-dynamic'


export default async function LogsPage() {
  const logs = await prisma.viewingLog.findMany({
    orderBy: { watchedDate: 'desc' },
    include: {
      user: true,
      work: {
        include: { theater: true },
      },
    },
  })

  return (
    <main className="container py-4">
      <h1 className="mb-3">観劇ログ一覧</h1>
      <a href="/logs/new" className="btn btn-primary mb-3">
        観劇ログを追加
      </a>
      {logs.length === 0 && <p>まだ観劇ログがありません。</p>}

      {logs.length > 0 && (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>日付</th>
              <th>タイトル</th>
              <th>劇場</th>
              <th>ユーザー</th>
              <th>メモ</th>
              <th>捜査</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id}>
                <td>
                  {log.watchedDate
                    ? new Date(log.watchedDate).toISOString().slice(0, 10)
                    : ''}
                </td>
                <td>{log.work?.title}</td>
                <td>{log.work?.theater?.name}</td>
                <td>{log.user?.name}</td>
                <td>{log.memo}</td>
                <td>
                  <a
                    href={`/logs/${log.id}/edit`}
                    className="btn btn-sm btn-outline-primary me-2"
                  >
                    編集
                  </a>
                  <DeleteLogButton id={log.id} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  )
}