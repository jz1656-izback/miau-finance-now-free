import express from 'express'
import cors from 'cors'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const DATA_DIR = path.join(__dirname, 'data')
const PORT = process.env.PORT || 5403

// ─── Ecosystem Services ──────────────────────────────
const SERVICES = [
  { name: 'Miau Homepage', port: 3001, icon: '🏠' },
  { name: 'Terminal', port: 5173, icon: '💻' },
  { name: 'Education', port: 5174, icon: '🎓' },
  { name: 'Ecosystem Site', port: 5175, icon: '🏠' },
  { name: 'Marketing Dashboard', port: 5176, icon: '📊' },
  { name: 'Log Viewer', port: 5177, icon: '📋' },
  { name: 'MiauBook', port: 5178, icon: '🐱' },
  { name: 'Admin', port: 5179, icon: '🔧' },
  { name: 'Service Desk', port: 5180, icon: '🎫' },
  { name: 'Cat Galaxy', port: 5181, icon: '🌌' },
  { name: 'CEO Dashboard', port: 5182, icon: '👑' },
  { name: 'Auth', port: 5190, icon: '🔐' },
  { name: 'MiauBook API', port: 5402, icon: '🐱' },
  { name: 'Marketing API', port: 5403, icon: '📈' },
  { name: 'DatChonk', port: 8765, icon: '🐈' },
]

// ─── Data Store ──────────────────────────────────────
const DB_FILE = path.join(DATA_DIR, 'marketing.json')

function loadDB() {
  try {
    fs.mkdirSync(DATA_DIR, { recursive: true })
    return JSON.parse(fs.readFileSync(DB_FILE, 'utf-8'))
  } catch {
    return { events: [], pages: {}, hourly: {}, geo: {}, referrers: {}, conversions: 0, sessions: {} }
  }
}

function saveDB(db) {
  fs.mkdirSync(DATA_DIR, { recursive: true })
  fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2))
}

let db = loadDB()

// Clean old events (>7 days)
function cleanDB() {
  const cutoff = Date.now() - 7 * 86400000
  db.events = db.events.filter(e => e.ts > cutoff)
  saveDB(db)
}
setInterval(cleanDB, 3600000)

// ─── Service Health Checker ──────────────────────────
import http from 'http'
import https from 'https'

let serviceStatus = SERVICES.map(s => ({ ...s, up: false, lastCheck: null }))
let papersData = { count: 0, papers: [] }
let coursesData = { count: 0 }

function scrapePapers() {
  http.get('http://localhost:3001/papers', { timeout: 3000 }, res => {
    let d = ''
    res.on('data', c => d += c)
    res.on('end', () => {
      const match = d.match(/(\d+)\s*Papers?/)
      if (match) papersData.count = parseInt(match[1])
      // Extract paper titles
      const titles = d.match(/<h3[^>]*>([^<]+)<\/h3>/g)
      if (titles) papersData.papers = titles.slice(0, 10).map(t => t.replace(/<[^>]+>/g, ''))
    })
  }).on('error', () => {})
}

function scrapeCourses() {
  // Count course files in the education platform
  const coursesDir = '/home/jevgeniz/Projekte/miau-finance/apps/education-platform/src/courses'
  try {
    const files = fs.readdirSync(coursesDir).filter(f => f.endsWith('.ts'))
    coursesData.count = files.length
  } catch { coursesData.count = 0 }
}

function checkServices() {
  scrapePapers()
  scrapeCourses()
  serviceStatus.forEach(s => {
    if (s.port === 5403) { s.up = true; s.lastCheck = Date.now(); return }
    const req = http.get(`http://localhost:${s.port}/`, { timeout: 3000 }, res => {
      s.up = true; s.lastCheck = Date.now()
      res.resume() // consume body to free socket
    })
    req.on('error', () => { s.up = false; s.lastCheck = Date.now() })
    req.on('timeout', () => { req.destroy(); s.up = false; s.lastCheck = Date.now() })
  })
}
checkServices()
setInterval(checkServices, 30000)

// ─── Data Generators ─────────────────────────────────
function servicesUpCount() { return serviceStatus.filter(s => s.up).length }

function generateHourly() {
  const now = Date.now(), hour = 3600000
  const h = {}
  for (let i = 0; i < 24; i++) {
    const t = new Date(now - (23 - i) * hour)
    const key = t.toISOString().slice(0, 13)
    const actual = db.hourly[key]
    h[key] = actual || {
      page_views: Math.floor(Math.random() * 50 + 10 * Math.max(1, servicesUpCount())),
      visitors: Math.floor(Math.random() * 20 + 5 * Math.max(1, servicesUpCount())),
    }
  }
  return h
}

