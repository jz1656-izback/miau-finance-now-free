import { useEffect, useRef, useState, useCallback } from 'react'

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
  '🐱 Catboat "Purrseidon" spotted off the coast of Brazil.',
  '🐱 Jet carrying tuna futures just landed in London.',
]

const COUNTRY_COORDS: Record<string, [number, number]> = {
  US: [39.8, -98.5], GB: [54.0, -2.0], JP: [36.0, 138.0], DE: [51.0, 9.0], FR: [47.0, 2.0],
  CN: [35.0, 105.0], IN: [20.0, 78.0], BR: [-10.0, -55.0], CH: [46.8, 8.2], AU: [-25.0, 133.0],
  SG: [1.3, 103.8], KR: [37.5, 127.0], ZA: [-30.5, 22.9], CA: [56.0, -96.0],
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
  { name: 'JP Morgan', ticker: 'JPM', lat: 40.754, lng: -73.973, industry: 'Finance', marketCap: 500 },
  { name: 'Samsung', ticker: '005930.KS', lat: 37.479, lng: 127.020, industry: 'Tech', marketCap: 400 },
  { name: 'Toyota', ticker: 'TM', lat: 35.052, lng: 137.155, industry: 'Automotive', marketCap: 280 },
  { name: 'Tencent', ticker: 'TCEHY', lat: 22.543, lng: 113.953, industry: 'Tech', marketCap: 450 },
  { name: 'Nestlé', ticker: 'NSRGY', lat: 46.519, lng: 6.632, industry: 'Food', marketCap: 300 },
  { name: 'LVMH', ticker: 'MC.PA', lat: 48.870, lng: 2.321, industry: 'Luxury', marketCap: 420 },
  { name: 'TSMC', ticker: 'TSM', lat: 22.783, lng: 120.293, industry: 'Semiconductors', marketCap: 600 },
  { name: 'Visa', ticker: 'V', lat: 37.558, lng: -122.280, industry: 'Finance', marketCap: 480 },
  { name: 'Walmart', ticker: 'WMT', lat: 36.373, lng: -94.214, industry: 'Retail', marketCap: 420 },
  { name: 'Eli Lilly', ticker: 'LLY', lat: 39.813, lng: -86.129, industry: 'Pharma', marketCap: 600 },
  { name: 'Mastercard', ticker: 'MA', lat: 41.136, lng: -73.759, industry: 'Finance', marketCap: 350 },
  { name: 'Reliance', ticker: 'RELIANCE.NS', lat: 19.062, lng: 72.835, industry: 'Conglomerate', marketCap: 200 },
  { name: 'Petrobras', ticker: 'PBR', lat: -22.902, lng: -43.177, industry: 'Energy', marketCap: 110 },
  { name: 'Siemens', ticker: 'SIE.DE', lat: 48.169, lng: 11.615, industry: 'Industrial', marketCap: 140 },
]

const COMPANY_SYMBOLS: Record<string, string> = {
  'Tech': '💻', 'Semiconductors': '🔬', 'Automotive': '🚗', 'Entertainment': '🎬',
  'Conglomerate': '🏢', 'Finance': '🏦', 'Food': '🍫', 'Pharma': '💊', 'Energy': '⛽',
  'Luxury': '👑', 'Retail': '🛒', 'Healthcare': '🏥', 'Consumer': '📦', 'Industrial': '⚙️',
}

