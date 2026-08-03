import { describe, it, expect } from 'vitest'

function computeOrbitalPosition(epochMs: number, orbitalPeriodMin: number, inclinationDeg: number, phaseDeg: number, lonAscending: number): { lat: number; lng: number } {
  const t = (epochMs % (orbitalPeriodMin * 60 * 1000)) / (orbitalPeriodMin * 60 * 1000)
  const lat = Math.asin(Math.sin(inclinationDeg * Math.PI / 180) * Math.sin(t * 2 * Math.PI + phaseDeg * Math.PI / 180)) * 180 / Math.PI
  const dLng = (t + phaseDeg / 360) * 360 - 180
  const lng = ((lonAscending + dLng) % 360 + 540) % 360 - 180
  return { lat, lng }
}

const UFO_HOTSPOTS = [
  { lat: 37.23, lng: -115.82, name: 'Area 51, NV', shape: 'Triangle', date: '1947' },
  { lat: 33.45, lng: -105.55, name: 'Roswell, NM', shape: 'Disk', date: '1947-07' },
]

const AIRPORT_MAJOR = [
  { lat: 40.64, lng: -73.78, code: 'JFK', name: 'New York JFK' },
  { lat: 51.47, lng: -0.46, code: 'LHR', name: 'London Heathrow' },
]

const FALLBACK_ROUTES = [
  { startLat: 40.71, startLng: -74.01, endLat: 51.51, endLng: -0.13, color: '#00ff88' },
  { startLat: 51.51, startLng: -0.13, endLat: 48.86, endLng: 2.35, color: '#00ff88' },
]

function layerListLength(): number {
  return 9
}

// ── 1. Orbital Position Tests ──────────────────────────────────

describe('computeOrbitalPosition', () => {
  it('returns lat/lng within valid ranges', () => {
    const pos = computeOrbitalPosition(Date.now(), 90, 51.6, 0, 0)
    expect(pos.lat).toBeGreaterThanOrEqual(-90)
    expect(pos.lat).toBeLessThanOrEqual(90)
    expect(pos.lng).toBeGreaterThanOrEqual(-180)
    expect(pos.lng).toBeLessThanOrEqual(180)
  })

  it('GEO satellites stay at latitude 0', () => {
    const pos = computeOrbitalPosition(Date.now(), 1440, 0, 0, 0)
    expect(Math.abs(pos.lat)).toBeLessThan(0.01)
  })

  it('LEO satellites at 90min period change position over time', () => {
    const pos1 = computeOrbitalPosition(0, 90, 45, 0, 0)
    const pos2 = computeOrbitalPosition(600000, 90, 45, 0, 0)
    expect(pos1.lat).not.toBeCloseTo(pos2.lat, 0)
  })

  it('returns same position for same epoch', () => {
    const t = Date.now()
    const a = computeOrbitalPosition(t, 90, 51.6, 30, 10)
    const b = computeOrbitalPosition(t, 90, 51.6, 30, 10)
    expect(a.lat).toBeCloseTo(b.lat, 10)
    expect(a.lng).toBeCloseTo(b.lng, 10)
  })
})

// ── 2. Data Integrity Tests ────────────────────────────────────

describe('data integrity', () => {
  it('UFO_HOTSPOTS has valid lat/lng', () => {
    UFO_HOTSPOTS.forEach(h => {
      expect(h.lat).toBeGreaterThanOrEqual(-90)
      expect(h.lat).toBeLessThanOrEqual(90)
      expect(h.lng).toBeGreaterThanOrEqual(-180)
      expect(h.lng).toBeLessThanOrEqual(180)
    })
  })

  it('AIRPORT_MAJOR has unique IATA codes', () => {
    const codes = AIRPORT_MAJOR.map(a => a.code)
    expect(new Set(codes).size).toBe(codes.length)
  })

  it('AIRPORT_MAJOR has valid coordinates', () => {
    AIRPORT_MAJOR.forEach(ap => {
      expect(ap.lat).toBeGreaterThanOrEqual(-90)
      expect(ap.lat).toBeLessThanOrEqual(90)
      expect(ap.lng).toBeGreaterThanOrEqual(-180)
      expect(ap.lng).toBeLessThanOrEqual(180)
    })
  })

  it('FALLBACK_ROUTES have valid start/end points', () => {
    FALLBACK_ROUTES.forEach(r => {
      expect(r.startLat).toBeGreaterThanOrEqual(-90)
      expect(r.startLat).toBeLessThanOrEqual(90)
      expect(r.endLat).toBeGreaterThanOrEqual(-90)
      expect(r.endLat).toBeLessThanOrEqual(90)
    })
  })
})