function generate30DayTrend() {
  const day = 86400000
  const base = Math.max(50, servicesUpCount() * 30)
  return Array.from({ length: 30 }, (_, i) => {
    const date = new Date(Date.now() - (29 - i) * day).toISOString().slice(0, 10)
    const visitors = Math.floor(base + Math.sin(i / 2) * base * 0.3 + Math.random() * base * 0.2)
    const page_views = Math.floor(visitors * (2 + Math.random()))
    return { date, visitors, page_views, conversions: Math.floor(visitors * (0.02 + Math.random() * 0.03)) }
  })
}

function generatePages() {
  const paths = ['/', '/pricing', '/features', '/docs', '/blog', '/login', '/about', '/contact', '/changelog', '/careers']
  const base = db.pages || {}
  return paths.map(p => ({
    path: p,
    views: (base[p] || 0) + Math.floor(Math.random() * 100 + 10 * servicesUpCount()),
  })).sort((a, b) => b.views - a.views)
}

// ─── Express App ─────────────────────────────────────
const app = express()
app.use(cors())
app.use(express.json())

// ─── Tracking Endpoint ──────────────────────────────
app.post('/api/v1/marketing/track', (req, res) => {
  const { event, path: pagePath, host, referrer, session_id, utm_source, utm_medium, utm_campaign, conversion_type, conversion_value } = req.body || {}
  
  const entry = { ts: Date.now(), event, path: pagePath || '/', host: host || 'unknown', referrer, session_id, utm_source, utm_medium, utm_campaign, conversion_type, conversion_value }
  db.events.push(entry)
  
  // Track page views
  const pageKey = pagePath || '/'
  db.pages[pageKey] = (db.pages[pageKey] || 0) + 1
  
  // Track hourly
  const hourKey = new Date().toISOString().slice(0, 13)
  if (!db.hourly[hourKey]) db.hourly[hourKey] = { page_views: 0, visitors: 0 }
  db.hourly[hourKey].page_views++
  if (session_id && !db.sessions[session_id + '_' + hourKey]) {
    db.hourly[hourKey].visitors++
    db.sessions[session_id + '_' + hourKey] = true
  }
  
  // Track geo (mock from referrer/ip for demo)
  const country = referrer?.includes('.de') ? 'Germany' : referrer?.includes('.uk') ? 'United Kingdom' :
                  referrer?.includes('.ca') ? 'Canada' : referrer?.includes('.au') ? 'Australia' :
                  referrer?.includes('.fr') ? 'France' : 'United States'
  db.geo[country] = (db.geo[country] || 0) + 1
  
  // Track referrer
  const src = referrer ? new URL(referrer).hostname : 'direct'
  db.referrers[src] = (db.referrers[src] || 0) + 1
  
  // Track conversions
  if (conversion_type) db.conversions = (db.conversions || 0) + 1
  
  saveDB(db)
  res.json({ ok: true })
})

// ─── Stats ──────────────────────────────────────────
app.get('/api/v1/marketing/stats', (req, res) => {
  const now = Date.now(), lastHour = now - 3600000
  const totalVisitors = Object.keys(db.hourly).reduce((s, k) => s + (db.hourly[k]?.visitors || 0), 0)
  const totalViews = Object.keys(db.pages).reduce((s, k) => s + db.pages[k], 0)
  const recentVisitors = db.events.filter(e => e.ts > lastHour).length
  const totalConversions = db.conversions || Math.floor(totalVisitors * 0.035)
  res.json({
    total_visitors: Math.max(totalVisitors, servicesUpCount() * 120),
    total_page_views: Math.max(totalViews, servicesUpCount() * 350),
    bounce_rate: 35 + Math.random() * 10,
    avg_session_duration: 120 + Math.random() * 120,
    conversion_rate: totalVisitors > 0 ? (totalConversions / Math.max(totalVisitors, 1)) * 100 : 3.2,
    active_sessions: servicesUpCount() * 2 + Math.floor(Math.random() * 10),
    total_conversions: totalConversions,
    services_up: servicesUpCount(),
    services_total: SERVICES.length,
    papers_total: papersData.count,
    papers_recent: papersData.papers.slice(0, 5),
    courses_total: coursesData.count,
  })
})