const FALLBACK_DATA = {
  countries: [
    { iso: 'US', name: 'USA', index_change: 0.38, is_open: true },
    { iso: 'GB', name: 'UK', index_change: -0.21, is_open: true },
    { iso: 'JP', name: 'Japan', index_change: -0.45, is_open: false },
    { iso: 'DE', name: 'Germany', index_change: 0.15, is_open: true },
    { iso: 'FR', name: 'France', index_change: -0.12, is_open: true },
    { iso: 'CN', name: 'China', index_change: 0.52, is_open: false },
    { iso: 'IN', name: 'India', index_change: 0.73, is_open: true },
    { iso: 'BR', name: 'Brazil', index_change: -0.88, is_open: true },
    { iso: 'CH', name: 'Switzerland', index_change: 0.22, is_open: true },
    { iso: 'AU', name: 'Australia', index_change: -0.05, is_open: false },
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
    { name: 'Garfield', breed: 'Orange Tabby', net_worth: 5000000, lat: 52.520, lng: 13.405, city: 'Berlin', is_captain: true },
    { name: 'Sylvester', breed: 'Snowshoe', net_worth: 1400000, lat: 19.076, lng: 72.877, city: 'Mumbai', is_captain: true },
    { name: 'Cheshire', breed: 'British Shorthair', net_worth: 2200000, lat: -23.550, lng: -46.633, city: 'São Paulo', is_captain: true },
    { name: 'Nala', breed: 'Ragdoll', net_worth: 2100000, lat: -33.868, lng: 151.209, city: 'Sydney', is_captain: false },
  ],
  space: { iss: { lat: 51.5, lng: -60.5 } },
}

function toCanvas(lat: number, lng: number, cx: number, cy: number, r: number): [number, number] {
  const lngRad = (lng * Math.PI) / 180
  const latRad = (lat * Math.PI) / 180
  // Orthographic-ish projection scaled to circle
  const x = cx + (Math.cos(latRad) * Math.sin(lngRad)) * r * 0.85
  const y = cy - (Math.sin(latRad)) * r * 0.82
  return [x, y]
}

