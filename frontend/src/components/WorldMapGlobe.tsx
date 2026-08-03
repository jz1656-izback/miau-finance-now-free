import { useEffect, useRef, useState, useCallback } from 'react'
import { createPortal } from 'react-dom'

interface Props {
  onClose?: () => void
  active?: boolean
}

const MARKETS = [
  { name: 'NYSE', ticker: '^NYA', lat: 40.707, lng: -74.011, region: 'North America', type: 'exchange' },
  { name: 'NASDAQ', ticker: '^IXIC', lat: 40.712, lng: -74.013, region: 'North America', type: 'exchange' },
  { name: 'LSE', ticker: '^FTSE', lat: 51.514, lng: -0.083, region: 'Europe', type: 'exchange' },
  { name: 'TSE', ticker: '^N225', lat: 35.676, lng: 139.773, region: 'Asia Pacific', type: 'exchange' },
  { name: 'SSE', ticker: '000001.SS', lat: 31.230, lng: 121.473, region: 'Asia Pacific', type: 'exchange' },
  { name: 'HKEX', ticker: '^HSI', lat: 22.284, lng: 114.158, region: 'Asia Pacific', type: 'exchange' },
  { name: 'BSE', ticker: '^BSESN', lat: 18.939, lng: 72.835, region: 'Asia Pacific', type: 'exchange' },
  { name: 'ASX', ticker: '^AXJO', lat: -33.868, lng: 151.207, region: 'Asia Pacific', type: 'exchange' },
  { name: 'SGX', ticker: '^STI', lat: 1.290, lng: 103.852, region: 'Asia Pacific', type: 'exchange' },
  { name: 'KRX', ticker: '^KS11', lat: 37.566, lng: 126.978, region: 'Asia Pacific', type: 'exchange' },
  { name: 'Euronext', ticker: '^FCHI', lat: 48.869, lng: 2.336, region: 'Europe', type: 'exchange' },
  { name: 'Xetra', ticker: '^GDAXI', lat: 50.111, lng: 8.682, region: 'Europe', type: 'exchange' },
  { name: 'SIX', ticker: '^SSMI', lat: 47.376, lng: 8.541, region: 'Europe', type: 'exchange' },
  { name: 'B3', ticker: '^BVSP', lat: -23.561, lng: -46.665, region: 'South America', type: 'exchange' },
  { name: 'JSE', ticker: '^JN0U.JO', lat: -26.204, lng: 28.041, region: 'Africa', type: 'exchange' },
  { name: 'TSX', ticker: '^GSPTSE', lat: 43.646, lng: -79.381, region: 'North America', type: 'exchange' },
]

const LAUNCH_PADS = [
  { name: 'Kennedy LC-39A', lat: 28.61, lng: -80.60 },
  { name: 'Cape Canaveral SLC-40', lat: 28.56, lng: -80.58 },
  { name: 'Vandenberg SLC-4E', lat: 34.63, lng: -120.61 },
  { name: 'Starbase', lat: 25.99, lng: -97.18 },
]

const LAUNCHES = [
  { mission: 'Starlink 6-42', rocket: 'Falcon 9', date: '2026-05-22', pad: 'SLC-40', lat: 28.56, lng: -80.58 },
  { mission: 'Starship Test', rocket: 'Starship', date: '2026-06-01', pad: 'Starbase', lat: 25.99, lng: -97.18 },
  { mission: 'Crew-10', rocket: 'Dragon', date: '2026-06-15', pad: 'LC-39A', lat: 28.61, lng: -80.60 },
]

const CAT_COMMENTS = [
  '🐱 The cat is monitoring global markets. Treat jar at 47%.',
  '🐱 ISS just passed overhead. The cat is tracking it.',
  '🐱 Catboat traffic is heavy in the Atlantic. The cat recommends patience.',
  '🐱 A smart money jet is heading to New York. Something big is happening.',
  '🐱 The cat sees SpaceX preparing for launch. Godspeed, cat.',
  '🐱 Markets are open in Asia. The cat is watching Tokyo.',
  '🐱 European markets are napping. The cat approves of this strategy.',
  '🐱 A Maine Coon just bought the dip. The cat is bullish.',
  '🐱 Catboat \"Purrseidon\" spotted off the coast of Brazil.',
  '🐱 Jet carrying tuna futures just landed in London.',
]

const COUNTRY_COORDS: Record<string, [number, number]> = {
  US: [39.8, -98.5], GB: [54.0, -2.0], JP: [36.0, 138.0], DE: [51.0, 9.0], FR: [47.0, 2.0],
  CN: [35.0, 105.0], IN: [20.0, 78.0], BR: [-10.0, -55.0], CH: [46.8, 8.2], AU: [-25.0, 133.0],
}

