import { useState, useEffect } from 'react'

interface Comment {
  id: string
  activity_id: string
  user_id: string
  username: string
  text: string
  created_at: string
}

interface Props {
  activityId: string
}

export default function CommentSection({ activityId }: Props) {
  const [comments, setComments] = useState<Comment[]>([])
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(true)

  const headers = { Authorization: `Bearer ${localStorage.getItem('token')}`, 'Content-Type': 'application/json' }

  const fetchComments = async () => {
    setLoading(true)
    try {
      const res = await fetch(`/api/v1/social/feed/${activityId}/comments`, { headers: { Authorization: headers.Authorization } })
      if (res.ok) {
        const data = await res.json()
        setComments(data.comments || [])
      }
    } catch { /* ignore */ }
    setLoading(false)
  }

  useEffect(() => { fetchComments() }, [activityId])

  const addComment = async () => {
    if (!text.trim()) return
    try {
      const res = await fetch(`/api/v1/social/feed/${activityId}/comment`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ text: text.trim() }),
      })
      if (res.ok) {
        setText('')
        fetchComments()
      }
    } catch { /* ignore */ }
  }

  const deleteComment = async (commentId: string) => {
    try {
      const res = await fetch(`/api/v1/social/comment/${commentId}`, {
        method: 'DELETE',
        headers: { Authorization: headers.Authorization },
      })
      if (res.ok) fetchComments()
    } catch { /* ignore */ }
  }

  return (
    <div className="mt-3 pl-4 border-l-2 border-gray-700 space-y-2">
      {loading ? (
        <p className="text-dim text-xs">Loading comments...</p>
      ) : comments.length === 0 ? (
        <p className="text-dim text-xs">No comments yet.</p>
      ) : (
        comments.map(c => (
          <div key={c.id} className="flex items-start justify-between">
            <div>
              <span className="text-green text-xs font-bold">{c.username}</span>
              <span className="text-white text-xs ml-1">{c.text}</span>
              <span className="text-dim text-xs ml-2">{new Date(c.created_at).toLocaleDateString()}</span>
            </div>
            <button onClick={() => deleteComment(c.id)} className="text-dim hover:text-red text-xs" aria-label="Delete comment">✕</button>
          </div>
        ))
      )}

      <div className="flex gap-2">
        <input
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && addComment()}
          placeholder="Add a comment..."
          className="flex-1 bg-gray-900 border border-gray-700 rounded px-2 py-1 text-xs text-green outline-none focus:border-green/50"
          aria-label="Comment text"
        />
        <button onClick={addComment} disabled={!text.trim()}
          className="px-3 py-1 bg-cyan-800 text-cyan rounded text-xs disabled:opacity-50 tap-target">
          Post
        </button>
      </div>
    </div>
  )
}
