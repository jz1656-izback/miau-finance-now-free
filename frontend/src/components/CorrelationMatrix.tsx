import { useState } from 'react'

interface CorrelationMatrixProps {
  tickers: string[]
  matrix: Record<string, Record<string, number>>
  width?: number
  height?: number
}

function colorForCorrelation(val: number): string {
  if (val > 0.7) return 'bg-green-700/80'
  if (val > 0.4) return 'bg-green-600/60'
  if (val > 0.2) return 'bg-green-500/40'
  if (val > -0.2) return 'bg-gray-600/30'
  if (val > -0.4) return 'bg-red-500/40'
  if (val > -0.7) return 'bg-red-600/60'
  return 'bg-red-700/80'
}

function textColorForBg(val: number): string {
  if (Math.abs(val) > 0.4) return 'text-white'
  return 'text-gray-300'
}

export default function CorrelationMatrix({ tickers, matrix, width = 600, height = 500 }: CorrelationMatrixProps) {
  const [hovered, setHovered] = useState<{ row: number; col: number } | null>(null)

  const n = tickers.length
  if (n === 0) {
    return (
      <div className="flex items-center justify-center h-48 text-dim text-sm">
        No correlation data available
      </div>
    )
  }

  const cellSize = Math.min(
    Math.floor((width - 80) / n),
    Math.floor((height - 40) / n),
    48,
  )
  const tableWidth = cellSize * n
  const tableHeight = cellSize * n

  return (
    <div className="p-2">
      <div className="flex items-center gap-3 mb-3">
        <h3 className="text-sm font-bold text-cyan">Correlation Matrix</h3>
        <span className="text-[10px] text-dim">
          {n} assets &middot; hover for values
        </span>
      </div>
      <div
        className="relative overflow-auto"
        style={{ maxWidth: width, maxHeight: height }}
      >
        <svg width={tableWidth + 80} height={tableHeight + 40}>
          {/* Column headers (tickers along top) */}
          {tickers.map((t, i) => (
            <text
              key={`ch-${i}`}
              x={80 + cellSize * i + cellSize / 2}
              y={18}
              textAnchor="end"
              transform={`rotate(-45, ${80 + cellSize * i + cellSize / 2}, 18)`}
              className="fill-gray-400"
              style={{ fontSize: 10, fontFamily: 'monospace' }}
            >
              {t}
            </text>
          ))}

          {/* Row headers (tickers along left) */}
          {tickers.map((t, i) => (
            <text
              key={`rh-${i}`}
              x={72}
              y={40 + cellSize * i + cellSize / 2 + 3}
              textAnchor="end"
              className="fill-gray-400"
              style={{ fontSize: 10, fontFamily: 'monospace' }}
            >
              {t}
            </text>
          ))}

          {/* Cells */}
          {tickers.map((t1, i) =>
            tickers.map((_t2, j) => {
              const val = matrix[t1]?.[tickers[j]]
              const displayVal = val != null ? val.toFixed(3) : 'N/A'
              const isHovered = hovered?.row === i && hovered?.col === j
              const isSameRow = hovered?.row === i || hovered?.col === j

              return (
                <g key={`c-${i}-${j}`}>
                  <rect
                    x={80 + cellSize * j}
                    y={40 + cellSize * i}
                    width={cellSize}
                    height={cellSize}
                    rx={2}
                    className={
                      val != null
                        ? `${colorForCorrelation(val)} ${isHovered ? 'ring-2 ring-white/50' : ''} ${isSameRow && !isHovered ? 'opacity-70' : ''}`
                        : 'fill-gray-800'
                    }
                    style={{ transition: 'opacity 0.15s' }}
                    onMouseEnter={() => setHovered({ row: i, col: j })}
                    onMouseLeave={() => setHovered(null)}
                  />
                  {cellSize >= 36 && val != null && (
                    <text
                      x={80 + cellSize * j + cellSize / 2}
                      y={40 + cellSize * i + cellSize / 2 + 3}
                      textAnchor="middle"
                      className={textColorForBg(val)}
                      style={{ fontSize: Math.max(8, Math.min(11, cellSize / 4)), fontFamily: 'monospace' }}
                    >
                      {displayVal}
                    </text>
                  )}
                </g>
              )
            })
          )}
        </svg>

        {/* Tooltip */}
        {hovered && (
          <div
            className="absolute bg-gray-900/95 border border-gray-700 rounded px-2 py-1 text-xs text-green font-mono whitespace-nowrap z-10"
            style={{
              left: 80 + cellSize * hovered.col + cellSize / 2,
              top: 40 + cellSize * hovered.row + cellSize + 8,
              transform: 'translateX(-50%)',
            }}
          >
            {tickers[hovered.row]} &times; {tickers[hovered.col]} = {matrix[tickers[hovered.row]]?.[tickers[hovered.col]]?.toFixed(4) ?? 'N/A'}
          </div>
        )}
      </div>
      {/* Color legend */}
      <div className="flex items-center gap-2 mt-3 text-[10px] text-dim">
        <span>-1.0</span>
        <div className="flex h-2 rounded overflow-hidden">
          <div className="w-6 bg-red-700/80" />
          <div className="w-6 bg-red-600/60" />
          <div className="w-6 bg-red-500/40" />
          <div className="w-6 bg-gray-600/30" />
          <div className="w-6 bg-green-500/40" />
          <div className="w-6 bg-green-600/60" />
          <div className="w-6 bg-green-700/80" />
        </div>
        <span>+1.0</span>
      </div>
    </div>
  )
}
