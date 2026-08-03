import { useEffect, useRef } from 'react'
import { createPortal } from 'react-dom'

const YIELD_DATA = [
  { maturity: '1M', yield: 4.32 },
  { maturity: '3M', yield: 4.28 },
  { maturity: '6M', yield: 4.15 },
  { maturity: '1Y', yield: 3.95 },
  { maturity: '2Y', yield: 3.82 },
  { maturity: '3Y', yield: 3.75 },
  { maturity: '5Y', yield: 3.68 },
  { maturity: '7Y', yield: 3.72 },
  { maturity: '10Y', yield: 3.85 },
  { maturity: '20Y', yield: 4.05 },
  { maturity: '30Y', yield: 4.12 },
]

export default function TreasuryChart({ onClose }: { onClose: () => void }) {
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

    const pad = { top: 60, bottom: 60, left: 80, right: 40 }
    const chartW = W - pad.left - pad.right
    const chartH = H - pad.top - pad.bottom
    const minY = 3.0, maxY = 5.0
    const range = maxY - minY

    const draw = () => {
      ctx.clearRect(0, 0, W, H)
      ctx.fillStyle = '#0a1a14'
      ctx.fillRect(0, 0, W, H)

      // Grid
      ctx.strokeStyle = '#002211'
      ctx.lineWidth = 1
      for (let i = 0; i <= 10; i++) {
        const y = pad.top + (chartH / 10) * i
        ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(W - pad.right, y)
        ctx.stroke()
      }

      // Y-axis labels
      ctx.fillStyle = '#557755'
      ctx.font = '12px monospace'
      ctx.textAlign = 'right'
      for (let i = 0; i <= 10; i++) {
        const val = maxY - (range / 10) * i
        const y = pad.top + (chartH / 10) * i
        ctx.fillText(val.toFixed(2) + '%', pad.left - 8, y + 4)
      }

      // Yield curve line
      const points = YIELD_DATA.map((d, i) => ({
        x: pad.left + (chartW / (YIELD_DATA.length - 1)) * i,
        y: pad.top + chartH - ((d.yield - minY) / range) * chartH,
        label: d.maturity,
        value: d.yield,
      }))

      // Fill area
      ctx.beginPath()
      ctx.moveTo(points[0].x, pad.top + chartH)
      points.forEach(p => ctx.lineTo(p.x, p.y))
      ctx.lineTo(points[points.length - 1].x, pad.top + chartH)
      ctx.closePath()
      ctx.fillStyle = 'rgba(0,230,118,0.05)'
      ctx.fill()

      // Line
      ctx.beginPath()
      points.forEach((p, i) => i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y))
      ctx.strokeStyle = '#00e676'
      ctx.lineWidth = 3
      ctx.stroke()

      // Glow
      ctx.shadowColor = '#00e676'
      ctx.shadowBlur = 15
      ctx.beginPath()
      points.forEach((p, i) => i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y))
      ctx.strokeStyle = 'rgba(0,230,118,0.3)'
      ctx.lineWidth = 6
      ctx.stroke()
      ctx.shadowBlur = 0

      // Points
      points.forEach(p => {
        ctx.beginPath()
        ctx.arc(p.x, p.y, 4, 0, Math.PI * 2)
        ctx.fillStyle = '#00e676'
        ctx.fill()
        ctx.strokeStyle = '#0a1a14'
        ctx.lineWidth = 2
        ctx.stroke()

        // Labels
        ctx.fillStyle = '#8899b0'
        ctx.font = '11px monospace'
        ctx.textAlign = 'center'
        ctx.fillText(p.label, p.x, pad.top + chartH + 18)
        ctx.fillStyle = '#00e676'
        ctx.font = '10px monospace'
        ctx.fillText(p.value.toFixed(2) + '%', p.x, p.y - 12)
      })

      // Title
      ctx.fillStyle = '#00e676'
      ctx.font = '18px monospace'
      ctx.textAlign = 'center'
      ctx.fillText('📈 US Treasury Yield Curve', W / 2, 30)

      // Spread indicator
      const spread = YIELD_DATA[8].yield - YIELD_DATA[4].yield
      ctx.fillStyle = spread > 0 ? '#00e676' : '#ef4444'
      ctx.font = '13px monospace'
      ctx.textAlign = 'left'
      ctx.fillText(`10Y-2Y Spread: ${spread.toFixed(2)}% ${spread > 0 ? '📈' : '📉'}`, pad.left, pad.top - 12)
      ctx.fillStyle = '#557755'
      ctx.font = '10px monospace'
      ctx.fillText('Inverted yield curve signals recession. The cat watches.', pad.left, pad.top + chartH + 40)
    }

    draw()
    window.addEventListener('resize', () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
      draw()
    })
  }, [])

  return createPortal(
    <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', zIndex: 99999, background: '#0a1a14' }}>
      <canvas ref={canvasRef} style={{ width: '100%', height: '100%' }} />
      <button onClick={onClose}
        style={{ position: 'fixed', top: 8, left: 8, zIndex: 100000, padding: '4px 12px', fontSize: 13, color: '#fff', background: '#1a1a1a', border: '1px solid #444', borderRadius: 4, cursor: 'pointer', fontFamily: 'monospace' }}>
        ← Back
      </button>
      <div style={{ position: 'fixed', bottom: 8, right: 12, zIndex: 100000, fontSize: 11, fontFamily: 'monospace', color: '#557755' }}>
        🐱 Treasury yield curve · data from FRED
      </div>
    </div>,
    document.body
  )
}
