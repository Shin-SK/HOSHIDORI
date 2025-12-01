// src/app/logs/new/LogForm.jsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function LogForm({ works, users }) {
  const router = useRouter()

  const [form, setForm] = useState({
    workId: works[0]?.id ?? '',
    userId: users[0]?.id ?? '',
    watchedDate: '',
    seat: '',
    memo: '',
    rating: '',
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    await fetch('/api/logs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...form,
        workId: Number(form.workId),
        userId: Number(form.userId),
        rating: form.rating ? Number(form.rating) : null,
        tags: [], // 今はタグなし
      }),
    })

    router.push('/logs')
    router.refresh()
  }

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <div className="mb-3">
        <label className="form-label">作品</label>
        <select
          className="form-select"
          name="workId"
          value={form.workId}
          onChange={handleChange}
        >
          {works.map((work) => (
            <option key={work.id} value={work.id}>
              {work.title}（{work.theater?.name}）
            </option>
          ))}
        </select>
      </div>

      <div className="mb-3">
        <label className="form-label">ユーザー</label>
        <select
          className="form-select"
          name="userId"
          value={form.userId}
          onChange={handleChange}
        >
          {users.map((u) => (
            <option key={u.id} value={u.id}>
              {u.name}
            </option>
          ))}
        </select>
      </div>

      <div className="mb-3">
        <label className="form-label">観た日</label>
        <input
          type="date"
          className="form-control"
          name="watchedDate"
          value={form.watchedDate}
          onChange={handleChange}
        />
      </div>

      <div className="mb-3">
        <label className="form-label">座席</label>
        <input
          type="text"
          className="form-control"
          name="seat"
          value={form.seat}
          onChange={handleChange}
          placeholder="A列12番 など"
        />
      </div>

      <div className="mb-3">
        <label className="form-label">メモ</label>
        <textarea
          className="form-control"
          name="memo"
          rows="3"
          value={form.memo}
          onChange={handleChange}
        />
      </div>

      <div className="mb-3">
        <label className="form-label">評価（1〜5）</label>
        <input
          type="number"
          min="1"
          max="5"
          className="form-control"
          name="rating"
          value={form.rating}
          onChange={handleChange}
        />
      </div>

      <button type="submit" className="btn btn-primary">
        保存する
      </button>
    </form>
  )
}