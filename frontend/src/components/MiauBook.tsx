import { useState, useEffect, useRef } from 'react'

interface Activity { id: string; username: string; action_type: string; message: string; created_at: string }
interface LeaderboardEntry { rank: number; username: string; value: number; positions: number }
interface Notification { id: string; message: string; type: string; is_read: boolean; created_at?: string }
interface Badge { name: string; icon: string }
interface Post { id: string; author: string; avatar: string; message: string; likes: number; comments: number; time: string; liked?: boolean }
interface UserProfile { username: string; avatar: string; followers: number; following: number; badges: Badge[]; joined: string; bio: string }

const CAT_EMOJIS = ['👍', '❤️', '😸', '🐟', '🔥', '😹', '🙀', '💎']

const DUMMY_PROFILE: UserProfile = {
  username: 'admin', avatar: '🐱', followers: 12, following: 8,
  badges: [{ name: 'first_trade', icon: '🎯' }, { name: 'ai_master', icon: '🤖' }, { name: 'diamond_paws', icon: '💎' }, { name: 'tuna_hoarder', icon: '🐟' }, { name: 'cat_whisperer', icon: '🐱' }],
  joined: '2026', bio: 'Cat trader · Terminal native · 🐟🐟🐟',
}

const DUMMY_POSTS: Post[] = [
  { id: '1', author: 'The Cat', avatar: '🐱', message: 'Bought the dip on TSLA. 42 bags of tuna deployed. The cat is pleased.', likes: 42, comments: 7, time: '2m ago' },
  { id: '2', author: 'Whiskers', avatar: '🐈', message: 'Just completed Paper Trading 101. 18% returns. Ready for real tuna! 📈', likes: 18, comments: 3, time: '15m ago' },
  { id: '3', author: 'Mittens', avatar: '😸', message: 'My portfolio hit 1M 🐟. Never selling. Diamond paws forever.', likes: 127, comments: 23, time: '1h ago' },
  { id: '4', author: 'Felix', avatar: '😺', message: 'Who else is watching NVDA earnings tonight? My cat says calls.', likes: 56, comments: 12, time: '2h ago' },
  { id: '5', author: 'Luna', avatar: '😻', message: 'DeFi yields looking juicy again. Aave 8% APY on USDC 🤑', likes: 33, comments: 5, time: '3h ago' },
  { id: '6', author: 'Professor Mittens', avatar: '🐈‍⬛', message: 'Bull flag forming on $MIAU. Technical analysis: the cat is sitting on the keyboard. BUY signal.', likes: 89, comments: 15, time: '5h ago' },
  { id: '7', author: 'Duchess Fluff', avatar: '😽', message: 'Your portfolio has 3.0% healthcare vs SPY 14.2%. Consider rebalancing. Purr.', likes: 64, comments: 8, time: '8h ago' },
]

const DUMMY_LEADERBOARD: LeaderboardEntry[] = [
  { rank: 1, username: '🐱 The Cat', value: 142.7, positions: 12 },
  { rank: 2, username: '🐈 Mittens', value: 98.3, positions: 8 },
  { rank: 3, username: '😸 Whiskers', value: 76.1, positions: 15 },
  { rank: 4, username: '😺 Felix', value: 54.2, positions: 6 },
  { rank: 5, username: '😻 Luna', value: 41.8, positions: 10 },
  { rank: 6, username: '🐈‍⬛ Prof. Mittens', value: 38.5, positions: 22 },
  { rank: 7, username: '😽 Duchess Fluff', value: 29.4, positions: 4 },
  { rank: 8, username: '🙀 Lord Scaredy', value: 18.2, positions: 3 },
  { rank: 9, username: '😹 Baron Tuna', value: 12.7, positions: 7 },
  { rank: 10, username: '🐟 Prof. Dr. Tuna', value: 8.1, positions: 1 },
]

