import { useState, useEffect, useCallback } from 'react'
import { isAuthenticated } from '../lib/auth'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend,
} from 'recharts'

interface BenchmarkPoint {
  date: string
  ticker: number
  benchmark: number
}

interface BenchmarkMetrics {
  alpha: number
  beta: number
  trackingError: number
  correlation: number
  tickerReturn: number
  benchmarkReturn: number
  outperformance: number
}

function calcMetrics(tickerRets: number[], benchRets: number[]): BenchmarkMetrics {
  const n = Math.min(tickerRets.length, benchRets.length)
  if (n < 2) return { alpha: 0, beta: 0, trackingError: 0, correlation: 0, tickerReturn: 0, benchmarkReturn: 0, outperformance: 0 }

  const tRets = tickerRets.slice(-n)
  const bRets = benchRets.slice(-n)

  const tMean = tRets.reduce((a, b) => a + b, 0) / n
  const bMean = bRets.reduce((a, b) => a + b, 0) / n

  let cov = 0, tVar = 0, bVar = 0
  let tSum = 1, bSum = 1
  for (let i = 0; i < n; i++) {
    cov += (tRets[i] - tMean) * (bRets[i] - bMean)
    tVar += (tRets[i] - tMean) ** 2
    bVar += (bRets[i] - bMean) ** 2
    tSum *= (1 + tRets[i])
    bSum *= (1 + bRets[i])
  }

  const beta = bVar > 0 ? cov / bVar : 0
  const alpha = (tMean - bMean) * 252 * 100
  const corr = Math.sqrt(tVar * bVar) > 0 ? cov / Math.sqrt(tVar * bVar) : 0

  let diffSum = 0
  for (let i = 0; i < n; i++) diffSum += (tRets[i] - bRets[i]) ** 2
  const trackingError = Math.sqrt(diffSum / n) * Math.sqrt(252) * 100

  const tickerReturn = (tSum - 1) * 100
  const benchmarkReturn = (bSum - 1) * 100

  return {
    alpha: Math.round(alpha * 100) / 100,
    beta: Math.round(beta * 1000) / 1000,
    trackingError: Math.round(trackingError * 100) / 100,
    correlation: Math.round(corr * 1000) / 1000,
    tickerReturn: Math.round(tickerReturn * 100) / 100,
    benchmarkReturn: Math.round(benchmarkReturn * 100) / 100,
    outperformance: Math.round((tickerReturn - benchmarkReturn) * 100) / 100,
  }
}

interface BenchmarkProps {
  ticker?: string
  benchmark?: string
  period?: string
}