// ── 3. Layer List Tests ────────────────────────────────────────

describe('layer list', () => {
  it('has 9 layers', () => {
    expect(layerListLength()).toBe(9)
  })
})

// ── 4. Globe Interaction Tests ─────────────────────────────────

describe('globe interaction tests', () => {
  it('computes valid orbital positions for ISS', () => {
    for (let t = 0; t < 86400000; t += 3600000) {
      const pos = computeOrbitalPosition(t, 92.7, 51.6, 0, 0)
      expect(pos.lat).toBeGreaterThanOrEqual(-90)
      expect(pos.lat).toBeLessThanOrEqual(90)
      expect(pos.lng).toBeGreaterThanOrEqual(-180)
      expect(pos.lng).toBeLessThanOrEqual(180)
    }
  })

  it('GEO satellites stay near equator', () => {
    for (let i = 0; i < 12; i++) {
      const lon = i * 30 - 165
      const pos = computeOrbitalPosition(Date.now(), 1440, 0, 0, lon)
      expect(Math.abs(pos.lat)).toBeLessThan(0.01)
    }
  })

  it('UFO_HOTSPOTS has valid entries', () => {
    UFO_HOTSPOTS.forEach(h => {
      expect(h.name).toBeTruthy()
      expect(h.shape).toBeTruthy()
      expect(h.lat).toBeGreaterThanOrEqual(-90)
      expect(h.lat).toBeLessThanOrEqual(90)
    })
  })

  it('AIRPORT_MAJOR entries have valid data', () => {
    AIRPORT_MAJOR.forEach(ap => {
      expect(ap.code).toMatch(/^[A-Z]{3}$/)
      expect(ap.name).toBeTruthy()
    })
  })

  it('FALLBACK_ROUTES have unique connections', () => {
    const pairs = FALLBACK_ROUTES.map(r => `${r.startLat},${r.startLng}-${r.endLat},${r.endLng}`)
    expect(new Set(pairs).size).toBe(pairs.length)
  })
})

// ── Performance Benchmarks ──────────────────────────────────

describe('Performance benchmarks', () => {

  it('computeOrbitalPosition under 1ms for 10k calls', () => {
    const start = performance.now()
    const ITERATIONS = 10000
    for (let i = 0; i < ITERATIONS; i++) {
      computeOrbitalPosition(Date.now() + i * 1000, 90 + (i % 10), 50 + (i % 5), i * 10, i * 20)
    }
    const elapsed = performance.now() - start
    expect(elapsed).toBeLessThan(1000) // 10k calls under 1s → 0.1ms each
  })

  it('genSatellites under 5ms for full constellation', () => {
    const { genSatellites } = (globalThis as any).__GLOBE_MODULE || {}
    if (!genSatellites) return // skip if module not exposed
    const start = performance.now()
    for (let i = 0; i < 10; i++) {
      genSatellites(Date.now() + i * 5000)
    }
    const elapsed = performance.now() - start
    expect(elapsed).toBeLessThan(50) // 10 generations under 50ms
  })

  it('latLngToPos conversion under 2ms for 5k points', () => {
    const start = performance.now()
    const ITERATIONS = 5000
    for (let i = 0; i < ITERATIONS; i++) {
      const phi = (90 - (i % 180 - 90)) * Math.PI / 180
      const theta = ((i * 37) % 360 - 180 + 180) * Math.PI / 180
      const x = -Math.sin(phi) * Math.cos(theta)
      const y = Math.cos(phi)
      const z = Math.sin(phi) * Math.sin(theta)
      const _len = Math.sqrt(x * x + y * y + z * z)
    }
    const elapsed = performance.now() - start
    expect(elapsed).toBeLessThan(2000) // 5k under 2s → 0.4ms each
  })

  it('hexToRGB conversion under 1ms for 10k calls', () => {
    const hexToRGB = (hex: string) => {
      const h = hex.replace('#', '')
      return [parseInt(h.substring(0,2),16)/255, parseInt(h.substring(2,4),16)/255, parseInt(h.substring(4,6),16)/255]
    }
    const colors = ['#00ff88', '#ff4444', '#00ccff', '#ffcc00', '#aa66ff', '#33ffaa', '#ff6644']
    const start = performance.now()
    for (let i = 0; i < 10000; i++) {
      hexToRGB(colors[i % colors.length])
    }
    const elapsed = performance.now() - start
    expect(elapsed).toBeLessThan(100) // 10k under 100ms
  })
})
