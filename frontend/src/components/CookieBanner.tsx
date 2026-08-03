import { useState, useEffect } from 'react'

export default function CookieBanner() {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const consent = localStorage.getItem('miau_cookie_consent')
    if (!consent) setVisible(true)
  }, [])

  const accept = () => {
    localStorage.setItem('miau_cookie_consent', 'accepted')
    setVisible(false)
  }

  const reject = () => {
    localStorage.setItem('miau_cookie_consent', 'rejected')
    setVisible(false)
  }

  if (!visible) return null

  return (
    <div style={{
      position: 'fixed', bottom: 0, left: 0, right: 0, zIndex: 999999,
      background: 'rgba(5,8,10,0.95)', borderTop: '1px solid rgba(0,255,136,0.2)',
      padding: '16px 24px', fontFamily: 'monospace', fontSize: 12,
      display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 16, flexWrap: 'wrap',
    }}>
      <span style={{ color: '#c8d6d0', maxWidth: 500 }}>
        🐱 This site uses cookies for analytics. No personal data is sold. 
        <a href="/impressum" style={{ color: '#00ff88', marginLeft: 6 }}>Impressum</a>
        <a href="/datenschutz" style={{ color: '#00ff88', marginLeft: 6 }}>Datenschutz</a>
      </span>
      <button onClick={reject} style={{
        padding: '6px 16px', fontSize: 11, fontFamily: 'monospace',
        background: 'transparent', border: '1px solid #444', borderRadius: 4,
        color: '#888', cursor: 'pointer',
      }}>Nur Notwendige</button>
      <button onClick={accept} style={{
        padding: '6px 16px', fontSize: 11, fontFamily: 'monospace',
        background: '#003322', border: '1px solid #00ff88', borderRadius: 4,
        color: '#00ff88', cursor: 'pointer',
      }}>✅ Alle Akzeptieren</button>
    </div>
  )
}