// ─── Trends ─────────────────────────────────────────
app.get('/api/v1/marketing/trends', (req, res) => {
  res.json(generate30DayTrend())
})

// ─── Pages ──────────────────────────────────────────
app.get('/api/v1/marketing/pages', (req, res) => {
  res.json(generatePages())
})

// ─── Campaigns ──────────────────────────────────────
app.get('/api/v1/marketing/campaigns', (req, res) => {
  const up = servicesUpCount()
  res.json([
    { name: '🐱 Q1 Brand Push', spend: Math.floor(8000 + up * 400), impressions: Math.floor(500000 + up * 30000), clicks: Math.floor(15000 + up * 600), conversions: Math.floor(600 + up * 25) },
    { name: '🎓 Education Launch', spend: Math.floor(6000 + up * 300), impressions: Math.floor(350000 + up * 20000), clicks: Math.floor(12000 + up * 500), conversions: Math.floor(450 + up * 20) },
    { name: '🐟 Tuna Referral', spend: Math.floor(4000 + up * 200), impressions: Math.floor(200000 + up * 15000), clicks: Math.floor(10000 + up * 400), conversions: Math.floor(350 + up * 15) },
    { name: '🤖 AI Advisor Promo', spend: Math.floor(3000 + up * 150), impressions: Math.floor(150000 + up * 10000), clicks: Math.floor(7000 + up * 300), conversions: Math.floor(250 + up * 10) },
    { name: '📊 Q2 Retargeting', spend: Math.floor(2500 + up * 100), impressions: Math.floor(120000 + up * 8000), clicks: Math.floor(5000 + up * 200), conversions: Math.floor(200 + up * 8) },
    { name: '🌍 Global Expansion', spend: Math.floor(2000 + up * 80), impressions: Math.floor(80000 + up * 5000), clicks: Math.floor(3500 + up * 150), conversions: Math.floor(140 + up * 6) },
  ])
})

// ─── Geo ────────────────────────────────────────────
app.get('/api/v1/marketing/geo', (req, res) => {
  const up = servicesUpCount()
  const geoData = [
    { country: 'United States', country_code: 'US', visitors: Math.floor(8000 + up * 200), page_views: Math.floor(20000 + up * 500) },
    { country: 'Germany', country_code: 'DE', visitors: Math.floor(6000 + up * 150), page_views: Math.floor(15000 + up * 400) },
    { country: 'United Kingdom', country_code: 'GB', visitors: Math.floor(4000 + up * 100), page_views: Math.floor(10000 + up * 300) },
    { country: 'Canada', country_code: 'CA', visitors: Math.floor(3000 + up * 80), page_views: Math.floor(8000 + up * 200) },
    { country: 'Australia', country_code: 'AU', visitors: Math.floor(2000 + up * 60), page_views: Math.floor(5000 + up * 150) },
    { country: 'France', country_code: 'FR', visitors: Math.floor(1500 + up * 50), page_views: Math.floor(4000 + up * 100) },
    { country: 'Netherlands', country_code: 'NL', visitors: Math.floor(1200 + up * 40), page_views: Math.floor(3000 + up * 80) },
    { country: 'Switzerland', country_code: 'CH', visitors: Math.floor(1000 + up * 30), page_views: Math.floor(2500 + up * 60) },
    { country: 'Austria', country_code: 'AT', visitors: Math.floor(800 + up * 25), page_views: Math.floor(2000 + up * 50) },
    { country: 'Japan', country_code: 'JP', visitors: Math.floor(600 + up * 20), page_views: Math.floor(1500 + up * 40) },
  ]
  // Boost countries that have been tracked via geo
  Object.entries(db.geo).forEach(([country, count]) => {
    const existing = geoData.find(g => g.country === country)
    if (existing) existing.visitors += Math.min(count, 500)
    else geoData.push({ country, country_code: country.slice(0, 2).toUpperCase(), visitors: count, page_views: count * 2 })
  })
  res.json(geoData.slice(0, 10))
})

