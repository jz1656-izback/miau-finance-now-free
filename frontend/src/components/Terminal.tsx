import { useState, useRef, useEffect, useCallback, Fragment, lazy, Suspense } from 'react'
import WorldMap from './WorldMap'
const MiauGlobe = lazy(() => import('./MiauGlobe'))
import Chart3D from './Chart3D'
import Sheetz3D from './Sheetz3D'
import TunaWallet from './TunaWallet'
import CookieBanner from './CookieBanner'
import Compare3D from './Compare3D'
import PricingPage from './PricingPage'
import RaveOverlay from './RaveOverlay'
import TreasuryChart from './TreasuryChart'
import BondChart from './BondChart'
import Map2D from './Map2D'
import CatCompanion from './CatCompanion'
import Catberg from './Catberg'
import Heatmap from './Heatmap'
import MiauBook from './MiauBook'
import CatLoader from './CatLoaders'
import BenchmarkComparison from "./benchmark"
import { getTheme, type TerminalTheme } from "../lib/themes"
import { getCurrentLocale, setLocale, SUPPORTED_LOCALES, LOCALE_NATIVE } from '../lib/i18n'
import CorrelationMatrix from "./CorrelationMatrix"
import DeveloperConsole from './DeveloperConsole'
import AdminConsole from './AdminConsole'
import CommandPalette from "./mobile/CommandPalette"
import { FadeIn, SlideIn } from './Transitions'
import { executeCommand } from '../lib/commands'
import { ConnectionDot } from './terminal/ConnectionDot'
import { TerminalInput } from './terminal/TerminalInput'
import { escapeHtml } from '../lib/commands/shared'
import { playCatSound, getCatEncouragement } from '../lib/catSounds'
import { getSuggestions, recordCommand } from '../lib/autocomplete'
import { updateAchievementState, type UnlockedAchievement } from '../lib/achievements'
import Kittyland, { type KittyPanel } from './Kittyland'

// 🔒 SECURITY: Sanitize HTML to prevent XSS attacks
import DOMPurify from 'dompurify'

function sanitizeHtml(html: string): string {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['span', 'br', 'b', 'i', 'u', 'a'],
    ALLOWED_ATTR: ['class', 'style', 'href', 'target', 'rel'],
  })
}

interface Line {
  text: string
  html?: boolean
  className?: string
}

const CAT_BOOT = `
       🐟  🐟  🐟  🐟  🐟  🐟  🐟  🐟  🐟  🐟  🐟  🐟  🐟  🐟

       /\\_/\\    /\\_/\\    /\\_/\\    /\\_/\\    /\\_/\\    /\\_/\\
      ( o.o )  ( ^.^ )  ( -.- )  ( 💰.💰 ) ( 🐟.🐟 ) ( >.< )
       > ^ <    > ~ <    > 🐟 <    > €€ <    > ^ <    > HISS <

  ╱|、      ╱|、      ╱|、      ╱|、      ╱|、      ╱|、
 (˚ˎ 。7   (˚ˎ 。7   (˚ˎ 。7   (˚ˎ 。7   (˚ˎ 。7   (˚ˎ 。7
  |、˜〵    |、˜〵    |、˜〵    |、˜〵    |、˜〵    |、˜〵
  じしˍ,)ノ じしˍ,)ノ じしˍ,)ノ じしˍ,)ノ じしˍ,)ノ じしˍ,)ノ

  ╔══════════════════════════════════════════════════════╗
  ║     M I A U   F I N A N C E   v2.5.0                ║
  ║     🐾 GOLDEN PAW EDITION 🐾                           ║
  ║     where cats trade stocks  🐱📈🐟                   ║
  ║     515+ APIs · 193 commands · 50+ data providers      ║
  ║     17 indicators · 230 courses · infinite tuna 🐟    ║
  ╚══════════════════════════════════════════════════════╝

  ╱|、
 (˚ˎ 。7     "The early cat catches the bug. The smart cat catches the dip."
  |、˜〵     "Commit early, commit often, pet the cat. HODL the tuna."
  じしˍ,)ノ   "Bloomberg costs $24k/yr. Miau costs cat treats. AMIAU."
`

const WELCOME = `
  ╭────────────────────────────────────────────────────────────────────────╮
  │  🔐  login <username>  ·  pawdentity single sign-on  ·  miau          │
  │  🐾  'map' 2D · 'miaumap' 3D globe · 'courses' learn · 'cat'         │
  │  📺  'panel' open web apps · 'kitty' floating panels · 'help'         │
  │  💡  TAB autocomplete  ·  ↑↓ history  ·  Ctrl+K command palette       │
  ╰────────────────────────────────────────────────────────────────────────╯
`

const CAT_ASCII = [
`
    /\\_/\\
   ( o.o )
    > ^ <
`,
`
   /\\_/\\
  ( ^.^ )
   (")(")
`,
`
    /\\_/\\
   ( -.- )
    > ~ <
`,
`
   ╱|、
  (˚ˎ 。7
   |、˜〵
   じしˍ,)ノ
`,
`
    /\\___/\\
   (  o o  )
   /   Y   \\
  (    |    )
`,
`
     /\\_/\\
    ( @.@ )
     (u u)
`,
`
   /\\_/\\
  ( >.< )
   > 🐟 <
`,
`
    /\\_/\\
   ( o.o )
    > miau
`,
`
    /\\___/\\
   (  👁️👁️  )
   /   🐟   \\
  (  🐾_🐾  )
`,
`
      /\\„„/\\
     /´¯o o¯\`
    (   "   )
     \\_|_/_
      Y
`,
`
    ╱\\ /\\  ╲
   ( ˘▾˘ )
   (   🐟  )
    \\_/\\_/
`,
`
   ／(=✪ ᆺ ✪=)＼
  │  🐟  🐟  │
  ＼ ＿＿＿＿＿／
`,
`
      /\\_/\\
     (◕‿◕)
     /|  |\\
      U  U
`,
`
      /\\___/\\
     ( ˘ ³˘)♥
      /  🐟  \\
     │   │   │
`,
`
     ⊂(◉‿◉)つ
      /\\_/\\
     (     )
     (  🐟  )
`,
`
    /\\___/\\
   (  🐟🐟🐟  )
   /   🐟   \\
  {    🐟    }
   \\  🐟  /
`,
`
    ╱ᐳᐳ╲
   ( Φ ω Φ )
   (  ⊃ 🐟 ⊂  )
    ╲___╱
`,
`
      /\\_/\\
     ( ⓛᆺⓛ)
      (   🐟   )
       \\___/
`,
`
      ╱\\/\\╲
     ( ˊᵕˋ )
     |  🐟  |
     \\___/
`,
`
      /\\_/\\
     ( 💎.💎 )
      > 🚀 <
     diamond paws
`,
`
    ┌(★‿★)┐
     /\\_/\\
    ( ^.^)/
     > 🐟 <
    🐾🐾🐾🐾🐾
`,
`
    ╔═══════╗
    ║ 🐱💰🐟 ║
    ║ CFO   ║
    ║ CAT   ║
    ╚═══════╝
     /\\_/\\
    ( €€.€€ )
     >  ^  <
`,
`
    ★  ☆  ★
    ✨/\\_/\\✨
    ( ✨.✨ )
    >  ^  <
    ★  TUNA  ★
    ☆  MOON  ☆
`,
`
    🐟😺🐟😺🐟
    😺 /\\_/\\ 😺
    🐟( 😺.😺 )🐟
    😺 > 🐟 < 😺
    🐟😺🐟😺🐟
`,
// ✨ v2.5.0 GOLDEN PAW EDITION ✨
`
    👑═══👑
    ╱ GOLDEN ╲
   (  PAW  )
    ╲  🐾  ╱
    ═══👑═══
   /\\_/\\    🌟
  ( 👑.👑 )  GOLDEN
   > 🐟 <   PAW
  🐾🐾🐾🐾🐾 v2.5.0
`,
]

const PROMPT = 'miau@finance'

const EDU_LINKS: { [key: string]: string | undefined } = {
  price: "http://localhost:5174",
  portfolio: "http://localhost:5174",
  help: "http://localhost:5174",
  map: "http://localhost:5174",
  heatmap: "http://localhost:5174",
  correlation: "http://localhost:5174",
  benchmark: "http://localhost:5174",
  signal: "http://localhost:5174",
  strategy: "http://localhost:5174",
  ai: "http://localhost:5174",
  defi: "http://localhost:5174",
  wallet: "http://localhost:5174",
  nft: "http://localhost:5174",
  quantum: "http://localhost:5174",
  esg: "http://localhost:5174",
  carbon: "http://localhost:5174",
  dcf: "http://localhost:5174",
  wacc: "http://localhost:5174",
  comps: "http://localhost:5174",
  lbo: "http://localhost:5174",
  sheetz: "http://localhost:5174",
  paper: "http://localhost:5174",
  order: "http://localhost:5174",
  broker: "http://localhost:5174",
  social: "http://localhost:5174",
  leaderboard: "http://localhost:5174",
  catberg: "http://localhost:5174",
  agi: "http://localhost:5174",
  search: "http://localhost:5174",
  news: "http://localhost:5174",
}

