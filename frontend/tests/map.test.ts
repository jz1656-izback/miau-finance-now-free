import { describe, it, expect } from 'vitest'

// ── distKm helper (extracted from WorldMap.tsx) ────────────────

function distKm(lat1: number, lng1: number, lat2: number, lng2: number): number {
  const R = 6371
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLng = (lng2 - lng1) * Math.PI / 180
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLng / 2) * Math.sin(dLng / 2)
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
}

// ── Continent filtering logic (extracted from WorldMap.tsx) ────

const CONTINENT_COUNTRIES: Record<string, string[]> = {
  all: [],
  north_america: ['US', 'CA', 'MX'],
  europe: ['GB', 'DE', 'FR', 'IT', 'ES', 'NL', 'CH', 'SE', 'DK', 'FI', 'NO', 'BE', 'AT', 'IE', 'PT'],
  asia: ['JP', 'CN', 'HK', 'SG', 'KR', 'IN', 'TW', 'TH', 'MY', 'ID', 'PH', 'VN', 'AE', 'SA', 'IL', 'QA', 'TR'],
  south_america: ['BR', 'AR', 'CL', 'CO', 'PE', 'UY', 'PY'],
  africa: ['ZA', 'NG', 'KE', 'EG', 'MA', 'DZ', 'TN', 'GH', 'SN', 'ET'],
  oceania: ['AU', 'NZ', 'PG', 'FJ'],
}

interface MapCompany {
  ticker: string
  name: string
  industry: string
  lat: number
  lng: number
  country: string
  marketCap: number
  price?: number
  change_pct?: number
}

function filterByContinent(companies: MapCompany[], continent: string): MapCompany[] {
  if (continent === 'all') return companies
  const allowed = CONTINENT_COUNTRIES[continent] || []
  return companies.filter(c => allowed.includes(c.country))
}

function filterBySearch(companies: MapCompany[], query: string): MapCompany[] {
  if (!query.trim()) return companies
  const q = query.toLowerCase()
  return companies.filter(c =>
    c.ticker.toLowerCase().includes(q) ||
    c.name.toLowerCase().includes(q) ||
    c.industry.toLowerCase().includes(q)
  )
}

function filterByViewport(
  companies: MapCompany[],
  bounds: { north: number; south: number; east: number; west: number } | null,
): MapCompany[] {
  if (!bounds) return companies
  return companies.filter(c =>
    c.lat <= bounds.north &&
    c.lat >= bounds.south &&
    c.lng <= bounds.east &&
    c.lng >= bounds.west
  )
}

// ── Marker creation logic ──────────────────────────────────────

const CAT_BY_INDUSTRY: Record<string, string> = {
  Tech: '😸', Semiconductors: '😼', Automotive: '🐱', Finance: '😺',
  Energy: '🙀', Healthcare: '😿', Pharma: '😽', Biotech: '😻',
  Consumer: '😻', Retail: '🐱', Food: '😸', Industrial: '🐱',
  Luxury: '😻', Entertainment: '😹', Media: '😹', Telecom: '😺',
  Aerospace: '🐱', Logistics: '🐱', Mining: '🙀', Chemicals: '😼',
  Insurance: '😺', 'Real Estate': '🐱', Hospitality: '😸', Airlines: '🐱',
  Conglomerate: '🐱', Forestry: '😸', Trading: '😼',
}

function createMarkerData(company: MapCompany): {
  emoji: string
  color: string
  size: number
} {
  const change = company.change_pct ?? 0
  const color = change > 0.5 ? '#0f8' : change < -0.5 ? '#f44' : '#0cf'
  const size = company.marketCap ? Math.min(24, Math.max(14, company.marketCap / 100)) : 18
  const emoji = CAT_BY_INDUSTRY[company.industry] || '🐱'
  return { emoji, color, size }
}

// ── 1. distKm ─────────────────────────────────────────────────

describe('distKm', () => {
  it('returns 0 for same point', () => {
    expect(distKm(40.712, -74.006, 40.712, -74.006)).toBeCloseTo(0, 1)
  })

  it('computes NY to London roughly 5570 km', () => {
    const d = distKm(40.712, -74.006, 51.507, -0.127)
    expect(d).toBeGreaterThan(5000)
    expect(d).toBeLessThan(6000)
  })

  it('computes Tokyo to Sydney roughly 7800 km', () => {
    const d = distKm(35.676, 139.650, -33.868, 151.209)
    expect(d).toBeGreaterThan(7000)
    expect(d).toBeLessThan(8500)
  })

  it('is symmetric', () => {
    const d1 = distKm(10, 20, 30, 40)
    const d2 = distKm(30, 40, 10, 20)
    expect(d1).toBeCloseTo(d2, 5)
  })
})

