import { useState, useEffect } from 'react'

interface Profile {
  id: string
  username: string
  email: string
  role: string
  follower_count: number
  following_count: number
  portfolio_count: number
  reputation: { total_points: number; level: string; next_level?: { name: string; points_needed: number } | null }
  badges: { name: string; description: string; icon: string }[]
}

interface Props {
  userId?: string
  username?: string
  onFollow?: () => void
}

export default function UserProfile({ userId, onFollow }: Props) {
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(true)
  const [following, setFollowing] = useState(false)

  useEffect(() => {
    const fetchProfile = async () => {
      const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` }
      const url = userId ? `/api/v1/social/profile/${userId}` : '/api/v1/users/me'
      try {
        const res = await fetch(url, { headers })
        if (res.ok) {
          const data = await res.json()
          setProfile(data.profile || data)
        }
      } catch { /* ignore */ }
      if (userId) {
        try {
          const res = await fetch(`/api/v1/social/follow/${userId}/status`, { headers })
          if (res.ok) {
            const data = await res.json()
            setFollowing(data.following)
          }
        } catch { /* ignore */ }
      }
      setLoading(false)
    }
    fetchProfile()
  }, [userId])

  const toggleFollow = async () => {
    if (!userId) return
    const headers = { Authorization: `Bearer ${localStorage.getItem('token')}`, 'Content-Type': 'application/json' }
    try {
      if (following) {
        await fetch(`/api/v1/social/follow/${userId}`, { method: 'DELETE', headers })
      } else {
        await fetch(`/api/v1/social/follow/${userId}`, { method: 'POST', headers })
      }
      setFollowing(!following)
      onFollow?.()
    } catch { /* ignore */ }
  }

  if (loading) return <div className="p-4 text-dim">Loading profile...</div>
  if (!profile) return <div className="p-4 text-red">User not found</div>

  return (
    <div className="p-4 border border-gray-700 rounded-lg bg-gray-900 space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-green">{profile.username}</h3>
          <p className="text-xs text-dim">{profile.role} · {profile.email}</p>
        </div>
        {userId && (
          <button
            onClick={toggleFollow}
            className={`px-4 py-1.5 rounded text-sm font-bold tap-target transition-colors ${
              following ? 'bg-gray-700 text-dim hover:bg-red-800 hover:text-red' : 'bg-green-800 text-green hover:bg-green-700'
            }`}
            aria-label={following ? 'Unfollow user' : 'Follow user'}
          >
            {following ? 'Following' : '+ Follow'}
          </button>
        )}
      </div>

      <div className="flex gap-4 text-sm">
        <div><span className="text-dim">Followers:</span> <span className="text-white">{profile.follower_count || 0}</span></div>
        <div><span className="text-dim">Following:</span> <span className="text-white">{profile.following_count || 0}</span></div>
        <div><span className="text-dim">Portfolios:</span> <span className="text-white">{profile.portfolio_count || 0}</span></div>
      </div>

      {profile.reputation && (
        <div className="p-2 bg-gray-800 rounded">
          <div className="text-xs text-dim">Reputation</div>
          <div className="text-sm"><span className="text-yellow">{profile.reputation.level}</span> · {profile.reputation.total_points} pts</div>
          {profile.reputation.next_level && (
            <div className="text-xs text-dim">{profile.reputation.next_level.points_needed} pts to {profile.reputation.next_level.name}</div>
          )}
        </div>
      )}

      {profile.badges && profile.badges.length > 0 && (
        <div>
          <div className="text-xs text-dim mb-1">Badges</div>
          <div className="flex flex-wrap gap-2">
            {profile.badges.map((b, i) => (
              <div key={i} className="px-2 py-1 bg-gray-800 rounded text-xs flex items-center gap-1" title={b.description}>
                <span>{b.icon}</span>
                <span className="text-cyan">{b.name}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
