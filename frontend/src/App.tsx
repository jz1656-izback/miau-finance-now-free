import { useState, useEffect } from 'react'
import Terminal from './components/Terminal'
import SplitTerminal from './components/SplitTerminal'
import ErrorBoundary from './components/ErrorBoundary'
import OfflineHandler from './components/OfflineHandler'
import BottomNav from './components/BottomNav'
import PwaUpdate from './components/PwaUpdate'
import MobileOnboarding from './components/MobileOnboarding'
import InstallPrompt from './components/mobile/InstallPrompt'
import DarkModeToggle from './components/mobile/DarkModeToggle'
import BillingSuccess from './components/BillingSuccess'
import BillingCancel from './components/BillingCancel'

export default function App() {
  const [splitMode, setSplitMode] = useState(false)
  const [page, setPage] = useState<'terminal' | 'success' | 'cancel'>('terminal')
  const isMobile = window.innerWidth < 768

  useEffect(() => {
    const path = window.location.pathname
    if (path === '/billing/success') setPage('success')
    else if (path === '/billing/cancel') setPage('cancel')
    // Restore clean URL in address bar without reload
    if (path === '/billing/success' || path === '/billing/cancel') {
      window.history.replaceState(null, '', '/')
    }
  }, [])

  const [showAnnouncement, setShowAnnouncement] = useState(() => {
    try { return !localStorage.getItem('miau_announcement_ib') } catch { return true }
  })

  const dismissAnnouncement = () => {
    setShowAnnouncement(false)
    try { localStorage.setItem('miau_announcement_ib', 'dismissed') } catch {}
  }

  if (page === 'success') return <BillingSuccess />
  if (page === 'cancel') return <BillingCancel />

  return (
    <ErrorBoundary>
      <OfflineHandler>
        <div className="absolute top-0 left-0 right-0 z-20 flex justify-end gap-4 px-4 py-1 bg-transparent">
          <a href="http://localhost:5174" target="_blank" className="text-[10px] text-green-500/50 hover:text-green-400 font-mono transition-colors">🎓 Learn</a>
          <a href="http://localhost:5175" target="_blank" className="text-[10px] text-green-500/50 hover:text-green-400 font-mono transition-colors">🏠 Ecosystem</a>
        </div>
        {showAnnouncement && (
          <div
            className="fixed top-0 left-0 right-0 z-30 flex items-center justify-center gap-2"
            style={{
              height: 36,
              background: 'linear-gradient(90deg, rgba(0,255,136,0.12), rgba(0,200,100,0.08))',
              borderBottom: '1px solid rgba(0,255,136,0.25)',
              fontFamily: '"JetBrains Mono", monospace',
              fontSize: 11,
            }}
          >
            <span>🐱💨</span>
            <span className="text-green">Miau Finance — Bloomberg for Cats. Free for Humans. €49.50/mo for the tuna.</span>
            <a href="http://localhost:5175" target="_blank" rel="noopener noreferrer" className="text-dim hover:text-green underline ml-1">learn more →</a>
            <button onClick={dismissAnnouncement} className="ml-2 text-dim hover:text-white" style={{ fontSize: 16, lineHeight: 1 }} aria-label="Dismiss">×</button>
          </div>
        )}
        <div className="fixed top-2 right-2 z-40">
          <DarkModeToggle />
        </div>
        {splitMode ? (
          <div className="scanline crt" style={{ minHeight: '100vh', background: '#0a0a0a' }}>
            <SplitTerminal />
          </div>
        ) : (
          <div className="scanline crt flex flex-col" style={{ minHeight: '100vh', background: '#0a0a0a' }}>
            <div className="flex-1">
              <Terminal onSplit={() => setSplitMode(true)} />
            </div>
            {isMobile && <BottomNav />}
          </div>
        )}
        <PwaUpdate />
        <InstallPrompt />
        <MobileOnboarding />
      </OfflineHandler>
    </ErrorBoundary>
  )
}