// ── 2. Continent filtering ────────────────────────────────────

describe('continent filtering', () => {
  const companies: MapCompany[] = [
    { ticker: 'AAPL', name: 'Apple', industry: 'Tech', lat: 37, lng: -122, country: 'US', marketCap: 3000 },
    { ticker: 'SAP', name: 'SAP SE', industry: 'Tech', lat: 49, lng: 8, country: 'DE', marketCap: 200 },
    { ticker: 'TM', name: 'Toyota', industry: 'Automotive', lat: 35, lng: 139, country: 'JP', marketCap: 250 },
    { ticker: 'B3', name: 'B3 SA', industry: 'Finance', lat: -23, lng: -46, country: 'BR', marketCap: 50 },
  ]

  it('returns all when continent is all', () => {
    expect(filterByContinent(companies, 'all')).toHaveLength(4)
  })

  it('filters to north_america', () => {
    const filtered = filterByContinent(companies, 'north_america')
    expect(filtered).toHaveLength(1)
    expect(filtered[0].ticker).toBe('AAPL')
  })

  it('filters to europe', () => {
    const filtered = filterByContinent(companies, 'europe')
    expect(filtered).toHaveLength(1)
    expect(filtered[0].ticker).toBe('SAP')
  })

  it('filters to asia', () => {
    const filtered = filterByContinent(companies, 'asia')
    expect(filtered).toHaveLength(1)
    expect(filtered[0].ticker).toBe('TM')
  })

  it('filters to south_america', () => {
    const filtered = filterByContinent(companies, 'south_america')
    expect(filtered).toHaveLength(1)
    expect(filtered[0].ticker).toBe('B3')
  })

  it('returns empty for unknown continent', () => {
    expect(filterByContinent(companies, 'antarctica')).toHaveLength(0)
  })
})

// ── 3. Company marker creation ────────────────────────────────

describe('company marker creation', () => {
  it('uses industry emoji', () => {
    const tech: MapCompany = { ticker: 'AAPL', name: 'Apple', industry: 'Tech', lat: 37, lng: -122, country: 'US', marketCap: 3000, change_pct: 1.0 }
    const energy: MapCompany = { ticker: 'XOM', name: 'Exxon', industry: 'Energy', lat: 30, lng: -95, country: 'US', marketCap: 500, change_pct: -1.0 }
    expect(createMarkerData(tech).emoji).toBe('😸')
    expect(createMarkerData(energy).emoji).toBe('🙀')
  })

  it('falls back to cat emoji for unknown industry', () => {
    const c: MapCompany = { ticker: 'XYZ', name: 'Unknown', industry: 'Weird', lat: 0, lng: 0, country: 'XX', marketCap: 100 }
    expect(createMarkerData(c).emoji).toBe('🐱')
  })

  it('colors green for positive change', () => {
    const c: MapCompany = { ticker: 'A', name: 'A', industry: 'Tech', lat: 0, lng: 0, country: 'US', marketCap: 100, change_pct: 1.0 }
    expect(createMarkerData(c).color).toBe('#0f8')
  })

  it('colors red for negative change', () => {
    const c: MapCompany = { ticker: 'B', name: 'B', industry: 'Tech', lat: 0, lng: 0, country: 'US', marketCap: 100, change_pct: -1.0 }
    expect(createMarkerData(c).color).toBe('#f44')
  })

  it('colors blue for neutral change', () => {
    const c: MapCompany = { ticker: 'C', name: 'C', industry: 'Tech', lat: 0, lng: 0, country: 'US', marketCap: 100, change_pct: 0 }
    expect(createMarkerData(c).color).toBe('#0cf')
  })

  it('sizes based on market cap', () => {
    const small: MapCompany = { ticker: 'S', name: 'S', industry: 'Tech', lat: 0, lng: 0, country: 'US', marketCap: 100 }
    const large: MapCompany = { ticker: 'L', name: 'L', industry: 'Tech', lat: 0, lng: 0, country: 'US', marketCap: 2400 }
    expect(createMarkerData(small).size).toBeLessThan(createMarkerData(large).size)
  })

  it('defaults size when marketCap is missing', () => {
    const c: MapCompany = { ticker: 'X', name: 'X', industry: 'Tech', lat: 0, lng: 0, country: 'US', marketCap: 0 }
    expect(createMarkerData(c).size).toBe(18)
  })
})