const COMPANIES = [
  { name: 'Apple', ticker: 'AAPL', lat: 37.336, lng: -122.007, industry: 'Tech', marketCap: 2800 },
  { name: 'Microsoft', ticker: 'MSFT', lat: 47.640, lng: -122.129, industry: 'Tech', marketCap: 2500 },
  { name: 'Google', ticker: 'GOOGL', lat: 37.422, lng: -122.084, industry: 'Tech', marketCap: 1900 },
  { name: 'Amazon', ticker: 'AMZN', lat: 47.615, lng: -122.339, industry: 'Tech', marketCap: 1700 },
  { name: 'Nvidia', ticker: 'NVDA', lat: 37.395, lng: -121.964, industry: 'Semiconductors', marketCap: 2200 },
  { name: 'Meta', ticker: 'META', lat: 37.485, lng: -122.149, industry: 'Tech', marketCap: 1100 },
  { name: 'Tesla', ticker: 'TSLA', lat: 30.223, lng: -97.620, industry: 'Automotive', marketCap: 800 },
  { name: 'Netflix', ticker: 'NFLX', lat: 37.258, lng: -121.946, industry: 'Entertainment', marketCap: 250 },
  { name: 'Berkshire Hathaway', ticker: 'BRK.A', lat: 41.256, lng: -95.934, industry: 'Conglomerate', marketCap: 750 },
  { name: 'JP Morgan', ticker: 'JPM', lat: 40.754, lng: -73.973, industry: 'Finance', marketCap: 500 },
  { name: 'Goldman Sachs', ticker: 'GS', lat: 40.714, lng: -74.010, industry: 'Finance', marketCap: 130 },
  { name: 'Samsung', ticker: '005930.KS', lat: 37.479, lng: 127.020, industry: 'Tech', marketCap: 400 },
  { name: 'Toyota', ticker: 'TM', lat: 35.052, lng: 137.155, industry: 'Automotive', marketCap: 280 },
  { name: 'Tencent', ticker: 'TCEHY', lat: 22.543, lng: 113.953, industry: 'Tech', marketCap: 450 },
  { name: 'Alibaba', ticker: 'BABA', lat: 30.274, lng: 120.155, industry: 'Tech', marketCap: 200 },
  { name: 'Nestlé', ticker: 'NSRGY', lat: 46.519, lng: 6.632, industry: 'Food', marketCap: 300 },
  { name: 'Roche', ticker: 'RHHBY', lat: 47.559, lng: 7.616, industry: 'Pharma', marketCap: 250 },
  { name: 'Shell', ticker: 'SHEL', lat: 52.077, lng: 4.310, industry: 'Energy', marketCap: 220 },
  { name: 'LVMH', ticker: 'MC.PA', lat: 48.870, lng: 2.321, industry: 'Luxury', marketCap: 420 },
  { name: 'SAP', ticker: 'SAP', lat: 49.293, lng: 8.640, industry: 'Tech', marketCap: 260 },
  { name: 'TSMC', ticker: 'TSM', lat: 22.783, lng: 120.293, industry: 'Semiconductors', marketCap: 600 },
  { name: 'Visa', ticker: 'V', lat: 37.558, lng: -122.280, industry: 'Finance', marketCap: 480 },
  { name: 'Walmart', ticker: 'WMT', lat: 36.373, lng: -94.214, industry: 'Retail', marketCap: 420 },
  { name: 'Eli Lilly', ticker: 'LLY', lat: 39.813, lng: -86.129, industry: 'Pharma', marketCap: 600 },
  { name: 'UnitedHealth', ticker: 'UNH', lat: 39.744, lng: -105.010, industry: 'Healthcare', marketCap: 450 },
  { name: 'J&J', ticker: 'JNJ', lat: 40.503, lng: -74.449, industry: 'Pharma', marketCap: 380 },
  { name: 'Mastercard', ticker: 'MA', lat: 41.136, lng: -73.759, industry: 'Finance', marketCap: 350 },
  { name: 'Procter & Gamble', ticker: 'PG', lat: 39.356, lng: -84.520, industry: 'Consumer', marketCap: 350 },
  { name: 'Baidu', ticker: 'BIDU', lat: 40.057, lng: 116.341, industry: 'Tech', marketCap: 40 },
  { name: 'Infosys', ticker: 'INFY', lat: 12.845, lng: 77.664, industry: 'Tech', marketCap: 70 },
  { name: 'Reliance', ticker: 'RELIANCE.NS', lat: 19.062, lng: 72.835, industry: 'Conglomerate', marketCap: 200 },
  { name: 'Petrobras', ticker: 'PBR', lat: -22.902, lng: -43.177, industry: 'Energy', marketCap: 110 },
  { name: 'MercadoLibre', ticker: 'MELI', lat: -34.619, lng: -58.436, industry: 'Tech', marketCap: 70 },
  { name: 'Adidas', ticker: 'ADS.DE', lat: 49.757, lng: 10.900, industry: 'Consumer', marketCap: 40 },
  { name: 'BNP Paribas', ticker: 'BNP.PA', lat: 48.876, lng: 2.333, industry: 'Finance', marketCap: 70 },
  { name: 'Siemens', ticker: 'SIE.DE', lat: 48.169, lng: 11.615, industry: 'Industrial', marketCap: 140 },
]

const COMPANY_SYMBOLS: Record<string, string> = {
  'Tech': '💻', 'Semiconductors': '🔬', 'Automotive': '🚗', 'Entertainment': '🎬',
  'Conglomerate': '🏢', 'Finance': '🏦', 'Food': '🍫', 'Pharma': '💊', 'Energy': '⛽',
  'Luxury': '👑', 'Retail': '🛒', 'Healthcare': '🏥', 'Consumer': '📦', 'Industrial': '⚙️',
}

