import { useEffect, useRef } from 'react'

const EMOJIS = ['🎓', '📚', '🐱', '🐾', '✨', '📖', '🎯', '🌟', '💡', '📜']
const COLORS = ['#00e676', '#a855f7', '#22d3ee', '#f472b6', '#fb923c']

export default function EduBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    let animId: number
    const particles: { x: number; y: number; vx: number; vy: number; size: number; alpha: number; life: number; emoji: string }[] = []
    const mouse = { x: -999, y: -999 }

    const resize = () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight }
    resize()
    window.addEventListener('resize', resize)
    window.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY })

    for (let i = 0; i < 30; i++) {
      particles.push({
        x: Math.random() * canvas.width, y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.3, vy: (Math.random() - 0.5) * 0.2 - 0.1,
        size: 14 + Math.random() * 14, alpha: 0.08 + Math.random() * 0.12,
        life: Math.random() * 300, emoji: EMOJIS[Math.floor(Math.random() * EMOJIS.length)],
      })
    }

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      particles.forEach((p) => {
        p.x += p.vx; p.y += p.vy
        p.vx += (Math.random() - 0.5) * 0.015; p.vy += (Math.random() - 0.5) * 0.015
        p.life += 0.3
        const dx = p.x - mouse.x; const dy = p.y - mouse.y
        const dist = Math.sqrt(dx * dx + dy * dy)
        if (dist < 150) { p.x += (dx / dist) * 1.5; p.y += (dy / dist) * 1.5 }
        if (p.y < -40 || p.life > 500) { p.y = canvas.height + 20; p.x = Math.random() * canvas.width; p.life = 0; p.emoji = EMOJIS[Math.floor(Math.random() * EMOJIS.length)] }
        if (p.x < -40) p.x = canvas.width + 20; if (p.x > canvas.width + 40) p.x = -20
        const pulse = Math.sin(p.life * 0.03) * 0.04
        ctx.globalAlpha = p.alpha + pulse
        ctx.font = `${p.size}px sans-serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'
        ctx.fillText(p.emoji, p.x, p.y)
        if (Math.random() < 0.02) {
          ctx.globalAlpha = 0.06; const c = COLORS[Math.floor(Math.random() * COLORS.length)]
          ctx.shadowColor = c; ctx.shadowBlur = 18
          ctx.fillText('✨', p.x + (Math.random() - 0.5) * 28, p.y + (Math.random() - 0.5) * 28)
          ctx.shadowBlur = 0
        }
      })
      ctx.globalAlpha = 1
      animId = requestAnimationFrame(animate)
    }
    animate()
    return () => { cancelAnimationFrame(animId); window.removeEventListener('resize', resize) }
  }, [])

  return <canvas ref={canvasRef} className="fixed inset-0 pointer-events-none" style={{ zIndex: 0, opacity: 0.5 }} />
}
