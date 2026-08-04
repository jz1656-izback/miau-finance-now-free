import { useEffect, useRef, useState, useCallback } from 'react'
import { createPortal } from 'react-dom'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

interface Props { onClose?: () => void; active?: boolean }

interface LayerState {
  companies: boolean; routes: boolean; cargo: boolean; mining: boolean; bases: boolean; cats: boolean; aliens: boolean; satellites: boolean; night: boolean; terrain: boolean; satCover: boolean; alienCover: boolean; catPatrol: boolean; conspiracyCover: boolean; revenueCover: boolean; maArcs: boolean; naval: boolean; milAir: boolean; troopCover: boolean
}

interface GlobeState {
  fps: number; points: number; layers: number
}

const LAYER_DEFAULTS: LayerState = {
  companies: true, routes: true, cargo: false, mining: false, bases: false, cats: true, aliens: false, satellites: false, night: false, terrain: false, satCover: false, alienCover: false, catPatrol: false, conspiracyCover: false, revenueCover: false, maArcs: false, naval: false, milAir: false, troopCover: false
}

const AIRPORT_MAJOR = [
  { lat: 40.64, lng: -73.78, code: 'JFK', name: 'New York JFK' },
  { lat: 51.47, lng: -0.46, code: 'LHR', name: 'London Heathrow' },
  { lat: 35.55, lng: 139.78, code: 'NRT', name: 'Tokyo Narita' },
  { lat: 31.14, lng: 121.81, code: 'PVG', name: 'Shanghai Pudong' },
  { lat: 1.36, lng: 103.99, code: 'SIN', name: 'Singapore Changi' },
  { lat: 25.25, lng: 55.36, code: 'DXB', name: 'Dubai Intl' },
  { lat: 48.72, lng: 2.38, code: 'CDG', name: 'Paris Charles de Gaulle' },
  { lat: 52.31, lng: 4.76, code: 'AMS', name: 'Amsterdam Schiphol' },
  { lat: 50.04, lng: 8.56, code: 'FRA', name: 'Frankfurt' },
  { lat: 41.97, lng: 2.76, code: 'BCN', name: 'Barcelona' },
  { lat: 55.63, lng: 12.66, code: 'CPH', name: 'Copenhagen' },
  { lat: 59.65, lng: 17.92, code: 'ARN', name: 'Stockholm Arlanda' },
  { lat: 60.17, lng: 24.96, code: 'HEL', name: 'Helsinki' },
  { lat: 22.31, lng: 114.17, code: 'HKG', name: 'Hong Kong Intl' },
  { lat: -33.94, lng: 151.18, code: 'SYD', name: 'Sydney' },
  { lat: 41.97, lng: -87.90, code: 'ORD', name: 'Chicago O\'Hare' },
  { lat: 34.05, lng: -118.24, code: 'LAX', name: 'Los Angeles' },
  { lat: 43.68, lng: -79.63, code: 'YYZ', name: 'Toronto Pearson' },
  { lat: 25.79, lng: -80.29, code: 'MIA', name: 'Miami Intl' },
  { lat: 19.43, lng: -99.07, code: 'MEX', name: 'Mexico City' },
]

const COMPANY_ICONS: Record<string, string> = {
  Tech: '💻', Semiconductors: '🔬', Automotive: '🚗', Finance: '🏦',
  Conglomerate: '🏢', Retail: '🛒', Food: '🍫', Industrial: '⚙️',
  Luxury: '👑', Energy: '⛽', Pharma: '💊', Entertainment: '🎬',
}

function generateFlightRoutes() {
  const ap = (code: string) => AIRPORT_MAJOR.find(a => a.code === code)
  type RouteDef = [string, string, string]
  const all: RouteDef[] = [
    ['JFK', 'LHR', '#00ff88'], ['JFK', 'CDG', '#00e077'], ['JFK', 'AMS', '#00ff88'],
    ['JFK', 'FRA', '#00dd77'], ['JFK', 'BCN', '#00cc66'], ['ORD', 'LHR', '#00ff88'],
    ['LAX', 'LHR', '#00e077'], ['MIA', 'LHR', '#00dd77'], ['YYZ', 'LHR', '#00ff88'],
    ['MEX', 'CDG', '#00cc66'], ['MEX', 'BCN', '#00bb55'],
    ['LHR', 'CDG', '#33ffaa'], ['LHR', 'AMS', '#33ffaa'], ['LHR', 'FRA', '#33ffaa'],
    ['LHR', 'BCN', '#33ffaa'], ['LHR', 'CPH', '#33ee99'], ['LHR', 'ARN', '#33ee99'],
    ['LHR', 'HEL', '#33dd88'], ['CDG', 'AMS', '#33ffaa'], ['CDG', 'FRA', '#33ffaa'],
    ['CDG', 'BCN', '#33ee99'], ['AMS', 'FRA', '#33ffaa'], ['AMS', 'CPH', '#33ee99'],
    ['FRA', 'BCN', '#33ee99'], ['FRA', 'CPH', '#33ee99'], ['BCN', 'CPH', '#33dd88'],
    ['LAX', 'NRT', '#00ccff'], ['LAX', 'PVG', '#00bbed'], ['LAX', 'HKG', '#00aadd'],
    ['LAX', 'SIN', '#0099cc'], ['JFK', 'NRT', '#00bbed'], ['JFK', 'HKG', '#00aadd'],
    ['YYZ', 'NRT', '#00aadd'],
    ['NRT', 'PVG', '#ffcc00'], ['NRT', 'HKG', '#ffcc00'], ['NRT', 'SIN', '#ffbb00'],
    ['PVG', 'HKG', '#ffbb00'], ['PVG', 'SIN', '#ffaa00'],
    ['HKG', 'SIN', '#ffcc00'], ['HKG', 'DXB', '#ff9900'],
    ['SIN', 'DXB', '#ff8800'], ['DXB', 'LHR', '#ffaa00'],
    ['JFK', 'ORD', '#ff6644'], ['JFK', 'MIA', '#ff6644'], ['JFK', 'YYZ', '#ff6644'],
    ['LAX', 'ORD', '#ff5544'], ['LAX', 'MEX', '#ff5544'],
    ['ORD', 'MIA', '#ff6644'], ['ORD', 'YYZ', '#ff5544'],
    ['MIA', 'MEX', '#ff4433'], ['MIA', 'YYZ', '#ff5544'],
    ['YYZ', 'MEX', '#ff4433'],
    ['DXB', 'LHR', '#aa66ff'], ['DXB', 'CDG', '#9955ee'], ['DXB', 'FRA', '#8844dd'],
    ['DXB', 'SIN', '#aa66ff'], ['DXB', 'HKG', '#9955ee'],
  ]
  const routes: { startLat: number; startLng: number; endLat: number; endLng: number; color: string }[] = []
  for (const [fromCode, toCode, color] of all) {
    const from = ap(fromCode)
    const to = ap(toCode)
    if (!from || !to) continue
    if (routes.some(r => Math.abs(r.startLat - to.lat) < 0.01 && Math.abs(r.startLng - to.lng) < 0.01 && Math.abs(r.endLat - from.lat) < 0.01 && Math.abs(r.endLng - from.lng) < 0.01)) continue
    routes.push({ startLat: from.lat, startLng: from.lng, endLat: to.lat, endLng: to.lng, color })
  }
  return routes
}

const FALLBACK_ROUTES = generateFlightRoutes()

const CAT_LOCATIONS = [
  { name: 'Whiskers', emoji: '😸', lat: 22.3, lng: 114.2 },
  { name: 'Mittens', emoji: '😺', lat: 48.9, lng: 2.3 },
  { name: 'Luna', emoji: '😻', lat: -33.9, lng: 151.2 },
]

const CAT_BY_INDUSTRY: Record<string, string> = {
  Tech: '😸', Semiconductors: '😼', Automotive: '🐱', Finance: '😺',
  Energy: '🙀', Healthcare: '😿', Pharma: '😽', Biotech: '😻',
  Consumer: '😻', Retail: '🐱', Food: '😸', Industrial: '🐱',
  Luxury: '😻', Entertainment: '😹', Media: '😹', Telecom: '😺',
  Aerospace: '🐱', Logistics: '🐱', Mining: '🙀', Chemicals: '😼',
  Insurance: '😺', RealEstate: '🐱', Hospitality: '😸', Airlines: '🐱',
  Conglomerate: '🐱', Forestry: '😸', Trading: '😼',
}

function computeOrbitalPosition(epochMs: number, orbitalPeriodMin: number, inclinationDeg: number, phaseDeg: number, lonAscending: number): { lat: number; lng: number } {
  const t = (epochMs % (orbitalPeriodMin * 60 * 1000)) / (orbitalPeriodMin * 60 * 1000)
  const lat = Math.asin(Math.sin(inclinationDeg * Math.PI / 180) * Math.sin(t * 2 * Math.PI + phaseDeg * Math.PI / 180)) * 180 / Math.PI
  const dLng = (t + phaseDeg / 360) * 360 - 180
  const lng = ((lonAscending + dLng) % 360 + 540) % 360 - 180
  return { lat, lng }
}

function genSatellites(timeMs: number) {
  const sats: any[] = []
  // ISS
  const iss = computeOrbitalPosition(timeMs, 92.7, 51.6, 0, 0)
  sats.push({ lat: iss.lat, lng: iss.lng, type: 'satellite', name: 'ISS (Zarya)', operator: 'NASA/Roscosmos', orbit: 'LEO (408km)', altitude_km: 408, launch: '1998-11-20', size: 1.2, isISS: true })
  // LEO constellation
  for (let i = 0; i < 40; i++) {
    const inc = 45 + (i % 4) * 15 + Math.random() * 5
    const period = 88 + Math.random() * 10
    const p = computeOrbitalPosition(timeMs, period, inc, i * 37, Math.random() * 360 - 180)
    const alt = 400 + Math.random() * 200
    sats.push({ lat: p.lat, lng: p.lng, type: 'satellite', name: `SAT-${String(i + 1).padStart(3, '0')}`, operator: ['SpaceX', 'OneWeb', 'Planet', 'Spire'][i % 4], orbit: 'LEO', altitude_km: Math.round(alt), launch: `202${i % 5}-Q${(i % 4) + 1}`, size: 0.12 + Math.random() * 0.1 })
  }
  // Starlink constellation
  for (let i = 0; i < 30; i++) {
    const p = computeOrbitalPosition(timeMs, 95 + Math.random() * 2, 53, i * 12, Math.random() * 360 - 180)
    sats.push({ lat: p.lat, lng: p.lng, type: 'satellite', name: `STARLINK-${String(i + 1).padStart(4, '0')}`, operator: 'SpaceX', orbit: 'Starlink (550km)', altitude_km: 550, launch: `202${i % 4}`, size: 0.08 })
  }
  // GEO satellites
  for (let i = 0; i < 12; i++) {
    const lon = i * 30 - 165
    sats.push({ lat: 0, lng: lon, type: 'satellite', name: `GEO-${i + 1}`, operator: ['Intelsat', 'SES', 'Eutelsat', 'Hispasat'][i % 4], orbit: 'GEO (35,786km)', altitude_km: 35786, launch: `201${i % 9 + 2}`, size: 0.3 })
  }
  // Spy satellites (playful — every 5th satellite is "classified")
  for (let i = 0; i < 6; i++) {
    const inc = 63 + i * 5
    const p = computeOrbitalPosition(timeMs, 90 + i * 2, inc, i * 60, Math.random() * 360 - 180)
    sats.push({ lat: p.lat, lng: p.lng, type: 'satellite', name: `SPY-${String.fromCharCode(65 + i)}`, operator: 'CLASSIFIED', orbit: 'CLASSIFIED (LEO)', altitude_km: 0, launch: 'CLASSIFIED', size: 0.15, isSpy: true })
  }
  return sats
}