// ─── Realtime ───────────────────────────────────────
app.get('/api/v1/marketing/realtime', (req, res) => {
  const last5min = db.events.filter(e => e.ts > Date.now() - 300000)
  const lastHour = db.events.filter(e => e.ts > Date.now() - 3600000)
  const topPath = Object.entries(db.pages).sort((a, b) => b[1] - a[1])[0]
  const topRef = Object.entries(db.referrers).sort((a, b) => b[1] - a[1])[0]
  res.json({
    active_visitors: servicesUpCount() * 2 + Math.floor(Math.random() * 5),
    page_views_today: lastHour.length + Math.floor(Math.random() * 100),
    page_views_last_minute: last5min.filter(e => e.ts > Date.now() - 60000).length,
    page_views_last_5_minutes: last5min.length,
    conversions_last_hour: lastHour.filter(e => e.event === 'conversion').length,
    top_page: topPath?.[0] || '/',
    top_source: topRef?.[0] || 'direct',
    services_up: servicesUpCount(),
    hourly_breakdown: Object.entries(generateHourly()).slice(-12).map(([hour, data]) => ({ hour, ...data })),
  })
})

// ─── SEO: Keywords ──────────────────────────────────
app.get('/api/v1/marketing/keywords', (req, res) => {
  const up = servicesUpCount()
  res.json([
    { kw: 'cat finance terminal', pos: 1, vol: 2400, traffic: Math.floor(500 + up * 20) },
    { kw: 'bloomberg alternative free', pos: 3, vol: 8200, traffic: Math.floor(1800 + up * 50) },
    { kw: 'terminal trading platform', pos: 2, vol: 4800, traffic: Math.floor(1500 + up * 40) },
    { kw: 'ai financial advisor', pos: 4, vol: 12000, traffic: Math.floor(2000 + up * 60) },
    { kw: 'paper trading simulator', pos: 5, vol: 6400, traffic: Math.floor(800 + up * 30) },
    { kw: 'cat themed finance', pos: 1, vol: 1800, traffic: Math.floor(600 + up * 15) },
    { kw: 'stock market terminal', pos: 6, vol: 9200, traffic: Math.floor(1000 + up * 35) },
    { kw: 'finance learning platform', pos: 3, vol: 5400, traffic: Math.floor(1200 + up * 30) },
    { kw: 'deFi dashboard', pos: 7, vol: 15000, traffic: Math.floor(1500 + up * 45) },
    { kw: 'investment analysis tool', pos: 4, vol: 3600, traffic: Math.floor(600 + up * 20) },
  ])
})

// ─── SEO: Backlinks ─────────────────────────────────
app.get('/api/v1/marketing/backlinks', (req, res) => {
  const up = servicesUpCount()
  res.json({ total: Math.floor(10000 + up * 400), domains: Math.floor(2500 + up * 100), new_month: Math.floor(300 + up * 15) })
})

// ─── SEO: Site Health ───────────────────────────────
app.get('/api/v1/marketing/sitehealth', (req, res) => {
  res.json({ score: 92 + Math.floor(Math.random() * 8), issues: 8 + Math.floor(Math.random() * 10), critical: 0 })
})

// ─── Sales ──────────────────────────────────────────
app.get('/api/v1/marketing/sales', (req, res) => {
  const up = servicesUpCount()
  res.json({
    pipeline: Math.floor(300000 + up * 15000),
    mrr: Math.floor(20000 + up * 1000),
    won: 4 + Math.floor(up / 3),
    lost: 1 + Math.floor(up / 5),
    deals: [
      { name: 'Enterprise Corp', stage: 'proposal', value: Math.floor(35000 + up * 1000), prob: 60 },
      { name: 'Startup Inc', stage: 'demo', value: Math.floor(10000 + up * 300), prob: 30 },
      { name: 'Fund Manager LLC', stage: 'negotiation', value: Math.floor(80000 + up * 2000), prob: 80 },
      { name: 'Trading Desk GmbH', stage: 'discovery', value: Math.floor(18000 + up * 500), prob: 20 },
      { name: 'Cat Asset Mgmt', stage: 'closed', value: Math.floor(30000 + up * 800), prob: 100 },
      { name: 'Whisker Ventures', stage: 'proposal', value: Math.floor(15000 + up * 400), prob: 50 },
      { name: 'Paw Capital', stage: 'discovery', value: Math.floor(60000 + up * 1500), prob: 15 },
      { name: 'Meow Bank AG', stage: 'demo', value: Math.floor(120000 + up * 3000), prob: 35 },
    ],
  })
})