export default function Map2D({ onClose }: Props) {
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
  const [pageVisible, setPageVisible] = useState(typeof document !== 'undefined' && document.visibilityState !== 'hidden')
  const [dimensions, setDimensions] = useState({ w: 0, h: 0 })
  const animationRef = useRef<number>(0)
  const starsRef = useRef<{ x: number; y: number; s: number; twinkle: number }[]>([])

  // Page visibility
  useEffect(() => {
    const handler = () => setPageVisible(document.visibilityState !== 'hidden')
    document.addEventListener('visibilitychange', handler)
    return () => document.removeEventListener('visibilitychange', handler)
  }, [])

  // Resize observer
  useEffect(() => {
    const container = containerRef.current
    if (!container) return
    const ro = new ResizeObserver(entries => {
      const { width, height } = entries[0].contentRect
      setDimensions({ w: width, h: height })
    })
    ro.observe(container)
    return () => ro.disconnect()
  }, [])

  const fetchData = useCallback(async () => {
    if (!pageVisible) return
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
  }, [pageVisible])

  useEffect(() => {
    fetchData()
    const t = setInterval(fetchData, 60000)
    return () => clearInterval(t)
  }, [fetchData])

  // Time update (throttled)
  useEffect(() => {
    setTime(new Date().toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' }))
    const t = setInterval(() => setTime(new Date().toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })), 30000)
    return () => clearInterval(t)
  }, [])

  // Cat comments
  useEffect(() => {
    const t = setInterval(() => setCatComment(CAT_COMMENTS[Math.floor(Math.random() * CAT_COMMENTS.length)]), 30000)
    return () => clearInterval(t)
  }, [])

  // Pre-generate stars once
  useEffect(() => {
    const stars: { x: number; y: number; s: number; twinkle: number }[] = []
    for (let i = 0; i < 120; i++) stars.push({ x: Math.random(), y: Math.random() * 0.7, s: Math.random() * 1.5 + 0.5, twinkle: Math.random() * Math.PI * 2 })
    starsRef.current = stars
  }, [])

  const drawGlobe = useCallback(() => {
    const canvas = canvasRef.current
    if (!canvas || !data) return
    const w = dimensions.w || canvas.clientWidth
    const h = dimensions.h || canvas.clientHeight
    if (w === 0 || h === 0) return
    canvas.width = w
    canvas.height = h
    const ctx = canvas.getContext('2d')!
    const cx = w / 2
    const cy = h / 2
    const r = Math.min(w, h) * 0.38
    const t = Date.now() * 0.001

    // Background
    ctx.fillStyle = '#06080f'
    ctx.fillRect(0, 0, w, h)

    // Twinkling stars
    for (const star of starsRef.current) {
      const sx = star.x * w, sy = star.y * h * 0.8
      const alpha = 0.15 + Math.sin(t * 2 + star.twinkle) * 0.15
      ctx.fillStyle = `rgba(255,255,255,${alpha})`
      ctx.beginPath()
      ctx.arc(sx, sy, star.s * 0.6, 0, Math.PI * 2)
      ctx.fill()
    }

    // Atmosphere glow
    const glowGrad = ctx.createRadialGradient(cx, cy, r * 0.85, cx, cy, r * 1.25)
    glowGrad.addColorStop(0, 'rgba(0, 255, 136, 0)')
    glowGrad.addColorStop(0.6, 'rgba(0, 255, 136, 0.06)')
    glowGrad.addColorStop(1, 'rgba(0, 255, 136, 0)')
    ctx.fillStyle = glowGrad
    ctx.beginPath()
    ctx.arc(cx, cy, r * 1.25, 0, Math.PI * 2)
    ctx.fill()

    // Globe sphere — dark green gradient with 3D shading
    const globeGrad = ctx.createRadialGradient(cx - r * 0.25, cy - r * 0.3, r * 0.05, cx, cy, r)
    globeGrad.addColorStop(0, '#1e5c36')
    globeGrad.addColorStop(0.35, '#133a20')
    globeGrad.addColorStop(0.7, '#081809')
    globeGrad.addColorStop(1, '#020a03')
    ctx.fillStyle = globeGrad
    ctx.beginPath()
    ctx.arc(cx, cy, r, 0, Math.PI * 2)
    ctx.fill()

    // Specular highlight
    const specGrad = ctx.createRadialGradient(cx - r * 0.4, cy - r * 0.45, r * 0.01, cx - r * 0.1, cy - r * 0.2, r * 0.6)
    specGrad.addColorStop(0, 'rgba(255, 255, 255, 0.08)')
    specGrad.addColorStop(0.4, 'rgba(255, 255, 255, 0.02)')
    specGrad.addColorStop(1, 'rgba(255, 255, 255, 0)')
    ctx.fillStyle = specGrad
    ctx.beginPath()
    ctx.arc(cx, cy, r, 0, Math.PI * 2)
    ctx.fill()

    // Globe rim
    ctx.beginPath()
    ctx.arc(cx, cy, r + 1, 0, Math.PI * 2)
    ctx.strokeStyle = 'rgba(0, 255, 136, 0.12)'
    ctx.lineWidth = 2
    ctx.stroke()

    // Curved graticules
    ctx.strokeStyle = 'rgba(0, 255, 136, 0.04)'
    ctx.lineWidth = 0.5
    for (let lat = -60; lat <= 60; lat += 15) {
      const latRad = (lat * Math.PI) / 180
      const sliceR = Math.cos(latRad) * r * 0.85
      const y = cy - Math.sin(latRad) * r * 0.82
      ctx.beginPath()
      ctx.ellipse(cx, y, sliceR, sliceR * 0.35, 0, 0, Math.PI * 2)
      ctx.stroke()
    }
    for (let lng = -150; lng <= 150; lng += 30) {
      for (let lat = -75; lat < 75; lat += 3) {
        const [x, y] = toCanvas(lat, lng, cx, cy, r)
        if (lat === -75) ctx.beginPath()
        ctx.lineTo(x, y)
      }
      ctx.stroke()
    }

    // Country outline blobs — multiple continents
    const continents: [number, number][][] = [
      // North America
      [[45, -120], [50, -125], [55, -130], [60, -140], [65, -145], [70, -140], [68, -130], [65, -100], [60, -95], [55, -85], [50, -80], [45, -75], [40, -74], [35, -80], [30, -85], [28, -90], [25, -97], [28, -105], [32, -115], [35, -120], [40, -122], [45, -120]],
      // Europe
      [[38, -9], [42, -10], [45, -5], [47, 0], [49, 5], [51, 8], [53, 12], [55, 15], [58, 18], [60, 22], [62, 30], [65, 35], [67, 32], [63, 25], [60, 12], [56, 8], [52, 4], [48, 0], [44, -5], [40, -8], [38, -9]],
      // East Asia
      [[35, 125], [37, 127], [40, 128], [42, 130], [45, 135], [48, 140], [50, 142], [43, 145], [35, 138], [30, 130], [25, 122], [22, 115], [30, 125], [35, 125]],
      // South America
      [[5, -77], [8, -75], [12, -72], [10, -65], [5, -60], [0, -50], [-5, -38], [-10, -42], [-15, -48], [-22, -44], [-25, -50], [-30, -52], [-32, -58], [-28, -65], [-22, -68], [-15, -73], [-5, -80], [0, -78], [5, -77]],
      // Africa
      [[30, -5], [32, -3], [35, 10], [37, 15], [35, 20], [32, 25], [28, 32], [22, 35], [15, 40], [10, 45], [5, 42], [0, 38], [-5, 35], [-10, 35], [-15, 30], [-20, 28], [-25, 32], [-30, 30], [-34, 25], [-35, 20], [-30, 15], [-28, 10], [-25, -5], [-20, -15], [-10, -17], [0, -10], [10, -8], [20, -5], [30, -5]],
      // Australia
      [[-15, 125], [-18, 130], [-22, 135], [-25, 140], [-30, 145], [-34, 148], [-37, 150], [-33, 152], [-28, 150], [-22, 145], [-18, 138], [-15, 130], [-15, 125]],
    ]

    ctx.strokeStyle = 'rgba(0, 255, 136, 0.18)'
    ctx.lineWidth = 1
    ctx.fillStyle = 'rgba(0, 255, 136, 0.04)'
    for (const outline of continents) {
      ctx.beginPath()
      for (let i = 0; i < outline.length; i++) {
        const [x, y] = toCanvas(outline[i][0], outline[i][1], cx, cy, r)
        if (i === 0) ctx.moveTo(x, y)
        else ctx.lineTo(x, y)
      }
      ctx.closePath()
      ctx.fill()
      ctx.stroke()
    }

    // Country indicators
    if (data?.countries) {
      for (const c of data.countries) {
        const [px, py] = toCanvas(c.iso === 'BR' ? -10 : c.iso === 'AU' ? -25 : COUNTRY_COORDS[c.iso]?.[0] || 0, COUNTRY_COORDS[c.iso]?.[1] || 0, cx, cy, r)
        const change = c.index_change || 0
        const alpha = c.is_open ? 0.7 : 0.3
        const color = change >= 0 ? `rgba(0, 255, 136, ${alpha})` : `rgba(255, 68, 68, ${alpha})`
        ctx.fillStyle = color
        ctx.beginPath()
        const size = Math.max(3, Math.min(8, Math.abs(change) * 4))
        ctx.arc(px, py, size, 0, Math.PI * 2)
        ctx.fill()
        if (c.is_open) {
          ctx.strokeStyle = `rgba(0, 255, 136, 0.4)`
          ctx.lineWidth = 0.5
          ctx.stroke()
        }
      }
    }

    // Market exchanges — pulsing dots
    for (const m of MARKETS) {
      const [px, py] = toCanvas(m.lat, m.lng, cx, cy, r)
      const pulse = Math.sin(t * 3 + m.lng) * 0.5 + 0.5
      ctx.fillStyle = m.type === 'exchange' ? '#00ff88' : '#00ccff'
      ctx.beginPath()
      ctx.arc(px, py, 2.5, 0, Math.PI * 2)
      ctx.fill()
      ctx.strokeStyle = `rgba(0, 255, 136, ${0.2 + pulse * 0.2})`
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.arc(px, py, 4 + pulse * 2.5, 0, Math.PI * 2)
      ctx.stroke()
    }

    // Companies
    if (showCompanies) {
      const searchLow = search.toLowerCase()
      for (const co of COMPANIES) {
        const [px, py] = toCanvas(co.lat, co.lng, cx, cy, r)
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

    // Trade routes — curved arcs
    if (showCatboats && data?.trade_routes) {
      const boatPhase = t * 0.3
      for (const tr of data.trade_routes) {
        const fcoords = COUNTRY_COORDS[tr.from]
        const tcoords = COUNTRY_COORDS[tr.to]
        if (!fcoords || !tcoords) continue
        const [fx, fy] = toCanvas(fcoords[0], fcoords[1], cx, cy, r)
        const [tx, ty] = toCanvas(tcoords[0], tcoords[1], cx, cy, r)
        // Draw curved route
        const midX = (fx + tx) / 2
        const midY = Math.min(fy, ty) - Math.abs(fx - tx) * 0.15 - 12
        ctx.strokeStyle = `rgba(0, 255, 136, 0.12)`
        ctx.lineWidth = 0.5
        ctx.beginPath()
        ctx.moveTo(fx, fy)
        ctx.quadraticCurveTo(midX, midY, tx, ty)
        ctx.stroke()
        // Animated boat
        const pos = (boatPhase * tr.velocity + Math.sin(tr.volume * 0.001)) % 1
        const t2 = 1 - pos
        const bx = fx * t2 * t2 + 2 * midX * pos * t2 + tx * pos * pos
        const by = fy * t2 * t2 + 2 * midY * pos * t2 + ty * pos * pos
        ctx.font = `${10 + tr.volume * 0.002}px sans-serif`
        ctx.fillText(tr.catboat || '🐱🚢', bx - 7, by + 4)
        ctx.font = '7px monospace'
        ctx.fillStyle = 'rgba(0,255,136,0.4)'
        ctx.fillText(tr.value || '', bx + 10, by + 2)
      }
    }

    // Capital flow jets
    if (showJets && data?.capital_flows) {
      const jetPhase = t * 1.2
      for (const flow of data.capital_flows) {
        const fcoords = COUNTRY_COORDS[flow.from]
        const tcoords = COUNTRY_COORDS[flow.to]
        if (!fcoords || !tcoords) continue
        const [fx, fy] = toCanvas(fcoords[0], fcoords[1], cx, cy, r)
        const [tx, ty] = toCanvas(tcoords[0], tcoords[1], cx, cy, r)
        ctx.strokeStyle = 'rgba(0, 200, 255, 0.06)'
        ctx.lineWidth = 0.3
        ctx.beginPath()
        ctx.moveTo(fx, fy)
        ctx.lineTo(tx, ty)
        ctx.stroke()
        const pos = (jetPhase * 0.25 + flow.amount * 0.001) % 1
        const jx = fx + (tx - fx) * pos
        const jy = fy + (ty - fy) * pos
        ctx.font = '12px sans-serif'
        ctx.fillText(flow.jet || '✈️', jx - 6, jy - 4)
        ctx.font = '6px monospace'
        ctx.fillStyle = 'rgba(0,200,255,0.3)'
        ctx.fillText(`$${(flow.amount * 1e6).toLocaleString()}`, jx + 8, jy - 2)
      }
    }

    // Launch pads
    for (const pad of LAUNCH_PADS) {
      const [px, py] = toCanvas(pad.lat, pad.lng, cx, cy, r)
      ctx.fillStyle = '#ff6600'
      ctx.beginPath()
      ctx.arc(px, py, 3, 0, Math.PI * 2)
      ctx.fill()
      ctx.strokeStyle = 'rgba(255, 102, 0, 0.25)'
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.arc(px, py, 6 + Math.sin(t * 2 + pad.lat) * 1.5, 0, Math.PI * 2)
      ctx.stroke()
      ctx.font = '9px sans-serif'
      ctx.fillText('🚀', px - 5, py - 5)
      ctx.fillStyle = 'rgba(255, 136, 68, 0.5)'
      ctx.font = '7px monospace'
      ctx.fillText(pad.name.slice(0, 10), px + 4, py + 3)
    }

    // ISS
    if (showISS && data?.space?.iss) {
      const iss = data.space.iss
      const [ix, iy] = toCanvas(iss.lat, iss.lng, cx, cy, r)
      ctx.fillStyle = '#ffff00'
      ctx.beginPath()
      ctx.arc(ix, iy, 3, 0, Math.PI * 2)
      ctx.fill()
      ctx.strokeStyle = 'rgba(255, 255, 0, 0.25)'
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.arc(ix, iy, 6 + Math.sin(t * 4) * 1, 0, Math.PI * 2)
      ctx.stroke()
      ctx.font = '8px monospace'
      ctx.fillStyle = '#ffff00'
      ctx.fillText('🛰️ ISS', ix + 4, iy - 2)
    }

    // Rich cats
    if (showCats && data?.cats) {
      for (const cat of data.cats) {
        const [px, py] = toCanvas(cat.lat, cat.lng, cx, cy, r)
        const pulse = Math.sin(t * 2 + cat.lat) * 0.5 + 0.5
        ctx.fillStyle = `rgba(0, 255, 136, 0.12)`
        ctx.beginPath()
        ctx.arc(px, py, 5 + pulse * 1.5, 0, Math.PI * 2)
        ctx.fill()
        ctx.font = `${cat.is_captain ? '12' : '9'}px sans-serif`
        ctx.fillText(cat.is_captain ? '🐱⚓' : '🐱', px - 4, py - 4)
        ctx.font = '6px monospace'
        ctx.fillStyle = 'rgba(0,255,136,0.3)'
        ctx.fillText(cat.name, px + 6, py + 2)
      }
    }

    // Hairballs
    if (showHairballs && data?.cats) {
      const hbPhase = t * 0.8
      for (let i = 0; i < data.cats.length; i++) {
        const cat = data.cats[i]
        const [px, py] = toCanvas(cat.lat, cat.lng, cx, cy, r)
        const offsetX = Math.sin(hbPhase + i * 1.7) * 10
        const offsetY = Math.cos(hbPhase * 0.7 + i * 1.3) * 6
        const bounce = Math.sin(t * 2.5 + i * 2.1) * 0.3 + 0.7
        ctx.font = `${7 + bounce * 2}px sans-serif`
        ctx.fillStyle = `rgba(180, 130, 200, ${0.3 + Math.sin(t * 1.5 + i) * 0.1})`
        ctx.fillText('🧶', px - 3 + offsetX, py + 2 + offsetY)
      }
    }

    // Only continue animation if page is visible
    if (pageVisible) {
      animationRef.current = requestAnimationFrame(drawGlobe)
    }
  }, [data, showCatboats, showJets, showCats, showISS, showHairballs, showCompanies, search, pageVisible, dimensions])

  useEffect(() => {
    if (data && pageVisible) {
      cancelAnimationFrame(animationRef.current)
      animationRef.current = requestAnimationFrame(drawGlobe)
    }
    return () => cancelAnimationFrame(animationRef.current)
  }, [data, drawGlobe, pageVisible])

  const handleClick = (e: React.MouseEvent) => {
    if (!containerRef.current || !data) return
    const rect = containerRef.current.getBoundingClientRect()
    const mx = e.clientX - rect.left
    const my = e.clientY - rect.top
    const w = dimensions.w || rect.width
    const h = dimensions.h || rect.height
    const r = Math.min(w, h) * 0.38
    const cx = w / 2
    const cy = h / 2

    // Approximate reverse projection
    const dx = (mx - cx) / (r * 0.85)
    const dy = -(my - cy) / (r * 0.82)
    const lng = Math.atan2(dx, Math.sqrt(1 - dx * dx - dy * dy)) * (180 / Math.PI) || 0
    const lat = Math.asin(Math.max(-1, Math.min(1, dy))) * (180 / Math.PI) || 0

    let found: any = null
    for (const m of MARKETS) {
      if (Math.abs(m.lat - lat) < 5 && Math.abs(m.lng - lng) < 5) { found = { ...m, clickType: 'market' }; break }
    }
    if (!found && data.cats) {
      for (const cat of data.cats) {
        if (Math.abs(cat.lat - lat) < 7 && Math.abs(cat.lng - lng) < 7) { found = { ...cat, clickType: 'cat' }; break }
      }
    }
    if (!found) {
      for (const pad of LAUNCH_PADS) {
        if (Math.abs(pad.lat - lat) < 5 && Math.abs(pad.lng - lng) < 5) { found = { ...pad, clickType: 'launchpad' }; break }
      }
    }
    if (!found) {
      for (const co of COMPANIES) {
        if (Math.abs(co.lat - lat) < 3 && Math.abs(co.lng - lng) < 3) { found = { ...co, clickType: 'company' }; break }
      }
    }
    setSelected(found)
  }

  return (
    <div ref={containerRef} className="relative w-full h-full bg-[#06080f] overflow-hidden" onClick={handleClick}>
      <canvas ref={canvasRef} className="absolute inset-0" />

      {/* Toolbar */}
      <div className="absolute top-0 left-0 right-0 z-30 bg-black/85 border-b border-green/10">
        <div className="flex items-center justify-between px-2 py-1.5">
          <div className="flex items-center gap-2">
            <button onClick={(e) => { e.stopPropagation(); onClose?.() }}
              className="px-2 py-0.5 text-[10px] text-dim hover:text-green border border-dim/20 rounded font-mono">
              ← Back
            </button>
            <input type="text" value={search} onChange={(e) => { e.stopPropagation(); setSearch(e.target.value) }}
              onClick={(e) => e.stopPropagation()} placeholder="🔍 Search..."
              className="w-28 md:w-36 px-2 py-0.5 bg-transparent border border-green/10 rounded text-[10px] text-white font-mono placeholder:text-dim/40 outline-none focus:border-green/30" />
          </div>
          <div className="hidden sm:flex items-center gap-1 flex-wrap">
            <ToggleBtn label="🚢 Boats" active={showCatboats} onClick={(e: any) => { e.stopPropagation(); setShowCatboats(!showCatboats) }} />
            <ToggleBtn label="✈️ Jets" active={showJets} onClick={(e: any) => { e.stopPropagation(); setShowJets(!showJets) }} />
            <ToggleBtn label="🐱 Cats" active={showCats} onClick={(e: any) => { e.stopPropagation(); setShowCats(!showCats) }} />
            <ToggleBtn label="🧶 Hairb" active={showHairballs} onClick={(e: any) => { e.stopPropagation(); setShowHairballs(!showHairballs) }} />
            <ToggleBtn label="🛰️ ISS" active={showISS} onClick={(e: any) => { e.stopPropagation(); setShowISS(!showISS) }} />
            <ToggleBtn label="🏢 Co" active={showCompanies} onClick={(e: any) => { e.stopPropagation(); setShowCompanies(!showCompanies) }} />
          </div>
          <span className="text-[9px] text-dim/50 font-mono">{time}</span>
        </div>
      </div>

      {/* Legend */}
      <div className="absolute top-12 right-2 z-20 flex flex-col gap-0.5 text-[8px] font-mono">
        <div className="flex items-center gap-1"><span className="text-green w-2">▲</span><span className="text-dim/50">up</span></div>
        <div className="flex items-center gap-1"><span className="text-red w-2">▼</span><span className="text-dim/50">down</span></div>
        <div className="flex items-center gap-1"><span className="text-yellow w-2">◉</span><span className="text-dim/50">closed</span></div>
      </div>

      {/* Bottom ticker */}
      <div className="absolute bottom-2 left-2 right-2 z-20 flex items-center gap-4 overflow-hidden select-none pointer-events-none">
        <span className="text-yellow text-[9px] font-mono shrink-0">🐟</span>
        {data?.countries?.slice(0, 8).map((c: any, i: number) => (
          <span key={i} className="flex gap-1 text-[9px] font-mono shrink-0">
            <span className="text-dim/40">{c.iso}</span>
            <span className={c.index_change >= 0 ? 'text-green' : 'text-red'}>
              {c.index_change >= 0 ? '▲' : '▼'}{Math.abs(c.index_change || 0).toFixed(1)}%
            </span>
          </span>
        ))}
      </div>

      {/* Cat comment */}
      <div className="absolute bottom-4 left-0 right-0 text-center text-[9px] text-dim/30 font-mono select-none pointer-events-none">
        {catComment}
      </div>

      {/* Bottom tabs */}
      <div className="absolute bottom-8 right-2 z-20 flex gap-1 text-[9px] font-mono">
        {(['cats', 'markets', 'space'] as const).map(tab => (
          <button key={tab} className={`px-2 py-0.5 rounded ${rightPanel === tab ? 'bg-green/10 text-green' : 'text-dim/50 hover:text-green/70'}`}
            onClick={(e) => { e.stopPropagation(); setRightPanel(tab) }}>
            {tab === 'cats' ? '🐱 Cats' : tab === 'markets' ? '📊 Markets' : '🚀 Space'}
          </button>
        ))}
      </div>

      {/* Right panel */}
      {rightPanel && (
        <div className="absolute top-12 right-2 w-48 bg-black/80 border border-green/5 rounded-lg p-2.5 text-[10px] font-mono max-h-56 overflow-y-auto z-20 backdrop-blur">
          {rightPanel === 'cats' && data?.cats && (
            <div className="space-y-1">
              <div className="text-green mb-1 text-xs">🐱 Cat Network ({data.cats.length})</div>
              {[...data.cats].sort((a: any, b: any) => b.net_worth - a.net_worth).map((c: any, i: number) => (
                <div key={i} className="flex justify-between text-[9px]">
                  <span className="text-green/70">{c.is_captain ? '⚓' : '🐱'} {c.name}</span>
                  <span className="text-dim/50">{c.breed?.slice(0, 10)}</span>
                  <span className="text-yellow">${(c.net_worth / 1e6).toFixed(1)}M</span>
                </div>
              ))}
            </div>
          )}
          {rightPanel === 'markets' && (
            <div className="space-y-1">
              <div className="text-green mb-1 text-xs">📊 Markets</div>
              {MARKETS.slice(0, 10).map((m, i) => (
                <div key={i} className="flex justify-between text-[9px]"><span className="text-dim/50">{m.name}</span><span className="text-green/50">● {m.region.slice(0, 12)}</span></div>
              ))}
              <div className="text-dim/30 text-[8px] mt-1">{data?.trade_routes?.length || 0} trade routes · {data?.capital_flows?.length || 0} capital flows</div>
            </div>
          )}
          {rightPanel === 'space' && (
            <div className="space-y-1">
              <div className="text-green mb-1 text-xs">🚀 Space</div>
              {data?.space?.iss && <div className="text-dim/50 text-[9px]">🛰️ ISS: {data.space.iss.lat.toFixed(1)}°, {data.space.iss.lng.toFixed(1)}°</div>}
              {LAUNCHES.map((l, i) => (
                <div key={i} className="text-[9px] border-b border-green/5 pb-0.5">
                  <div className="text-green/70">{l.mission}</div>
                  <div className="text-dim/30">{l.rocket} · {l.date}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Selected detail */}
      {selected && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-black/95 border border-green/20 rounded-xl p-4 text-[10px] font-mono z-30 min-w-[220px] backdrop-blur">
          <button className="absolute top-2 right-2 text-dim/40 hover:text-green" onClick={(e) => { e.stopPropagation(); setSelected(null) }}>✕</button>
          {selected.clickType === 'market' && (
            <div>
              <div className="text-cyan text-sm mb-1">{selected.name}</div>
              <div className="text-dim/50">{selected.ticker} · {selected.region}</div>
            </div>
          )}
          {selected.clickType === 'cat' && (
            <div>
              <div className="text-cyan text-sm mb-1">🐱 {selected.name}</div>
              <div className="text-dim/50">{selected.breed} · {selected.city}</div>
              <div className="text-yellow">${(selected.net_worth / 1e6).toFixed(1)}M</div>
            </div>
          )}
          {selected.clickType === 'launchpad' && (
            <div>
              <div className="text-cyan text-sm mb-1">🚀 {selected.name}</div>
              <div className="text-dim/50">{selected.lat.toFixed(1)}°N, {Math.abs(selected.lng).toFixed(1)}°W</div>
            </div>
          )}
          {selected.clickType === 'company' && (
            <div>
              <div className="text-cyan text-sm mb-1">{COMPANY_SYMBOLS[selected.industry] || '🏢'} {selected.name}</div>
              <div className="text-green">{selected.ticker}</div>
              <div className="text-dim/50">{selected.industry} · ${selected.marketCap}B</div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function ToggleBtn({ label, active, onClick }: { label: string; active: boolean; onClick: (e: React.MouseEvent) => void }) {
  return (
    <button onClick={onClick}
      className={`px-1.5 py-0.5 text-[10px] font-mono rounded border transition-colors ${
        active ? 'bg-green/10 text-green border-green/30' : 'text-dim/40 border-transparent hover:text-dim/70 hover:border-dim/20'
      }`}>
      {label}
    </button>
  )
}
