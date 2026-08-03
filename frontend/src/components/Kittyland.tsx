import { useState, useCallback, useRef, useEffect } from 'react'

export interface KittyPanel {
  id: string
  title: string
  content: string
  icon?: string
  x: number
  y: number
  w: number
  h: number
  pinned?: boolean
  url?: string          // If set, renders an iframe instead of text content
  refreshKey?: number   // Bumps when user wants to reload the iframe
}

interface KittylandProps {
  panels: KittyPanel[]
  onClose: (id: string) => void
  onPin: (id: string) => void
  onClear: () => void
  onRefresh?: (id: string) => void
}

export default function Kittyland({ panels, onClose, onPin, onClear, onRefresh }: KittylandProps) {
  const [dragging, setDragging] = useState<string | null>(null)
  const dragRef = useRef({ startX: 0, startY: 0, panelX: 0, panelY: 0 })

  const handleMouseDown = useCallback((e: React.MouseEvent, id: string) => {
    const panel = panels.find(p => p.id === id)
    if (!panel) return
    setDragging(id)
    dragRef.current = { startX: e.clientX, startY: e.clientY, panelX: panel.x, panelY: panel.y }
  }, [panels])

  useEffect(() => {
    if (!dragging) return
    const handleMove = (e: MouseEvent) => {
      const dx = e.clientX - dragRef.current.startX
      const dy = e.clientY - dragRef.current.startY
      const panel = panels.find(p => p.id === dragging)
      if (!panel) return
      panel.x = Math.max(0, Math.min(100, dragRef.current.panelX + dx / 12))
      panel.y = Math.max(0, Math.min(100, dragRef.current.panelY + dy / 12))
      // Force re-render by updating state
      setDragging(dragging)
    }
    const handleUp = () => setDragging(null)
    window.addEventListener('mousemove', handleMove)
    window.addEventListener('mouseup', handleUp)
    return () => { window.removeEventListener('mousemove', handleMove); window.removeEventListener('mouseup', handleUp) }
  }, [dragging, panels])

  if (panels.length === 0) return null

  return (
    <div className="absolute inset-0 z-50 pointer-events-none">
      {/* Panel container */}
      {panels.map((panel) => (
        <div
          key={panel.id}
          className="pointer-events-auto absolute rounded-lg overflow-hidden border border-green/20 bg-gray-950/95 shadow-2xl shadow-green/5"
          style={{
            left: `${panel.x}%`, top: `${panel.y}%`,
            width: `${panel.w}%`, height: `${panel.h}%`,
            minWidth: 200, minHeight: 100,
            zIndex: dragging === panel.id ? 100 : 50,
          }}
        >
          {/* Title bar */}
          <div
            className="flex items-center justify-between px-2 py-1 bg-gray-900 border-b border-green/10 cursor-move select-none"
            onMouseDown={(e) => handleMouseDown(e, panel.id)}
          >
            <span className="text-[10px] text-green/70 font-mono truncate">
              {panel.icon || '📦'} {panel.title}
            </span>
            <div className="flex gap-1">
              <button
                onClick={() => onPin(panel.id)}
                className={`text-[10px] px-1 rounded ${panel.pinned ? 'text-yellow' : 'text-dim/30 hover:text-dim/60'}`}
                title={panel.pinned ? 'Unpin' : 'Pin'}
              >📌</button>
              <button
                onClick={() => onClose(panel.id)}
                className="text-[10px] px-1 text-dim/30 hover:text-red-400"
              >✕</button>
            </div>
          </div>
          {/* Content */}
          {panel.url ? (
            <div className="relative h-[calc(100%-28px)]">
              <iframe
                key={panel.refreshKey || 0}
                src={panel.url}
                className="w-full h-full border-0 bg-white"
                title={panel.title}
                sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
              />
              <div className="absolute top-1 right-8 flex gap-1">
                <button
                  onClick={(e) => { e.stopPropagation(); onRefresh?.(panel.id) }}
                  className="text-[9px] bg-gray-800/80 hover:bg-gray-700 rounded px-1.5 py-0.5 text-dim/60 hover:text-green/80"
                  title="Reload"
                >↻</button>
              </div>
            </div>
          ) : (
            <div className="p-2 h-[calc(100%-28px)] overflow-y-auto font-mono text-[11px] leading-relaxed text-gray-300 whitespace-pre-wrap">
              {panel.content}
            </div>
          )}
        </div>
      ))}

      {/* Panel count badge */}
      <div className="pointer-events-auto absolute bottom-2 right-2 bg-gray-900/80 border border-green/10 rounded px-2 py-1 text-[9px] text-green/50 font-mono">
        🖥️ {panels.length} panel{panels.length > 1 ? 's' : ''}
        <button onClick={onClear} className="ml-2 text-dim/30 hover:text-red-400">✕ all</button>
      </div>
    </div>
  )
}