export default function BenchmarkComparison({ ticker = 'AAPL', benchmark = 'SPY', period = '1y' }: BenchmarkProps) {
  const [tickerInput, setTickerInput] = useState(ticker)
  const [benchInput, setBenchInput] = useState(benchmark)
  const [periodInput, setPeriodInput] = useState(period)
  const [data, setData] = useState<BenchmarkPoint[]>([])
  const [metrics, setMetrics] = useState<BenchmarkMetrics | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchData = useCallback(async (t: string, b: string, p: string) => {
    if (!isAuthenticated()) return
    setLoading(true)
    setError('')
    try {
      const [tickerRes, benchRes] = await Promise.all([
        fetch(`/api/v1/market/historical/${t}?period=${p}`).then(r => r.ok ? r.json() : null),
        fetch(`/api/v1/market/historical/${b}?period=${p}`).then(r => r.ok ? r.json() : null),
      ])

      if (!tickerRes?.prices || !benchRes?.prices) {
        setError('Could not fetch price data')
        setData([])
        setMetrics(null)
        return
      }

      const tickerPrices = tickerRes.prices
      const benchPrices = benchRes.prices

      const minLen = Math.min(tickerPrices.length, benchPrices.length)
      const tTrimmed = tickerPrices.slice(-minLen)
      const bTrimmed = benchPrices.slice(-minLen)

      const t0 = tTrimmed[0]?.close || 1
      const b0 = bTrimmed[0]?.close || 1

      const tRets: number[] = []
      const bRets: number[] = []
      const points: BenchmarkPoint[] = []

      for (let i = 0; i < minLen; i++) {
        const tPrice = tTrimmed[i]?.close
        const bPrice = bTrimmed[i]?.close
        if (tPrice == null || bPrice == null) continue

        const tCum = tPrice / t0
        const bCum = bPrice / b0

        if (i > 0) {
          tRets.push(tTrimmed[i].close / tTrimmed[i - 1].close - 1)
          bRets.push(bTrimmed[i].close / bTrimmed[i - 1].close - 1)
        }

        points.push({
          date: tTrimmed[i].date || tTrimmed[i].timestamp || String(i),
          ticker: Math.round(tCum * 10000) / 100,
          benchmark: Math.round(bCum * 10000) / 100,
        })
      }

      setData(points)
      setMetrics(calcMetrics(tRets, bRets))
    } catch {
      setError('Failed to load data')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchData(ticker, benchmark, period)
  }, [])

  const handleCompare = () => {
    fetchData(tickerInput.toUpperCase(), benchInput.toUpperCase(), periodInput)
  }

  const MetricCard = ({ label, value, fmt }: { label: string; value: number; fmt?: (v: number) => string }) => {
    const formatted = fmt ? fmt(value) : value.toFixed(2)
    const color = value >= 0 ? 'text-green' : 'text-red'
    return (
      <div className="bg-gray-900/60 border border-gray-700/50 rounded px-2 py-1.5 text-center min-w-[90px]">
        <div className="text-[10px] text-dim uppercase tracking-wider">{label}</div>
        <div className={`text-sm font-bold font-mono ${color}`}>{formatted}</div>
      </div>
    )
  }

  return (
    <div className="p-3">
      <div className="flex items-center gap-3 mb-3 flex-wrap">
        <h3 className="text-sm font-bold text-cyan">Benchmark Comparison</h3>
        <div className="flex items-center gap-1.5 ml-auto">
          <input
            className="w-20 px-1.5 py-1 text-xs bg-gray-800 border border-gray-700 rounded text-gray-200 font-mono"
            value={tickerInput}
            onChange={e => setTickerInput(e.target.value)}
            placeholder="Ticker"
          />
          <span className="text-dim text-xs">vs</span>
          <input
            className="w-20 px-1.5 py-1 text-xs bg-gray-800 border border-gray-700 rounded text-gray-200 font-mono"
            value={benchInput}
            onChange={e => setBenchInput(e.target.value)}
            placeholder="Benchmark"
          />
          <select
            className="px-1.5 py-1 text-xs bg-gray-800 border border-gray-700 rounded text-gray-200"
            value={periodInput}
            onChange={e => setPeriodInput(e.target.value)}
          >
            <option value="1mo">1M</option>
            <option value="3mo">3M</option>
            <option value="6mo">6M</option>
            <option value="1y">1Y</option>
            <option value="2y">2Y</option>
            <option value="5y">5Y</option>
          </select>
          <button
            className="px-2.5 py-1 text-xs bg-cyan/20 border border-cyan/40 rounded text-cyan hover:bg-cyan/30 transition-colors"
            onClick={handleCompare}
          >
            Compare
          </button>
        </div>
      </div>

      {loading && <div className="text-dim text-xs py-4 text-center">Loading comparison data...</div>}

      {error && <div className="text-red text-xs py-2">{error}</div>}

      {metrics && (
        <div className="flex gap-2 mb-3 flex-wrap">
          <MetricCard label="Alpha" value={metrics.alpha} fmt={v => `${v >= 0 ? '+' : ''}${v.toFixed(2)}%`} />
          <MetricCard label="Beta" value={metrics.beta} />
          <MetricCard label="Tracking Error" value={metrics.trackingError} fmt={v => `${v.toFixed(2)}%`} />
          <MetricCard label="Correlation" value={metrics.correlation} />
          <MetricCard label="Ticker Return" value={metrics.tickerReturn} fmt={v => `${v >= 0 ? '+' : ''}${v.toFixed(2)}%`} />
          <MetricCard label="Benchmark Return" value={metrics.benchmarkReturn} fmt={v => `${v >= 0 ? '+' : ''}${v.toFixed(2)}%`} />
          <MetricCard label="Outperformance" value={metrics.outperformance} fmt={v => `${v >= 0 ? '+' : ''}${v.toFixed(2)}%`} />
        </div>
      )}

      {data.length > 0 && (
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 5, right: 10, left: 10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,200,150,0.08)" />
              <XAxis
                dataKey="date"
                tick={{ fontSize: 9, fill: '#4a7a8a' }}
                tickLine={false}
                axisLine={{ stroke: 'rgba(0,200,150,0.15)' }}
                interval="preserveStartEnd"
              />
              <YAxis
                tick={{ fontSize: 9, fill: '#4a7a8a' }}
                tickLine={false}
                axisLine={{ stroke: 'rgba(0,200,150,0.15)' }}
                tickFormatter={v => `${v.toFixed(0)}%`}
                domain={['auto', 'auto']}
              />
              <Tooltip
                contentStyle={{
                  background: 'rgba(10,26,46,0.95)',
                  border: '1px solid rgba(0,200,150,0.3)',
                  borderRadius: 4,
                  fontSize: 11,
                  fontFamily: '"JetBrains Mono", monospace',
                }}
                labelStyle={{ color: '#00ff88' }}
                formatter={(value: number, name: string) => [`${value.toFixed(2)}%`, name === 'ticker' ? tickerInput.toUpperCase() : benchInput.toUpperCase()]}
              />
              <Legend
                wrapperStyle={{ fontSize: 10, fontFamily: '"JetBrains Mono", monospace' }}
                formatter={(value: string) => value === 'ticker' ? tickerInput.toUpperCase() : benchInput.toUpperCase()}
              />
              <Line type="monotone" dataKey="ticker" stroke="#00ff88" strokeWidth={2} dot={false} name="ticker" />
              <Line type="monotone" dataKey="benchmark" stroke="#00ccff" strokeWidth={2} dot={false} name="benchmark" strokeDasharray="4 2" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
