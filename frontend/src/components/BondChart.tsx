import { useEffect, useRef } from 'react'
import { createPortal } from 'react-dom'

const BOND_DATA = [
  { name: 'US 10Y', yield_: 3.85, change: 0.02, color: '#00e676' },
  { name: 'US 2Y', yield_: 3.82, change: -0.01, color: '#22d3ee' },
  { name: 'DE 10Y', yield_: 2.45, change: 0.01, color: '#a855f7' },
  { name: 'UK 10Y', yield_: 4.12, change: -0.03, color: '#f472b6' },
  { name: 'JP 10Y', yield_: 0.95, change: 0.005, color: '#facc15' },
  { name: 'IT 10Y', yield_: 3.55, change: 0.04, color: '#fb923c' },
]

export default function BondChart({ onClose }: { onClose: () => void }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [onClose])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')!
    const W = canvas.width = window.innerWidth
    const H = canvas.height = window.innerHeight

    const draw = () => {
      ctx.clearRect(0, 0, W, H)
      ctx.fillStyle = '#0a1a14'
      ctx.fillRect(0, 0, W, H)

      ctx.fillStyle = '#00e676'
      ctx.font = '18px monospace'
      ctx.textAlign = 'center'
      ctx.fillText('📊 Global Bond Yields', W / 2, 35)

      const barW = Math.min(100, (W - 120) / BOND_DATA.length)
      const maxYield = Math.max(...BOND_DATA.map(b => b.yield_)) * 1.2
      const chartH = H - 160
      const bottomY = H - 80

      BOND_DATA.forEach((b, i) => {
        const x = 60 + i * (barW + 20)
        const barH = (b.yield_ / maxYield) * chartH
        const y = bottomY - barH

        // Bar
        const grad = ctx.createLinearGradient(x, y, x, bottomY)
        grad.addColorStop(0, b.color)
        grad.addColorStop(1, b.color + '33')
        ctx.fillStyle = grad
        ctx.beginPath()
        ctx.roundRect(x, y, barW, barH, [4, 4, 0, 0])
        ctx.fill()

        // Glow
        ctx.shadowColor = b.color
        ctx.shadowBlur = 10
        ctx.fillStyle = b.color + '44'
        ctx.beginPath()
        ctx.roundRect(x, y, barW, barH, [4, 4, 0, 0])
        ctx.fill()
        ctx.shadowBlur = 0

        // Yield value
        ctx.fillStyle = '#fff'
        ctx.font = '14px monospace'
        ctx.textAlign = 'center'
        ctx.fillText(b.yield_.toFixed(2) + '%', x + barW / 2, y - 8)

        // Change
        ctx.fillStyle = b.change >= 0 ? '#00e676' : '#ef4444'
        ctx.font = '11px monospace'
        ctx.fillText(`${b.change >= 0 ? '▲' : '▼'} ${Math.abs(b.change).toFixed(2)}%`, x + barW / 2, y - 24)

        // Label
        ctx.fillStyle = '#8899b0'
        ctx.font = '11px monospace'
        ctx.textAlign = 'center'
        const lines = b.name.split(' ')
        lines.forEach((line, li) => {
          ctx.fillText(line, x + barW / 2, bottomY + 16 + li * 14)
        })
      })

      // Spread indicator
      ctx.fillStyle = '#557755'
      ctx.font = '10px monospace'
      ctx.textAlign = 'left'
      ctx.fillText('Bond yields move inversely to prices. The cat knows this.', 60, H - 20)
    }

    draw()
    window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; draw() })
  }, [])

  return createPortal(
    <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', zIndex: 99999, background: '#0a1a14' }}>
      <canvas ref={canvasRef} style={{ width: '100%', height: '100%' }} />
      <button onClick={onClose} style={{ position: 'fixed', top: 8, left: 8, zIndex: 100000, padding: '4px 12px', fontSize: 13, color: '#fff', background: '#1a1a1a', border: '1px solid #444', borderRadius: 4, cursor: 'pointer', fontFamily: 'monospace' }}>← Back</button>
      <div style={{ position: 'fixed', bottom: 8, right: 12, zIndex: 100000, fontSize: 11, fontFamily: 'monospace', color: '#557755' }}>🐱 Global bond yields</div>
    </div>,
    document.body
  )
}