const DUMMY_NOTIFS: Notification[] = [
  { id: 'n1', message: '🐈 Whiskers liked your post', type: 'like', is_read: false },
  { id: 'n2', message: '😻 Luna started following you', type: 'follow', is_read: false },
  { id: 'n3', message: '💎 Your portfolio hit a new high! +12.4%', type: 'milestone', is_read: false },
  { id: 'n4', message: '🎯 You earned badge: diamond_paws', type: 'badge', is_read: true },
  { id: 'n5', message: '😸 Mittens commented on your post', type: 'comment', is_read: true },
]

const CAT_ART = `  ╱|、\n (˚ˎ 。7\n  |、˜〵\n  じしˍ,)ノ`

function randomId() { return Math.random().toString(36).slice(2, 9) }

export default function MiauBook({ onClose, active }: { onClose: () => void; active: boolean }) {
  const [tab, setTab] = useState<'feed' | 'leaderboard' | 'notifications' | 'profile'>('feed')
  const [feed, setFeed] = useState<Activity[]>([])
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>(DUMMY_LEADERBOARD)
  const [notifications, setNotifications] = useState<Notification[]>(DUMMY_NOTIFS)
  const [posts, setPosts] = useState<Post[]>(DUMMY_POSTS)
  const [loading, setLoading] = useState(true)
  const [composing, setComposing] = useState(false)
  const [draft, setDraft] = useState('')
  const [profile] = useState<UserProfile>(DUMMY_PROFILE)
  const [isFollowing, setIsFollowing] = useState(false)
  const [followers, setFollowers] = useState(profile.followers)
  const [token] = useState(() => localStorage.getItem('miau_token'))
  const [catFalling, setCatFalling] = useState<{ id: number; emoji: string; x: number; delay: number }[]>([])
  const inputRef = useRef<HTMLInputElement>(null)

  const h: HeadersInit = token ? { Authorization: `Bearer ${token}` } : {}

  useEffect(() => {
    if (!active) return
    Promise.all([
      fetch('/api/v1/social/feed?limit=10', { headers: h }).then(r => r.ok ? r.json() : null),
      fetch('/api/v1/social/leaderboard?limit=10', { headers: h }).then(r => r.ok ? r.json() : null),
      fetch('/api/v1/social/notifications', { headers: h }).then(r => r.ok ? r.json() : null),
    ]).then(([feedData, lbData, notifData]) => {
      if (feedData?.activities) setFeed(feedData.activities)
      if (lbData?.leaderboard) setLeaderboard(lbData.leaderboard)
      const notifs = Array.isArray(notifData) ? notifData : notifData?.notifications || []
      if (notifs.length > 0) setNotifications(notifs)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [active])

  useEffect(() => { if (composing && inputRef.current) inputRef.current.focus() }, [composing])

  const unreadNotifs = notifications.filter(n => !n.is_read).length

  function handlePost() {
    if (!draft.trim()) return
    const newPost: Post = {
      id: randomId(), author: 'admin', avatar: '🐱',
      message: draft.trim(), likes: 0, comments: 0, time: 'just now',
    }
    setPosts(prev => [newPost, ...prev])
    setDraft('')
    setComposing(false)
  }

  function toggleLike(id: string) {
    setPosts(prev => prev.map(p => p.id === id ? { ...p, liked: !p.liked, likes: p.liked ? p.likes - 1 : p.likes + 1 } : p))
  }

  function handleFollow() {
    setIsFollowing(prev => !prev)
    setFollowers(prev => isFollowing ? prev - 1 : prev + 1)
  }

  function addReaction(_postId: string, emoji: string) {
    const fall = { id: Date.now(), emoji, x: Math.random() * 80 + 10, delay: Math.random() * 0.3 }
    setCatFalling(prev => [...prev, fall])
    setTimeout(() => setCatFalling(prev => prev.filter(f => f.id !== fall.id)), 2000)
  }

  function markAllRead() {
    setNotifications(prev => prev.map(n => ({ ...n, is_read: true })))
  }

  function clearNotif(id: string) {
    setNotifications(prev => prev.filter(n => n.id !== id))
  }

  if (!active) return null

  const TabButton = ({ t, label }: { t: typeof tab; label: string }) => (
    <button onClick={() => setTab(t)} style={{
      padding: '6px 14px', border: 'none', cursor: 'pointer', fontSize: 11, borderRadius: '6px 6px 0 0',
      background: tab === t ? 'rgba(0,230,118,0.12)' : 'transparent',
      color: tab === t ? '#00e676' : '#4a5568',
      fontWeight: tab === t ? 600 : 400,
      borderBottom: tab === t ? '2px solid #00e676' : '2px solid transparent',
      transition: 'all 0.15s',
    }}>{label}</button>
  )

  const style = {
    card: (highlight = false): React.CSSProperties => ({
      padding: '12px 16px', background: highlight ? 'rgba(0,230,118,0.03)' : 'rgba(19,19,26,0.85)',
      borderRadius: 8, border: highlight ? '1px solid rgba(0,230,118,0.15)' : '1px solid rgba(42,42,64,0.4)',
      transition: 'all 0.2s',
    }),
    btn: (green = false): React.CSSProperties => ({
      padding: '4px 10px', background: green ? 'rgba(0,230,118,0.12)' : 'transparent',
      border: `1px solid ${green ? 'rgba(0,230,118,0.3)' : 'rgba(42,42,64,0.4)'}`,
      borderRadius: 4, color: green ? '#00e676' : '#8899b0',
      cursor: 'pointer', fontSize: 10, transition: 'all 0.15s',
    }),
  }

  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 9999, background: 'radial-gradient(ellipse at 50% 0%, #0d1a12 0%, #07090e 100%)', display: 'flex', flexDirection: 'column', overflow: 'hidden', fontFamily: 'monospace' }}>
      {/* Falling emojis */}
      {catFalling.map(f => (
        <div key={f.id} style={{
          position: 'fixed', top: -30, left: `${f.x}%`, zIndex: 10000, fontSize: 20,
          animation: `catFall 2s ease-in forwards`,
          animationDelay: `${f.delay}s`, pointerEvents: 'none',
        }}>{f.emoji}</div>
      ))}


      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 16px', background: 'rgba(19,19,26,0.95)', borderBottom: '1px solid rgba(42,42,64,0.4)', flexShrink: 0 }}>
        <button onClick={onClose} style={{ padding: '4px 10px', background: 'transparent', border: '1px solid rgba(42,42,64,0.4)', borderRadius: 4, color: '#8899b0', cursor: 'pointer', fontSize: 12, transition: 'all 0.15s' }}
          onMouseEnter={e => { e.currentTarget.style.borderColor = 'rgba(0,230,118,0.3)'; e.currentTarget.style.color = '#00e676' }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = 'rgba(42,42,64,0.4)'; e.currentTarget.style.color = '#8899b0' }}
        >← Terminal</button>
        <span style={{ fontSize: 22, animation: 'pulse 3s ease-in-out infinite' }}>📕</span>
        <h1 style={{ fontSize: 16, fontWeight: 'bold', background: 'linear-gradient(135deg,#00e676,#a855f7,#22d3ee)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>MiauBook</h1>
        <span style={{ fontSize: 10, color: '#4a5568' }}>social for cat traders</span>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: 2 }}>
          <TabButton t="feed" label="📰 Feed" />
          <TabButton t="leaderboard" label="🏆 Leaders" />
          <TabButton t="notifications" label={`🔔${unreadNotifs > 0 ? ` (${unreadNotifs})` : ''}`} />
          <TabButton t="profile" label="👤 Me" />
        </div>
      </div>

      {/* Trending Tickers */}
      <div style={{ display: 'flex', gap: 12, padding: '6px 16px', background: 'rgba(0,255,136,0.03)', borderBottom: '1px solid rgba(42,42,64,0.3)', fontSize: 10, fontFamily: 'monospace', color: '#4a5568', overflow: 'hidden', whiteSpace: 'nowrap' }}>
        <span style={{ color: '#00ff88' }}>🔥 Trending</span>
        {['AAPL', 'MSFT', 'NVDA', 'TSLA', 'BTC'].map(t => (
          <span key={t} style={{ color: '#c8d6d0', cursor: 'pointer' }}
            onClick={() => { try { window.open(`http://localhost:5173`, '_blank') } catch {} }}>
            {t} <span style={{ color: Math.random() > 0.5 ? '#00ff88' : '#ff4444' }}>{Math.random() > 0.5 ? '▲' : '▼'}{(Math.random() * 3).toFixed(2)}%</span>
          </span>
        ))}
      </div>

      {/* Content */}
      <div style={{ flex: 1, overflow: 'auto', padding: 16, maxWidth: 680, margin: '0 auto', width: '100%' }}>
        {loading && (
          <div style={{ textAlign: 'center', padding: 80 }}>
            <div style={{ fontSize: 40, animation: 'pulse 1.5s ease-in-out infinite', marginBottom: 12 }}>🐱</div>
            <div style={{ color: '#4a5568', fontSize: 12 }}>loading MiauBook...</div>
          </div>
        )}

        {!loading && tab === 'feed' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {!composing ? (
              <div onClick={() => setComposing(true)} style={{ ...style.card(), cursor: 'text', padding: '10px 14px', display: 'flex', alignItems: 'center', gap: 8 }}
                onMouseEnter={e => e.currentTarget.style.borderColor = 'rgba(0,230,118,0.2)'}
                onMouseLeave={e => e.currentTarget.style.borderColor = 'rgba(42,42,64,0.4)'}>
                <span style={{ fontSize: 18 }}>🐱</span>
                <span style={{ fontSize: 11, color: '#4a5568' }}>What's on your mind, trader?</span>
              </div>
            ) : (
              <div style={{ ...style.card(), padding: '10px 14px' }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: 8 }}>
                  <span style={{ fontSize: 18 }}>🐱</span>
                  <input ref={inputRef} type="text" value={draft} onChange={e => setDraft(e.target.value)}
                    onKeyDown={e => { if (e.key === 'Enter') handlePost(); if (e.key === 'Escape') { setComposing(false); setDraft('') } }}
                    placeholder="Share your trade idea..."
                    style={{ flex: 1, background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(0,230,118,0.2)', borderRadius: 4, padding: '6px 10px', color: '#e0e0e0', fontSize: 12, outline: 'none', fontFamily: 'monospace' }}
                  />
                </div>
                <div style={{ display: 'flex', gap: 6, justifyContent: 'flex-end', marginTop: 8 }}>
                  <button onClick={() => { setComposing(false); setDraft('') }} style={style.btn()}>Cancel</button>
                  <button onClick={handlePost} style={style.btn(true)} disabled={!draft.trim()}>📤 Post</button>
                </div>
              </div>
            )}

            {posts.map(p => (
              <div key={p.id} style={style.card()} onMouseEnter={e => e.currentTarget.style.borderColor = 'rgba(0,230,118,0.12)'}
                onMouseLeave={e => e.currentTarget.style.borderColor = 'rgba(42,42,64,0.4)'}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                  <span style={{ fontSize: 16 }}>{p.avatar}</span>
                  <span style={{ fontWeight: 600, fontSize: 12, color: '#e0e0e0' }}>{p.author}</span>
                  <span style={{ fontSize: 9, color: '#4a5568', marginLeft: 'auto' }}>{p.time}</span>
                </div>
                <div style={{ fontSize: 12, color: '#c0c0c0', marginBottom: 10, lineHeight: 1.6, paddingLeft: 24 }}>{p.message}</div>
                <div style={{ display: 'flex', gap: 12, fontSize: 11, color: '#4a5568', alignItems: 'center' }}>
                  <button onClick={() => toggleLike(p.id)} style={{ background: 'none', border: 'none', cursor: 'pointer', color: p.liked ? '#ef4444' : '#4a5568', fontSize: 11, display: 'flex', alignItems: 'center', gap: 4, padding: 0 }}>
                    {p.liked ? '❤️' : '👍'} {p.likes}
                  </button>
                  <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>💬 {p.comments}</span>
                  <div style={{ marginLeft: 'auto', display: 'flex', gap: 2 }}>
                    {CAT_EMOJIS.slice(0, 4).map(e => (
                      <button key={e} onClick={() => addReaction(p.id, e)}
                        style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: 11, padding: '1px 3px', borderRadius: 3, opacity: 0.5, transition: 'all 0.15s' }}
                        onMouseEnter={e2 => e2.currentTarget.style.opacity = '1'}
                        onMouseLeave={e2 => e2.currentTarget.style.opacity = '0.5'}>
                        {e}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ))}

            {feed.map(a => (
              <div key={a.id} style={{ ...style.card(), padding: '8px 14px', display: 'flex', alignItems: 'center', gap: 8 }}>
                <span style={{ fontSize: 11, color: '#4a5568' }}>🐾</span>
                <span style={{ color: '#00e676', fontSize: 11, fontWeight: 600 }}>{a.username}</span>
                <span style={{ color: '#8899b0', fontSize: 10 }}>{a.message || a.action_type}</span>
                <span style={{ fontSize: 9, color: '#4a5568', marginLeft: 'auto' }}>{a.created_at?.slice(0, 10) || ''}</span>
              </div>
            ))}
          </div>
        )}

        {!loading && tab === 'leaderboard' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            <div style={{ fontSize: 11, color: '#8899b0', marginBottom: 6 }}>🏆 Top Cat Traders — Monthly Returns</div>
            {leaderboard.map((e, i) => (
              <div key={i} style={{
                ...style.card(i < 3), display: 'flex', alignItems: 'center', gap: 10,
                background: i === 0 ? 'rgba(255,215,0,0.06)' : i === 1 ? 'rgba(192,192,192,0.04)' : i === 2 ? 'rgba(205,127,50,0.04)' : 'rgba(19,19,26,0.85)',
                borderColor: i === 0 ? 'rgba(255,215,0,0.2)' : i === 1 ? 'rgba(192,192,192,0.15)' : i === 2 ? 'rgba(205,127,50,0.15)' : 'rgba(42,42,64,0.4)',
              }}>
                <span style={{ color: i === 0 ? '#ffd700' : i === 1 ? '#c0c0c0' : i === 2 ? '#cd7f32' : '#4a5568', fontSize: 14, fontWeight: 'bold', width: 24, textAlign: 'center' }}>
                  {i < 3 ? ['🥇', '🥈', '🥉'][i] : `#${i + 1}`}
                </span>
                <span style={{ fontSize: 14 }}>{e.username.split(' ')[0]}</span>
                <span style={{ color: '#e0e0e0', fontSize: 12, flex: 1 }}>{e.username.replace(/^[^\s]+\s/, '')}</span>
                <span style={{ color: '#00e676', fontSize: 13, fontWeight: 600 }}>{e.value?.toFixed(1)}%</span>
                <span style={{ color: '#4a5568', fontSize: 10 }}>{e.positions} trades</span>
              </div>
            ))}
          </div>
        )}

        {!loading && tab === 'notifications' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
              <span style={{ fontSize: 11, color: '#8899b0' }}>🔔 Notifications ({unreadNotifs} unread)</span>
              {unreadNotifs > 0 && (
                <button onClick={markAllRead} style={style.btn()} onMouseEnter={e => { e.currentTarget.style.borderColor = 'rgba(0,230,118,0.3)'; e.currentTarget.style.color = '#00e676' }}
                  onMouseLeave={e => { e.currentTarget.style.borderColor = 'rgba(42,42,64,0.4)'; e.currentTarget.style.color = '#8899b0' }}>✓ Mark all read</button>
              )}
            </div>
            {notifications.map(n => (
              <div key={n.id} style={{ ...style.card(), padding: '8px 14px', display: 'flex', alignItems: 'center', gap: 8, opacity: n.is_read ? 0.6 : 1 }}>
                <span style={{ fontSize: 14 }}>{n.is_read ? '📭' : '📬'}</span>
                <span style={{ color: n.is_read ? '#8899b0' : '#e0e0e0', fontSize: 11, flex: 1 }}>{n.message || n.type}</span>
                <span style={{ fontSize: 9, color: '#4a5568', whiteSpace: 'nowrap' }}>{n.created_at?.slice(0, 10) || ''}</span>
                <button onClick={() => clearNotif(n.id)} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#4a5568', fontSize: 10, padding: '2px 4px' }}>✕</button>
              </div>
            ))}
            {notifications.length === 0 && <div style={{ textAlign: 'center', color: '#4a5568', padding: 40, fontSize: 11 }}>🔔 No notifications. Follow some cats!</div>}
          </div>
        )}

        {!loading && tab === 'profile' && (
          <div style={{ ...style.card(), textAlign: 'center', padding: 24, maxWidth: 400, margin: '0 auto' }}>
            <div style={{ fontSize: 48, marginBottom: 4, animation: 'pulse 3s ease-in-out infinite' }}>{profile.avatar}</div>
            <h2 style={{ fontSize: 18, fontWeight: 'bold', margin: '4px 0 2px', color: '#e0e0e0' }}>{profile.username}</h2>
            <p style={{ fontSize: 10, color: '#8899b0', marginBottom: 2 }}>{profile.bio}</p>
            <p style={{ fontSize: 9, color: '#4a5568', marginBottom: 10 }}>Cat trader · Miau since {profile.joined}</p>
            <div style={{ display: 'flex', justifyContent: 'center', gap: 32, margin: '12px 0 16px' }}>
              <div><div style={{ fontSize: 18, fontWeight: 'bold', color: '#00e676' }}>{followers}</div><div style={{ fontSize: 9, color: '#4a5568' }}>Followers</div></div>
              <div><div style={{ fontSize: 18, fontWeight: 'bold', color: '#00e676' }}>{profile.following}</div><div style={{ fontSize: 9, color: '#4a5568' }}>Following</div></div>
              <div><div style={{ fontSize: 18, fontWeight: 'bold', color: '#00e676' }}>{profile.badges.length}</div><div style={{ fontSize: 9, color: '#4a5568' }}>Badges</div></div>
            </div>
            <button onClick={handleFollow} style={{
              padding: '6px 20px', borderRadius: 20, cursor: 'pointer', fontSize: 11, fontWeight: 600,
              background: isFollowing ? 'rgba(0,230,118,0.1)' : 'rgba(0,230,118,0.2)',
              color: isFollowing ? '#00e676' : '#0a0a0f',
              border: isFollowing ? '1px solid rgba(0,230,118,0.3)' : '1px solid transparent',
              transition: 'all 0.2s', marginBottom: 12,
            }}>{isFollowing ? '✓ Following' : '+ Follow'}</button>
            <div style={{ display: 'flex', gap: 6, justifyContent: 'center', flexWrap: 'wrap' }}>
              {profile.badges.map((b, i) => (
                <span key={i} style={{ padding: '2px 8px', background: 'rgba(0,230,118,0.06)', border: '1px solid rgba(0,230,118,0.1)', borderRadius: 10, fontSize: 9, color: '#8899b0', display: 'flex', alignItems: 'center', gap: 3 }}>
                  {b.icon} {b.name.replace('_', ' ')}
                </span>
              ))}
            </div>
          </div>
        )}

        <pre style={{ fontSize: 6, lineHeight: '8px', color: 'rgba(0,230,118,0.08)', marginTop: 24, textAlign: 'center', fontFamily: 'monospace', userSelect: 'none' }}>{CAT_ART}</pre>
      </div>

      <div style={{ padding: '5px 16px', background: 'rgba(19,19,26,0.95)', borderTop: '1px solid rgba(42,42,64,0.3)', fontSize: 9, color: 'rgba(136,153,176,0.2)', textAlign: 'center', flexShrink: 0, fontFamily: 'monospace' }}>
        📕 MiauBook · where cats trade · feed · like · follow · lead · 🐟
      </div>
    </div>
  )
}
