import { useState } from 'react'
import type { User } from '../App'
import { apiFetch } from '../lib/api'

interface Props {
  onClose: () => void
  onLogin: (user: User) => void
}

export function AuthModal({ onClose, onLogin }: Props) {
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (mode === 'register') {
        await apiFetch('/api/v1/auth/register', {
          method: 'POST',
          body: JSON.stringify({ email, username, password }),
        })
        setMode('login')
        setLoading(false)
        return
      }

      const res = await apiFetch<{ access_token: string }>('/api/v1/auth/token', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      })

      localStorage.setItem('miau_token', res.access_token)

      // For demo: if backend doesn't have tier info, default to 'pro' for registered users
      onLogin({
        username: username || email.split('@')[0] || 'trader',
        email: email || `${username}@miau.edu`,
        tier: 'free',
      })
    } catch {
      setError(mode === 'login' ? 'Invalid credentials. Please try again.' : 'Registration failed')
    }
    setLoading(false)
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-miau-bg/90 backdrop-blur-sm" onClick={onClose}>
      <div className="bg-miau-surface border border-miau-border rounded-lg w-full max-w-md p-6 mx-4" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-2">
            <span className="text-xl">🐱</span>
            <span className="text-xs font-bold text-miau-green">{mode === 'login' ? 'Sign In' : 'Create Account'}</span>
          </div>
          <button onClick={onClose} className="text-miau-text-dim hover:text-miau-text text-xs font-mono">✕</button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          {mode === 'register' && (
            <div>
              <label className="text-[10px] text-miau-text-dim block mb-1 font-mono uppercase">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 bg-miau-bg border border-miau-border/50 rounded text-sm text-miau-text font-mono placeholder:text-miau-text-dim/30 outline-none focus:border-miau-green/50 transition-colors"
                placeholder="trader@miau.finance"
                required
              />
            </div>
          )}
          <div>
            <label className="text-[10px] text-miau-text-dim block mb-1 font-mono uppercase">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 bg-miau-bg border border-miau-border/50 rounded text-sm text-miau-text font-mono placeholder:text-miau-text-dim/30 outline-none focus:border-miau-green/50 transition-colors"
              placeholder="admin"
              required
            />
          </div>
          <div>
            <label className="text-[10px] text-miau-text-dim block mb-1 font-mono uppercase">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 bg-miau-bg border border-miau-border/50 rounded text-sm text-miau-text font-mono placeholder:text-miau-text-dim/30 outline-none focus:border-miau-green/50 transition-colors"
              placeholder="••••••••"
              required
            />
          </div>

          {error && (
            <div className="p-2 bg-miau-red/10 border border-miau-red/20 rounded text-xs text-miau-red font-mono">
              {error}
            </div>
          )}

          {mode === 'register' && (
            <div className="p-2 bg-miau-green/5 border border-miau-green/10 rounded text-[10px] text-miau-text-dim">
              After registration, you'll be redirected to log in.
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 bg-miau-green text-miau-bg rounded font-bold font-mono text-sm hover:bg-miau-green/90 transition-colors disabled:opacity-50"
          >
            {loading ? '...' : mode === 'login' ? 'Sign In' : 'Create Account'}
          </button>
        </form>

        <div className="mt-4 text-center">
          <button
            onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setError('') }}
            className="text-xs text-miau-text-dim hover:text-miau-green font-mono transition-colors"
          >
            {mode === 'login' ? "Don't have an account? Register" : 'Already have an account? Sign in'}
          </button>
        </div>

        <div className="mt-3 pt-3 border-t border-miau-border/30 text-center">
          <button
            onClick={async () => {
              try {
                const res = await fetch('/api/v1/auth/education-student', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                })
                if (res.ok) {
                  const data = await res.json()
                  localStorage.setItem('miau_token', data.access_token)
                }
              } catch {}
              onLogin({ username: 'guest_cat', email: 'guest@miau.edu', tier: 'free' })
            }}
            className="text-xs text-miau-text-dim/50 hover:text-miau-text-dim font-mono transition-colors"
          >
            🎓 Continue as Student (free courses + live data)
          </button>
        </div>
      </div>
    </div>
  )
}
