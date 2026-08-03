import { useState } from 'react'

const countries = [
  { code: 'US', name: 'United States', lat: 37.09, lng: -95.71, market: 'NYSE/NASDAQ', flag: '🇺🇸' },
  { code: 'GB', name: 'United Kingdom', lat: 55.38, lng: -3.44, market: 'LSE', flag: '🇬🇧' },
  { code: 'JP', name: 'Japan', lat: 36.20, lng: 138.25, market: 'TSE', flag: '🇯🇵' },
  { code: 'CN', name: 'China', lat: 35.86, lng: 104.19, market: 'SSE/SZSE', flag: '🇨🇳' },
  { code: 'DE', name: 'Germany', lat: 51.17, lng: 10.45, market: 'FSE', flag: '🇩🇪' },
  { code: 'FR', name: 'France', lat: 46.60, lng: 2.21, market: 'EURONEXT', flag: '🇫🇷' },
  { code: 'IN', name: 'India', lat: 20.59, lng: 78.96, market: 'NSE/BSE', flag: '🇮🇳' },
  { code: 'BR', name: 'Brazil', lat: -14.24, lng: -51.93, market: 'B3', flag: '🇧🇷' },
  { code: 'CA', name: 'Canada', lat: 56.13, lng: -106.35, market: 'TSX', flag: '🇨🇦' },
  { code: 'AU', name: 'Australia', lat: -25.27, lng: 133.78, market: 'ASX', flag: '🇦🇺' },
  { code: 'HK', name: 'Hong Kong', lat: 22.32, lng: 114.17, market: 'HKEX', flag: '🇭🇰' },
  { code: 'SG', name: 'Singapore', lat: 1.35, lng: 103.82, market: 'SGX', flag: '🇸🇬' },
  { code: 'CH', name: 'Switzerland', lat: 46.82, lng: 8.23, market: 'SIX', flag: '🇨🇭' },
  { code: 'KR', name: 'South Korea', lat: 35.91, lng: 127.77, market: 'KRX', flag: '🇰🇷' },
  { code: 'SE', name: 'Sweden', lat: 60.13, lng: 18.64, market: 'OMX', flag: '🇸🇪' },
  { code: 'NL', name: 'Netherlands', lat: 52.13, lng: 5.29, market: 'EURONEXT', flag: '🇳🇱' },
  { code: 'ZA', name: 'South Africa', lat: -30.56, lng: 22.94, market: 'JSE', flag: '🇿🇦' },
  { code: 'RU', name: 'Russia', lat: 61.52, lng: 105.32, market: 'MOEX', flag: '🇷🇺' },
  { code: 'MX', name: 'Mexico', lat: 23.63, lng: -102.55, market: 'BMV', flag: '🇲🇽' },
  { code: 'IT', name: 'Italy', lat: 41.87, lng: 12.57, market: 'BORSA ITALIANA', flag: '🇮🇹' },
]