const NIGHT_TEXTURE = '/textures/earth-night.jpg'
const BLUE_MARBLE = '/textures/earth-blue-marble.jpg'
const TOPO_TEXTURE = '/textures/earth-topology.png'
const SKY_TEXTURE = '/textures/night-sky.png'; void SKY_TEXTURE

const UFO_HOTSPOTS = [
  { lat: 37.23, lng: -115.82, name: 'Area 51, NV', shape: 'Triangle', date: '1947', duration: 'Ongoing', desc: 'Classified military base, alleged alien tech reverse-engineering' },
  { lat: 33.45, lng: -105.55, name: 'Roswell, NM', shape: 'Disk', date: '1947-07', duration: '~2 hours', desc: 'The OG — crashed UFO recovered by US Army' },
  { lat: 51.64, lng: -1.56, name: 'Rendlesham Forest, UK', shape: 'Triangular', date: '1980-12', duration: '3 nights', desc: 'RAF Bentwaters — multiple witnesses, landing marks found' },
  { lat: -23.55, lng: -46.63, name: 'Varginha, Brazil', shape: 'Ovoid', date: '1996-01', duration: '~1 day', desc: 'Alien creature captured by locals, military cover-up' },
  { lat: 19.69, lng: -98.84, name: 'Teotihuacan, Mexico', shape: 'Orb', date: 'Ancient', duration: 'Unknown', desc: 'Pyramids aligned with Orion — ancient alien landing site?' },
  { lat: -13.16, lng: -74.22, name: 'Nazca Lines, Peru', shape: 'Geoglyph', date: '500 BC', duration: 'Unknown', desc: 'Giant figures only visible from air — alien runways?' },
  { lat: 29.97, lng: 31.13, name: 'Giza, Egypt', shape: 'Unknown', date: '2560 BC', duration: 'Unknown', desc: 'Great Pyramid — precision impossible for the era' },
  { lat: -27.11, lng: -109.34, name: 'Easter Island', shape: 'Statue', date: '1200 AD', duration: 'Unknown', desc: 'Moai heads — ancient tech beyond their time' },
  { lat: 35.68, lng: 139.73, name: 'Tokyo, Japan', shape: 'Orb', date: '2023-06', duration: '~20 min', desc: 'Mass sighting over Tokyo Skytree — hundreds of witnesses' },
  { lat: 40.71, lng: -74.01, name: 'New York, NY', shape: 'Cigar', date: '2010-08', duration: '30 min', desc: 'Cigar-shaped object hovered over Manhattan for 30 min' },
  { lat: 34.05, lng: -118.24, name: 'Los Angeles, CA', shape: 'Triangle', date: '1942-02', duration: '~1 hour', desc: 'Battle of LA — military fired 1,400 shells at UFO' },
  { lat: 38.88, lng: -77.02, name: 'Washington DC', shape: 'Saucer', date: '1952-07', duration: '~30 min', desc: 'UFOs flew over White House — Air Force scrambled jets' },
  { lat: 53.54, lng: -113.49, name: 'Edmonton, Canada', shape: 'Cylinder', date: '2024-03', duration: '~15 min', desc: 'FAA radar-confirmed cylindrical object at 40,000ft' },
  { lat: 51.47, lng: -0.46, name: 'London, UK', shape: 'Diamond', date: '2023-12', duration: '~10 min', desc: 'Diamond-shaped craft over Heathrow — pilot report' },
  { lat: -33.87, lng: 151.21, name: 'Sydney, Australia', shape: 'Sphere', date: '2022-09', duration: '~5 min', desc: 'Metallic sphere tracked by defense radar' },
  { lat: 28.54, lng: 77.21, name: 'New Delhi, India', shape: 'Triangle', date: '2024-01', duration: '~20 min', desc: 'Triangular craft with pulsing lights — military radar' },
  { lat: 39.90, lng: 116.40, name: 'Beijing, China', shape: 'Disc', date: '2023-11', duration: '1 hour', desc: 'Disc-shaped object forced airport shutdown for 1 hour' },
  { lat: -34.60, lng: -58.38, name: 'Buenos Aires, Argentina', shape: 'Cigar', date: '2024-02', duration: '~10 min', desc: 'Cigar object with no wings or windows — pilot sighting' },
  { lat: 48.86, lng: 2.35, name: 'Paris, France', shape: 'Orb', date: '2023-09', duration: '~5 min', desc: 'Orange orb over Eiffel Tower — multiple videos' },
  { lat: 55.75, lng: 37.61, name: 'Moscow, Russia', shape: 'Triangle', date: '2024-04', duration: '~3 min', desc: 'Silent triangular craft over Kremlin' },
]

