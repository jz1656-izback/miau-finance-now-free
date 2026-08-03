import { useEffect, useRef } from 'react'

const EMOJIS = ['🐱','😸','😹','😻','😺','🐟','🎉','✨','💫','🌟','⭐','🌈','🎊','🎈','🎀','💎','🔮','🎵','🎶','💃','🕺','🪩','⚡','🔥','💥','🍕','🧁','🍦','🎂']

export default function RaveOverlay({ active }: { active: boolean }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (!active || !canvasRef.current) return
    const canvas = canvasRef.current
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
    const ctx = canvas.getContext('2d')!
    const particles: { x: number; y: number; speed: number; size: number; emoji: string; drift: number; hue: number }[] = []

    for (let i = 0; i < 60; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: -50 - Math.random() * canvas.height,
        speed: 1 + Math.random() * 3,
        size: 14 + Math.random() * 20,
        emoji: EMOJIS[Math.floor(Math.random() * EMOJIS.length)],
        drift: (Math.random() - 0.5) * 1.5,
        hue: Math.random() * 360,
      })
    }

    let hueShift = 0
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      hueShift += 0.5

      particles.forEach(p => {
        p.y += p.speed
        p.x += p.drift + Math.sin(p.y * 0.01) * 0.5
        if (p.y > canvas.height + 50) { p.y = -50; p.x = Math.random() * canvas.width }
        if (p.x < -50) p.x = canvas.width + 50
        if (p.x > canvas.width + 50) p.x = -50

        ctx.save()
        ctx.globalAlpha = 0.7 + Math.sin(p.y * 0.02) * 0.2
        ctx.font = `${p.size}px sans-serif`
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillText(p.emoji, p.x, p.y)
        ctx.restore()
      })

      id = requestAnimationFrame(animate)
    }
    let id = requestAnimationFrame(animate)

    return () => cancelAnimationFrame(id)
  }, [active])

  if (!active) return null

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh',
        zIndex: 99998, pointerEvents: 'none',
      }}
    />
  )
}
