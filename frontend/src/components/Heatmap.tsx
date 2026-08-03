import { useState, useEffect, useCallback, useRef } from 'react'
import { createPinchZoomHandler, createTapHandler } from '../lib/gestures'

interface SectorData {
  ticker: string
  name: string
  price: number
  change_pct: number
}

interface AnomalyData {
  ticker: string
  anomaly_score: number
  is_anomaly: boolean
}

interface HeatmapProps {
  data: SectorData[]
  width?: number
  height?: number
  mode?: 'change' | 'correlation' | 'anomaly'
  anomalyData?: AnomalyData[]
}

export default function Heatmap({ data, width = 400, height = 300, mode = 'change', anomalyData }: HeatmapProps) {
  const [canvasRef, setCanvasRef] = useState<HTMLCanvasElement | null>(null)
  const [sectorData, setSectorData] = useState<SectorData[]>([])
  const [displayMode, setDisplayMode] = useState<'change' | 'correlation' | 'anomaly'>(mode)
  const [tooltip, setTooltip] = useState<{ x: number; y: number; text: string } | null>(null)
  const [zoom, setZoom] = useState(1)
  const heatmapRef = useRef<HTMLDivElement>(null)
  const lastPinchScale = useRef(1)

  const pinchZoom = createPinchZoomHandler((scale) => {
    setZoom(s => Math.max(0.5, Math.min(5, s * scale / lastPinchScale.current)))
    lastPinchScale.current = scale
  })

  const tapHandler = createTapHandler(
    (x, y) => {
      if (!heatmapRef.current) return
      const rect = heatmapRef.current.getBoundingClientRect()
      const mx = x - rect.left
      const my = y - rect.top
      const cols = Math.ceil(Math.sqrt(sectorData.length))
      const cellW = width / cols
      const cellH = height / Math.ceil(sectorData.length / cols)
      const col = Math.floor(mx / cellW)
      const row = Math.floor(my / cellH)
      const idx = row * cols + col
      if (idx >= 0 && idx < sectorData.length) {
        const s = sectorData[idx]
        setTooltip({ x: mx, y: my, text: `${s.ticker}: ${s.change_pct >= 0 ? '+' : ''}${s.change_pct.toFixed(2)}%` })
      }
    },
    () => {
      setZoom(1)
    }
  )

  useEffect(() => {
    setSectorData(data)
  }, [data])

  const getAnomalyScore = useCallback((ticker: string): number => {
    if (!anomalyData) return 0
    const found = anomalyData.find(a => a.ticker === ticker)
    return found ? found.anomaly_score : 0
  }, [anomalyData])

  const drawHeatmap = useCallback(() => {
    if (!canvasRef || !sectorData.length) return

    const ctx = canvasRef.getContext('2d')
    if (!ctx) return

    ctx.clearRect(0, 0, width, height)
    ctx.fillStyle = '#0a1a14'
    ctx.fillRect(0, 0, width, height)

    if (sectorData.length === 0) {
      ctx.fillStyle = '#666'
      ctx.font = '12px monospace'
      ctx.fillText('No sector data', 10, 20)
      return
    }

    const cols = Math.ceil(Math.sqrt(sectorData.length))
    const rows = Math.ceil(sectorData.length / cols)
    const cellWidth = width / cols
    const cellHeight = height / rows
    const padding = 2

    const changes = sectorData.map(d => d.change_pct)
    const minChange = Math.min(...changes)
    const maxChange = Math.max(...changes)
    const range = maxChange - minChange || 1

    const maxAnomaly = anomalyData ? Math.max(...anomalyData.map(a => a.anomaly_score), 1) : 1

    sectorData.forEach((sector, index) => {
      const row = Math.floor(index / cols)
      const col = index % cols

      const x = col * cellWidth + padding
      const y = row * cellHeight + padding
      const cellW = cellWidth - padding * 2
      const cellH = cellHeight - padding * 2

      if (displayMode === 'anomaly' && anomalyData) {
        const score = getAnomalyScore(sector.ticker)
        const intensity = Math.min(score / maxAnomaly, 1)
        const red = Math.round(255 * intensity)
        const green = Math.round(60 * (1 - intensity))
        ctx.fillStyle = `rgb(${red}, ${green}, 50)`
      } else {
        const normalized = (sector.change_pct - minChange) / range
        const hue = normalized * 120
        ctx.fillStyle = `hsl(${hue}, 80%, ${30 + normalized * 30}%)`
      }

      ctx.fillRect(x, y, cellW, cellH)
      ctx.strokeStyle = '#1a3a2a'
      ctx.lineWidth = 1
      ctx.strokeRect(x, y, cellW, cellH)

      ctx.fillStyle = '#00ff88'
      ctx.font = '10px monospace'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      ctx.fillText(sector.ticker, x + cellW / 2, y + cellH * 0.3)

      if (displayMode === 'anomaly') {
        const score = getAnomalyScore(sector.ticker)
        ctx.fillStyle = score > 0.8 ? '#ff4444' : score > 0.5 ? '#ffaa00' : '#00ff88'
        ctx.fillText(`score: ${score.toFixed(2)}`, x + cellW / 2, y + cellH * 0.7)
      } else {
        const changeText = `${sector.change_pct >= 0 ? '+' : ''}${sector.change_pct.toFixed(1)}%`
        ctx.fillStyle = sector.change_pct >= 0 ? '#00ff88' : '#ff4444'
        ctx.fillText(changeText, x + cellW / 2, y + cellH * 0.7)
      }
    })
  }, [canvasRef, sectorData, width, height, displayMode, anomalyData, getAnomalyScore])

  useEffect(() => {
    drawHeatmap()
  }, [drawHeatmap])

  useEffect(() => {
    if (!canvasRef) return
    const resizeObserver = new ResizeObserver(() => drawHeatmap())
    resizeObserver.observe(canvasRef)
    return () => resizeObserver.disconnect()
  }, [drawHeatmap])

  return (
    <div className="relative">
      <div className="flex gap-2 mb-2">
        {(['change', 'correlation', 'anomaly'] as const).map(m => (
          <button
            key={m}
            onClick={() => setDisplayMode(m)}
            className={`text-xs px-2 py-1 rounded border transition-colors ${
              displayMode === m
                ? 'bg-green/20 border-green text-green'
                : 'border-[#1a3a2a] text-dim hover:text-green'
            }`}
          >
            {m}
          </button>
        ))}
      </div>
      <div ref={heatmapRef} className="relative overflow-hidden"
        style={{ transform: `scale(${zoom})`, transformOrigin: 'top left' }}
      >
        <canvas
          ref={setCanvasRef}
          width={width}
          height={height}
          className="border border-gray-600"
          onMouseMove={(e) => {
            if (!canvasRef) return
            const rect = canvasRef.getBoundingClientRect()
            const mx = e.clientX - rect.left
            const my = e.clientY - rect.top
            const cols = Math.ceil(Math.sqrt(sectorData.length))
            const cellW = width / cols
            const cellH = height / Math.ceil(sectorData.length / cols)
            const col = Math.floor(mx / cellW)
            const row = Math.floor(my / cellH)
            const idx = row * cols + col
            if (idx >= 0 && idx < sectorData.length) {
              const s = sectorData[idx]
              if (displayMode === 'anomaly') {
                const score = getAnomalyScore(s.ticker)
                setTooltip({ x: mx, y: my, text: `${s.ticker}: anomaly score ${score.toFixed(3)}` })
              } else {
                setTooltip({ x: mx, y: my, text: `${s.ticker}: ${s.change_pct >= 0 ? '+' : ''}${s.change_pct.toFixed(2)}%` })
              }
            } else {
              setTooltip(null)
            }
          }}
          onMouseLeave={() => setTooltip(null)}
          onTouchStart={(e) => { pinchZoom.onTouchStart(e.nativeEvent); tapHandler.onTouchStart?.(e.nativeEvent as any) }}
          onTouchMove={(e) => pinchZoom.onTouchMove(e.nativeEvent)}
          onTouchEnd={(e) => { pinchZoom.onTouchEnd(); tapHandler.onTouchEnd(e.nativeEvent) }}
        />
      </div>
      {tooltip && (
        <div
          className="absolute bg-black/80 text-green text-xs px-2 py-1 rounded pointer-events-none z-10"
          style={{ left: tooltip.x + 10, top: tooltip.y - 30 }}
        >
          {tooltip.text}
        </div>
      )}
    </div>
  )
}