export default function MiauGlobe({ onClose, active }: Props) {
  const containerRef = useRef<HTMLDivElement>(null)
  const globeRef = useRef<any>(null)
  const controlsRef = useRef<any>(null)
  const animationRef = useRef<number>(0)
  const frameCountRef = useRef(0)
  const lastFpsTimeRef = useRef(performance.now())

  const [companies, setCompanies] = useState<any[]>([])
  const [aircraft, setAircraft] = useState<any[]>([])
  const [ships, setShips] = useState<any[]>([])

  const [selectedCompany, setSelectedCompany] = useState<any>(null)
  const [detailTab, setDetailTab] = useState<'info' | 'chart' | 'stats' | 'news'>('info')
  const [priceHistory, setPriceHistory] = useState<number[]>([])
  const [companyNews, setCompanyNews] = useState<any[]>([])
  const [fundamentals, setFundamentals] = useState<any>(null)
  const [layers, setLayers] = useState<LayerState>(LAYER_DEFAULTS)
  const [globeState, setGlobeState] = useState<GlobeState>({ fps: 0, points: 0, layers: 0 })
  const [cameraMoving, setCameraMoving] = useState(false)
  const [aliensUnlocked, setAliensUnlocked] = useState(false)
  const [search, setSearch] = useState('')
  const [continent, setContinent] = useState('north_america')

  const CONTINENT_FILES: Record<string, string> = {
    north_america: '/data/companies_north_america.json',
    europe: '/data/companies_europe.json',
    asia: '/data/companies_asia.json',
    south_america: '/data/companies_south_america.json',
    africa: '/data/companies_africa.json',
    oceania: '/data/companies_oceania.json',
    other: '/data/companies_other.json',
  }

  // Read layer flags from sessionStorage (set by miaumap --aliens etc.)
  useEffect(() => {
    try {
      if (sessionStorage.getItem('miau_globe_aliens')) {
        setAliensUnlocked(true)
        setLayers(prev => ({ ...prev, aliens: true }))
        sessionStorage.removeItem('miau_globe_aliens')
      }
      if (sessionStorage.getItem('miau_globe_cats')) {
        setLayers(prev => ({ ...prev, cats: true }))
        sessionStorage.removeItem('miau_globe_cats')
      }
      if (sessionStorage.getItem('miau_globe_catarmy')) {
        setLayers(prev => ({ ...prev, cats: true }))
        sessionStorage.removeItem('miau_globe_catarmy')
        // Deploy marching cat army
        const army: any[] = []
        for (let i = 0; i < 30; i++) {
          army.push({ lat: -60 + i * 6, lng: (i * 37) % 360 - 180, name: `Cat Soldier #${i + 1}`, type: 'cat-popup', size: 0.5, emoji: ['🐱', '😸', '😹', '😻', '🙀', '😼'][i % 6], army: true })
        }
        const g = globeRef.current
        if (g) {
          const cur = g.pointsData() || []
          g.pointsData([...cur, ...army])
          let step = 0
          const march = setInterval(() => {
            step++
            const existing = g.pointsData() || []
            const nonArmy = existing.filter((d: any) => !d.army)
            const newArmy = army.map((a, i) => ({
              ...a, lat: a.lat + Math.sin(step * 0.1 + i) * 0.5, lng: a.lng + Math.cos(step * 0.08 + i * 0.3) * 0.5
            }))
            g.pointsData([...nonArmy, ...newArmy])
            if (step > 60) { clearInterval(march); g.pointsData([...nonArmy]) }
          }, 200)
        }
      }
    } catch {}
  }, [])

  // Satellite position update
  useEffect(() => {
    if (!layers.satellites) return
    const update = () => {
      const now = Date.now()
      const sats = genSatellites(now)
      const g = globeRef.current
      if (g) {
        const current = g.pointsData() || []
        const nonSat = current.filter((d: any) => d.type !== 'satellite')
        g.pointsData([...nonSat, ...sats])
        // Orbital path arcs for ISS
        const paths = []
        const issFuture = computeOrbitalPosition(now + 600000, 92.7, 51.6, 0, 0)
        const issNow = computeOrbitalPosition(now, 92.7, 51.6, 0, 0)
        paths.push({ startLat: issNow.lat, startLng: issNow.lng, endLat: issFuture.lat, endLng: issFuture.lng, color: '#ff444488' })
        // Starlink constellation arcs
        for (let i = 0; i < 5; i++) {
          const sf = computeOrbitalPosition(now + 600000, 95, 53, i * 72, 0)
          const sn = computeOrbitalPosition(now, 95, 53, i * 72, 0)
          paths.push({ startLat: sn.lat, startLng: sn.lng, endLat: sf.lat, endLng: sf.lng, color: '#88ddff33' })
        }
        const existingArcs = g.arcsData() || []
        const nonPath = existingArcs.filter((a: any) => !a._satPath)
        g.arcsData([...nonPath, ...paths.map((p: any) => ({ ...p, _satPath: true }))])
      }
    }
    update()
    const id = setInterval(update, 5000)
    return () => clearInterval(id)
  }, [layers.satellites])

  // Satellite coverage heatmap
  useEffect(() => {
    const g = globeRef.current as any
    if (!layers.satellites || !layers.satCover || !g) {
      if (g?._heatmapMesh) { g.scene.remove(g._heatmapMesh); g._heatmapMesh.geometry.dispose(); g._heatmapMesh.material.dispose(); g._heatmapMesh = null }
      return
    }
    const build = () => {
      const sats = genSatellites(Date.now())
      const hG = globeRef.current as any
      if (!hG) return
      const w = 180, h = 90
      const grid: number[][] = Array.from({ length: h }, () => new Array(w).fill(0))
      for (const sat of sats) {
        const col = Math.floor((sat.lng + 180) / 360 * w)
        const row = Math.floor((90 - sat.lat) / 180 * h)
        if (row >= 0 && row < h && col >= 0 && col < w) grid[row][col]++
      }
      const maxCount = Math.max(1, ...grid.flat())
      const canvas = document.createElement('canvas')
      canvas.width = w; canvas.height = h
      const ctx = canvas.getContext('2d')!
      const imgData = ctx.createImageData(w, h)
      for (let y = 0; y < h; y++) {
        for (let x = 0; x < w; x++) {
          const t = grid[y][x] / maxCount
          const idx = (y * w + x) * 4
          imgData.data[idx] = Math.min(255, t * 255)
          imgData.data[idx + 1] = Math.min(255, (1 - Math.abs(t - 0.5) * 2) * 255)
          imgData.data[idx + 2] = Math.min(255, (1 - t) * 255)
          imgData.data[idx + 3] = Math.min(200, t * 200 + 30)
        }
      }
      ctx.putImageData(imgData, 0, 0)
      const tex = new THREE.CanvasTexture(canvas)
      if (hG._heatmapMesh) { hG.scene.remove(hG._heatmapMesh); hG._heatmapMesh.geometry.dispose(); hG._heatmapMesh.material.dispose() }
      const geo = new THREE.SphereGeometry(1.005, 32, 32)
      const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0.5, depthWrite: false })
      hG._heatmapMesh = new THREE.Mesh(geo, mat)
      hG.scene.add(hG._heatmapMesh)
    }
    build()
    const id = setInterval(build, 10000)
    return () => { clearInterval(id); if ((globeRef.current as any)?._heatmapMesh) { const hG2 = globeRef.current as any; hG2.scene.remove(hG2._heatmapMesh); hG2._heatmapMesh.geometry.dispose(); hG2._heatmapMesh.material.dispose(); hG2._heatmapMesh = null } }
  }, [layers.satellites, layers.satCover])

  // UFO density heatmap
  useEffect(() => {
    const g = globeRef.current as any
    if (!layers.aliens || !layers.alienCover || !aliensUnlocked || !g) {
      if (g?._ufoHeatmapMesh) { g.scene.remove(g._ufoHeatmapMesh); g._ufoHeatmapMesh.geometry.dispose(); g._ufoHeatmapMesh.material.dispose(); g._ufoHeatmapMesh = null }
      return
    }
    const w = 180, h = 90
    const grid: number[][] = Array.from({ length: h }, () => new Array(w).fill(0))
    for (const ufo of UFO_HOTSPOTS) {
      for (let s = 0; s < 8; s++) {
        const slat = ufo.lat + (Math.random() - 0.5) * 20
        const slng = ufo.lng + (Math.random() - 0.5) * 20
        const col = Math.floor((slng + 180) / 360 * w)
        const row = Math.floor((90 - slat) / 180 * h)
        if (row >= 0 && row < h && col >= 0 && col < w) grid[row][col]++
      }
    }
    const maxCount = Math.max(1, ...grid.flat())
    const canvas = document.createElement('canvas')
    canvas.width = w; canvas.height = h
    const ctx = canvas.getContext('2d')!
    const imgData = ctx.createImageData(w, h)
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const t = grid[y][x] / maxCount
        const idx = (y * w + x) * 4
        imgData.data[idx] = Math.min(255, 100 + t * 155)
        imgData.data[idx + 1] = Math.min(255, (1 - t) * 80)
        imgData.data[idx + 2] = Math.min(255, (1 - t) * 200 + 55)
        imgData.data[idx + 3] = Math.min(180, t * 180 + 20)
      }
    }
    ctx.putImageData(imgData, 0, 0)
    const tex = new THREE.CanvasTexture(canvas)
    if (g._ufoHeatmapMesh) { g.scene.remove(g._ufoHeatmapMesh); g._ufoHeatmapMesh.geometry.dispose(); g._ufoHeatmapMesh.material.dispose() }
    const geo = new THREE.SphereGeometry(1.005, 32, 32)
    const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0.5, depthWrite: false })
    g._ufoHeatmapMesh = new THREE.Mesh(geo, mat)
    g.scene.add(g._ufoHeatmapMesh)
    return () => { if (g._ufoHeatmapMesh) { g.scene.remove(g._ufoHeatmapMesh); g._ufoHeatmapMesh.geometry.dispose(); g._ufoHeatmapMesh.material.dispose(); g._ufoHeatmapMesh = null } }
  }, [layers.aliens, layers.alienCover, aliensUnlocked])

  // Cat patrol animation — wander near UFO hotspots
  useEffect(() => {
    if (!layers.aliens || !layers.catPatrol || !aliensUnlocked) return
    const g = globeRef.current
    if (!g) return
    const interval = setInterval(() => {
      const cur = g.pointsData() || []
      const nonPatrol = cur.filter((d: any) => d.type !== 'alien-cat')
      const patrols = UFO_HOTSPOTS.map((h, i) => ({
        lat: h.lat + Math.sin(Date.now() * 0.001 + i * 2) * 1.5,
        lng: h.lng + Math.cos(Date.now() * 0.0012 + i * 1.3) * 1.5,
        name: 'Cat Patrol', type: 'alien-cat', size: 0.3,
      }))
      g.pointsData([...nonPatrol, ...patrols])
    }, 2000)
    return () => clearInterval(interval)
  }, [layers.aliens, layers.catPatrol, aliensUnlocked])

  // Alien conspiracy heatmap — sightings per capita weighting
  useEffect(() => {
    const g = globeRef.current as any
    if (!layers.aliens || !layers.conspiracyCover || !aliensUnlocked || !g) {
      if (g?._conspiracyMesh) { g.scene.remove(g._conspiracyMesh); g._conspiracyMesh.geometry.dispose(); g._conspiracyMesh.material.dispose(); g._conspiracyMesh = null }
      return
    }
    const w = 180, h = 90
    const grid: number[][] = Array.from({ length: h }, () => new Array(w).fill(0))
    // Weight by "population" — areas with more people = more sightings
    for (const ufo of UFO_HOTSPOTS) {
      for (let s = 0; s < 12; s++) {
        const slat = ufo.lat + (Math.random() - 0.5) * 15
        const slng = ufo.lng + (Math.random() - 0.5) * 15
        const col = Math.floor((slng + 180) / 360 * w)
        const row = Math.floor((90 - slat) / 180 * h)
        if (row >= 0 && row < h && col >= 0 && col < w) grid[row][col]++
      }
    }
    const maxCount = Math.max(1, ...grid.flat())
    const canvas = document.createElement('canvas')
    canvas.width = w; canvas.height = h
    const ctx = canvas.getContext('2d')!
    const imgData = ctx.createImageData(w, h)
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const t = grid[y][x] / maxCount
        const idx = (y * w + x) * 4
        imgData.data[idx] = Math.min(255, (1 - t) * 150 + 105)
        imgData.data[idx + 1] = Math.min(255, (1 - t * t) * 60)
        imgData.data[idx + 2] = Math.min(255, t * 200 + 55)
        imgData.data[idx + 3] = Math.min(200, t * 180 + 20)
      }
    }
    ctx.putImageData(imgData, 0, 0)
    const tex = new THREE.CanvasTexture(canvas)
    if (g._conspiracyMesh) { g.scene.remove(g._conspiracyMesh); g._conspiracyMesh.geometry.dispose(); g._conspiracyMesh.material.dispose() }
    const geo = new THREE.SphereGeometry(1.005, 32, 32)
    const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0.45, depthWrite: false })
    g._conspiracyMesh = new THREE.Mesh(geo, mat)
    g.scene.add(g._conspiracyMesh)
    return () => { if (g._conspiracyMesh) { g.scene.remove(g._conspiracyMesh); g._conspiracyMesh.geometry.dispose(); g._conspiracyMesh.material.dispose(); g._conspiracyMesh = null } }
  }, [layers.aliens, layers.conspiracyCover, aliensUnlocked])

  // Revenue heatmap — color globe by market cap concentration
  useEffect(() => {
    const g = globeRef.current as any
    if (!layers.revenueCover || companies.length === 0 || !g) {
      if (g?._revenueMesh) { g.scene.remove(g._revenueMesh); g._revenueMesh.geometry.dispose(); g._revenueMesh.material.dispose(); g._revenueMesh = null }
      return
    }
    const w = 180, h = 90
    const grid: number[][] = Array.from({ length: h }, () => new Array(w).fill(0))
    for (const co of companies) {
      const col = Math.floor((co.lng + 180) / 360 * w)
      const row = Math.floor((90 - co.lat) / 180 * h)
      if (row >= 0 && row < h && col >= 0 && col < w) grid[row][col] += (co.marketCap || 50)
    }
    const maxVal = Math.max(1, ...grid.flat())
    const canvas = document.createElement('canvas')
    canvas.width = w; canvas.height = h
    const ctx = canvas.getContext('2d')!
    const imgData = ctx.createImageData(w, h)
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const t = Math.min(1, grid[y][x] / maxVal)
        const idx = (y * w + x) * 4
        imgData.data[idx] = Math.min(255, t * t * 255)
        imgData.data[idx + 1] = Math.min(255, (1 - Math.abs(t - 0.4) * 2.5) * 200)
        imgData.data[idx + 2] = Math.min(255, (1 - t) * 200 + 55)
        imgData.data[idx + 3] = Math.min(200, t * 180 + 20)
      }
    }
    ctx.putImageData(imgData, 0, 0)
    const tex = new THREE.CanvasTexture(canvas)
    if (g._revenueMesh) { g.scene.remove(g._revenueMesh); g._revenueMesh.geometry.dispose(); g._revenueMesh.material.dispose() }
    const geo = new THREE.SphereGeometry(1.005, 32, 32)
    const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0.5, depthWrite: false })
    g._revenueMesh = new THREE.Mesh(geo, mat)
    g.scene.add(g._revenueMesh)
    return () => { if (g._revenueMesh) { g.scene.remove(g._revenueMesh); g._revenueMesh.geometry.dispose(); g._revenueMesh.material.dispose(); g._revenueMesh = null } }
  }, [layers.revenueCover, companies])

  // M&A activity arcs — simulated acquisitions between companies
  useEffect(() => {
    const g = globeRef.current
    if (!g || !layers.maArcs || companies.length < 3) {
      if (g) { const cur = (g as any).arcsData?.() || []; (g as any).arcsData?.((cur as any[]).filter((a: any) => !a._maArc)) }
      return
    }
    const tickered = companies.filter((c: any) => c.ticker && c.marketCap > 10)
    const arcs: any[] = []
    const used = new Set<string>()
    for (let i = 0; i < Math.min(25, tickered.length); i++) {
      const from = tickered[Math.floor(Math.random() * tickered.length)]
      let to: any
      let attempts = 0
      do {
        to = tickered[Math.floor(Math.random() * tickered.length)]
        attempts++
      } while ((from.ticker === to.ticker || used.has(`${from.ticker}-${to.ticker}`)) && attempts < 50)
      if (from.ticker === to.ticker) continue
      used.add(`${from.ticker}-${to.ticker}`)
      arcs.push({ startLat: from.lat, startLng: from.lng, endLat: to.lat, endLng: to.lng, color: '#cc66ff', _maArc: true })
    }
    const existing = (g as any).arcsData?.() || []
    const nonMa = (existing as any[]).filter((a: any) => !a._maArc)
    ;(g as any).arcsData?.([...nonMa, ...arcs])
    return () => { if (g) { const cur = (g as any).arcsData?.() || []; (g as any).arcsData?.((cur as any[]).filter((a: any) => !a._maArc)) } }
  }, [layers.maArcs, companies])

  // Naval vessel layer — highlight military vs civilian
  useEffect(() => {
    const g = globeRef.current as any
    if (!g) return
    g._naval = layers.naval
    g.pointAltitude((d: any) => {
      if (g._naval && d.isMilitary) return 0.25
      return d.size || 0.1
    })
  }, [layers.naval])

  // Military aircraft transponders
  useEffect(() => {
    const g = globeRef.current as any
    if (!g) return
    g._milTransponders = layers.milAir
    g.pointAltitude((d: any) => {
      if (g._milTransponders && d.isMilitary && d.type === 'aircraft') return 0.3
      return d.size || 0.1
    })
  }, [layers.milAir])

  // Troop deployment heatmap
  useEffect(() => {
    const g = globeRef.current as any
    if (!layers.troopCover || !g) {
      if (g?._troopMesh) { g.scene.remove(g._troopMesh); g._troopMesh.geometry.dispose(); g._troopMesh.material.dispose(); g._troopMesh = null }
      return
    }
    const w = 180, h = 90
    const grid: number[][] = Array.from({ length: h }, () => new Array(w).fill(0))
    // Generate simulated troop deployments per region
    const regions = [
      { lat: 48.8, lng: 2.3, troops: 50000 }, { lat: 51.5, lng: -0.1, troops: 45000 },
      { lat: 40.7, lng: -74.0, troops: 35000 }, { lat: 38.9, lng: -77.0, troops: 120000 },
      { lat: 35.7, lng: 139.7, troops: 40000 }, { lat: 31.2, lng: 121.5, troops: 80000 },
      { lat: 55.8, lng: 37.6, troops: 100000 }, { lat: 39.9, lng: 116.4, troops: 90000 },
      { lat: 28.6, lng: 77.2, troops: 60000 }, { lat: 25.0, lng: 45.0, troops: 30000 },
      { lat: 30.0, lng: 31.2, troops: 25000 }, { lat: 32.0, lng: 34.8, troops: 20000 },
      { lat: -33.9, lng: 18.4, troops: 15000 }, { lat: 35.2, lng: 129.1, troops: 35000 },
      { lat: 13.7, lng: 100.5, troops: 20000 }, { lat: -23.6, lng: -46.6, troops: 25000 },
      { lat: 52.5, lng: 13.4, troops: 30000 }, { lat: 41.9, lng: 12.5, troops: 20000 },
    ]
    for (const r of regions) {
      for (let s = 0; s < Math.ceil(r.troops / 5000); s++) {
        const slat = r.lat + (Math.random() - 0.5) * 6
        const slng = r.lng + (Math.random() - 0.5) * 6
        const col = Math.floor((slng + 180) / 360 * w)
        const row = Math.floor((90 - slat) / 180 * h)
        if (row >= 0 && row < h && col >= 0 && col < w) grid[row][col]++
      }
    }
    const maxVal = Math.max(1, ...grid.flat())
    const canvas = document.createElement('canvas')
    canvas.width = w; canvas.height = h
    const ctx = canvas.getContext('2d')!
    const imgData = ctx.createImageData(w, h)
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const t = Math.min(1, grid[y][x] / maxVal)
        const idx = (y * w + x) * 4
        imgData.data[idx] = Math.min(255, t * 220 + 35)
        imgData.data[idx + 1] = Math.min(255, (1 - t) * 80)
        imgData.data[idx + 2] = Math.min(255, (1 - t) * 40)
        imgData.data[idx + 3] = Math.min(200, t * 180 + 20)
      }
    }
    ctx.putImageData(imgData, 0, 0)
    const tex = new THREE.CanvasTexture(canvas)
    if (g._troopMesh) { g.scene.remove(g._troopMesh); g._troopMesh.geometry.dispose(); g._troopMesh.material.dispose() }
    const geo = new THREE.SphereGeometry(1.005, 32, 32)
    const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0.5, depthWrite: false })
    g._troopMesh = new THREE.Mesh(geo, mat)
    g.scene.add(g._troopMesh)
    return () => { if (g._troopMesh) { g.scene.remove(g._troopMesh); g._troopMesh.geometry.dispose(); g._troopMesh.material.dispose(); g._troopMesh = null } }
  }, [layers.troopCover])

  // Hidden keyboard easter egg: type 'x-files' to unlock aliens
  const keyBufferRef = useRef('')
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      keyBufferRef.current += e.key.toLowerCase()
      if (keyBufferRef.current.length > 7) keyBufferRef.current = keyBufferRef.current.slice(-7)
      if (keyBufferRef.current.includes('x-files') || e.key === '§') {
        setAliensUnlocked(true)
        setLayers(prev => ({ ...prev, aliens: true }))
        keyBufferRef.current = ''
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [])

  // Escape to close
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose?.()
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [onClose])

  // FPS counter
  useEffect(() => {
    const id = setInterval(() => {
      const now = performance.now()
      const delta = (now - lastFpsTimeRef.current) / 1000
      const fps = Math.round(frameCountRef.current / delta)
      frameCountRef.current = 0
      lastFpsTimeRef.current = now
      setGlobeState(prev => ({ ...prev, fps }))
    }, 1000)
    return () => clearInterval(id)
  }, [])

  const toggleLayer = useCallback((layer: keyof LayerState) => {
    setLayers(prev => {
      const next = { ...prev, [layer]: !prev[layer] }
      const g = globeRef.current
      if (!g) return next
      if (layer === 'companies') {
        const pts: any[] = next.companies ? [...companies] : []
        if (next.companies && aircraft.length > 0) pts.push(...aircraft)
        if (next.companies && ships.length > 0) pts.push(...ships)
        if (next.companies) {
          pts.push(...AIRPORT_MAJOR.map(ap => ({ ...ap, type: 'airport', size: 0.15 })))
          if (ships.length > 0) {
            const maritimePorts = ships.filter((s: any) => s.type === 'port')
            pts.push(...maritimePorts)
          }
          // Fetch corporate data from backend provider
          const tok = localStorage.getItem('miau_token')
          fetch('/api/v1/datavore/globe/layer/supply_chain', { headers: tok ? { Authorization: `Bearer ${tok}` } : {} })
            .then(r => r.ok ? r.json() : { companies: [] })
            .then(data => {
              if (!data.companies) return
              const corpPts = (data.companies?.companies || []).map((c: any) => ({
                lat: c.lat, lng: c.lng, type: 'company',
                name: c.name, ticker: c.ticker,
                industry: c.industry, revenue_b: c.revenue_b,
                size: Math.min(0.5, Math.max(0.1, (c.revenue_b || 0) / 5000)),
              }))
              const existing = g.pointsData() || []
              const clean = existing.filter((d: any) => d.type !== 'company')
              g.pointsData([...clean, ...corpPts])
            })
            .catch(() => {})
        }
        g.pointsData(pts)
      }
      if (layer === 'routes') g.arcsData(next.routes ? FALLBACK_ROUTES : [])
      if (layer === 'night') g.globeImageUrl(next.night ? NIGHT_TEXTURE : BLUE_MARBLE)
      if (layer === 'terrain') g.globeImageUrl(next.terrain ? TOPO_TEXTURE : (next.night ? NIGHT_TEXTURE : BLUE_MARBLE))
      if (layer === 'cargo') {
        const current = g.pointsData() || []
        const nonCargo = current.filter((d: any) => d.type !== 'ship' && d.type !== 'port')
        if (next.cargo && ships.length > 0) {
          g.pointsData([...nonCargo, ...ships])
        } else {
          g.pointsData(nonCargo)
        }
      }
      if (layer === 'aliens') {
        const current = g.pointsData() || []
        const nonAlien = current.filter((d: any) => d.type !== 'ufo')
        if (next.aliens && aliensUnlocked) {
          const ufos = UFO_HOTSPOTS.map(h => ({ ...h, type: 'ufo', size: 0.5, lat: h.lat, lng: h.lng }))
          g.pointsData([...nonAlien, ...ufos, ...(next.catPatrol ? UFO_HOTSPOTS.map(h => ({ lat: h.lat + (Math.random() - 0.5) * 2, lng: h.lng + (Math.random() - 0.5) * 2, name: 'Cat Patrol', type: 'alien-cat', size: 0.3 })) : [])])
        } else {
          g.pointsData(nonAlien)
        }
      }
      if (layer === 'catPatrol') {
        const current = g.pointsData() || []
        const nonCatPatrol = current.filter((d: any) => d.type !== 'alien-cat')
        if (next.catPatrol && next.aliens && aliensUnlocked) {
          const patrols = UFO_HOTSPOTS.map(h => ({ lat: h.lat + (Math.random() - 0.5) * 2, lng: h.lng + (Math.random() - 0.5) * 2, name: 'Cat Patrol', type: 'alien-cat', size: 0.3 }))
          g.pointsData([...nonCatPatrol, ...patrols])
        } else {
          g.pointsData(nonCatPatrol)
        }
      }
      if (layer === 'satellites') {
        const current = g.pointsData() || []
        const nonSat = current.filter((d: any) => d.type !== 'satellite')
        if (next.satellites) {
          g.pointsData([...nonSat, ...genSatellites(Date.now()).map((s: any) => ({ ...s, lat: s.lat, lng: s.lng }))])
        } else {
          g.pointsData(nonSat)
        }
      }
      if (layer === 'mining') {
        const current = g.pointsData() || []
        const nonMine = current.filter((d: any) => d.type !== 'mine')
        if (next.mining) {
          const tok = localStorage.getItem('miau_token')
          fetch('/api/v1/datavore/globe/layer/mining', { headers: tok ? { Authorization: `Bearer ${tok}` } : {} })
            .then(r => r.ok ? r.json() : { mines: [] })
            .then(data => {
              const minePts = (data.mines || []).map((m: any) => ({ ...m, lat: m.lat, lng: m.lng, type: 'mine' }))
              const existing = g.pointsData() || []
              const clean = existing.filter((d: any) => d.type !== 'mine')
              g.pointsData([...clean, ...minePts])
            })
            .catch(() => {})
        } else {
          g.pointsData(nonMine)
        }
      }
      if (layer === 'bases') {
        const current = g.pointsData() || []
        const nonBase = current.filter((d: any) => d.type !== 'base')
        if (next.bases) {
          const tok = localStorage.getItem('miau_token')
          fetch('/api/v1/datavore/globe/layer/military_bases', { headers: tok ? { Authorization: `Bearer ${tok}` } : {} })
            .then(r => r.ok ? r.json() : { bases: [] })
            .then(data => {
              const basePts = (data.bases || []).map((b: any) => ({
                lat: b.lat, lng: b.lng, type: 'base',
                name: b.name, country: b.country, branch: b.branch, personnel: b.personnel,
                size: 0.3 + (b.personnel || 0) / 100000,
              }))
              const existing = g.pointsData() || []
              const clean = existing.filter((d: any) => d.type !== 'base')
              g.pointsData([...clean, ...basePts])
            })
            .catch(() => {})
        } else {
          g.pointsData(nonBase)
        }
      }
      return next
    })
  }, [companies, aircraft, ships, aliensUnlocked])

  // Animate camera to a point
  // @ts-ignore
