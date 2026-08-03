import { useState, useEffect } from 'react'
import CommentSection from './CommentSection'

interface Activity {
  id: string
  user_id: string
  username: string
  action_type: string
  resource_type: string
  message: string
  comment_count: number
  created_at: string
}

export default function SocialFeed() {
  const [activities, setActivities] = useState<Activity[]>([])
  const [nextCursor, setNextCursor] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('global')
  const [expanded, setExpanded] = useState<string | null>(null)

  const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` }

  const fetchFeed = async (cursor?: string) => {
    const url = cursor
      ? `/api/v1/social/feed?limit=20&cursor=${cursor}&filter=${filter}`
      : `/api/v1/social/feed?limit=20&filter=${filter}`
    try {
      const res = await fetch(url, { headers })
      if (res.ok) {
        const data = await res.json()
        if (cursor) {
          setActivities(prev => [...prev, ...data.activities])
        } else {
          setActivities(data.activities)
        }
        setNextCursor(data.next_cursor)
      }
    } catch { /* ignore */ }
    setLoading(false)
  }

  useEffect(() => { fetchFeed() }, [filter])

  if (loading) return <div className="p-4 text-dim">Loading feed...</div>

  return (
    <div className="p-4 space-y-3">
      <div className="flex items-center gap-2 mb-3">
        <h2 className="text-lg font-bold text-cyan">Social Feed</h2>
        <select value={filter} onChange={e => { setFilter(e.target.value); setActivities([]); setLoading(true) }}
          className="bg-gray-800 border border-gray-700 rounded px-2 py-1 text-xs text-white">
          <option value="global">Global</option>
          <option value="following">Following</option>
          <option value="own">My Activity</option>
        </select>
      </div>

      {activities.length === 0 ? (
        <p className="text-dim text-sm">No activity yet. Share a portfolio or follow users to populate your feed!</p>
      ) : (
        activities.map(a => (
          <div key={a.id} className="p-3 bg-gray-800 rounded border border-gray-700">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-green font-bold">{a.username}</span>
                <span className="text-dim text-sm"> {a.message}</span>
              </div>
              <span className="text-dim text-xs">{a.created_at ? new Date(a.created_at).toLocaleDateString() : ''}</span>
            </div>
            <div className="mt-2 flex items-center gap-3 text-xs">
              <button onClick={() => setExpanded(expanded === a.id ? null : a.id)}
                className="text-cyan hover:text-white transition-colors">
                💬 {a.comment_count || 0} comments
              </button>
            </div>
            {expanded === a.id && <CommentSection activityId={a.id} />}
          </div>
        ))
      )}

      {nextCursor && (
        <button onClick={() => fetchFeed(nextCursor)}
          className="w-full py-2 text-sm text-cyan hover:text-white bg-gray-800 rounded transition-colors tap-target">
          Load more
        </button>
      )}
    </div>
  )
}
