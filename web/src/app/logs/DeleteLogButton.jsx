// src/app/logs/DeleteLogButton.jsx
'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'

export default function DeleteLogButton({ id }) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)

  const handleDelete = async () => {
    if (!window.confirm('このログを削除しますか？')) return

    setLoading(true)
    try {
      await fetch(`/api/logs/${id}`, {
        method: 'DELETE',
      })
      router.refresh()
    } finally {
      setLoading(false)
    }
  }

  return (
    <button
      type="button"
      className="btn btn-sm btn-outline-danger"
      onClick={handleDelete}
      disabled={loading}
    >
      {loading ? '削除中...' : '削除'}
    </button>
  )
}