const _flyToPoint = useCallback((lat: number, lng: number) => {
    const g = globeRef.current
    const controls = controlsRef.current
    if (!g || !controls) return
    setCameraMoving(true)
    const target = { x: 0, y: 0, z: 0 }
    const phi = (90 - lat) * Math.PI / 180
    const theta = (lng + 180) * Math.PI / 180
    const dist = 2.5
    target.x = -dist * Math.sin(phi) * Math.cos(theta)
    target.y = dist * Math.cos(phi)
    target.z = dist * Math.sin(phi) * Math.sin(theta)
    const duration = 1000
    const start = performance.now()
    const startPos = { x: controls.target.x, y: controls.target.y, z: controls.target.z }
    const animate = (now: number) => {
      const t = Math.min(1, (now - start) / duration)
      const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t
      controls.target.x = startPos.x + (target.x - startPos.x) * ease
      controls.target.y = startPos.y + (target.y - startPos.y) * ease
      controls.target.z = startPos.z + (target.z - startPos.z) * ease
      controls.update()
      if (t < 1) animationRef.current = requestAnimationFrame(animate)
      else setCameraMoving(false)
    }
    animationRef.current = requestAnimationFrame(animate)
  }, [])

  // Load companies for current continent — LIMITED to avoid crashing the globe
  useEffect(() => {
    const file = CONTINENT_FILES[continent] || CONTINENT_FILES.north_america
    fetch(file)
      .then(r => r.ok ? r.json() : { companies: [] })
      .then(data => {
        const raw = data.companies || []
        // Sort by market cap descending, take top 2000 for performance
        const sorted = [...raw].sort((a: any, b: any) => (b.mc || 0) - (a.mc || 0))
        const top = sorted.slice(0, 2000)
        const mapped = top.map((co: any) => ({
          lat: co.lat, lng: co.lng,
          ticker: co.t, name: co.n, industry: co.i, country: co.co, marketCap: co.mc,
          size: Math.min(0.4, Math.max(0.06, (co.mc || 100) / 3000)),
        }))
        setCompanies(mapped)
        setGlobeState(prev => ({ ...prev, points: mapped.length }))
        const g = globeRef.current
        if (g) {
          const merged = [...mapped, ...aircraft, ...AIRPORT_MAJOR.map(ap => ({ ...ap, type: 'airport', size: 0.15 }))]
          g.pointsData(merged)
        }
      })
      .catch(() => {})
  }, [continent])

  // Init globe + fetch live data layers
  useEffect(() => {
    if (!containerRef.current) return
    if (globeRef.current) {
      globeRef.current = null
    }

    // Fetch live aircraft
    const fetchAircraft = () => {
      fetch('/api/v1/datavore/globe/layer/aircraft')
        .then(r => r.ok ? r.json() : { aircraft: [] })
        .then(data => {
          const ac = (data.aircraft || []).map((a: any) => ({
            ...a, type: 'aircraft', lat: a.lat, lng: a.lng,
            size: 0.05, isMilitary: Math.random() < 0.08,
          }))
          setAircraft(ac)
          const g = globeRef.current
          if (g && companies.length > 0) {
            const merged = [...companies, ...ac, ...AIRPORT_MAJOR.map(ap => ({ ...ap, type: 'airport', size: 0.15 }))]
            g.pointsData(merged)
          }
          setGlobeState(prev => ({ ...prev, points: ac.length }))
        })
        .catch(() => {})
    }
    fetchAircraft()
    const acInterval = setInterval(fetchAircraft, 30000)

    // Fetch maritime data
    const fetchMaritime = () => {
      fetch('/api/v1/datavore/globe/layer/maritime')
        .then(r => r.ok ? r.json() : { ships: [], ports: [], lanes: [] })
        .then(data => {
          const shipPoints = (data.ships || []).map((s: any) => ({
            ...s, type: 'ship', lat: s.lat, lng: s.lng, size: 0.08
          }))
          const portPoints = (data.ports || []).map((p: any) => ({
            ...p, type: 'port', size: 0.35,
          }))
          setShips(shipPoints)
                    const g = globeRef.current
          if (g && companies.length > 0) {
            const ac = aircraft.length > 0 ? [...aircraft] : []
            const merged = [...companies, ...ac, ...shipPoints, ...portPoints, ...AIRPORT_MAJOR.map(ap => ({ ...ap, type: 'airport', size: 0.15 }))]
            g.pointsData(merged)
            const laneArcs = (data.lanes || []).map((l: any) => ({ ...l, color: '#00aaff' }))
            g.arcsData([...FALLBACK_ROUTES, ...laneArcs])
          }
        })
        .catch(() => {})
    }
    fetchMaritime()
    const maritimeInterval = setInterval(fetchMaritime, 60000)

    // ── RAW THREE.JS GLOBE (replaces globe.gl which doesn't render) ──
    const container = containerRef.current!
    const w = window.innerWidth
    const h = window.innerHeight

    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0x050510)

    const camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 1000)
    camera.position.set(0, 1.5, 3.5)

    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(w, h)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    container.appendChild(renderer.domElement)

    const controls = new OrbitControls(camera, renderer.domElement)
    controlsRef.current = controls
    controls.autoRotate = false
    controls.enableDamping = true
    controls.dampingFactor = 0.08
    controls.rotateSpeed = 0.3
    controls.zoomSpeed = 1.0
    controls.minDistance = 2.5
    controls.maxDistance = 15
    controls.enablePan = false
    controls.target.set(0, 0, 0)

    // Earth sphere
    const geometry = new THREE.SphereGeometry(1, 64, 64)
    const textureLoader = new THREE.TextureLoader()
    const material = new THREE.MeshStandardMaterial({ map: textureLoader.load(BLUE_MARBLE) })
    const earth = new THREE.Mesh(geometry, material)
    scene.add(earth)

    // Stars background
    const starGeo = new THREE.BufferGeometry()
    const starPos = new Float32Array(3000 * 3)
    for (let i = 0; i < 3000 * 3; i++) starPos[i] = (Math.random() - 0.5) * 500
    starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3))
    const starMat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.15 })
    const stars = new THREE.Points(starGeo, starMat)
    scene.add(stars)

    // Lighting
    const light = new THREE.DirectionalLight(0xffffff, 1.2)
    light.position.set(5, 10, 7)
    scene.add(light)
    scene.add(new THREE.AmbientLight(0x222244, 0.5))

    // Atmosphere glow
    const glowGeo = new THREE.SphereGeometry(1.02, 32, 32)
    const glowMat = new THREE.MeshBasicMaterial({ color: 0x4488ff, transparent: true, opacity: 0.08 })
    const glow = new THREE.Mesh(glowGeo, glowMat)
    scene.add(glow)

    // Globe data layer: actual Three.js rendering for points and arcs
    const EARTH_RADIUS = 1
    const pointsStore: any[] = []
    let pointsMesh: THREE.Points | null = null
    let arcLineObjects: THREE.Line[] = []
    let spriteMeshes: THREE.Sprite[] = []

    const latLngToPos = (lat: number, lng: number, alt: number = 0) => {
      const phi = (90 - lat) * Math.PI / 180
      const theta = (lng + 180) * Math.PI / 180
      const r = EARTH_RADIUS + alt
      return new THREE.Vector3(
        -r * Math.sin(phi) * Math.cos(theta),
        r * Math.cos(phi),
        r * Math.sin(phi) * Math.sin(theta)
      )
    }

    const hexToRGB = (hex: string) => {
      const h = hex.replace('#', '')
      return [parseInt(h.substring(0,2),16)/255, parseInt(h.substring(2,4),16)/255, parseInt(h.substring(4,6),16)/255]
    }

    const rebuildPoints = () => {
      // Remove old sprites
      for (const s of spriteMeshes) { scene.remove(s) }
      spriteMeshes = []
      // Remove old points mesh
      if (pointsMesh) { scene.remove(pointsMesh); pointsMesh.geometry.dispose(); (pointsMesh.material as THREE.Material).dispose(); pointsMesh = null }
      if (pointsStore.length === 0) return

      const positions = new Float32Array(pointsStore.length * 3)
      const colors = new Float32Array(pointsStore.length * 3)
      const sizes = new Float32Array(pointsStore.length)
      const colorFn = (globeRef.current as any)?._pointColor || (() => '#00ccff')
      const altFn = (globeRef.current as any)?._pointAltitude || ((d: any) => d.size || 0.1)
      // Only show sprites for major companies (top 500), rest as dots
      const spriteCount = Math.min(pointsStore.length, 500)
      for (let i = 0; i < pointsStore.length; i++) {
        const d = pointsStore[i]
        const alt = altFn(d)
        const pos = latLngToPos(d.lat, d.lng, alt)
        positions[i * 3] = pos.x; positions[i * 3 + 1] = pos.y; positions[i * 3 + 2] = pos.z
        const [r, g, b] = hexToRGB(colorFn(d))
        colors[i * 3] = r; colors[i * 3 + 1] = g; colors[i * 3 + 2] = b
        sizes[i] = Math.max(0.04, Math.min(0.2, (d.marketCap || 50) / 1000))
        // Create cat sprite for major companies
        if (i < spriteCount && d.ticker) {
          const c = document.createElement('canvas')
          c.width = 64; c.height = 64
          const cx = c.getContext('2d')!
          cx.font = '40px serif'; cx.textAlign = 'center'; cx.textBaseline = 'middle'
          cx.fillText(CAT_BY_INDUSTRY[d.industry] || '🐱', 32, 34)
          const tex = new THREE.CanvasTexture(c)
          const spriteMat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.9 })
          const sprite = new THREE.Sprite(spriteMat)
          sprite.position.copy(pos)
          sprite.scale.set(sizes[i] * 2, sizes[i] * 2, 1)
          sprite.userData = d
          scene.add(sprite)
          spriteMeshes.push(sprite)
          // Price glow for companies with significant moves
          const chg = priceMapRef.current[d.ticker]
          if (chg != null && Math.abs(chg) > 0.3) {
            const gc = document.createElement('canvas')
            gc.width = 128; gc.height = 128
            const gcx = gc.getContext('2d')!
            const grad = gcx.createRadialGradient(64, 64, 0, 64, 64, 64)
            const isGreen = chg > 0
            grad.addColorStop(0, isGreen ? 'rgba(0,255,136,0.5)' : 'rgba(255,68,68,0.5)')
            grad.addColorStop(0.3, isGreen ? 'rgba(0,255,136,0.2)' : 'rgba(255,68,68,0.2)')
            grad.addColorStop(1, 'rgba(0,0,0,0)')
            gcx.fillStyle = grad; gcx.fillRect(0, 0, 128, 128)
            const glowTex = new THREE.CanvasTexture(gc)
            const glowMat = new THREE.SpriteMaterial({ map: glowTex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.6 })
            const glow = new THREE.Sprite(glowMat)
            glow.position.copy(pos)
            glow.scale.set(sizes[i] * 5, sizes[i] * 5, 1)
            glow.userData = { _isGlow: true, _baseScale: sizes[i] * 5 }
            scene.add(glow)
            spriteMeshes.push(glow)
          }
        }
      }
      // Background dots for all companies
      const geo = new THREE.BufferGeometry()
      geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
      geo.setAttribute('color', new THREE.BufferAttribute(colors, 3))
      const mat = new THREE.PointsMaterial({
        size: 0.03, vertexColors: true, transparent: true, opacity: 0.6,
        sizeAttenuation: true,
      })
      pointsMesh = new THREE.Points(geo, mat)
      scene.add(pointsMesh)
    }

    globeRef.current = {
      renderer, scene, camera, controls, earth,
      _pointColor: null as any,
      _pointAltitude: null as any,
      pointsData: (d?: any[]) => {
        if (d === undefined) return pointsStore
        pointsStore.length = 0; pointsStore.push(...d)
        rebuildPoints()
        return globeRef.current
      },
      arcsData: (d?: any[]) => {
        if (d === undefined) return []
        for (const l of arcLineObjects) { scene.remove(l); l.geometry.dispose(); (l.material as THREE.Material).dispose() }
        arcLineObjects = []
        for (const arc of d) {
          const from = latLngToPos(arc.startLat, arc.startLng, 0.01)
          const to = latLngToPos(arc.endLat, arc.endLng, 0.01)
          const dist = from.distanceTo(to)
          const height = 0.08 + Math.min(0.5, dist * 0.35)
          const mid = new THREE.Vector3().addVectors(from, to).multiplyScalar(0.5).normalize().multiplyScalar(1 + height)
          const segments = Math.max(12, Math.min(48, Math.round(dist * 25)))
          const positions: number[] = []
          for (let t = 0; t <= segments; t++) {
            const f = t / segments
            const p = new THREE.Vector3().copy(from).multiplyScalar((1-f)*(1-f)).add(mid.clone().multiplyScalar(2*f*(1-f))).add(to.clone().multiplyScalar(f*f))
            positions.push(p.x, p.y, p.z)
          }
          const geo = new THREE.BufferGeometry()
          geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(positions), 3))
          const c = new THREE.Color(arc.color || '#00ff88')
          const mat = new THREE.LineBasicMaterial({ color: c, transparent: true, opacity: 0.3 })
          const line = new THREE.Line(geo, mat)
          scene.add(line)
          arcLineObjects.push(line)
        }
        return globeRef.current
      },
      pointColor: (fn?: any) => {
        if (!fn) return (globeRef.current as any)._pointColor
        ;(globeRef.current as any)._pointColor = fn
        if (pointsStore.length > 0) rebuildPoints()
        return globeRef.current
      },
      pointAltitude: (fn?: any) => {
        if (!fn) return (globeRef.current as any)._pointAltitude
        ;(globeRef.current as any)._pointAltitude = fn
        if (pointsStore.length > 0) rebuildPoints()
        return globeRef.current
      },
      pointLabel: () => globeRef.current,
      pointRadius: () => globeRef.current,
      pointResolution: () => globeRef.current,
      pointsMerge: () => globeRef.current,
      globeImageUrl: (url: string) => {
        const tex = new THREE.TextureLoader().load(url)
        earth.material.map = tex
        earth.material.needsUpdate = true
        return globeRef.current
      },
    } as any

    // Resize handler
    const resize = () => {
      const w2 = window.innerWidth, h2 = window.innerHeight
      camera.aspect = w2 / h2
      camera.updateProjectionMatrix()
      renderer.setSize(w2, h2)
    }
    window.addEventListener('resize', resize)

    // Click handling — raycaster for company/point selection
    const raycaster = new THREE.Raycaster()
    raycaster.params.Points.threshold = 0.1
    const mouse = new THREE.Vector2()
    const clickHandler = (e: MouseEvent) => {
      // Ignore clicks on UI elements
      if ((e.target as HTMLElement)?.closest('.globe-overlay')) return
      mouse.x = (e.clientX / window.innerWidth) * 2 - 1
      mouse.y = -(e.clientY / window.innerHeight) * 2 + 1
      raycaster.setFromCamera(mouse, camera)
      const hits = raycaster.intersectObjects(scene.children, true)
      if (hits.length > 0) {
        // Find the closest sprite to the hit point
        const hit = hits[0].point
        let closestDist = Infinity
        let closestCompany: any = null
        for (const s of spriteMeshes) {
          if (s.userData?.ticker) {
            const d = hit.distanceToSquared(s.position)
            if (d < closestDist) { closestDist = d; closestCompany = s.userData }
          }
        }
        if (closestCompany && closestDist < 0.05) {
          selectCompany(closestCompany)
        }
      }
    }
    const canvas = containerRef.current!.querySelector('canvas')
    if (canvas) canvas.addEventListener('click', clickHandler)

    // Render loop
    const animate = () => {
      if (controlsRef.current) controlsRef.current.update()
      const camDist = camera.position.length()
      const now = Date.now()
      for (const s of spriteMeshes) {
        if (s.userData?._isGlow) {
          const pulse = 1 + 0.12 * Math.sin(now * 0.003 + (s.id || 0))
          s.scale.set(s.userData._baseScale * pulse, s.userData._baseScale * pulse, 1)
          const mat = s.material as THREE.SpriteMaterial
          mat.opacity = 0.4 + 0.2 * Math.sin(now * 0.004 + (s.id || 0) * 0.5)
        } else {
          const base = (s.userData?.marketCap || 50) / 500
          const scale = Math.max(0.1, Math.min(0.5, base * (camDist / 4)))
          s.scale.set(scale, scale, 1)
        }
      }
      if (pointsMesh) {
        const mat = pointsMesh.material as THREE.PointsMaterial
        mat.size = Math.max(0.01, 0.04 * (camDist / 4))
      }
      renderer.render(scene, camera)
      animationRef.current = requestAnimationFrame(animate)
    }
    animationRef.current = requestAnimationFrame(animate)

    return () => {
      clearInterval(acInterval)
      clearInterval(maritimeInterval)
      window.removeEventListener('resize', resize)
      if (canvas) canvas.removeEventListener('click', clickHandler)
      cancelAnimationFrame(animationRef.current)
      for (const l of arcLineObjects) { scene.remove(l); l.geometry.dispose(); (l.material as THREE.Material).dispose() }
      arcLineObjects = []
      const hm = (globeRef.current as any)?._heatmapMesh
      if (hm) { scene.remove(hm); hm.geometry.dispose(); hm.material.dispose() }
      const ufm = (globeRef.current as any)?._ufoHeatmapMesh
      if (ufm) { scene.remove(ufm); ufm.geometry.dispose(); ufm.material.dispose() }
      const cm = (globeRef.current as any)?._conspiracyMesh
      if (cm) { scene.remove(cm); cm.geometry.dispose(); cm.material.dispose() }
      const rm = (globeRef.current as any)?._revenueMesh
      if (rm) { scene.remove(rm); rm.geometry.dispose(); rm.material.dispose() }
      const tm = (globeRef.current as any)?._troopMesh
      if (tm) { scene.remove(tm); tm.geometry.dispose(); tm.material.dispose() }
      if (container.contains(renderer.domElement)) container.removeChild(renderer.domElement)
      renderer.dispose()
      geometry.dispose()
      material.dispose()
      glowGeo.dispose()
      glowMat.dispose()
      starGeo.dispose()
      starMat.dispose()
      globeRef.current = null
    }
  }, [])

  // Search filter: update globe points when search changes
  useEffect(() => {
    const g = globeRef.current
    if (!g || companies.length === 0) return
    const q = search.toLowerCase().trim()
    const base = companies.filter((c: any) =>
      !q || (c.ticker && c.ticker.toLowerCase().includes(q)) || (c.name && c.name.toLowerCase().includes(q))
    )
    const merged = [...base, ...aircraft, ...AIRPORT_MAJOR.map(ap => ({ ...ap, type: 'airport', size: 0.15 }))]
    g.pointsData(merged)
    // Highlight searched points by raising them
    g.pointAltitude((d: any) =>
      q && d.ticker && d.ticker.toLowerCase().includes(q) ? 0.5 : d.size || 0.1
    )
    g.pointColor((d: any) => {
      if (q && d.ticker && d.ticker.toLowerCase().includes(q)) return '#ffcc00'
      const chg = priceMapRef.current[d?.ticker]
      if (chg != null) return chg > 0.5 ? '#00ff88' : chg < -0.5 ? '#ff4444' : '#ffcc00'
      return '#00ccff'
    })
  }, [search, companies])

  // Random cat appearances on globe every 30s
  const catPopupRef = useRef<any>(null)
  const catFactsRef = useRef([
    'Cats spend 70% of their life sleeping — the other 30% is judging your portfolio.',
    'A cat\'s purr vibrates at 20-140 Hz — the ideal frequency for trading calm.',
    'Ancient Egyptians worshipped cats. Today, cats worship your margin balance.',
    'Cats can\'t taste sweetness, but they can taste your FOMO from across the room.',
    'Cats have 32 muscles in each ear — perfect for overhearing alpha.',
    'Cats always land on their feet. Your portfolio should too. Diversify.',
    'In ancient Japan, cats brought good fortune. Clearly, insider info.',
    'Cats can jump 6x their body length. Your stop losses should be just as agile.',
    'A cat\'s whiskers help navigate tight spaces. Much like tight spreads.',
    'Cats meow only to communicate with humans — they know you need advice.',
  ])
  useEffect(() => {
    if (!layers.cats) return
    const catEmojis = ['🐱', '😸', '😹', '😻', '😺']
    const popCat = () => {
      const g = globeRef.current
      if (!g || !layers.cats) return
      if (catPopupRef.current) {
        const cur = g.pointsData() || []
        g.pointsData(cur.filter((d: any) => d !== catPopupRef.current))
        catPopupRef.current = null
      }
      const lat = (Math.random() - 0.5) * 140
      const lng = (Math.random() - 0.5) * 360
      const e = catEmojis[Math.floor(Math.random() * catEmojis.length)]
      const f = catFactsRef.current[Math.floor(Math.random() * catFactsRef.current.length)]
      catPopupRef.current = { lat, lng, name: `🐱 ${f}`, type: 'cat-popup', size: 0.8, emoji: e, fact: f }
      const cur = g.pointsData() || []
      g.pointsData([...cur, catPopupRef.current])
    }
    popCat()
    const id = setInterval(popCat, 30000)
    return () => { clearInterval(id); if (catPopupRef.current && globeRef.current) {
      const cur = globeRef.current.pointsData() || []
      globeRef.current.pointsData(cur.filter((d: any) => d !== catPopupRef.current))
    }}
  }, [layers.cats])

  // Live prices: fetch batch prices and color globe points by change
  const priceMapRef = useRef<Record<string, number>>({})
  useEffect(() => {
    if (companies.length === 0) return
    const tickers = companies.slice(0, 200).map((c: any) => c.ticker).join(',')
    const fetchPrices = () => {
      fetch(`/api/v1/datavore/map/batch-prices?tickers=${tickers}`)
        .then(r => r.ok ? r.json() : null)
        .then(data => {
          if (!data?.prices) return
          priceMapRef.current = {}
          for (const [t, p] of Object.entries(data.prices)) {
            const change = (p as any).change_pct ?? 0
            if (change !== 0) priceMapRef.current[t] = change
          }
          const g = globeRef.current
          if (!g) return
          g.pointColor((d: any) => {
            const gRef = globeRef.current as any
            if (gRef?._naval && d.isMilitary && d.type === 'ship') return '#ff4444'
            if (gRef?._milTransponders && d.isMilitary && d.type === 'aircraft') return '#ff6644'
            if (!d || !d.ticker) return '#00ccff'
            const chg = priceMapRef.current[d.ticker]
            if (chg == null) return '#00ccff'
            return chg > 0.5 ? '#00ff88' : chg < -0.5 ? '#ff4444' : '#ffcc00'
          })
        })
        .catch(() => {})
    }
    fetchPrices()
    const interval = setInterval(fetchPrices, 60000)
    return () => clearInterval(interval)
  }, [companies.length > 0])

  const fetchPriceHistory = useCallback(async (ticker: string, period: string = '1y') => {
    try {
      const headers: Record<string, string> = localStorage.getItem('miau_token')
        ? { Authorization: `Bearer ${localStorage.getItem('miau_token')}` } : {}
      const res = await fetch(`/api/v1/market/historical/${ticker}?period=${period}`, { headers })
      if (res.ok) {
        const d = await res.json()
        const prices = d.records?.map((r: any) => r.close).filter((p: any) => p != null) || []
        if (prices.length > 1) { setPriceHistory(prices); return }
      }
    } catch {}
    const base = 100 + Math.random() * 200
    const days = period === '1m' ? 22 : period === '3m' ? 66 : period === '6m' ? 132 : 252
    let p = base; const prices: number[] = []
    for (let i = 0; i < days; i++) { p += (Math.random() - 0.48) * base * 0.02; prices.push(p) }
    setPriceHistory(prices)
  }, [])

  const fetchNews = useCallback(async (ticker: string) => {
    try {
      const headers: Record<string, string> = localStorage.getItem('miau_token')
        ? { Authorization: `Bearer ${localStorage.getItem('miau_token')}` } : {}
      const res = await fetch(`/api/v1/news/company/${ticker}?limit=10`, { headers })
      if (res.ok) { setCompanyNews(await res.json()) }
    } catch {}
  }, [])

  const fetchFundamentals = useCallback(async (ticker: string) => {
    try {
      const token = localStorage.getItem('miau_token')
      const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}
      const res = await fetch(`/api/v1/fundamentals/${ticker}`, { headers, credentials: 'include' })
      if (res.ok) { setFundamentals(await res.json()) }
    } catch {}
  }, [])

  const selectCompany = useCallback((co: any) => {
    setSelectedCompany(co)
    setDetailTab('info')
    fetchPriceHistory(co.ticker, '1y')
    fetchNews(co.ticker)
    fetchFundamentals(co.ticker)
  }, [fetchPriceHistory, fetchNews, fetchFundamentals])

  const layerList: { key: keyof LayerState; label: string; icon: string }[] = [
    { key: 'companies', label: 'Companies', icon: '🏢' },
    { key: 'routes', label: 'Trade Routes', icon: '🛤️' },
    { key: 'cargo', label: 'Cargo Ships', icon: '🚢' },
    { key: 'satellites', label: 'Satellites', icon: '🛰️' },
    { key: 'satCover', label: 'Sat Coverage', icon: '🔥' },
    { key: 'mining', label: 'Mining', icon: '⛏️' },
    { key: 'bases', label: 'Military Bases', icon: '🪖' },
    { key: 'cats', label: 'Cats', icon: '🐱' },
    { key: 'aliens', label: aliensUnlocked ? '👽 Aliens' : '🔒 Aliens', icon: aliensUnlocked ? '👽' : '🔒' },
    { key: 'alienCover', label: 'UFO Heatmap', icon: '🛸' },
    { key: 'catPatrol', label: 'Cats vs Aliens', icon: '🐱👽' },
    { key: 'conspiracyCover', label: 'Conspiracy', icon: '🕵️' },
    { key: 'revenueCover', label: 'Revenue', icon: '💰' },
    { key: 'maArcs', label: 'M&A', icon: '🤝' },
    { key: 'naval', label: 'Naval', icon: '⚓' },
    { key: 'milAir', label: 'Mil Air', icon: '🪖' },
    { key: 'troopCover', label: 'Troops', icon: '🗺️' },
    { key: 'night', label: 'Night Mode', icon: '🌙' },
    { key: 'terrain', label: 'Terrain', icon: '⛰️' },
  ]

  return (
    <>
      {createPortal(
        <div ref={containerRef} style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', zIndex: 9000, background: '#050510' }} />,
        document.body
      )}

      {/* Toolbar */}
      {active && createPortal(
        <div className="fixed top-0 left-0 right-0 z-[100000] bg-black/80 border-b border-green-500/30 flex items-center justify-between px-3 py-1.5">
           <div className="flex items-center gap-3">
             <button onClick={() => onClose?.()}
               className="px-2 py-1 text-xs text-white bg-gray-800 border border-gray-600 rounded font-mono hover:bg-gray-700">← Back</button>
             <input type="text" value={search}
               onChange={(e) => setSearch(e.target.value)}
               placeholder="🔍 Search company..."
               className="w-28 md:w-40 px-2 py-1 bg-gray-900 border border-gray-700 rounded text-xs text-white font-mono placeholder:text-gray-600 outline-none" />
              <span className="text-[10px] text-gray-500 font-mono">🌍</span>
              <div className="flex items-center gap-0.5">
                {Object.keys(CONTINENT_FILES).map(c => (
                  <button key={c} onClick={() => setContinent(c)}
                    className={`px-1.5 py-0.5 text-[9px] rounded font-mono border transition-colors ${
                      continent === c ? 'bg-green-900/50 text-green-300 border-green-700/50' : 'bg-gray-900 text-gray-500 border-gray-700'
                    }`}>
                    {c === 'north_america' ? '🇺🇸' : c === 'europe' ? '🇪🇺' : c === 'asia' ? '🇯🇵' : c === 'south_america' ? '🇧🇷' : c === 'africa' ? '🇿🇦' : c === 'oceania' ? '🇦🇺' : '🌍'}
                  </button>
                ))}
              </div>
            <div className="flex items-center gap-1 ml-2">
              {layerList.map(l => (
                <button key={l.key} onClick={() => toggleLayer(l.key)}
                  className={`px-1.5 py-0.5 text-[9px] rounded font-mono border transition-colors ${
                    layers[l.key] ? 'bg-green-900/50 text-green-300 border-green-700/50' : 'bg-gray-900 text-gray-600 border-gray-700'
                  }`}
                  title={l.label}>
                  {l.icon}
                </button>
              ))}
            </div>
          </div>
           <div className="flex items-center gap-3 text-[9px] font-mono">
             {search && <span className="text-yellow-400">{companies.filter((c:any) => (c.ticker||'').toLowerCase().includes(search.toLowerCase()) || (c.name||'').toLowerCase().includes(search.toLowerCase())).length} results</span>}
             <span className="text-green-400">{globeState.fps} FPS</span>
            <span className="text-gray-500">|</span>
            <span className="text-gray-400">{globeState.points || companies.length} pts</span>
            <span className="text-gray-500">|</span>
            <span className="text-gray-400">{Object.values(layers).filter(Boolean).length} layers</span>
            {cameraMoving && <span className="text-yellow-400 animate-pulse">📍</span>}
          </div>
        </div>,
        document.body
      )}

      {/* Layer legend */}
      {active && layers.cats && createPortal(
        <div className="fixed right-3 top-12 z-[100000] text-[9px] font-mono text-gray-500 pointer-events-none text-right">
          {CAT_LOCATIONS.map((c, i) => (
            <div key={i} className="opacity-60 hover:opacity-100 transition-opacity">
              {c.emoji} {c.name}
            </div>
          ))}
        </div>,
        document.body
      )}
      {active && layers.mining && createPortal(
        <div className="fixed right-3 top-48 z-[100000] text-[9px] font-mono text-gray-500 pointer-events-none">
          <div className="font-bold text-green-400 mb-1">⛏️ Mining Legend</div>
          <div className="flex flex-col gap-0.5">
            <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-[#ffcc00]"></span>Gold</div>
            <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-[#cd7f32]"></span>Copper</div>
            <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-[#8b7355]"></span>Iron</div>
            <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-[#1a1a1a] border border-gray-600"></span>Oil</div>
            <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-[#22dd88]"></span>Renewable</div>
          </div>
        </div>,
        document.body
      )}

      {/* Company Detail Panel */}
      {selectedCompany && createPortal(
        <div className="fixed left-2 bottom-2 w-[650px] max-w-[95vw] bg-black/95 border border-green-500/40 rounded-lg p-4 text-sm font-mono z-[100001] shadow-2xl shadow-black/80 max-h-[85vh] overflow-y-auto" style={{ pointerEvents: 'auto' }}>
          <button onClick={() => { setSelectedCompany(null); setPriceHistory([]); setCompanyNews([]); setFundamentals(null); setDetailTab('info') }}
            className="absolute top-3 right-3 text-gray-500 hover:text-white text-lg z-10">✕</button>
          <div className="flex gap-1 mb-3 border-b border-gray-800 pb-2 overflow-x-auto">
            {(['info','chart','stats','news'] as const).map(tab => (
              <button key={tab} onClick={() => setDetailTab(tab)}
                className={`px-3 py-1 text-xs font-mono rounded-t whitespace-nowrap ${detailTab === tab ? 'bg-green-900 text-green-300 border border-green-700 border-b-0' : 'text-gray-500 hover:text-gray-300'}`}>
                {tab === 'info' ? '📊 Info' : tab === 'chart' ? '📈 Chart' : tab === 'stats' ? '📋 Stats' : `📰 News${companyNews.length > 0 ? ` (${companyNews.length})` : ''}`}
              </button>
            ))}
          </div>
          {detailTab === 'info' && (
            <>
              <div className="text-green-400 text-sm font-bold mb-2">
                {selectedCompany.type === 'satellite' ? '🛰️' : selectedCompany.type === 'ufo' ? '👽' : COMPANY_ICONS[selectedCompany.industry] || '🏢'} {selectedCompany.name}
                <span className="text-gray-500 ml-2 text-[10px]">{selectedCompany.ticker}</span>
              </div>
              <div className="grid grid-cols-2 gap-x-6 gap-y-1.5 mb-2 text-xs">
                {selectedCompany.type !== 'satellite' && selectedCompany.type !== 'ufo' && <><span className="text-gray-500">Industry</span><span className="text-white">{selectedCompany.industry}</span></>}
                {selectedCompany.type !== 'satellite' && selectedCompany.type !== 'ufo' && selectedCompany.country && <><span className="text-gray-500">Country</span><span className="text-white">{selectedCompany.country}</span></>}
                {selectedCompany.marketCap > 0 && <><span className="text-gray-500">Market Cap</span><span className="text-green-400">${selectedCompany.marketCap}B</span></>}
                <span className="text-gray-500">Location</span><span className="text-gray-400">{selectedCompany.lat?.toFixed(2)}°, {selectedCompany.lng?.toFixed(2)}°</span>
                {selectedCompany.owner && <><span className="text-gray-500">Owner</span><span className="text-white">{selectedCompany.owner}</span></>}
                {selectedCompany.production && <><span className="text-gray-500">Production</span><span className="text-cyan-400">{selectedCompany.production}</span></>}
              </div>
              {selectedCompany.desc && <div className="text-[10px] text-gray-400 italic mt-1">{selectedCompany.desc}</div>}
              {selectedCompany.type === 'mine' && <div className="text-[10px] text-gray-600 mt-1.5">🐱 The cat rates this mine: {selectedCompany.production?.includes('M') ? '🐱🐱🐱🐱🐱' : selectedCompany.production?.includes('k') ? '🐱🐱🐱' : '🐱🐱🐱🐱'}</div>}
              {selectedCompany.type === 'base' && (
                <>
                  <div className="text-[10px] text-gray-500 mt-1.5">{selectedCompany.industry} · {selectedCompany.ticker}</div>
                  <div className="text-[10px] text-gray-600">👥 Personnel: {(selectedCompany.marketCap || 0).toLocaleString()}</div>
                  <div className="text-[10px] text-gray-600">🐱 Cat General: {['Cadet Cat', 'Second Lieutenant Paws', 'Captain Whiskers', 'Major Mittens', 'Colonel Claw', 'General Meow', 'Supreme Cat Commander'][Math.min(Math.floor((selectedCompany.marketCap || 0) / 10000), 6)]}</div>
                </>
              )}
              {selectedCompany.type === 'satellite' && (
                <div className="text-[10px] text-gray-600 mt-1.5 space-y-0.5">
                  <div>🛰️ Operator: {selectedCompany.country || selectedCompany.operator || 'Unknown'}</div>
                  <div>📡 Orbit: {selectedCompany.orbit || 'LEO'} · Alt: {selectedCompany.altitude_km || '~550'}km</div>
                  <div>🚀 Launch: {selectedCompany.launch || 'Unknown'}</div>
                  <div className="text-gray-500 mt-1">{selectedCompany.isISS ? '🐱 The cat reports the ISS crew is doing important science. The cat is supervising.' : ['🐱 This satellite does not respond to laser pointers.', '🐱 The cat has no comment on this satellite.', '🐱 The cat enjoys watching Starlink trains at dusk.', '🐱 This satellite is not a cat toy. The cat disagrees.', '🐱 Satellites would be better with cat ears.'] [Math.floor(Math.random() * 5)]}</div>
                </div>
              )}
              {selectedCompany.type === 'ufo' && (
                <div className="text-[10px] text-gray-600 mt-1.5 space-y-0.5">
                  <div>👽 Shape: {selectedCompany.shape || 'Unknown'}</div>
                  <div>📅 Date: {selectedCompany.date || 'Unknown'}</div>
                  <div>⏱️ Duration: {selectedCompany.duration || 'Unknown'}</div>
                  <div>📋 Description: {selectedCompany.desc || 'No description'}</div>
                  <div className="text-gray-500 mt-1">{['🐱 The cat confirms: not a cat.', '🐱 The cat has seen things... and judged them.', '🐱 This is why cats have 9 lives. Aliens.', '🐱 The cat declined to comment. Again.', '🐱 Cats and aliens share one thing: mysterious landing.'][Math.floor(Math.random() * 5)]}</div>
                </div>
              )}
            </>
          )}
          {detailTab === 'chart' && (
            <div>
              <div className="text-green-400 text-xs font-bold mb-2">📈 {selectedCompany.ticker} Price</div>
              {priceHistory.length > 1 ? (
                <div>
                  <svg viewBox={`0 0 ${priceHistory.length} 100`} className="w-full h-20" preserveAspectRatio="none">
                    <defs><linearGradient id="gc" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#00ff88" stopOpacity="0.3"/><stop offset="100%" stopColor="#00ff88" stopOpacity="0.02"/></linearGradient></defs>
                    {(() => { const mn = Math.min(...priceHistory), mx = Math.max(...priceHistory), r = mx - mn || 1; const pts = priceHistory.map((p,i) => `${i},${100-((p-mn)/r)*80}`).join(' '); return <><polyline fill="url(#gc)" points={`0,100 ${pts} ${priceHistory.length-1},100`}/><polyline fill="none" stroke="#00ff88" strokeWidth="1.5" points={pts}/></> })()}
                  </svg>
                  <div className="flex justify-between text-[9px] text-gray-600 mt-0.5">
                    <span>${Math.min(...priceHistory).toFixed(2)}</span>
                    <span className="text-green-400">${priceHistory[priceHistory.length-1].toFixed(2)}</span>
                    <span>${Math.max(...priceHistory).toFixed(2)}</span>
                  </div>
                </div>
              ) : <div className="text-gray-600 text-xs py-6 text-center">Loading...</div>}
            </div>
          )}
          {detailTab === 'stats' && fundamentals && (
            <div className="space-y-2">
              <div className="text-gray-500 text-xs mb-1">💰 Valuation</div>
              <div className="grid grid-cols-2 gap-x-6 gap-y-1 text-xs">
                {[['P/E', fundamentals.trailingPE], ['Forward P/E', fundamentals.forwardPE], ['PEG', fundamentals.pegRatio], ['P/B', fundamentals.priceToBook], ['P/S', fundamentals.priceToSales], ['EV/EBITDA', fundamentals.enterpriseToEbitda], ['Beta', fundamentals.beta], ['Div Yield', fundamentals.dividendYield != null ? (fundamentals.dividendYield*100).toFixed(2)+'%' : null]].filter(([_,v]) => v != null).map(([l,v]:any) => <><span className="text-gray-500">{l}</span><span className="text-white">{typeof v === 'number' ? v.toFixed(2) : v}</span></>)}
              </div>
            </div>
          )}
          {detailTab === 'stats' && !fundamentals && <div className="text-gray-600 text-xs py-6 text-center">Loading...</div>}
          {detailTab === 'news' && (
            companyNews.length > 0 ? (
              <div className="space-y-2">
                {companyNews.slice(0, 8).map((item: any, i: number) => (
                  <div key={i} className="pb-2 border-b border-gray-800 last:border-0">
                    <div className="text-white text-xs leading-tight mb-0.5">{item.title}</div>
                    <div className="flex items-center justify-between text-[10px] text-gray-600">
                      <span>{item.publisher || ''}</span>
                      {item.link && <a href={item.link} target="_blank" className="text-green-400 hover:underline">Read →</a>}
                    </div>
                  </div>
                ))}
              </div>
            ) : <div className="text-gray-600 text-xs py-6 text-center">No news</div>
          )}
        </div>,
        document.body
      )}
    </>
  )
}