const FALLBACK_DATA = {
  countries: [
    { iso: 'US', name: 'USA', index_change: 0.38, is_open: true, gdp: 0 },
    { iso: 'GB', name: 'UK', index_change: -0.21, is_open: true, gdp: 0 },
    { iso: 'JP', name: 'Japan', index_change: -0.45, is_open: false, gdp: 0 },
    { iso: 'DE', name: 'Germany', index_change: 0.15, is_open: true, gdp: 0 },
    { iso: 'FR', name: 'France', index_change: -0.12, is_open: true, gdp: 0 },
    { iso: 'CN', name: 'China', index_change: 0.52, is_open: false, gdp: 0 },
    { iso: 'IN', name: 'India', index_change: 0.73, is_open: true, gdp: 0 },
    { iso: 'BR', name: 'Brazil', index_change: -0.88, is_open: true, gdp: 0 },
    { iso: 'CH', name: 'Switzerland', index_change: 0.22, is_open: true, gdp: 0 },
    { iso: 'AU', name: 'Australia', index_change: -0.05, is_open: false, gdp: 0 },
  ],
  trade_routes: [
    { from: 'US', to: 'GB', volume: 1500, velocity: 0.4, catboat: '🐱🚢', value: '1.2B' },
    { from: 'GB', to: 'DE', volume: 800, velocity: 0.6, catboat: '😼⛴️', value: '0.8B' },
    { from: 'US', to: 'JP', volume: 2000, velocity: 0.3, catboat: '🐱🚤', value: '2.1B' },
    { from: 'CN', to: 'US', volume: 3500, velocity: 0.5, catboat: '🐱🛳️', value: '4.5B' },
    { from: 'JP', to: 'CN', volume: 1200, velocity: 0.7, catboat: '😸🛥️', value: '1.0B' },
    { from: 'IN', to: 'GB', volume: 600, velocity: 0.55, catboat: '🐱⛵', value: '0.5B' },
    { from: 'BR', to: 'US', volume: 900, velocity: 0.45, catboat: '🐱🚣', value: '0.7B' },
    { from: 'AU', to: 'CN', volume: 1100, velocity: 0.35, catboat: '🐱🛶', value: '1.3B' },
    { from: 'FR', to: 'DE', volume: 700, velocity: 0.65, catboat: '🐱⚓', value: '0.6B' },
    { from: 'CH', to: 'GB', volume: 400, velocity: 0.5, catboat: '😺⛴️', value: '0.4B' },
  ],
  capital_flows: [
    { from: 'US', to: 'JP', amount: 500, jet: '✈️' },
    { from: 'GB', to: 'US', amount: 300, jet: '🛩️' },
    { from: 'DE', to: 'CN', amount: 200, jet: '🛫' },
    { from: 'JP', to: 'US', amount: 400, jet: '🛬' },
    { from: 'FR', to: 'DE', amount: 150, jet: '🚁' },
  ],
  cats: [
    { name: 'Whiskers', breed: 'Maine Coon', net_worth: 2500000, lat: 40.712, lng: -74.006, city: 'New York', is_captain: true },
    { name: 'Mittens', breed: 'Persian', net_worth: 1800000, lat: 51.507, lng: -0.127, city: 'London', is_captain: true },
    { name: 'Felix', breed: 'Sphynx', net_worth: 3200000, lat: 48.856, lng: 2.352, city: 'Paris', is_captain: false },
    { name: 'Luna', breed: 'Bengal', net_worth: 4100000, lat: 35.676, lng: 139.65, city: 'Tokyo', is_captain: true },
    { name: 'Simba', breed: 'Siamese', net_worth: 1500000, lat: 31.230, lng: 121.473, city: 'Shanghai', is_captain: false },
    { name: 'Oreo', breed: 'American Shorthair', net_worth: 2800000, lat: 40.707, lng: -74.011, city: 'New York', is_captain: false },
    { name: 'Cleo', breed: 'Abyssinian', net_worth: 950000, lat: 51.514, lng: -0.083, city: 'London', is_captain: false },
    { name: 'Garfield', breed: 'Orange Tabby', net_worth: 5000000, lat: 52.520, lng: 13.405, city: 'Berlin', is_captain: true },
    { name: 'Salem', breed: 'Black Shorthair', net_worth: 1200000, lat: 22.543, lng: 114.057, city: 'Hong Kong', is_captain: false },
    { name: 'Nala', breed: 'Ragdoll', net_worth: 2100000, lat: -33.868, lng: 151.209, city: 'Sydney', is_captain: false },
    { name: 'Tom', breed: 'British Shorthair', net_worth: 1750000, lat: 41.902, lng: 12.453, city: 'Rome', is_captain: true },
    { name: 'Jerry', breed: 'Scottish Fold', net_worth: 800000, lat: 37.774, lng: -122.419, city: 'San Francisco', is_captain: false },
    { name: 'Sylvester', breed: 'Snowshoe', net_worth: 1400000, lat: 19.076, lng: 72.877, city: 'Mumbai', is_captain: true },
    { name: 'Tigger', breed: 'Toyger', net_worth: 3600000, lat: 1.352, lng: 103.819, city: 'Singapore', is_captain: false },
    { name: 'Cheshire', breed: 'British Shorthair', net_worth: 2200000, lat: -23.550, lng: -46.633, city: 'São Paulo', is_captain: true },
  ],
  space: {
    iss: { lat: 51.5, lng: -60.5 },
  },
}

function colorForChange(change: number): string {
  if (change >= 2) return '#00ff88'
  if (change >= 0) return '#44cc66'
  if (change >= -1) return '#ffaa00'
  return '#ff4444'
}