// ── 4. Search filtering ───────────────────────────────────────

describe('search filtering', () => {
  const companies: MapCompany[] = [
    { ticker: 'AAPL', name: 'Apple Inc.', industry: 'Tech', lat: 37, lng: -122, country: 'US', marketCap: 3000 },
    { ticker: 'MSFT', name: 'Microsoft Corp', industry: 'Tech', lat: 47, lng: -122, country: 'US', marketCap: 2800 },
    { ticker: 'XOM', name: 'Exxon Mobil', industry: 'Energy', lat: 30, lng: -95, country: 'US', marketCap: 500 },
    { ticker: 'JPM', name: 'JPMorgan Chase', industry: 'Finance', lat: 40, lng: -74, country: 'US', marketCap: 600 },
  ]

  it('filters by ticker', () => {
    expect(filterBySearch(companies, 'aapl')).toHaveLength(1)
  })

  it('filters by name', () => {
    expect(filterBySearch(companies, 'microsoft')).toHaveLength(1)
  })

  it('filters by industry', () => {
    expect(filterBySearch(companies, 'energy')).toHaveLength(1)
  })

  it('returns all for empty query', () => {
    expect(filterBySearch(companies, '')).toHaveLength(4)
  })

  it('returns all for whitespace query', () => {
    expect(filterBySearch(companies, '   ')).toHaveLength(4)
  })

  it('returns empty for no match', () => {
    expect(filterBySearch(companies, 'zzz')).toHaveLength(0)
  })

  it('is case insensitive', () => {
    expect(filterBySearch(companies, 'aapl')).toHaveLength(1)
    expect(filterBySearch(companies, 'AAPL')).toHaveLength(1)
    expect(filterBySearch(companies, 'Aapl')).toHaveLength(1)
  })
})

// ── 5. Marker click handler ───────────────────────────────────

describe('marker click handler', () => {
  type ClickHandler = (company: MapCompany) => void

  it('sets selected company on click', () => {
    let selected: MapCompany | null = null
    const onClick: ClickHandler = (c) => { selected = c }

    const company: MapCompany = { ticker: 'AAPL', name: 'Apple', industry: 'Tech', lat: 37, lng: -122, country: 'US', marketCap: 3000 }
    onClick(company)
    expect(selected).toBe(company)
    expect(selected!.ticker).toBe('AAPL')
  })

  it('can clear selection on close', () => {
    let selected: MapCompany | null = { ticker: 'AAPL', name: 'Apple', industry: 'Tech', lat: 37, lng: -122, country: 'US', marketCap: 3000 }
    const onClose = () => { selected = null }
    onClose()
    expect(selected).toBeNull()
  })

  it('handles undefined change_pct', () => {
    const c: MapCompany = { ticker: 'A', name: 'A', industry: 'Tech', lat: 0, lng: 0, country: 'US', marketCap: 100 }
    const marker = createMarkerData(c)
    expect(marker.color).toBe('#0cf')
  })
})

// ── 6. Viewport bounds filtering ──────────────────────────────

describe('viewport bounds filtering', () => {
  const companies: MapCompany[] = [
    { ticker: 'NY', name: 'NY Co', industry: 'Finance', lat: 40.7, lng: -74.0, country: 'US', marketCap: 100 },
    { ticker: 'LDN', name: 'London Co', industry: 'Finance', lat: 51.5, lng: -0.1, country: 'GB', marketCap: 100 },
    { ticker: 'TKY', name: 'Tokyo Co', industry: 'Tech', lat: 35.7, lng: 139.7, country: 'JP', marketCap: 100 },
  ]

  const nyBounds = { north: 45, south: 35, east: -70, west: -80 }

  it('filters companies within bounds', () => {
    const result = filterByViewport(companies, nyBounds)
    expect(result).toHaveLength(1)
    expect(result[0].ticker).toBe('NY')
  })

  it('returns all companies when bounds is null', () => {
    expect(filterByViewport(companies, null)).toHaveLength(3)
  })

  it('returns empty for bounds far from data', () => {
    const pacificBounds = { north: 0, south: -40, east: 180, west: 120 }
    expect(filterByViewport(companies, pacificBounds)).toHaveLength(0)
  })

  it('includes companies on boundary edges', () => {
    const tight = { north: 40.71, south: 40.69, east: -73.99, west: -74.01 }
    const result = filterByViewport(companies, tight)
    expect(result).toHaveLength(1)
  })
})
