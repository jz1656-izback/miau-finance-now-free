import { useState, useEffect } from 'react'

interface Activity { id: string; username: string; action_type: string; message: string; created_at: string }
interface LeaderboardEntry { rank: number; username: string; value: number; positions: number }
interface Notification { id: string; message: string; type: string; is_read: boolean; created_at?: string }
interface Badge { name: string; icon: string }

const CAT_ART = `  ╱|、\n (˚ˎ 。7\n  |、˜〵\n  じしˍ,)ノ`

export default function SocialDashboard({ token }: { token: string }) {
  const [feed, setFeed] = useState<Activity[]>([])
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([])
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [profile, setProfile] = useState<{ username: string; badges: Badge[]; followers: number; following: number } | null>(null)
  const [tab, setTab] = useState<'feed' | 'leaderboard' | 'notifications'>('feed')
  const [loading, setLoading] = useState(true)

  const h = { Authorization: `Bearer ${token}` }

  useEffect(() => {
    Promise.all([
      fetch('/api/v1/social/feed?limit=10', { headers: h }).then(r => r.ok ? r.json() : null),
      fetch('/api/v1/social/leaderboard?limit=10', { headers: h }).then(r => r.ok ? r.json() : null),
      fetch('/api/v1/social/notifications', { headers: h }).then(r => r.ok ? r.json() : null),
      fetch('/api/v1/social/badges', { headers: h }).then(r => r.ok ? r.json() : null),
    ]).then(([feedData, lbData, notifData, badgeData]) => {
      if (feedData?.activities) setFeed(feedData.activities)
      if (lbData?.leaderboard) setLeaderboard(lbData.leaderboard)
      const notifs = Array.isArray(notifData) ? notifData : notifData?.notifications || []
      setNotifications(notifs)
      setProfile({ username: 'admin', badges: badgeData?.badges || [], followers: 12, following: 8 })
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  if (loading) return <div style={{ padding: 40, textAlign: 'center', color: '#4a5568' }}>🐱 loading social data...</div>

  return (
    <div style={{ padding: 20, maxWidth: 900, margin: '0 auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 20 }}>
        <span style={{ fontSize: 24 }}>🐱</span>
        <h1 style={{ fontSize: 20, fontWeight: 'bold', background: 'linear-gradient(135deg,#00e676,#a855f7,#22d3ee)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Social</h1>
        {profile && <span style={{ fontSize: 11, color: '#8899b0' }}>👤 {profile.username} · 👥 {profile.followers} followers · {profile.following} following · {profile.badges.length} badges</span>}
      </div>

      <div style={{ display: 'flex', gap: 4, marginBottom: 16 }}>
        {(['feed', 'leaderboard', 'notifications'] as const).map(t => (
          <button key={t} onClick={() => setTab(t)} style={{
            padding: '6px 14px', borderRadius: 6, cursor: 'pointer', fontSize: 12,
            background: tab === t ? 'rgba(0,230,118,0.15)' : 'rgba(19,19,26,0.8)',
            color: tab === t ? '#00e676' : '#8899b0', fontWeight: tab === t ? 600 : 400,
            border: `1px solid ${tab === t ? 'rgba(0,230,118,0.3)' : 'rgba(42,42,64,0.4)'}`,
          }}>
            {t === 'feed' ? '📰 Feed' : t === 'leaderboard' ? '🏆 Leaderboard' : '🔔 Notifications'}
            {t === 'notifications' && notifications.filter(n => !n.is_read).length > 0 &&
              <span style={{ marginLeft: 6, background: '#ef4444', color: '#fff', borderRadius: 8, padding: '1px 6px', fontSize: 9 }}>
                {notifications.filter(n => !n.is_read).length}
              </span>}
          </button>
        ))}
      </div>

      {tab === 'feed' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          {feed.length === 0 && <div style={{ textAlign: 'center', color: '#4a5568', padding: 40 }}>📭 No activity yet</div>}
          {feed.map(a => (
            <div key={a.id} style={{ padding: '10px 14px', background: 'rgba(19,19,26,0.85)', borderRadius: 8, border: '1px solid rgba(42,42,64,0.4)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <span style={{ color: '#00e676', fontSize: 12, fontWeight: 600 }}>{a.username}</span>
                <span style={{ color: '#8899b0', fontSize: 11, marginLeft: 6 }}>{a.message || a.action_type}</span>
              </div>
              <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                <a href={`javascript:void(0)`} onClick={() => {
                  fetch(`/api/v1/social/feed/${a.id}/like`, { method: 'POST', headers: h })
                }} style={{ fontSize: 11, color: '#6366f1', cursor: 'pointer', textDecoration: 'none' }}>👍</a>
                <span style={{ fontSize: 10, color: '#4a5568' }}>{a.created_at?.slice(0, 10) || ''}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {tab === 'leaderboard' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          {leaderboard.length === 0 && <div style={{ textAlign: 'center', color: '#4a5568', padding: 40 }}>📭 No leaderboard data</div>}
          {leaderboard.map((e, i) => (
            <div key={i} style={{ padding: '8px 14px', background: i === 0 ? 'rgba(255,215,0,0.05)' : 'rgba(19,19,26,0.85)', borderRadius: 6, border: `1px solid ${i === 0 ? 'rgba(255,215,0,0.2)' : 'rgba(42,42,64,0.4)'}`, display: 'flex', alignItems: 'center', gap: 12 }}>
              <span style={{ color: i === 0 ? '#ffd700' : i === 1 ? '#c0c0c0' : i === 2 ? '#cd7f32' : '#4a5568', fontSize: 14, fontWeight: 'bold', width: 24 }}>#{i + 1}</span>
              <span style={{ color: '#e0e0e0', fontSize: 12, flex: 1 }}>{e.username}</span>
              <span style={{ color: '#00e676', fontSize: 12, fontWeight: 600 }}>{e.value?.toFixed(2)}%</span>
              <span style={{ color: '#4a5568', fontSize: 10 }}>{e.positions} pos</span>
            </div>
          ))}
        </div>
      )}

      {tab === 'notifications' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          {notifications.length === 0 && <div style={{ textAlign: 'center', color: '#4a5568', padding: 40 }}>🔔 No notifications</div>}
          {notifications.map(n => (
            <div key={n.id} style={{ padding: '8px 14px', background: 'rgba(19,19,26,0.85)', borderRadius: 6, border: '1px solid rgba(42,42,64,0.4)', display: 'flex', alignItems: 'center', gap: 8 }}>
              <span>{n.is_read ? '📭' : '📬'}</span>
              <span style={{ color: n.is_read ? '#8899b0' : '#e0e0e0', fontSize: 12, flex: 1 }}>{n.message || n.type}</span>
              <span style={{ fontSize: 9, color: '#4a5568' }}>{n.created_at?.slice(0, 10) || ''}</span>
            </div>
          ))}
        </div>
      )}

      <pre style={{ fontSize: 7, lineHeight: '9px', color: 'rgba(0,230,118,0.1)', marginTop: 20, textAlign: 'center', fontFamily: 'monospace' }}>{CAT_ART}</pre>
    </div>
  )
}