export default function WorldMapGlobe({ onClose, active }: Props) {
  const containerRef = useRef<HTMLDivElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [data, setData] = useState<any>(FALLBACK_DATA)
  const [time, setTime] = useState('')
  const [catComment, setCatComment] = useState(CAT_COMMENTS[0])
  const [selected, setSelected] = useState<any>(null)
  const [rightPanel, setRightPanel] = useState<string>('cats')
  const [showCatboats, setShowCatboats] = useState(true)
  const [showJets, setShowJets] = useState(true)
  const [showCats, setShowCats] = useState(true)
  const [showISS, setShowISS] = useState(true)
  const [showCompanies, setShowCompanies] = useState(true)
  const [showHairballs, setShowHairballs] = useState(true)
  const [search, setSearch] = useState('')
  const animationRef = useRef<number>(0)

  const fetchData = useCallback(async () => {
    try {
      const token = localStorage.getItem('miau_token')
      const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}
      const res = await fetch('/api/v1/worldmap/live', { headers })
      if (res.ok) {
        const apiData = await res.json()
        setData({
          countries: apiData.countries && apiData.countries.length > 0 ? apiData.countries : FALLBACK_DATA.countries,
          trade_routes: apiData.trade_routes && apiData.trade_routes.length > 0 ? apiData.trade_routes : FALLBACK_DATA.trade_routes,
          capital_flows: apiData.capital_flows && apiData.capital_flows.length > 0 ? apiData.capital_flows : FALLBACK_DATA.capital_flows,
          cats: apiData.cats && apiData.cats.length > 0 ? apiData.cats : FALLBACK_DATA.cats,
          space: { ...FALLBACK_DATA.space, ...(apiData.space || {}) },
        })
      }
    } catch {}
  }, [])

  useEffect(() => {
    fetchData()
    const t = setInterval(fetchData, 30000)
    return () => clearInterval(t)
  }, [fetchData])

  useEffect(() => {
    setTime(new Date().toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' }))
    const t = setInterval(() => setTime(new Date().toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })), 1000)
    return () => clearInterval(t)
  }, [])

  useEffect(() => {
    const t = setInterval(() => setCatComment(CAT_COMMENTS[Math.floor(Math.random() * CAT_COMMENTS.length)]), 20000)
    return () => clearInterval(t)
  }, [])

  const drawGlobe = useCallback(() => {
    const canvas = canvasRef.current
    const container = containerRef.current
    if (!canvas || !container || !data) return
    const w = container.clientWidth
    const h = container.clientHeight
    canvas.width = w
    canvas.height = h
    const ctx = canvas.getContext('2d')!
    const cx = w / 2
    const cy = h / 2
    const r = Math.min(w, h) * 0.38

    ctx.fillStyle = '#050510'
    ctx.fillRect(0, 0, w, h)

    if (!(canvas as any)._stars) {
      const stars = []
      for (let i = 0; i < 200; i++) stars.push({ x: Math.random() * w, y: Math.random() * h * 0.7, s: Math.random() * 1.5 + 0.5 })
      ;(canvas as any)._stars = stars
    }
    const stars = (canvas as any)._stars
    const starTime = Date.now() * 0.0001
    for (const s of stars) {
      ctx.fillStyle = `rgba(255,255,255,${0.3 + Math.sin(starTime + s.x) * 0.2})`
      ctx.fillRect(s.x, s.y, s.s, s.s)
    }

    ctx.beginPath()
    ctx.arc(cx, cy, r, 0, Math.PI * 2)
    const grad = ctx.createRadialGradient(cx - r * 0.3, cy - r * 0.3, r * 0.1, cx, cy, r)
    grad.addColorStop(0, '#1a4a2a')
    grad.addColorStop(0.5, '#0d3319')
    grad.addColorStop(1, '#061208')
    ctx.fillStyle = grad
    ctx.fill()

    ctx.beginPath()
    ctx.arc(cx, cy, r + 3, 0, Math.PI * 2)
    ctx.strokeStyle = 'rgba(0, 255, 136, 0.15)'
    ctx.lineWidth = 6
    ctx.stroke()

    ctx.strokeStyle = 'rgba(0, 255, 136, 0.05)'
    ctx.lineWidth = 0.5
    for (let lat = -75; lat <= 75; lat += 15) {
      const y = cy + (lat / 90) * r * 0.9
      ctx.beginPath()
      ctx.moveTo(0, y)
      ctx.lineTo(w, y)
      ctx.stroke()
    }
    for (let lng = -165; lng <= 165; lng += 15) {
      const x = cx + (lng / 180) * r * 0.8
      ctx.beginPath()
      ctx.moveTo(x, 0)
      ctx.lineTo(x, h)
      ctx.stroke()
    }

    ctx.strokeStyle = 'rgba(0, 255, 136, 0.2)'
    ctx.lineWidth = 1
    ctx.beginPath()
    const outlines = [
      [40, -74, 42, -80, 45, -85, 48, -95, 50, -100, 52, -105, 55, -110, 58, -108, 60, -100, 55, -90, 50, -80, 45, -75, 40, -74],
      [35, 139, 40, 140, 43, 142, 42, 145, 37, 140, 35, 139],
      [51, -0, 53, 1, 50, 10, 47, 12, 45, 8, 47, 2, 49, -1, 51, -0],
      [-23, -46, -20, -40, -10, -37, 5, -35, 12, -70, 10, -75, 5, -77, -5, -72, -15, -55, -23, -46],
    ]
    for (const o of outlines) {
      for (let i = 0; i < o.length; i += 2) {
        const lng = o[i + 1], lat = o[i]
        const px = cx + (lng / 180) * r * 0.85
        const py = cy - (lat / 90) * r * 0.82
        if (i === 0) ctx.moveTo(px, py)
        else ctx.lineTo(px, py)
      }
      ctx.stroke()
    }

    if (data?.countries) {
      for (const c of data.countries) {
        const coords = COUNTRY_COORDS[c.iso]
        if (!coords) continue
        const px = cx + (coords[1] / 180) * r * 0.82
        const py = cy - (coords[0] / 90) * r * 0.80
        const change = c.index_change || 0
        const color = colorForChange(change)
        const alpha = c.is_open ? 0.6 : 0.25
        ctx.fillStyle = `rgba(${color === '#00ff88' ? '0,255,136' : color === '#44cc66' ? '68,204,102' : color === '#ffaa00' ? '255,170,0' : '255,68,68'}, ${alpha})`
        ctx.beginPath()
        const size = Math.max(3, Math.min(8, Math.abs(change) * 4))
        ctx.arc(px, py, size, 0, Math.PI * 2)
        ctx.fill()
        if (c.is_open) {
          ctx.strokeStyle = `rgba(${color === '#00ff88' ? '0,255,136' : '255,170,0'}, 0.5)`
          ctx.lineWidth = 0.5
          ctx.stroke()
        }
      }
    }

    for (const m of MARKETS) {
      const px = cx + (m.lng / 180) * r * 0.85
      const py = cy - (m.lat / 90) * r * 0.82
      ctx.fillStyle = m.type === 'exchange' ? '#00ff88' : '#00ccff'
      ctx.beginPath()
      ctx.arc(px, py, 2.5, 0, Math.PI * 2)
      ctx.fill()
      const pulse = Math.sin(Date.now() * 0.005 + m.lng) * 0.5 + 0.5
      ctx.strokeStyle = `rgba(0, 255, 136, ${0.3 + pulse * 0.2})`
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.arc(px, py, 4 + pulse * 2, 0, Math.PI * 2)
      ctx.stroke()
    }

    // Companies
    if (showCompanies) {
      const searchLow = search.toLowerCase()
      for (const co of COMPANIES) {
        const px = cx + (co.lng / 180) * r * 0.85
        const py = cy - (co.lat / 90) * r * 0.82
        const match = searchLow && (co.name.toLowerCase().includes(searchLow) || co.ticker.toLowerCase().includes(searchLow))
        const alpha = match ? 1 : searchLow ? 0.2 : 0.5
        const size = match ? 5 : 3
        ctx.fillStyle = match ? '#00ff88' : `rgba(0, 200, 255, ${alpha * 0.6})`
        ctx.beginPath()
        ctx.arc(px, py, size, 0, Math.PI * 2)
        ctx.fill()
        if (match) {
          ctx.strokeStyle = 'rgba(0, 255, 136, 0.6)'
          ctx.lineWidth = 1.5
          ctx.beginPath()
          ctx.arc(px, py, 8, 0, Math.PI * 2)
          ctx.stroke()
          ctx.font = 'bold 11px monospace'
          ctx.fillStyle = '#00ff88'
          ctx.fillText(`${co.ticker} — ${co.name}`, px + 10, py + 3)
          ctx.font = '8px monospace'
          ctx.fillStyle = 'rgba(0,255,136,0.5)'
          ctx.fillText(`${COMPANY_SYMBOLS[co.industry] || '🏢'} ${co.industry} · $${co.marketCap}B`, px + 10, py + 14)
        } else if (!searchLow) {
          ctx.font = '7px monospace'
          ctx.fillStyle = `rgba(0,200,255,${alpha * 0.7})`
          ctx.fillText(co.ticker, px + 4, py + 2)
        }
      }
    }

    if (showCatboats && data?.trade_routes) {
      const boatPhase = Date.now() * 0.0005
      for (const tr of data.trade_routes) {
        const fcoords = COUNTRY_COORDS[tr.from]
        const tcoords = COUNTRY_COORDS[tr.to]
        if (!fcoords || !tcoords) continue
        const fx = cx + (fcoords[1] / 180) * r * 0.80
        const fy = cy - (fcoords[0] / 90) * r * 0.78
        const tx = cx + (tcoords[1] / 180) * r * 0.80
        const ty = cy - (tcoords[0] / 90) * r * 0.78
        ctx.strokeStyle = 'rgba(0, 255, 136, 0.1)'
        ctx.lineWidth = 0.5
        ctx.beginPath()
        ctx.moveTo(fx, fy)
        ctx.lineTo(tx, ty)
        ctx.stroke()
        const pos = (boatPhase * tr.velocity + Math.sin(tr.volume * 0.001)) % 1
        const bx = fx + (tx - fx) * pos
        const by = fy + (ty - fy) * pos
        ctx.font = `${10 + tr.volume * 0.002}px sans-serif`
        ctx.fillText(tr.catboat || '🐱🚢', bx - 7, by + 4)
        ctx.font = '7px monospace'
        ctx.fillStyle = 'rgba(0,255,136,0.4)'
        ctx.fillText(tr.value || '', bx + 8, by + 2)
      }
    }

    if (showJets && data?.capital_flows) {
      const jetPhase = Date.now() * 0.001
      for (const flow of data.capital_flows) {
        const fcoords = COUNTRY_COORDS[flow.from]
        const tcoords = COUNTRY_COORDS[flow.to]
        if (!fcoords || !tcoords) continue
        const fx = cx + (fcoords[1] / 180) * r * 0.82
        const fy = cy - (fcoords[0] / 90) * r * 0.80
        const tx = cx + (tcoords[1] / 180) * r * 0.82
        const ty = cy - (tcoords[0] / 90) * r * 0.80
        ctx.strokeStyle = 'rgba(0, 200, 255, 0.08)'
        ctx.lineWidth = 0.3
        ctx.beginPath()
        ctx.moveTo(fx, fy)
        ctx.lineTo(tx, ty)
        ctx.stroke()
        const pos = (jetPhase * 0.3 + flow.amount * 0.001) % 1
        const jx = fx + (tx - fx) * pos
        const jy = fy + (ty - fy) * pos
        ctx.font = '12px sans-serif'
        ctx.fillText(flow.jet || '✈️', jx - 6, jy - 4)
        ctx.font = '6px monospace'
        ctx.fillStyle = 'rgba(0,200,255,0.3)'
        ctx.fillText(`$${(flow.amount * 1e6).toLocaleString()}`, jx + 8, jy - 2)
      }
    }

    for (const pad of LAUNCH_PADS) {
      const px = cx + (pad.lng / 180) * r * 0.85
      const py = cy - (pad.lat / 90) * r * 0.82
      ctx.fillStyle = '#ff6600'
      ctx.beginPath()
      ctx.arc(px, py, 3, 0, Math.PI * 2)
      ctx.fill()
      ctx.strokeStyle = 'rgba(255, 102, 0, 0.3)'
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.arc(px, py, 6, 0, Math.PI * 2)
      ctx.stroke()
      ctx.fillStyle = '#ff8844'
      ctx.font = '9px sans-serif'
      ctx.fillText('🚀', px - 5, py - 5)
      ctx.fillStyle = 'rgba(255, 136, 68, 0.6)'
      ctx.font = '7px monospace'
      ctx.fillText(pad.name.slice(0, 10), px + 4, py + 3)
    }

    if (showISS && data?.space?.iss) {
      const iss = data.space.iss
      const ix = cx + (iss.lng / 180) * r * 0.88
      const iy = cy - (iss.lat / 90) * r * 0.85
      ctx.fillStyle = '#ffff00'
      ctx.beginPath()
      ctx.arc(ix, iy, 2.5, 0, Math.PI * 2)
      ctx.fill()
      ctx.strokeStyle = 'rgba(255, 255, 0, 0.3)'
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.arc(ix, iy, 5, 0, Math.PI * 2)
      ctx.stroke()
      ctx.font = '7px monospace'
      ctx.fillStyle = '#ffff00'
      ctx.fillText('🛰️ ISS', ix + 4, iy - 2)
    }

    if (showCats && data?.cats) {
      for (const cat of data.cats) {
        const px = cx + (cat.lng / 180) * r * 0.85
        const py = cy - (cat.lat / 90) * r * 0.82
        const pulse = Math.sin(Date.now() * 0.003 + cat.lat) * 0.5 + 0.5
        ctx.fillStyle = `rgba(0, 255, 136, ${0.1 + pulse * 0.15})`
        ctx.beginPath()
        ctx.arc(px, py, 4 + pulse * 1, 0, Math.PI * 2)
        ctx.fill()
        ctx.font = `${cat.is_captain ? '12' : '9'}px sans-serif`
        const emoji = cat.is_captain ? '🐱⚓' : '🐱'
        ctx.fillText(emoji, px - 4, py - 4)
        ctx.font = '6px monospace'
        ctx.fillStyle = 'rgba(0,255,136,0.3)'
        ctx.fillText(cat.name, px + 6, py + 2)
      }
    }

    // Hairballs
    if (showHairballs && data?.cats) {
      const hairballPhase = Date.now() * 0.002
      for (let i = 0; i < data.cats.length; i++) {
        const cat = data.cats[i]
        const offset = Math.sin(hairballPhase + i * 1.7) * 8
        const px = cx + (cat.lng / 180) * r * 0.85 + offset
        const py = cy - (cat.lat / 90) * r * 0.82 + Math.cos(hairballPhase * 0.7 + i * 1.3) * 4
        const bounce = Math.sin(Date.now() * 0.004 + i * 2.1) * 0.3 + 0.7
        ctx.font = `${6 + bounce * 2}px sans-serif`
        const alpha = 0.3 + Math.sin(Date.now() * 0.002 + i) * 0.1
        ctx.fillStyle = `rgba(180, 130, 200, ${alpha})`
        ctx.fillText('🧶', px - 3, py + 2)
      }
    }

    animationRef.current = requestAnimationFrame(drawGlobe)
  }, [data, showCatboats, showJets, showCats, showISS, showHairballs, showCompanies])

  useEffect(() => {
    if (data) {
      animationRef.current = requestAnimationFrame(drawGlobe)
      return () => cancelAnimationFrame(animationRef.current)
    }
    return undefined
  }, [data, drawGlobe])

  const handleClick = (e: React.MouseEvent) => {
    if (!containerRef.current || !data) return
    const rect = containerRef.current.getBoundingClientRect()
    const mx = e.clientX - rect.left
    const my = e.clientY - rect.top
    const w = rect.width
    const h = rect.height
    const r = Math.min(w, h) * 0.38
    const cx = w / 2
    const cy = h / 2
    const lng = ((mx - cx) / (r * 0.85)) * 180
    const lat = -((my - cy) / (r * 0.82)) * 90
    let found: any = null

    for (const m of MARKETS) {
      if (Math.abs(m.lat - lat) < 3 && Math.abs(m.lng - lng) < 3) { found = { ...m, clickType: 'market' }; break }
    }
    if (!found && data.cats) {
      for (const cat of data.cats) {
        if (Math.abs(cat.lat - lat) < 5 && Math.abs(cat.lng - lng) < 5) { found = { ...cat, clickType: 'cat' }; break }
      }
    }
    if (!found) {
      for (const pad of LAUNCH_PADS) {
        if (Math.abs(pad.lat - lat) < 3 && Math.abs(pad.lng - lng) < 3) { found = { ...pad, clickType: 'launchpad' }; break }
      }
    }
    // Check companies
    if (!found) {
      for (const co of COMPANIES) {
        if (Math.abs(co.lat - lat) < 2 && Math.abs(co.lng - lng) < 2) { found = { ...co, clickType: 'company' }; break }
      }
    }
    setSelected(found)
  }



  return (
    <div ref={containerRef} className="relative w-full h-full bg-[#050510] overflow-hidden" onClick={handleClick}>
      <canvas ref={canvasRef} className="absolute inset-0" />

      {/* Toolbar — rendered via portal to body (escapes all stacking contexts) */}
      {active && createPortal(
        <div className="fixed top-0 left-0 right-0 z-[9999] bg-black/90 border-b border-green-500/30">
          <div className="flex items-center justify-between px-2 py-1">
            <div className="flex items-center gap-2">
              <button
                onClick={(e) => { e.stopPropagation(); onClose?.() }}
                className="px-2 py-0.5 text-xs text-white bg-gray-800 border border-gray-600 rounded font-mono hover:bg-gray-700"
              >
                ← Back
              </button>
              <input
                type="text"
                value={search}
                onChange={(e) => { e.stopPropagation(); setSearch(e.target.value) }}
                onClick={(e) => e.stopPropagation()}
                placeholder="🔍 Search..."
                className="w-32 md:w-44 px-2 py-0.5 bg-gray-900 border border-gray-700 rounded text-xs text-white font-mono placeholder:text-gray-600 outline-none"
              />
            </div>
            <div className="hidden sm:flex items-center gap-1 flex-wrap">
              <button onClick={(e) => { e.stopPropagation(); setShowCatboats(!showCatboats) }}
                className={`px-1.5 py-0.5 text-[10px] font-mono rounded ${showCatboats ? 'bg-green-900 text-green-300 border border-green-600' : 'text-gray-500 border border-transparent'}`}>
                🚢 Boats
              </button>
              <button onClick={(e) => { e.stopPropagation(); setShowJets(!showJets) }}
                className={`px-1.5 py-0.5 text-[10px] font-mono rounded ${showJets ? 'bg-cyan-900 text-cyan-300 border border-cyan-600' : 'text-gray-500 border border-transparent'}`}>
                ✈️ Jets
              </button>
              <button onClick={(e) => { e.stopPropagation(); setShowCats(!showCats) }}
                className={`px-1.5 py-0.5 text-[10px] font-mono rounded ${showCats ? 'bg-yellow-900 text-yellow-300 border border-yellow-600' : 'text-gray-500 border border-transparent'}`}>
                🐱 Cats
              </button>
              <button onClick={(e) => { e.stopPropagation(); setShowHairballs(!showHairballs) }}
                className={`px-1.5 py-0.5 text-[10px] font-mono rounded ${showHairballs ? 'bg-purple-900 text-purple-300 border border-purple-600' : 'text-gray-500 border border-transparent'}`}>
                🧶 Hairballs
              </button>
              <button onClick={(e) => { e.stopPropagation(); setShowISS(!showISS) }}
                className={`px-1.5 py-0.5 text-[10px] font-mono rounded ${showISS ? 'bg-yellow-900 text-yellow-300 border border-yellow-600' : 'text-gray-500 border border-transparent'}`}>
                🛰️ ISS
              </button>
              <button onClick={(e) => { e.stopPropagation(); setShowCompanies(!showCompanies) }}
                className={`px-1.5 py-0.5 text-[10px] font-mono rounded ${showCompanies ? 'bg-blue-900 text-blue-300 border border-blue-600' : 'text-gray-500 border border-transparent'}`}>
                🏢 Companies
              </button>
            </div>
            <span className="text-[9px] text-gray-500 font-mono">{time}</span>
          </div>
          {search && (
            <div className="max-h-48 overflow-y-auto bg-gray-900 border border-gray-700 rounded p-1.5 text-[10px] font-mono" onClick={(e) => e.stopPropagation()}>
              <div className="text-gray-500 text-[8px] mb-1">Search: "{search}"</div>
              {COMPANIES.filter(co => co.name.toLowerCase().includes(search.toLowerCase()) || co.ticker.toLowerCase().includes(search.toLowerCase())).map(co => (
                <div key={co.ticker}
                  className="flex items-center justify-between px-2 py-1 hover:bg-gray-800 rounded cursor-pointer text-white"
                  onClick={(e) => { e.stopPropagation(); setSearch(co.ticker) }}
                >
                  <span>{COMPANY_SYMBOLS[co.industry] || '🏢'} <span className="text-green-400">{co.ticker}</span> — {co.name}</span>
                  <span className="text-gray-500">${co.marketCap}B · {co.industry}</span>
                </div>
              ))}
              {COMPANIES.filter(co => co.name.toLowerCase().includes(search.toLowerCase()) || co.ticker.toLowerCase().includes(search.toLowerCase())).length === 0 && (
                <div className="text-gray-600 text-center py-2">No companies for "{search}"</div>
              )}
            </div>
          )}
        </div>,
        document.body
      )}

      {/* Legend */}
      <div className="absolute top-2 right-4 z-20 flex flex-col gap-0.5" style={{ marginTop: 60 }}>
        <div className="text-[8px] text-gray-600 font-mono flex items-center gap-1"><span className="text-green-400">▲</span> up</div>
        <div className="text-[8px] text-gray-600 font-mono flex items-center gap-1"><span className="text-red-400">▼</span> down</div>
        <div className="text-[8px] text-gray-600 font-mono flex items-center gap-1"><span className="text-yellow-400">◉</span> closed</div>
      </div>
      {/* Bottom ticker bar */}
      <div className="absolute bottom-8 left-2 right-2 z-20 flex items-center h-4 gap-4 overflow-hidden select-none pointer-events-none">
        <span className="text-yellow-400 text-[9px] font-mono shrink-0">🐟</span>
        {data?.countries?.slice(0, 8).map((c: any, i: number) => (
          <span key={i} className="flex gap-1 text-[9px] font-mono shrink-0">
            <span className="text-gray-600">{c.iso}</span>
            <span className={c.index_change >= 0 ? 'text-green-400' : 'text-red-400'}>
              {c.index_change >= 0 ? '▲' : '▼'}{Math.abs(c.index_change || 0).toFixed(1)}%
            </span>
          </span>
        ))}
      </div>

      <div className="absolute bottom-4 left-2 right-2 z-20 text-center text-[9px] text-gray-600 font-mono select-none pointer-events-none">
        {catComment}
      </div>

      {/* Bottom panel tabs */}
      <div className="absolute bottom-10 right-2 z-20 flex gap-2 text-[9px] font-mono">
        {['cats', 'markets', 'space'].map(tab => (
          <button key={tab} className={`px-2 py-0.5 rounded ${rightPanel === tab ? 'bg-green-500/20 text-green-400' : 'text-gray-500 hover:text-green-400'}`} onClick={(e) => { e.stopPropagation(); setRightPanel(tab) }}>
            {tab === 'cats' ? '🐱 Cats' : tab === 'markets' ? '📊 Markets' : '🚀 Space'}
          </button>
        ))}
      </div>

      {/* Right panel */}
      <div className="absolute top-2 right-2 w-56 bg-black/70 border border-green-500/10 rounded p-2 text-[10px] font-mono max-h-64 overflow-y-auto z-10" style={{ top: 30, display: rightPanel ? undefined : 'none' }}>
        {rightPanel === 'cats' && data?.cats && (
          <div className="space-y-1">
            <div className="text-green-400 mb-1">🐱 Global Cat Network ({data.cats.length})</div>
            <div className="text-gray-500 text-[8px]">Richest cats:</div>
            {[...data.cats].sort((a: any, b: any) => b.net_worth - a.net_worth).slice(0, 8).map((c: any, i: number) => (
              <div key={i} className="flex justify-between text-[8px]">
                <span className="text-green-400">{c.is_captain ? '⚓' : '🐱'} {c.name}</span>
                <span className="text-gray-500">{c.breed}</span>
                <span className="text-yellow-400">${(c.net_worth / 1e6).toFixed(1)}M</span>
              </div>
            ))}
            <div className="text-gray-600 text-[8px] mt-1">Click a cat on the globe for details</div>
          </div>
        )}
        {rightPanel === 'markets' && (
          <div className="space-y-1">
            <div className="text-green-400 mb-1">📊 Markets</div>
            {MARKETS.slice(0, 10).map((m, i) => (
              <div key={i} className="flex justify-between text-[8px]">
                <span className="text-gray-500">{m.name}</span>
                <span className="text-green-400">● {m.region}</span>
              </div>
            ))}
            <div className="text-gray-600 text-[8px] mt-1">{data?.trade_routes?.length || 0} trade routes active</div>
            <div className="text-gray-600 text-[8px]">{data?.capital_flows?.length || 0} capital flow jets</div>
          </div>
        )}
        {rightPanel === 'space' && (
          <div className="space-y-1">
            <div className="text-green-400 mb-1">🚀 Space Operations</div>
            {data?.space?.iss && <div className="text-gray-500 text-[8px]">🛰️ ISS: {data.space.iss.lat.toFixed(1)}°, {data.space.iss.lng.toFixed(1)}°</div>}
            <div className="text-yellow-400 text-[8px] mt-1">Upcoming:</div>
            {LAUNCHES.map((l, i) => (
              <div key={i} className="text-[8px] border-b border-green/5 pb-0.5">
                <div className="text-green-400">{l.mission}</div>
                <div className="text-gray-500">{l.rocket} · {l.date}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Selected item detail */}
      {selected && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-black/90 border border-green-500/30 rounded-lg p-3 text-[10px] font-mono z-30 min-w-[200px]">
          <button className="absolute top-1 right-2 text-gray-500 hover:text-green-400" onClick={(e) => { e.stopPropagation(); setSelected(null) }}>✕</button>
          {selected.clickType === 'market' && (
            <div>
              <div className="text-cyan-400 text-xs mb-1">{selected.name}</div>
              <div className="text-gray-500">Ticker: {selected.ticker}</div>
              <div className="text-gray-500">Region: {selected.region}</div>
            </div>
          )}
          {selected.clickType === 'cat' && (
            <div>
              <div className="text-cyan-400 text-xs mb-1">🐱 {selected.name}</div>
              <div className="text-gray-500">Breed: {selected.breed}</div>
              <div className="text-gray-500">Net Worth: ${(selected.net_worth / 1e6).toFixed(1)}M</div>
              <div className="text-gray-500">City: {selected.city}</div>
              <div className="text-yellow-400 text-[8px] mt-1">{selected.is_captain ? '⚓ Catboat Captain' : 'Investor Cat'}</div>
            </div>
          )}
          {selected.clickType === 'launchpad' && (
            <div>
              <div className="text-cyan-400 text-xs mb-1">🚀 {selected.name}</div>
              <div className="text-gray-500">Coordinates: {selected.lat}, {selected.lng}</div>
              <div className="text-yellow-400 text-[8px] mt-1">Active launch site</div>
            </div>
          )}
          {selected.type === 'company' && (
            <div>
              <div className="text-cyan-400 text-xs mb-1">{COMPANY_SYMBOLS[selected.industry] || '🏢'} {selected.name}</div>
              <div className="text-gray-500">Ticker: <span className="text-green-400">{selected.ticker}</span></div>
              <div className="text-gray-500">Industry: {selected.industry}</div>
              <div className="text-gray-500">Market Cap: <span className="text-yellow-400">${selected.marketCap}B</span></div>
              <div className="text-yellow text-[8px] mt-1">HQ: {selected.lat.toFixed(2)}°, {selected.lng.toFixed(2)}°</div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
