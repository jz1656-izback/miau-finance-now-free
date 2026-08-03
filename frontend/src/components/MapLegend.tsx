import { useState } from 'react'

interface MapLegendProps {
  regions?: { name: string; color: string }[]
  marketTypes?: { type: string; label: string; icon: string }[]
  onClose?: () => void
}

const DEFAULT_REGIONS = [
  { name: 'North America', color: '#00ff88' },
  { name: 'Europe', color: '#00ccff' },
  { name: 'Asia Pacific', color: '#ffcc00' },
  { name: 'South America', color: '#ff8844' },
  { name: 'Middle East', color: '#cc88ff' },
]

const DEFAULT_TYPES = [
  { type: 'exchange', label: 'Stock Exchange', icon: '🏛' },
  { type: 'index', label: 'Market Index', icon: '📊' },
  { type: 'commodity', label: 'Commodity', icon: '🛢' },
]

export default function MapLegend({
  regions = DEFAULT_REGIONS,
  marketTypes = DEFAULT_TYPES,
  onClose,
}: MapLegendProps) {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <div
      style={{
        position: 'absolute',
        left: 15,
        bottom: 50,
        background: 'rgba(10, 26, 46, 0.92)',
        border: '1px solid rgba(0, 200, 150, 0.35)',
        borderRadius: 6,
        padding: collapsed ? '6px 10px' : '10px',
        fontFamily: '"JetBrains Mono", monospace',
        fontSize: '10px',
        color: '#88ddbb',
        zIndex: 10,
        minWidth: 180,
        cursor: 'pointer',
        transition: 'all 0.2s',
      }}
      onClick={() => setCollapsed(c => !c)}
    >
      {collapsed ? (
        <div style={{ color: '#00ff88', fontSize: 11, userSelect: 'none' }}>
          📖 Legend
        </div>
      ) : (
        <>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: 8,
            }}
          >
            <div style={{ color: '#00ff88', fontWeight: 'bold', fontSize: 11, userSelect: 'none' }}>
              📖 Legend
            </div>
            {onClose && (
              <span
                style={{ color: '#4a7a8a', cursor: 'pointer', fontSize: 11 }}
                onClick={e => { e.stopPropagation(); onClose() }}
              >
                ✕
              </span>
            )}
          </div>

          {/* Change colors */}
          <div style={{ marginBottom: 8 }}>
            <div style={{ color: '#4a7a8a', fontSize: 9, marginBottom: 4, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Performance
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 2 }}>
              <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#00ff88', display: 'inline-block' }} />
              <span>Positive change</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 2 }}>
              <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#ff4444', display: 'inline-block' }} />
              <span>Negative change</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#88ddbb', display: 'inline-block' }} />
              <span>No data</span>
            </div>
          </div>

          {/* Regions */}
          <div style={{ marginBottom: 8 }}>
            <div style={{ color: '#4a7a8a', fontSize: 9, marginBottom: 4, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Regions
            </div>
            {regions.map(r => (
              <div key={r.name} style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 2 }}>
                <span style={{ width: 10, height: 10, borderRadius: 2, background: r.color, display: 'inline-block' }} />
                <span>{r.name}</span>
              </div>
            ))}
          </div>

          {/* Market types */}
          <div>
            <div style={{ color: '#4a7a8a', fontSize: 9, marginBottom: 4, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Market Types
            </div>
            {marketTypes.map(t => (
              <div key={t.type} style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 2 }}>
                <span style={{ fontSize: 12 }}>{t.icon}</span>
                <span>{t.label}</span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
