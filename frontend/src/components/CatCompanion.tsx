import { useState, useEffect } from 'react'

interface CatState {
  name: string; emoji: string; pose: string; mood: string; tuna: number
}

const CATS = [
  { name: 'Whiskers', emoji: '🐱', poses: ['sleeping', 'sitting', 'stretching', 'pawing'] },
  { name: 'Mittens', emoji: '🐈', poses: ['watching', 'grooming', 'playing', 'eating'] },
  { name: 'Oreo', emoji: '🐈‍⬛', poses: ['hunting', 'climbing', 'napping', 'begging'] },
  { name: 'Simba', emoji: '🦁', poses: ['roaring', 'strutting', 'lounging', 'stalking'] },
  { name: 'Luna', emoji: '😺', poses: ['dancing', 'singing', 'cuddling', 'purring'] },
]

const MOODS = ['😸', '😻', '😾', '😴', '🤔', '🙀', '😽']

export default function CatCompanion() {
  const [cat, setCat] = useState<CatState>(() => {
    const saved = localStorage.getItem('miau-cat')
    if (saved) return JSON.parse(saved)
    return { name: 'Whiskers', emoji: '🐱', pose: 'sitting', mood: '😸', tuna: 0 }
  })
  const [visible] = useState(true)
  const [message, setMessage] = useState('')

  useEffect(() => {
    localStorage.setItem('miau-cat', JSON.stringify(cat))
  }, [cat])

  useEffect(() => {
    const interval = setInterval(() => {
      const cmds = parseInt(localStorage.getItem('miau-commands') || '0')
      const tuna = Math.floor(cmds / 5)
      if (tuna !== cat.tuna) setCat(prev => ({ ...prev, tuna }))
      if (Math.random() < 0.1) {
        const c = CATS[Math.floor(Math.random() * CATS.length)]
        setCat(prev => ({ ...prev, pose: c.poses[Math.floor(Math.random() * c.poses.length)] }))
      }
    }, 10000)
    return () => clearInterval(interval)
  }, [cat.tuna])

  const pet = () => {
    const mood = MOODS[Math.floor(Math.random() * MOODS.length)]
    setCat(prev => ({ ...prev, mood }))
    const purrs = ['purrr...', 'meow~', '*headbutts*', 'prrr prrr', 'mrrrow!']
    setMessage(purrs[Math.floor(Math.random() * purrs.length)])
    setTimeout(() => setMessage(''), 2000)
  }

  useEffect(() => {
    const handler = (e: CustomEvent) => {
      if (e.detail?.tuna) setCat(prev => ({ ...prev, tuna: prev.tuna + e.detail.tuna }))
    }
    window.addEventListener('miau-cat-earn' as any, handler as any)
    return () => window.removeEventListener('miau-cat-earn' as any, handler as any)
  }, [])

  if (!visible) return null

  return (
    <div
      className="fixed bottom-4 right-4 z-50 select-none cursor-pointer"
      onClick={pet}
      title={`${cat.name} — ${cat.tuna} 🐟`}
    >
      <div className="relative">
        <div className="text-4xl animate-bounce-slow">{cat.emoji}</div>
        <div className="absolute -top-1 -right-1 bg-yellow-900/80 text-yellow text-[9px] px-1 rounded-full">
          {cat.tuna}🐟
        </div>
        {message && (
          <div className="absolute -top-6 right-0 bg-gray-900/90 text-green text-[10px] px-2 py-0.5 rounded whitespace-nowrap">
            {message}
          </div>
        )}
      </div>
    </div>
  )
}