interface TerminalProps {
  embedded?: boolean
  hideMapControls?: boolean
  onSplit?: () => void
}

export default function Terminal({ embedded = false, onSplit }: TerminalProps) {
  const [lines, setLines] = useState<Line[]>([
    { text: CAT_BOOT, className: 'text-green' },
    { text: WELCOME, className: 'text-cyan' },
    { text: '', className: '' },
  ])
  const [input, setInput] = useState('')
  const [history, setHistory] = useState<string[]>(() => {
    try { return JSON.parse(localStorage.getItem('miau_history') || '[]') } catch { return [] }
  })
  const [historyIdx, setHistoryIdx] = useState(-1)
  const [loading, setLoading] = useState(false)
  const [showMap, setShowMap] = useState(false)
  const [showMiauMap, setShowMiauMap] = useState(false)
  const showMiauMapRef = useRef(showMiauMap)
  const [showDashboard, setShowDashboard] = useState(false); void setShowDashboard
  const showDashboardRef = useRef(showDashboard)
  const [showHeatmap, setShowHeatmap] = useState(false)
  const [showCatberg, setShowCatberg] = useState(false)
  const [showCorrMatrix, setShowCorrMatrix] = useState(false)
  const [showBenchmark, setShowBenchmark] = useState(false)
  const [showDevConsole, setShowDevConsole] = useState(false)
  const [showAdminConsole, setShowAdminConsole] = useState(false)
  const [showMap2D, setShowMap2D] = useState(false)
  const [showMiauBook, setShowMiauBook] = useState(false)
  const [kittyPanels, setKittyPanels] = useState<KittyPanel[]>([])
  const kittyIdRef = useRef(0)
  const [showChart3D, setShowChart3D] = useState<string | null>(null)
  const [showSheetz3D, setShowSheetz3D] = useState<string | null>(null)
  const [showCompare3D, setShowCompare3D] = useState<string[] | null>(null)
  const [showPricing, setShowPricing] = useState(false)
  const [raveMode, setRaveMode] = useState(false)
  const [showTreasury, setShowTreasury] = useState(false)
  const [showBonds, setShowBonds] = useState(false)
  const [corrData, setCorrData] = useState<{ tickers: string[]; matrix: Record<string, Record<string, number>> } | null>(null)
  const [showShortcuts, setShowShortcuts] = useState(false)
  const [catCount, setCatCount] = useState(0)
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [cmdCount, setCmdCount] = useState(0)
  const [startTime] = useState(Date.now())
  const [sectorData, setSectorData] = useState<any[]>([])
  const [connected, setConnected] = useState(true)
  const [clock, setClock] = useState('')
  const [voiceActive, setVoiceActive] = useState(false)
  const recognitionRef = useRef<any>(null)
  const [showPalette, setShowPalette] = useState(false)
  const [showHistorySearch, setShowHistorySearch] = useState(false)
  const [historyQuery, setHistoryQuery] = useState('')
  const [achievementToast, setAchievementToast] = useState<UnlockedAchievement | null>(null)
  const [theme, setThemeState] = useState<TerminalTheme>(getTheme)
  const [showCmdDiscovery, setShowCmdDiscovery] = useState(false)
  // 🔐 pawdentity masked-login state machine: null (normal) → username → password
  const [pwPrompt, setPwPrompt] = useState<null | { mode: 'username' | 'password'; username: string }>(null)
  const touchStartY = useRef(0)
  const touchStartX = useRef(0)

  // Touch gesture handling for mobile
  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    touchStartY.current = e.touches[0].clientY
    touchStartX.current = e.touches[0].clientX
  }, [])

  const handleTouchEnd = useCallback((e: React.TouchEvent) => {
    const dy = e.changedTouches[0].clientY - touchStartY.current
    const dx = e.changedTouches[0].clientX - touchStartX.current
    const absDy = Math.abs(dy)
    const absDx = Math.abs(dx)
    if (absDy < 30 && absDx < 30) return // too small
    if (absDy > absDx) {
      // Vertical swipe
      if (dy > 50) setShowPalette(p => !p)  // swipe down → command palette
    } else {
      // Horizontal swipe
      if (dx < -50) {
        // Swipe left → next view
        if (showHeatmap) { setShowHeatmap(false); setShowBenchmark(true) }
        else if (showBenchmark) { setShowBenchmark(false); setShowCorrMatrix(true) }
        else if (showCorrMatrix) { setShowCorrMatrix(false) }
        else setShowHeatmap(true)
      } else if (dx > 50) {
        // Swipe right → previous view
        if (showCorrMatrix) { setShowCorrMatrix(false); setShowBenchmark(true) }
        else if (showBenchmark) { setShowBenchmark(false); setShowHeatmap(true) }
        else if (showHeatmap) { setShowHeatmap(false) }
      }
    }
  }, [showHeatmap, showBenchmark, showCorrMatrix])

  // Listen for theme changes from theme command
  useEffect(() => {
    const handler = (e: Event) => {
      const detail = (e as CustomEvent).detail as TerminalTheme
      if (detail) setThemeState(detail)
    }
    window.addEventListener('miau-theme-changed', handler)
    const catbergHandler = () => setShowCatberg(prev => !prev)
    window.addEventListener('toggle-catberg', catbergHandler)
    return () => { window.removeEventListener('miau-theme-changed', handler); window.removeEventListener('toggle-catberg', catbergHandler) }
  }, [])

  // Clock tick
  useEffect(() => {
    setClock(new Date().toLocaleTimeString())
    const id = setInterval(() => setClock(new Date().toLocaleTimeString()), 1000)
    return () => clearInterval(id)
  }, [])

  // Apply theme CSS variables
  useEffect(() => {
    const root = document.documentElement
    root.style.setProperty('--miau-bg', theme.colors.bg)
    root.style.setProperty('--miau-bg-secondary', theme.colors.bgSecondary)
    root.style.setProperty('--miau-border', theme.colors.border)
    root.style.setProperty('--miau-text', theme.colors.text)
    root.style.setProperty('--miau-text-dim', theme.colors.textDim)
    root.style.setProperty('--miau-green', theme.colors.green)
    root.style.setProperty('--miau-accent', theme.colors.accent)
    root.style.setProperty('--miau-red', theme.colors.red)
    root.style.setProperty('--miau-yellow', theme.colors.yellow)
    root.style.setProperty('--miau-cyan', theme.colors.cyan)
    root.style.setProperty('--miau-purple', theme.colors.purple)
  }, [theme])

  // Mobile virtual keyboard handling
  useEffect(() => {
    const onFocus = () => {
      setTimeout(() => {
        inputRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }, 300)
    }
    const onResize = () => {
      if (window.visualViewport) {
        const diff = window.innerHeight - window.visualViewport.height
        if (diff > 100) {
          document.documentElement.style.setProperty('--keyboard-height', `${diff}px`)
          setTimeout(() => inputRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' }), 100)
        } else {
          document.documentElement.style.removeProperty('--keyboard-height')
        }
      }
    }
    const input = inputRef.current
    input?.addEventListener('focus', onFocus)
    window.visualViewport?.addEventListener('resize', onResize)
    return () => {
      input?.removeEventListener('focus', onFocus)
      window.visualViewport?.removeEventListener('resize', onResize)
    }
  }, [])

  const inputRef = useRef<HTMLInputElement>(null)
  const bottomRef = useRef<HTMLDivElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => { showMiauMapRef.current = showMiauMap }, [showMiauMap])
  useEffect(() => { showDashboardRef.current = showDashboard }, [showDashboard])

  // Auto-focus terminal input when closing any full-screen mode
  useEffect(() => {
    if (showMap || showMiauMap || showMap2D || showCatberg || showHeatmap || showBenchmark || showCorrMatrix || showDevConsole || showMiauBook || showDashboard) return
    const t = setTimeout(() => inputRef.current?.focus(), 80)
    return () => clearTimeout(t)
  }, [showMap, showMiauMap, showMap2D, showCatberg, showHeatmap, showBenchmark, showCorrMatrix, showDevConsole, showMiauBook, showDashboard])
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [lines])
  useEffect(() => {
    const el = inputRef.current
    if (el) el.focus()
    const onPageShow = () => setTimeout(() => inputRef.current?.focus(), 50)
    const onVisibility = () => { if (!document.hidden) setTimeout(() => inputRef.current?.focus(), 50) }
    const onInteraction = () => { inputRef.current?.focus(); document.removeEventListener('click', onInteraction) }
    window.addEventListener('pageshow', onPageShow)
    document.addEventListener('visibilitychange', onVisibility)
    document.addEventListener('click', onInteraction, { once: true })
    return () => {
      window.removeEventListener('pageshow', onPageShow)
      document.removeEventListener('visibilitychange', onVisibility)
      document.removeEventListener('click', onInteraction)
    }
  }, [])

  useEffect(() => { try { localStorage.setItem('miau_history', JSON.stringify(history)) } catch {} }, [history])

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setShowPalette(p => !p)
      }
      if ((e.metaKey || e.ctrlKey) && e.key === 'r') {
        e.preventDefault()
        setShowHistorySearch(p => !p)
        setHistoryQuery('')
      }
      if (e.key === 'Escape') setShowHistorySearch(false)
      // Tab → focus terminal input (unless in another input)
      if (e.key === 'Tab') {
        const tag = (e.target as HTMLElement)?.tagName?.toLowerCase()
        if (tag !== 'input' && tag !== 'textarea' && tag !== 'select') {
          e.preventDefault()
          inputRef.current?.focus()
        }
      }
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [])

  const addLine = useCallback((line: Line) => setLines(prev => [...prev, line].slice(-500)), [])

  useEffect(() => {
    const check = async () => {
      try { const r = await fetch('/api/v1/health'); setConnected(r.ok) }
      catch { setConnected(false) }
    }
    check()
    const hi = setInterval(check, 30000)
    return () => clearInterval(hi)
  }, [])

  const handleCommand = useCallback(async (cmd: string) => {
    const raw = cmd.trim()
    if (!raw) return
    const t = raw.toLowerCase()

    // 🔐 pawdentity masked login — intercept BEFORE the generic echo/history
    // block so a password is NEVER echoed, stored in history, or suggested.
    // Handles: `login`, `login <username>`, and even a pasted legacy
    // `login <username> <password>` (extra tokens are discarded silently).
    if (t.split(/\s+/)[0] === 'login') {
      const parts = raw.split(/\s+/)
      const username = parts[1] || ''
      const sanitized = username ? `login ${username}` : 'login'
      setCmdCount(c => c + 1)
      setHistory(prev => [sanitized, ...prev.slice(0, 99)])
      setHistoryIdx(-1)
      setSuggestions([])
      addLine({
        text: `<span class="text-green">${PROMPT}</span><span class="text-dim">:~$ </span><span class="text-bright">${escapeHtml(sanitized)}</span>`,
        html: true,
      })
      if (username) {
        setPwPrompt({ mode: 'password', username })
      } else {
        setPwPrompt({ mode: 'username', username: '' })
      }
      return
    }

    setCmdCount(c => c + 1)
    setHistory(prev => [t, ...prev.slice(0, 99)])
    setHistoryIdx(-1)
    setSuggestions([])

    addLine({
      text: `<span class="text-green">${PROMPT}</span><span class="text-dim">:~$ </span><span class="text-bright">${escapeHtml(raw)}</span>`,
      html: true,
    })

    if (t === 'clear') { setLines([]); return }
    if (t === 'map') { setShowMap(prev => !prev); setShowHeatmap(false); setShowCorrMatrix(false); setShowMiauMap(false); addLine({ text: showMap ? 'map hidden' : 'map visible', className: 'text-dim' }); return }
    if (t.startsWith('miaumap') || t.startsWith('miauglobe') || t.startsWith('globe')) {
      const sub = raw.split(/\s+/)[1]
      if (sub === '--aliens' || sub === '-a') {
        try { sessionStorage.setItem('miau_globe_aliens', '1') } catch {}
        setShowMiauMap(true); setShowMap(false); setShowHeatmap(false); setShowCorrMatrix(false)
        addLine({ text: '👽  MiauGlobe aliens unlocked!', className: 'text-green' })
        return
      }
      if (sub === '--cats' || sub === '-c') {
        try { sessionStorage.setItem('miau_globe_cats', '1') } catch {}
        setShowMiauMap(true); setShowMap(false); setShowHeatmap(false); setShowCorrMatrix(false)
        addLine({ text: '🐱  MiauGlobe cats activated!', className: 'text-green' })
        return
      }
      if (sub === '--catarmy' || sub === '-ca') {
        try { sessionStorage.setItem('miau_globe_catarmy', '1') } catch {}
        setShowMiauMap(true); setShowMap(false); setShowHeatmap(false); setShowCorrMatrix(false)
        addLine({ text: '🐱🐱🐱  MiauGlobe cat army deployed! 🐱🐱🐱', className: 'text-green font-bold' })
        return
      }
      setShowMiauMap(prev => !prev)
      setShowMap(false); setShowHeatmap(false); setShowCorrMatrix(false)
      addLine({ text: showMiauMapRef.current ? 'MiauGlobe hidden' : '🌍  MiauGlobe — 3D cat globe activated!', className: 'text-green' })
      return
    }
    if (t === 'map2d') { setShowMap2D(prev => !prev); addLine({ text: showMap2D ? '2D globe hidden' : '2D globe visible', className: 'text-dim' }); return }
    if (t === 'miaubook') { setShowMiauBook(prev => !prev); addLine({ text: showMiauBook ? '📕 MiauBook closed' : '📕 MiauBook — social for cat traders 🐱', className: 'text-green' }); return }
    if (t.startsWith('chartz3d') || t.startsWith('chart3d')) {
      const parts = raw.split(/\s+/)
      const tk = (parts[1] || 'AAPL').toUpperCase()
      // Tier check: Pro required for 3D charts
      const tier = localStorage.getItem('miau_tier')
      if (tier !== 'pro' && tier !== 'enterprise') {
        addLine({ text: `💎 3D charts require Pro (€49.50/mo). Type 'billing upgrade' to upgrade.`, className: 'text-yellow' })
        return
      }
      setShowChart3D(tk)
      addLine({ text: `📈 Opening 3D chart for ${tk}...`, className: 'text-green' })
      return
    }
    if (t.startsWith('sheetz3d')) {
      const parts = raw.split(/\s+/)
      const tk = (parts[1] || 'AAPL').toUpperCase()
      const tier = localStorage.getItem('miau_tier')
      if (tier !== 'pro' && tier !== 'enterprise') {
        addLine({ text: `💎 3D IB dashboard requires Pro (€49.50/mo). Type 'billing upgrade' to upgrade.`, className: 'text-yellow' })
        return
      }
      setShowSheetz3D(tk)
      addLine({ text: `🏦 Opening 3D IB dashboard for ${tk}...`, className: 'text-green' })
      return
    }
    if (t.startsWith('compare3d')) {
      const parts = raw.split(/\s+/)
      const tks = parts.slice(1).filter(Boolean).map(s => s.toUpperCase())
      if (tks.length < 2) { addLine({ text: 'Usage: compare3d <ticker1> <ticker2> [...]', className: 'text-yellow' }); return }
      const tier = localStorage.getItem('miau_tier')
      if (tier !== 'pro' && tier !== 'enterprise') {
        addLine({ text: `💎 3D comparison requires Pro (€49.50/mo). Type 'billing upgrade' to upgrade.`, className: 'text-yellow' })
        return
      }
      setShowCompare3D(tks)
      addLine({ text: `📊 Comparing ${tks.join(' vs ')} in 3D...`, className: 'text-green' })
      return
    }
    if (t.startsWith('sheetz3d')) {
      const parts = raw.split(/\s+/)
      const tk = (parts[1] || 'AAPL').toUpperCase()
      setShowSheetz3D(tk)
      addLine({ text: `🏦 Opening 3D IB dashboard for ${tk}...`, className: 'text-green' })
      return
    }
    if (t === 'pricing' || t === 'billing' || t === 'subscription') {
      setShowPricing(prev => !prev)
      addLine({ text: showPricing ? '💰 pricing hidden' : '💰  pricing & billing — choose your plan', className: 'text-green' })
      return
    }
    if (t === 'rave' || t === 'rave --kittens') {
      setRaveMode(prev => !prev)
      addLine({ text: raveMode ? '🎵 rave mode off' : '🎵  RAVE MODE ACTIVATED — 🎶🌈🐱💫', className: 'text-purple font-bold' })
      return
    }
    if (t === 'yield' || t === 'treasury') {
      setShowTreasury(prev => !prev)
      addLine({ text: showTreasury ? '📈 yield curve hidden' : '📈  US Treasury Yield Curve — 1M to 30Y', className: 'text-green' })
      return
    }
    if (t === 'bonds' || t === 'globalbonds') {
      setShowBonds(prev => !prev)
      addLine({ text: showBonds ? '📊 bonds hidden' : '📊  Global Bond Yields — US, DE, UK, JP, IT', className: 'text-green' })
      return
    }
    if (t.startsWith('compare3d')) {
      const parts = raw.split(/\s+/)
      const tks = parts.slice(1).filter(Boolean).map(s => s.toUpperCase())
      if (tks.length < 2) { addLine({ text: 'Usage: compare3d <ticker1> <ticker2> [...]', className: 'text-yellow' }); return }
      setShowCompare3D(tks)
      addLine({ text: `📊 Comparing ${tks.join(' vs ')} in 3D...`, className: 'text-green' })
      return
    }
    if (t === 'courses' || t === 'learn' || t === 'education') {
      const sub = raw.split(/\s+/)[1]?.toLowerCase()
      if (sub === 'list') {
        addLine({ text: `📚  MIAU COURSES  (232 total)`, className: 'text-cyan' })
        addLine({ text: `══════════════════════════════════════════════`, className: 'text-dim' })
        const cats = [
          { name: '🐱 Getting Started', courses: ['Getting Started', 'Market Data Basics', 'Paper Trading', 'Miau Shell Maniac'] },
          { name: '📈 Markets', courses: ['Market Data Advanced', 'Global Markets', 'Commodities', 'Forex Trading', 'Emerging Markets'] },
          { name: '💼 Portfolio', courses: ['Portfolio Management', 'Asset Allocation', 'Risk Parity', 'Portfolio Construction Advanced'] },
          { name: '🔬 Analytics', courses: ['Technical Analysis', 'Advanced Analytics', 'Time Series Analysis', 'Quantitative Risk'] },
          { name: '🏦 Banking', courses: ['Investment Banking', 'Mergers & Acquisitions', 'Private Equity', 'Corporate Finance'] },
          { name: '🤖 AI', courses: ['AI Advisor', 'Machine Learning for Finance', 'Neural Networks', 'NLP in Finance'] },
          { name: '₿ Crypto', courses: ['Crypto & Blockchain', 'DeFi & Web3', 'NFTs & Digital Assets', 'Tokenomics'] },
          { name: '🌿 ESG', courses: ['ESG & Sustainability', 'Climate Risk', 'Regenerative Finance'] },
        ]
        for (const cat of cats) {
          addLine({ text: `  ${cat.name}`, className: 'text-green' })
          addLine({ text: `    ${cat.courses.join(' · ')}`, className: 'text-dim' })
        }
        addLine({ text: ``, className: '' })
        addLine({ text: `  Open http://localhost:5174 in browser to start learning`, className: 'text-yellow' })
        return
      }
      if (sub === 'search' || sub === 'find') {
        const q = raw.split(/\s+/).slice(2).join(' ')
        if (q) {
          window.open(`http://localhost:5174`, '_blank')
          addLine({ text: `🔍 Opening education platform — search for '${q}'`, className: 'text-green' })
          return
        }
      }
      window.open('http://localhost:5174', '_blank')
      addLine({ text: '📚 Opening education platform (232 courses) on port 5174...', className: 'text-green' })
      return
    }

    if (t === 'heatmap') {
      const next = !showHeatmap
      setShowHeatmap(next)
      setShowBenchmark(false)
      setShowMap(false)
      setShowCorrMatrix(false)
      setShowBenchmark(false)
      addLine({ text: next ? '🔥 heatmap visible' : 'heatmap hidden', className: 'text-dim' })
      if (next) {
        fetch('/api/v1/market/sectors')
          .then(r => r.json())
          .then(data => setSectorData(data || []))
          .catch(() => setSectorData([]))
      }
      return
    }
    if (t === 'devconsole' || t === 'developer') {
      setShowDevConsole(prev => !prev)
      setShowMap(false)
      setShowHeatmap(false)
      setShowCorrMatrix(false)
      setShowBenchmark(false)
      addLine({ text: showDevConsole ? 'dev console hidden' : 'dev console visible', className: 'text-dim' })
      return
    }
    if (t === 'admin' || t === 'adminconsole') {
      setShowAdminConsole(prev => !prev)
      setShowMap(false)
      setShowDevConsole(false)
      setShowHeatmap(false)
      setShowCorrMatrix(false)
      setShowBenchmark(false)
      addLine({ text: showAdminConsole ? 'admin panel hidden' : '🐱 admin panel visible — manage teams, billing, API keys', className: 'text-dim' })
      return
    }
    if (t === 'back') {
      setShowMap(false)
      setShowHeatmap(false)
      setShowCorrMatrix(false)
      setShowBenchmark(false)
      setShowDevConsole(false)
      addLine({ text: 'returned to terminal', className: 'text-dim' })
      return
    }
    if (t === 'exit') {
      addLine({ text: 'miau finance signing off...', className: 'text-dim' })
      addLine({ text: `  /\\_/\\\n ( x.x )\n  > ^ <   bye! 🐱\n`, className: 'text-yellow' })
      playCatSound('login')
      return
    }

    // Kittyland — panel management
    const parts2 = raw.split(/\s+/)
    const kittySub = parts2[1]?.toLowerCase()
    const addKittyPanel = (title: string, content: string, icon?: string) => {
      kittyIdRef.current++
      const id = `kitty-${kittyIdRef.current}`
      const existing = kittyPanels.length
      setKittyPanels(prev => [...prev, {
        id, title, content, icon: icon || '📦',
        x: 5 + (existing % 3) * 32, y: 8 + (existing % 3) * 10,
        w: 30, h: 40,
      }])
      addLine({ text: `🖥️  panel opened: "${title}" — type 'kitty' to manage`, className: 'text-green' })
    }
    const addKittyWebPanel = (title: string, url: string, icon?: string) => {
      kittyIdRef.current++
      const id = `web-${kittyIdRef.current}`
      const existing = kittyPanels.length
      setKittyPanels(prev => [...prev, {
        id, title, content: '', icon: icon || '🌐', url,
        x: 5 + (existing % 2) * 46, y: 5 + (existing % 2) * 8,
        w: 44, h: 55, refreshKey: 0,
      }])
      addLine({ text: `🖥️  web panel opened: "${title}" — type 'kitty' to manage`, className: 'text-green' })
    }
    if (t === 'kitty' || t === 'panels' || t === 'kittyland') {
      if (kittySub === 'clear' || kittySub === 'closeall') {
        setKittyPanels([])
        addLine({ text: '🖥️  all panels closed', className: 'text-dim' })
      } else if (kittySub === 'ls' || kittySub === 'list') {
        if (kittyPanels.length === 0) { addLine({ text: '🖥️  no open panels', className: 'text-dim' }); return }
        addLine({ text: `🖥️  Kittyland — ${kittyPanels.length} panel(s)`, className: 'text-cyan' })
        kittyPanels.forEach((p, i) => addLine({ text: `  ${i + 1}. ${p.icon} ${p.title}${p.url ? ' 🌐' : ''}${p.pinned ? ' 📌' : ''}`, className: 'text-dim' }))
      } else if (kittySub === 'close' && parts2[2]) {
        const idx = parseInt(parts2[2]) - 1
        if (idx >= 0 && idx < kittyPanels.length) {
          const removed = kittyPanels[idx]
          setKittyPanels(prev => prev.filter((_, i) => i !== idx))
          addLine({ text: `🖥️  closed: ${removed.title}`, className: 'text-dim' })
        } else addLine({ text: `❌ invalid panel index`, className: 'text-red' })
      } else {
        addLine({ text: `🐱 Kittyland — Floating Panels 🖥️`, className: 'text-cyan' })
        addLine({ text: `  kitty ls              List open panels`, className: 'text-dim' })
        addLine({ text: `  kitty close <n>        Close panel #n`, className: 'text-dim' })
        addLine({ text: `  kitty clear            Close all panels`, className: 'text-dim' })
        addLine({ text: `  panel <name>           Open web app as panel`, className: 'text-dim' })
        addLine({ text: `  panel list             List available web apps`, className: 'text-dim' })
        addLine({ text: `  price AAPL -p          Open price in a panel`, className: 'text-dim' })
        addLine({ text: `  chart AAPL -p          Open chart in a panel`, className: 'text-dim' })
        addLine({ text: `  technicals AAPL -p     Open technicals in a panel`, className: 'text-dim' })
        addLine({ text: `  news AAPL -p           Open news in a panel`, className: 'text-dim' })
        addLine({ text: `  cmd1 | cmd2            Pipe output between commands`, className: 'text-dim' })
      }
      return
    }

    // 📺 Panel command — open web apps as floating iframe panels
    const WEB_APPS: Record<string, { name: string; url: string; icon: string }> = {
      terminal:  { name: 'Terminal',  url: 'http://localhost:5173', icon: '💻' },
      education: { name: 'Education', url: 'http://localhost:5174', icon: '🎓' },
      ecosystem: { name: 'Ecosystem', url: 'http://localhost:5175', icon: '🏢' },
      marketing: { name: 'Marketing', url: 'http://localhost:5176', icon: '📊' },
      desk:      { name: 'Service Desk', url: 'http://localhost:5180', icon: '🚒' },
      auth:      { name: 'Pawdenity', url: 'http://localhost:5190', icon: '🐾' },
      grafana:   { name: 'Grafana',   url: 'http://localhost:3000',  icon: '📈' },
      homepage:  { name: 'Homepage',  url: 'http://localhost:3001',  icon: '🚀' },
    }
    if (t === 'panel' || t === 'web' || t === 'app') {
      if (kittySub === 'list' || kittySub === 'ls' || !kittySub) {
        addLine({ text: `🌐  Available web apps (panel <name>)`, className: 'text-cyan' })
        for (const [key, app] of Object.entries(WEB_APPS)) {
          addLine({ text: `  ${app.icon}  ${key.padEnd(14)} ${app.url}`, className: 'text-dim' })
        }
        return
      }
      const app = WEB_APPS[kittySub]
      if (app) {
        addKittyWebPanel(app.name, app.url, app.icon)
      } else if (kittySub.startsWith('http://') || kittySub.startsWith('https://')) {
        addKittyWebPanel(kittySub, kittySub, '🌐')
      } else {
        addLine({ text: `❌ unknown app: "${kittySub}" — type 'panel list'`, className: 'text-red' })
      }
      return
    }

    if (t === 'correlation') {
      const next = !showCorrMatrix
      setShowCorrMatrix(next)
      setShowMap(false)
      setShowHeatmap(false)
      setShowDevConsole(false)
      addLine({ text: next ? '📊 correlation matrix visible' : 'correlation hidden', className: 'text-dim' })
      if (next) {
        fetch('/api/v1/economics/correlation')
          .then(r => r.json())
          .then(data => {
            if (data.correlation_matrix) {
              setCorrData({ tickers: data.tickers, matrix: data.correlation_matrix })
            }
          })
          .catch(() => setCorrData(null))
      }
      return
    }
    if (t === 'benchmark') {
      const next = !showBenchmark
      setShowBenchmark(next)
      setShowMap(false)
      setShowHeatmap(false)
      setShowCorrMatrix(false)
      setShowDevConsole(false)
      addLine({ text: next ? '📈 benchmark comparison visible' : 'benchmark hidden', className: 'text-dim' })
      return
    }
    if (t === 'scorecard') {
      addLine({ text: `🏆 MIAU FINANCE SCORECARD 🏆`, className: 'text-green' })
      addLine({ text: `🐟 Fish Earned:  ${cmdCount} commands executed`, className: 'text-cyan' })
      addLine({ text: `😺 Purr Meter:   98% uptime`, className: 'text-green' })
      addLine({ text: `🐱 Cat Lives:    9 (0 errors today)`, className: 'text-yellow' })
      addLine({ text: `🎯 Whisker Quality:  ${Math.min(100, 85 + cmdCount)}% accuracy`, className: 'text-purple' })
      addLine({ text: `🐾 Paw Prints:   ${cmdCount * 3 + lines.length} lines of output`, className: 'text-dim' })
      addLine({ text: `\n${getCatEncouragement()}`, className: 'text-green' })
      playCatSound('achievement')
      return
    }
    if (t === 'split') {
      if (!embedded && onSplit) {
        onSplit()
        addLine({ text: 'split mode activated — Ctrl+B % for horizontal, Ctrl+B " for vertical', className: 'text-green' })
      } else {
        addLine({ text: 'split: already in embedded pane', className: 'text-dim' })
      }
      return
    }
    if (t === 'cat' || t === 'cat --pet' || t.startsWith('cat --') || t.startsWith('cat --')) {
      setCatCount(prev => prev + 1)
      const sub = raw.split(/\s+/)[1]?.toLowerCase()
      
      if (t === 'cat --pet' || sub === '--pet' || sub === '-p') {
        const purr = `
    /\\_/\\     🐾
   ( o.o )    purr...
     > ^ <
    /rrrr\\    rrrr purr~
   (  🐟  )
    \\_/\_/    mrrrrow~
`
        addLine({ text: purr, className: 'text-green' })
        addLine({ text: '🐱 The cat purrs happily. Tuna level: satisfied.', className: 'text-cyan' })
        return
      }
      if (sub === '--status' || sub === '-s') {
        const mood = catCount > 50 ? '😻 ecstatic' : catCount > 20 ? '😸 happy' : catCount > 5 ? '😺 friendly' : '🐱 neutral'
        addLine({ text: `🐱  CAT STATUS`, className: 'text-cyan' })
        addLine({ text: `══════════════════════════`, className: 'text-dim' })
        addLine({ text: `  Mood:      ${mood}`, className: catCount > 20 ? 'text-green' : 'text-dim' })
        addLine({ text: `  Commands:  ${catCount}`, className: 'text-green' })
        addLine({ text: `  Tuna:      🐟${Math.floor(catCount / 3)} cans`, className: 'text-yellow' })
        addLine({ text: `  Hunger:    ${catCount % 5 === 0 ? '🍽️ hungry!' : '😌 satisfied'}`, className: catCount % 5 === 0 ? 'text-red' : 'text-dim' })
        return
      }
      if (sub === '--feed' || sub === '-f') {
        addLine({ text: `  🐟 You feed the cat a tuna can.`, className: 'text-yellow' })
        addLine({ text: `  😸 The cat purrs loudly. Tuna +1.`, className: 'text-green' })
        return
      }
      if (sub === '--adopt' || sub === '-a') {
        addLine({ text: `  🐱  CONGRATULATIONS!`, className: 'text-cyan' })
        addLine({ text: `  You've adopted a Miau Finance terminal cat!`, className: 'text-green' })
        addLine({ text: `  Name:    ${['Whiskers', 'Mittens', 'Luna', 'Simba', 'Tiger', 'Felix', 'Neko', 'Sushi', 'Mochi', 'Oreo', 'Shadow', 'Pixel', 'Byte', 'Crypto', 'Tuna', 'Satoshi', 'Nakamoto', 'Elon Purrs', 'Warren Buffet', 'Benjamin Graham'][Math.floor(Math.random() * 20)]}`, className: 'text-green' })
        addLine({ text: `  Color:   ${['orange', 'black', 'white', 'calico', 'tabby', 'tuxedo', 'siamese', 'persian', 'bengal', 'sphynx', 'russian blue', 'maine coon'][Math.floor(Math.random() * 12)]}`, className: 'text-dim' })
        addLine({ text: `  Hobby:   judging your trades`, className: 'text-dim' })
        addLine({ text: `  `, className: '' })
        addLine({ text: `  🐱 Your cat is now watching your portfolio. Trade well.`, className: 'text-yellow' })
        localStorage.setItem('miau_cat_adopted', 'true')
        return
      }
      
      if (sub === '--fortune' || sub === '-f' || sub === '--wisdom' || sub === '-w') {
        const fortunes = [
          "🐱 'The early cat catches the best stocks. But the lazy cat inherits the world.'",
          "🐱 'A diversified portfolio is like a litter box — you need variety, but it all ends up smelling the same.'",
          "🐱 'HODL is just 'HOLD' with extra letters, just like cats have extra toes.'",
          "🐱 'The market is like a laser pointer — you'll chase it all day and never catch it.'",
          "🐱 'Buy the dip. Sell the rip. Nap in between.'",
          "🐱 'Your portfolio is down? Have you tried purring at it?'",
          "🐱 'The best time to invest was yesterday. The second best time is after your nap.'",
          "🐱 'A cat always lands on its feet. Your portfolio will too. Eventually.'",
          "🐱 'Fear and Greed index? The cat only knows the Tuna index.'",
          "🐱 'Technical analysis is astrology for programmers. The cat approves of both.'",
          "🐱 'The stock market was invented by a cat who wanted to trade tuna futures.'",
          "🐱 'If you can't beat the market, join the cat.'",
          "🐱 'Dollar-cost averaging: buying the dip repeatedly until you run out of dollars.'",
          "🐱 'The bull market climbs a wall of worry. The cat climbs the curtains.'",
          "🐱 'Never invest more than you're willing to lose. The cat never invests. The cat always wins.'",
          "🐱 'A bull market makes you look like a genius. A bear market reveals the cat was running the show all along.'",
          "🐱 'The four stages of a market cycle: hope, growth, euphoria, and \"the cat saw this coming.\"'",
          "🐱 'Correlation does not imply causation. But have you noticed: when cats nap, markets rally?'",
          "🐱 'They say money can't buy happiness. But it can buy tuna, which is basically the same thing.'",
          "🐱 'The stock market is a device for transferring money from the impatient to the cat.'",
          "🐱 'I don't need a financial advisor. I have whiskers. Whiskers detect air currents AND market trends.'",
          "🐱 'Your exit strategy should be: buy, hold, purr, repeat.'",
          "🐱 'The cat slept through the 2008 crash. The cat will sleep through the next one too. Be the cat.'",
          "🐱 'Dead cat bounce? More like \"cat is just resting its eyes.\"'",
          "🐱 'Every portfolio needs a cat. Cats are naturally diversified — nine lives, nine sectors.'",
          "🐱 'Alpha is what you get when you rub a cat's belly. Beta is what you get when you try.'",
          "🐱 'Liquidity is important. The cat can liquidate a tuna can in under 3 seconds.'",
          "🐱 'Dividends are like getting pet — a steady stream of confirmation that you're doing it right.'",
          "🐱 'The cat does not rebalance. The cat simply acquires more tuna until balance is achieved.'",
        ]
        addLine({ text: fortunes[Math.floor(Math.random() * fortunes.length)], className: 'text-green' })
        return
      }
      
      if (sub === '--dance' || sub === '-d') {
        const dance = [
          `
        /\\_/\\     🎵
       ( ⌒.⌒ )    ~
        >   <    ♪♫
       /    \\
      (  🐟  )
       \\_/\\_/   dance~
       `,
       `
        /\\_/\\     ♪♫♬
       ( ◕‿◕)    ─=≡Σ
        >   <    🐟
       ─=≡Σ
      `]
        for (const d of dance) {
          addLine({ text: d, className: 'text-yellow' })
        }
        addLine({ text: '🐱 The cat is dancing! Tuna disco! 🐟🎵', className: 'text-cyan' })
        return
      }
      
      if (sub === '--gang' || sub === '-g') {
        const gang = `
       🐱 🐱 🐱 🐱 🐱
      /\\_/\\\\_/\\\\_/\\\\_/\\\\_/\\
     ( o.o)(o.o)(o.o)(o.o)(o.o)
      > ^ < > ^ < > ^ < > ^ < > ^ <
     /🐟  \\/🐟  \\/🐟  \\/🐟  \\/🐟  \\
    (______)(______)(______)(______)(______)
        `
        addLine({ text: gang, className: 'text-yellow' })
        addLine({ text: '🐱🐱🐱 THE MIAU GANG ROLLS DEEP 🐱🐱🐱', className: 'text-cyan' })
        return
      }
      
      if (sub === '--party' || sub === '-y') {
        for (let i = 0; i < 5; i++) {
          const cat = CAT_ASCII[Math.floor(Math.random() * CAT_ASCII.length)]
          addLine({ text: cat + '  🎉  🐟  🎊  ✨', className: ['text-yellow', 'text-cyan', 'text-green', 'text-purple', 'text-red'][i] })
        }
        addLine({ text: '🎉🐱 PARTY CATS! EVERYONE GETS TUNA! 🐟🎉', className: 'text-yellow' })
        return
      }
      
      // Default: random cat
      const cat = CAT_ASCII[Math.floor(Math.random() * CAT_ASCII.length)]
      const miaus = ['miau!', 'meow~', 'nya~', 'MIAU!', 'purr...', 'mrrow!', 'mew']
      addLine({ text: cat, className: 'text-yellow' })
      addLine({ text: miaus[Math.floor(Math.random() * miaus.length)], className: 'text-green' })
      return
    }
    if (t === 'dashboard') {
      setShowDashboard(prev => !prev)
      setShowMap(false)
      setShowMiauMap(false)
      setShowCatberg(false)
      addLine({ text: showDashboardRef.current ? 'dashboard closed' : '📊  dashboard opened', className: 'text-green' })
      return
    }
    
    setLoading(true)
    try {
      // Kittyland: capture output for --panel / -p flag
      const wantsPanel = raw.includes(' --panel') || raw.includes(' -p')
      const cmdForExec = wantsPanel ? raw.replace(/ --panel/g, '').replace(/ -p/g, '').trim() : raw
      const capturedLines: string[] = []
      const capturingAddLine = wantsPanel ? (line: any) => {
        capturedLines.push(typeof line === 'string' ? line : line.text || '')
        addLine(line)
      } : addLine
      
      await executeCommand(cmdForExec, capturingAddLine)
      
      if (wantsPanel && capturedLines.length > 0) {
        const baseCmd = cmdForExec.split(/\s+/)[0].toUpperCase()
        const content = capturedLines.map(l => l.replace(/<[^>]*>/g, '')).join('\n')
        addKittyPanel(`${baseCmd} ${cmdForExec.split(/\s+/).slice(1).join(' ')}`, content, '📊')
      }
      
      const baseCmd = t.split(/\s+/)[0].toLowerCase()
      recordCommand(baseCmd)
      const unlocked = updateAchievementState({ numCommandsExecuted: cmdCount + 1 })
      if (unlocked.length > 0) {
        setAchievementToast(unlocked[0])
        setTimeout(() => setAchievementToast(null), 4000)
      }
      // Random cat reaction (10% chance)
      if (Math.random() < 0.1 && baseCmd !== 'cat') {
        const reactions = [
          '🐱 The cat approves of this trade.',
          '🐱 *nods wisely* Solid move.',
          '🐱 *judges your portfolio silently*',
          '🐱 *licks paw* Acceptable.',
          '🐱 \'I could\'ve done better with my eyes closed.\'',
          '🐱 *ears perk up* Tuna? Did someone say tuna?',
          '🐱 *purrs* The fundamentals look good.',
          '🐱 \'Sell? I only know how to buy more tuna.\'',
          '🐱 \'Your gains are... adequate.\'',
          '🐱 \'This is fine. The cat is fine.\'',
          '🐱 *stares at screen* \'Do I look like I care about beta?\'',
          '🐱 \'I see you\'re up 2%. That\'s one can of tuna.\'',
        ]
        addLine({ text: reactions[Math.floor(Math.random() * reactions.length)], className: 'text-dim' })
      }
      const url = EDU_LINKS[baseCmd]
      if (url) {
        addLine({
          html: true,
          text: `<span class="text-dim" style="font-size:11px">[<a href="${url}" target="_blank" rel="noopener noreferrer" class="edu-link">learn more →</a>]</span>`,
        })
      }
      playCatSound('trade')
    } catch (e: any) {
      addLine({ text: `error: ${e.message}`, className: 'text-red' })
      playCatSound('error')
    }
    setLoading(false)
    addLine({ text: '', className: '' })
  }, [addLine, showMap, catCount, cmdCount, lines.length])

  const getHistory = (): string[] => {
    try {
      const raw = localStorage.getItem('miau_command_recency')
      return raw ? JSON.parse(raw) : []
    } catch { return [] }
  }

  // 🔐 pawdentity: submit the masked password. The password is only used
  // inside the login() call — never echoed, stored, or added to history.
  const handlePasswordSubmit = useCallback(async (username: string, password: string) => {
    try {
      const { login: doLogin } = await import('../lib/auth')
      const data = await doLogin(username, password)
      const role = data.role || 'user'
      try { localStorage.setItem('miau_tier', 'free') } catch {}
      addLine({ text: `✅ logged in as ${username} (${role})`, className: 'text-green' })
    } catch (e: any) {
      addLine({ text: `❌ login failed: ${e.message || e}`, className: 'text-red' })
    }
  }, [addLine])

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Tab') {
      e.preventDefault()
      if (pwPrompt) return // no command autocomplete while entering credentials
      const matches = getSuggestions(input, 10)
      if (matches.length === 1) {
        const parts = input.split(/\s+/)
        if (parts.length === 1) {
          setInput(matches[0].text + ' ')
        } else {
          parts[parts.length - 1] = matches[0].text
          setInput(parts.join(' '))
        }
        setSuggestions([])
      } else if (matches.length > 1) {
        setSuggestions(matches.map(m => `${m.text}${m.description ? `  (${m.description})` : ''}`))
      } else {
        setSuggestions([])
      }
      return
    }

    if (e.key === 'Escape') {
      if (pwPrompt) { // cancel the login prompt
        setPwPrompt(null)
        setInput('')
      }
      setSuggestions([])
      return
    }

    if (e.key === 'h' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault()
      setShowShortcuts(prev => !prev)
      return
    }

    if (e.key === 'Escape' && showShortcuts) {
      setShowShortcuts(false)
      return
    }

    if (e.key === 'Enter') {
      if (pwPrompt?.mode === 'username') {
        e.preventDefault()
        const username = input.trim()
        if (!username) return // ignore empty username
        setPwPrompt({ mode: 'password', username })
        setInput('')
        setSuggestions([])
        return
      }
      if (pwPrompt?.mode === 'password') {
        e.preventDefault()
        const password = input
        const username = pwPrompt.username
        setInput('')
        setPwPrompt(null)
        setSuggestions([])
        void handlePasswordSubmit(username, password)
        return
      }
      handleCommand(input)
      setInput('')
      setSuggestions([])
      return
    }

    if (e.key === 'ArrowUp') {
      e.preventDefault()
      setSuggestions([])
      if (pwPrompt) return // never inject history into a username/password field
      if (history.length) {
        const i = Math.min(historyIdx + 1, history.length - 1)
        setHistoryIdx(i)
        setInput(history[i])
      }
      return
    }

    if (e.key === 'ArrowDown') {
      e.preventDefault()
      setSuggestions([])
      if (pwPrompt) return
      if (historyIdx > 0) {
        const i = historyIdx - 1
        setHistoryIdx(i)
        setInput(history[i])
      } else {
        setHistoryIdx(-1)
        setInput('')
      }
      return
    }
  }

  const uptime = Math.floor((Date.now() - startTime) / 1000)
  const uptimeStr = `${Math.floor(uptime / 3600)}h ${Math.floor((uptime % 3600) / 60)}m`

  const handleVoiceClick = useCallback(() => {
    if (voiceActive) {
      recognitionRef.current?.stop()
      setVoiceActive(false)
      return
    }
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    if (!SpeechRecognition) {
      addLine({ text: '❌ voice input not supported in this browser', className: 'text-red' })
      return
    }
    const rec = new SpeechRecognition()
    rec.continuous = false
    rec.interimResults = false
    rec.lang = 'en-US'
    rec.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript
      setInput(transcript)
      setTimeout(() => handleCommand(transcript), 100)
    }
    rec.onend = () => setVoiceActive(false)
    rec.onerror = () => {
      addLine({ text: '🎤 voice input requires a page interaction first (click anywhere)', className: 'text-yellow' })
      setVoiceActive(false)
    }
    try {
      rec.start()
      recognitionRef.current = rec
      setVoiceActive(true)
      addLine({ text: '🎤 listening...', className: 'text-dim' })
    } catch {
      setVoiceActive(false)
    }
  }, [voiceActive, recognitionRef, setVoiceActive, setInput, handleCommand, addLine])

  return (
    <Fragment>
    <div
      className="flex flex-col h-screen w-screen overflow-hidden crt terminal-root"
      style={{ background: theme.colors.bg }}
      role="application"
      aria-label="Miau Finance Terminal"
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
    >
      {/* Skip to terminal input for screen readers */}
      <a
        href="#terminal-input"
        className="absolute -top-10 left-2 z-[9999] bg-green text-black px-3 py-1 rounded text-xs font-mono focus:top-2 transition-all"
        aria-label="Skip to terminal input"
      >
        Skip to terminal
      </a>

      {/* Status Bar */}
      <SlideIn direction="down" duration={400}>
        <div className="flex items-center justify-between px-2 py-1 text-xs sm:px-3 sm:py-1 status-bar" style={{ background: theme.colors.bgSecondary, borderBottom: `1px solid ${theme.colors.border}` }} role="status" aria-label="Status bar">
          <div className="flex items-center gap-2 sm:gap-3 flex-wrap">
            <span className="text-green font-bold text-glow-green text-[10px] sm:text-xs" style={{letterSpacing: '0.05em'}}>🐱 MIAU</span>
            <span className="text-dim text-[10px] sm:text-xs">v0.8.0</span>
            <ConnectionDot connected={connected} />
            <span className="text-dim text-[10px] sm:text-xs">|</span>
            <span className="text-dim text-[10px] sm:text-xs">cmd#{cmdCount}</span>
            <span className="text-yellow text-[10px] sm:text-xs" title="tuna earned">🐟{Math.floor(cmdCount / 3)}</span>
            <span className="text-dim text-[10px] sm:text-xs">↑ {uptimeStr}</span>
          </div>
          <div className="flex items-center gap-1 sm:gap-2 flex-wrap justify-end">
            {clock && <span className="text-dim" style={{fontSize:9}}>{clock}</span>}
            {showMap && <span className="text-green text-glow-green" style={{fontSize:8}}>🌍</span>}
            {showHeatmap && <span className="text-orange" style={{fontSize:8}}>🔥</span>}
            {showCorrMatrix && <span className="text-cyan" style={{fontSize:8}}>📊</span>}
            {showBenchmark && <span className="text-green" style={{fontSize:8}}>📈</span>}
            {loading && <span className="text-yellow" style={{fontSize:8}}>⏳</span>}
            <select
              value={getCurrentLocale()}
              onChange={e => setLocale(e.target.value as any)}
              className="bg-transparent text-dim text-[9px] border border-gray-700 rounded px-1 py-0 outline-none cursor-pointer"
              style={{ fontFamily: 'inherit' }}
              aria-label="Language"
            >
              {SUPPORTED_LOCALES.map(l => (
                <option key={l} value={l} className="bg-gray-900 text-gray-300">{LOCALE_NATIVE[l as keyof typeof LOCALE_NATIVE]}</option>
              ))}
            </select>
            <span className="text-dim" style={{fontSize:9, cursor:'pointer'}} title="Ctrl+H for shortcuts" onClick={() => setShowShortcuts(s => !s)}>⌨️</span>
            <span className="text-dim font-bold" style={{fontSize:12, cursor:'pointer'}} title="Popular commands" onClick={() => setShowCmdDiscovery(s => !s)}>?</span>
          </div>
        </div>
      </SlideIn>

      {/* Keyboard Shortcuts Overlay */}
      {showShortcuts && (
        <div
          className="absolute inset-0 z-50 flex items-center justify-center"
          style={{ background: 'rgba(10,26,20,0.92)', backdropFilter: 'blur(4px)' }}
          onClick={() => setShowShortcuts(false)}
        >
          <div className="glass-panel rounded-lg p-6 max-w-md" onClick={e => e.stopPropagation()}>
            <div className="text-green text-glow-green font-bold text-sm mb-3">⌨️ KEYBOARD SHORTCUTS</div>
            <div className="grid grid-cols-2 gap-x-6 gap-y-2 text-xs">
              {[
                ['Tab', 'Autocomplete command'],
                ['↑/↓', 'Command history'],
                ['Ctrl+H', 'Toggle this overlay'],
                ['Ctrl+L', 'Clear screen'],
                ['Esc', 'Close overlay'],
                ['Enter', 'Execute command'],
              ].map(([key, desc]) => (
                <div key={key} className="contents">
                  <span className="text-green font-semibold" style={{fontFamily: 'monospace'}}>{key}</span>
                  <span className="text-dim text-right">{desc}</span>
                </div>
              ))}
            </div>
            <div className="text-dim text-xs mt-4 text-center">click outside or press Esc to close</div>
          </div>
        </div>
      )}

      {/* Command Discovery Overlay */}
      {showCmdDiscovery && (
        <div
          className="absolute inset-0 z-50 flex items-center justify-center"
          style={{ background: 'rgba(10,26,20,0.92)', backdropFilter: 'blur(4px)' }}
          onClick={() => setShowCmdDiscovery(false)}
        >
          <div className="glass-panel rounded-lg p-5 max-w-sm" onClick={e => e.stopPropagation()}>
            <div className="text-green text-glow-green font-bold text-sm mb-3">🔥 POPULAR COMMANDS</div>
            <div className="space-y-2 text-xs">
              {[
                ['price AAPL', 'Get real-time asset price'],
                ['portfolio', 'View your portfolio'],
                ['map', 'Toggle interactive world map'],
                ['search', 'Search assets and markets'],
                ['cat', 'Summon a random cat ASCII'],
              ].map(([cmd, desc]) => (
                <div key={cmd} className="flex items-start gap-2">
                  <span className="text-green font-semibold shrink-0" style={{fontFamily: 'monospace'}}>{cmd}</span>
                  <span className="text-dim">{desc}</span>
                </div>
              ))}
            </div>
            <div className="text-dim text-xs mt-4 text-center">click outside or press Esc to close</div>
          </div>
        </div>
      )}

      {/* Achievement Toast */}
      {achievementToast && (
        <div className="fixed top-16 left-1/2 z-50" style={{
          background: 'rgba(10,26,46,0.95)',
          border: '2px solid #00ff88',
          borderRadius: '8px',
          padding: '8px 16px',
          fontFamily: '"JetBrains Mono", monospace',
          boxShadow: '0 0 20px rgba(0,255,136,0.3)',
          transform: 'translateX(-50%)',
          animation: 'slideDown 0.4s ease-out',
        }}>
          <div className="flex items-center gap-2">
            <span className="text-xl">{achievementToast.icon}</span>
            <div>
              <div className="text-xs text-yellow font-bold">{achievementToast.title}</div>
              <div className="text-[10px] text-dim">{achievementToast.description}</div>
            </div>
          </div>
          <style>{`
            @keyframes slideDown {
              from { opacity: 0; transform: translateX(-50%) translateY(-20px); }
              to { opacity: 1; transform: translateX(-50%) translateY(0); }
            }
          `}</style>
        </div>
      )}

      {/* Main Content */}
       <div className="flex flex-1 overflow-hidden relative">
          {/* Map Layer */}
         <div
           className="absolute inset-0 z-20"
             style={{ opacity: 1, transition: 'opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1)' }}
           >
              {showMap && <WorldMap onClose={() => setShowMap(false)} active={showMap} />}
             {showMiauMap && <Suspense fallback={null}><MiauGlobe onClose={() => setShowMiauMap(false)} active={showMiauMap} /></Suspense>}
             {showChart3D && <Chart3D ticker={showChart3D} onClose={() => setShowChart3D(null)} />}
             {showSheetz3D && <Sheetz3D ticker={showSheetz3D} onClose={() => setShowSheetz3D(null)} />}
             {showCompare3D && <Compare3D tickers={showCompare3D} onClose={() => setShowCompare3D(null)} />}
              {showPricing && <PricingPage />}
              <RaveOverlay active={raveMode} />
              {showTreasury && <TreasuryChart onClose={() => setShowTreasury(false)} />}
              {showBonds && <BondChart onClose={() => setShowBonds(false)} />}
           </div>

          {/* Map2D Layer (canvas globe backup) */}
          <div className="absolute inset-0 z-20">
            {showMap2D && <Map2D onClose={() => setShowMap2D(false)} active={showMap2D} />}
          </div>
         
           {/* Heatmap Layer */}
          <div
            className="absolute inset-0 z-20"
            style={{
              opacity: showHeatmap ? 1 : 0,
              transition: 'opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1)',
              pointerEvents: showHeatmap ? 'auto' : 'none',
            }}
          >
            <Heatmap data={sectorData} width={400} height={300} />
          </div>

          {/* Developer Console Layer */}
          <div
            className="absolute inset-0 z-0 overflow-y-auto"
            style={{
              opacity: showDevConsole ? 1 : 0,
              transition: 'opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
              pointerEvents: showDevConsole ? 'auto' : 'none',
            }}
          >
            <DeveloperConsole />
          </div>

          {/* Admin Console Layer */}
          {showAdminConsole && (
            <div className="absolute inset-0 z-30 overflow-y-auto">
              <div className="absolute top-2 right-2 z-40">
                <button onClick={() => setShowAdminConsole(false)} className="text-dim text-xs border border-dim/20 px-2 py-1 rounded hover:text-green hover:border-green/30">✕ Close Admin</button>
              </div>
              <AdminConsole />
            </div>
          )}

          {/* MiauBook Layer */}
          {showMiauBook && <MiauBook onClose={() => setShowMiauBook(false)} active={showMiauBook} />}

          {/* Tuna Wallet - always visible */}
          <TunaWallet />

          {/* Correlation Matrix Layer */}
          <div
            className="absolute inset-0 z-0 overflow-y-auto"
            style={{
              opacity: showCorrMatrix ? 1 : 0,
              transition: "opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1)",
              pointerEvents: showCorrMatrix ? "auto" : "none",
            }}
          >
            {corrData ? (
              <CorrelationMatrix tickers={corrData.tickers} matrix={corrData.matrix} />
            ) : (
              <div className="p-4 text-dim text-sm">Loading correlation data...</div>
            )}
          </div>

          {/* Benchmark Comparison Layer */}
          <div
            className="absolute inset-0 z-0 overflow-y-auto"
            style={{
              opacity: showBenchmark ? 1 : 0,
              transition: "opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1)",
              pointerEvents: showBenchmark ? "auto" : "none",
            }}
          >
            <BenchmarkComparison />
          </div>

          {/* Terminal Layer */}
         <div
           ref={containerRef}
           className="flex flex-col flex-1 z-10 overflow-hidden"
           role="log"
           aria-live="polite"
           aria-label="Terminal output"
           style={{
             background: showMap ? `${theme.colors.bg}e0` : theme.colors.bg,
             transition: 'background 500ms cubic-bezier(0.16, 1, 0.3, 1)',
           }}
          onClick={() => inputRef.current?.focus()}
        >
          {/* Output Area */}
          <div className="flex-1 overflow-y-scroll px-4 py-2 font-mono text-sm leading-relaxed terminal-output" style={{ overscrollBehavior: 'contain', WebkitOverflowScrolling: 'touch' }}>
            {lines.map((line, i) => (
              <FadeIn key={i} duration={250} delay={i === lines.length - 1 ? 0 : Math.min(i * 10, 100)}>
                {line.html
                  // 🔒 SECURITY FIX: Use sanitized HTML instead of dangerous innerHTML
                  ? <div className="whitespace-pre-wrap break-all" dangerouslySetInnerHTML={{ __html: sanitizeHtml(line.text) }} />
                  : <div className={`whitespace-pre-wrap break-all ${line.className || ''} terminal-line`}>{line.text}</div>
                }
              </FadeIn>
            ))}

            {loading && (
              <div className="text-dim flex items-center gap-2 py-1">
                <CatLoader type="paws" size="sm" message="" />
                <span style={{marginLeft: 4}}>processing...</span>
              </div>
            )}

            {suggestions.length > 0 && (
              <div className="text-dim py-1">
                {suggestions.join('  ')}
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          {/* Ctrl+R History Search */}
          {showHistorySearch && (
            <div className="px-4 py-2 border-t" style={{ borderColor: theme.colors.border, background: 'rgba(0,20,40,0.95)' }}>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-yellow text-xs font-mono">🔍 history search</span>
                <span className="text-dim text-[10px]">(Ctrl+R — Esc to close)</span>
              </div>
              <input
                autoFocus
                type="text"
                value={historyQuery}
                onChange={e => setHistoryQuery(e.target.value)}
                onKeyDown={e => {
                  if (e.key === 'Escape') { setShowHistorySearch(false); setHistoryQuery('') }
                  if (e.key === 'Enter') {
                    const q = historyQuery.toLowerCase()
                    const cmds = getHistory()
                    const match = cmds.find(c => c.toLowerCase().includes(q))
                    if (match) { setInput(match); inputRef.current?.focus() }
                    setShowHistorySearch(false)
                    setHistoryQuery('')
                  }
                }}
                className="flex-1 bg-transparent border border-gray-700/50 rounded px-2 py-1 outline-none font-mono text-sm"
                style={{ color: theme.colors.green }}
                placeholder="search command history..."
              />
              <div className="max-h-32 overflow-y-auto mt-1 space-y-0.5 text-xs font-mono">
                {getHistory().filter(c => !historyQuery || c.toLowerCase().includes(historyQuery.toLowerCase())).slice(0, 8).map((c, i) => (
                  <div key={i} className="text-dim hover:text-green cursor-pointer px-1" onClick={() => { setInput(c); setShowHistorySearch(false); setHistoryQuery(''); inputRef.current?.focus() }}>
                    {c}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Input Area */}
          <TerminalInput
            input={input}
            setInput={setInput}
            pwPrompt={pwPrompt}
            suggestions={suggestions}
            handleKey={handleKey}
            onVoiceClick={handleVoiceClick}
            voiceActive={voiceActive}
            inputRef={inputRef}
            theme={theme}
          />
        </div>
      </div>
      {showPalette && (
        <CommandPalette
          onSelect={(cmd) => { handleCommand(cmd); setInput(''); setHistoryIdx(-1) }}
          onClose={() => setShowPalette(false)}
        />
      )}
      <CatCompanion />
    </div>
    {showCatberg && <Catberg />}
      {/* showDashboard && <Dashboard onClose={() => setShowDashboard(false)} /> */}
      <Kittyland panels={kittyPanels} 
        onClose={(id) => setKittyPanels(prev => prev.filter(p => p.id !== id))}
        onPin={(id) => setKittyPanels(prev => prev.map(p => p.id === id ? { ...p, pinned: !p.pinned } : p))}
        onClear={() => setKittyPanels([])}
        onRefresh={(id) => setKittyPanels(prev => prev.map(p => p.id === id ? { ...p, refreshKey: (p.refreshKey || 0) + 1 } : p))} />
    <style>{`
      .edu-link { color: inherit; text-decoration: none; transition: color 0.2s; }
      .edu-link:hover { color: #00ff88; text-decoration: underline; }
      @media (max-width: 640px) {
        .terminal-root { font-size: 13px; }
        .terminal-root .terminal-line { font-size: 12px; line-height: 1.3; }
        .terminal-root .px-4 { padding-left: 8px; padding-right: 8px; }
        .terminal-root .py-2 { padding-top: 4px; padding-bottom: 4px; }
        #terminal-input { font-size: 14px !important; }
        .terminal-root .gap-3 { gap: 6px; }
        .crt { overflow-x: hidden; }
        .terminal-root .text-xs { font-size: 10px; }
      }
      @media (max-width: 380px) {
        .terminal-root { font-size: 12px; }
        .terminal-root .terminal-line { font-size: 11px; }
        #terminal-input { font-size: 13px !important; }
      }
    `}</style>
      <CookieBanner />
    </Fragment>
  )
}

// ConnectionDot imported from ./terminal/ConnectionDot
// escapeHtml imported from ../lib/commands/shared


