import { useState, useEffect } from 'react'

export default function DarkModeToggle() {
  const [dark, setDark] = useState(() => {
    const saved = localStorage.getItem('miau:dark-mode')
    return saved !== null ? saved === 'true' : window.matchMedia('(prefers-color-scheme: dark)').matches
  })

  useEffect(() => {
    localStorage.setItem('miau:dark-mode', String(dark))
    if (dark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [dark])

  return (
    <button
      onClick={() => setDark(!dark)}
      className="text-green-400 hover:text-green-300 transition-colors px-2 py-1 text-sm font-mono"
      aria-label={dark ? 'Switch to light mode' : 'Switch to dark mode'}
    >
      {dark ? '☀️' : '🌙'}
    </button>
  )
}