export default function MapView() {
  const [hovered, setHovered] = useState<string | null>(null)

  return (
    <div
      className="min-h-screen"
      style={{ background: '#0a0a0a' }}
    >
      <div className="p-4 md:p-8">
        <div className="text-green text-sm mb-2">miau@finance:~$ map --world</div>
        <div className="text-cyan text-sm mb-4">📍 loading fish finder...</div>
        <div className="text-xs text-dim mb-6">hover a country to see market data</div>

        <div className="relative overflow-hidden rounded-lg border border-green/20"
          style={{ background: '#0d1a12' }}
        >
          {/* Simple world map using positioned country markers */}
          <svg viewBox="0 0 1200 600" className="w-full h-auto" style={{ filter: 'hue-rotate(120deg) saturate(0.5)' }}>
            {/* World outline (simplified) */}
            <rect x="0" y="0" width="1200" height="600" fill="#0a1a12" />

            {/* Grid lines */}
            {Array.from({length: 12}).map((_, i) => (
              <line key={`v${i}`} x1={i * 100} y1="0" x2={i * 100} y2="600" stroke="#0d2a1a" strokeWidth="0.5" />
            ))}
            {Array.from({length: 6}).map((_, i) => (
              <line key={`h${i}`} x1="0" y1={i * 100} x2="1200" y2={i * 100} stroke="#0d2a1a" strokeWidth="0.5" />
            ))}

            {/* Country markers with data points */}
            {countries.map((c, i) => {
              const x = ((c.lng + 180) / 360) * 1200
              const y = ((90 - c.lat) / 180) * 600
              const isHovered = hovered === c.code
              const perf = [1.2, -0.8, 2.1, -0.3, 0.5, 1.8, -1.5, 0.1, -0.6, 2.3, 1.1, -0.9, 0.7, -1.2, 0.3, -0.4, 1.5, -2.1, 0.8, -0.2]
              const p = perf[i % perf.length]
              const color = p >= 0 ? '#00ff88' : '#ff4444'

              return (
                <g
                  key={c.code}
                  onMouseEnter={() => setHovered(c.code)}
                  onMouseLeave={() => setHovered(null)}
                  style={{ cursor: 'crosshair' }}
                >
                  {/* Glow */}
                  <circle cx={x} cy={y} r={isHovered ? 30 : 15} fill={color} opacity={isHovered ? 0.15 : 0.05} />
                  {/* Dot */}
                  <circle cx={x} cy={y} r={isHovered ? 6 : 3} fill={color} opacity={0.8} />
                  {/* Pulse ring */}
                  <circle cx={x} cy={y} r={12} fill="none" stroke={color} strokeWidth="0.5" opacity={0.3}>
                    <animate attributeName="r" values="8;20;8" dur="3s" repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.4;0;0.4" dur="3s" repeatCount="indefinite" />
                  </circle>
                  {/* Label */}
                  {isHovered && (
                    <>
                      <text x={x} y={y - 18} textAnchor="middle" fill={color} fontSize="11" fontWeight="bold">
                        {c.flag} {c.code}
                      </text>
                      <rect x={x - 70} y={y + 8} width="140" height="55" rx="4" fill="#0a1a12" stroke={color} strokeWidth="0.5" opacity="0.95" />
                      <text x={x} y={y + 24} textAnchor="middle" fill="#00ff88" fontSize="10">{c.market}</text>
                      <text x={x} y={y + 37} textAnchor="middle" fill={color} fontSize="13" fontWeight="bold">{p >= 0 ? '+' : ''}{p}%</text>
                      <text x={x} y={y + 50} textAnchor="middle" fill="#335544" fontSize="8">{c.name}</text>
                    </>
                  )}
                </g>
              )
            })}

            {/* Connecting lines - financial flows */}
            {countries.slice(0, 8).map((c, i) => {
              const x1 = ((c.lng + 180) / 360) * 1200
              const y1 = ((90 - c.lat) / 180) * 600
              const next = countries[(i + 1) % 8]
              const x2 = ((next.lng + 180) / 360) * 1200
              const y2 = ((90 - next.lat) / 180) * 600
              return (
                <line key={`flow${i}`} x1={x1} y1={y1} x2={x2} y2={y2}
                  stroke="#00ff88" strokeWidth="0.3" opacity="0.15" strokeDasharray="4,4">
                  <animate attributeName="stroke-dashoffset" values="0;20" dur="2s" repeatCount="indefinite" />
                </line>
              )
            })}
          </svg>
        </div>

        {/* Country data panel */}
        <div className="mt-4 grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-2">
          {countries.map((c, i) => {
            const perf = [1.2, -0.8, 2.1, -0.3, 0.5, 1.8, -1.5, 0.1, -0.6, 2.3, 1.1, -0.9, 0.7, -1.2, 0.3, -0.4, 1.5, -2.1, 0.8, -0.2]
            const p = perf[i % perf.length]
            return (
              <div
                key={c.code}
                onMouseEnter={() => setHovered(c.code)}
                onMouseLeave={() => setHovered(null)}
                className="px-2 py-1.5 rounded cursor-crosshair transition-all text-xs"
                style={{
                  background: hovered === c.code ? '#0d2a1a' : 'transparent',
                  border: `1px solid ${hovered === c.code ? '#00ff8844' : 'transparent'}`,
                }}
              >
                <span className="text-green">{c.flag}</span>
                {' '}
                <span className="text-dim">{c.code}</span>
                {' '}
                <span className={p >= 0 ? 'text-green' : 'text-red'}>{p >= 0 ? '+' : ''}{p}%</span>
              </div>
            )
          })}
        </div>

        <div className="mt-8 text-xs text-dim border-t border-green/10 pt-4">
          <span className="text-green">🐟</span> fish finder active — {countries.length} markets tracked
          {' · '}
          <span className="text-green">←</span> type <span className="text-cyan">help</span> or <span className="text-cyan">back</span> to return to terminal
        </div>
      </div>
    </div>
  )
}