// ─── Content: Blog Posts ────────────────────────────
app.get('/api/v1/marketing/posts', (req, res) => {
  const up = servicesUpCount()
  res.json([
    { title: 'Why Cats Make Better Traders Than Humans', views: Math.floor(8000 + up * 300), shares: Math.floor(200 + up * 10), date: '2026-05-20' },
    { title: 'The Tuna-Nap Theorem Explained', views: Math.floor(6000 + up * 200), shares: Math.floor(150 + up * 8), date: '2026-05-18' },
    { title: 'Terminal Trading for Beginners', views: Math.floor(4000 + up * 150), shares: Math.floor(100 + up * 5), date: '2026-05-15' },
    { title: 'DeFi Yield Farming with Cat Intelligence', views: Math.floor(3500 + up * 120), shares: Math.floor(300 + up * 12), date: '2026-05-12' },
    { title: 'Bloomberg vs Miau: The Honest Comparison', views: Math.floor(7000 + up * 250), shares: Math.floor(450 + up * 15), date: '2026-05-10' },
    { title: 'How to Pass CFA Using Only Cat Memes', views: Math.floor(5000 + up * 180), shares: Math.floor(600 + up * 20), date: '2026-05-08' },
  ])
})

// ─── Content: Social Media ──────────────────────────
app.get('/api/v1/marketing/social', (req, res) => {
  const up = servicesUpCount()
  res.json([
    { platform: '🐦 Twitter/X', followers: Math.floor(8000 + up * 400), engagement: 3.5 + Math.random(), posts: Math.floor(30 + up) },
    { platform: '💼 LinkedIn', followers: Math.floor(6000 + up * 300), engagement: 3.2 + Math.random(), posts: Math.floor(20 + up * 0.8) },
    { platform: '📹 YouTube', subscribers: Math.floor(3500 + up * 200), engagement: 5.5 + Math.random(), videos: Math.floor(15 + up * 0.5) },
    { platform: '🤖 GitHub', stars: Math.floor(2000 + up * 150), forks: Math.floor(500 + up * 40), repos: Math.floor(8 + up * 0.3) },
    { platform: '🎮 Discord', members: Math.floor(1500 + up * 100), active: Math.floor(200 + up * 15), messages: Math.floor(2000 + up * 100) },
  ])
})

// ─── Service Status ─────────────────────────────────
app.get('/api/v1/marketing/services', (req, res) => {
  res.json({ services: serviceStatus, up: servicesUpCount(), total: SERVICES.length })
})

// ─── Health ─────────────────────────────────────────
app.get('/api/v1/marketing/health', (req, res) => {
  res.json({ status: 'ok', services_up: servicesUpCount(), events_tracked: db.events.length, papers: papersData.count, courses: coursesData.count, uptime: process.uptime() })
})

// ─── Ecosystem Data ────────────────────────────────
app.get('/api/v1/marketing/ecosystem', (req, res) => {
  res.json({ services: serviceStatus, papers: papersData, courses: coursesData, events_tracked: db.events.length })
})

// ─── Campaigns Data (full) ──────────────────────────
app.get('/api/v1/marketing/campaigns', (req, res) => {
  const up = servicesUpCount()
  res.json([
    { name: '🐱 Q1 Brand Push', spend: Math.floor(10000 + up * 500), impressions: Math.floor(700000 + up * 40000), clicks: Math.floor(18000 + up * 800), conversions: Math.floor(700 + up * 30) },
    { name: '🎓 Education Launch', spend: Math.floor(7000 + up * 350), impressions: Math.floor(400000 + up * 25000), clicks: Math.floor(14000 + up * 600), conversions: Math.floor(500 + up * 25) },
    { name: '🐟 Tuna Referral', spend: Math.floor(4500 + up * 200), impressions: Math.floor(250000 + up * 18000), clicks: Math.floor(12000 + up * 500), conversions: Math.floor(400 + up * 18) },
    { name: '🤖 AI Advisor Promo', spend: Math.floor(3500 + up * 150), impressions: Math.floor(180000 + up * 12000), clicks: Math.floor(8000 + up * 350), conversions: Math.floor(300 + up * 12) },
    { name: '📊 Q2 Retargeting', spend: Math.floor(2800 + up * 120), impressions: Math.floor(140000 + up * 10000), clicks: Math.floor(6000 + up * 250), conversions: Math.floor(220 + up * 10) },
    { name: '🌍 Global Expansion', spend: Math.floor(2200 + up * 100), impressions: Math.floor(100000 + up * 6000), clicks: Math.floor(4000 + up * 200), conversions: Math.floor(160 + up * 8) },
  ])
})

app.listen(PORT, () => {
  console.log(`📈 Miau Marketing API running on :${PORT}`)
  console.log(`   Tracking ${SERVICES.length} ecosystem services`)
  checkServices()
})
