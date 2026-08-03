import { useState, useEffect, useCallback } from 'react'

const STEPS = [
  {
    title: 'Welcome to Miau Finance',
    icon: '🐱',
    description: 'Your cat-powered financial analytics terminal. Type commands, explore markets, and manage portfolios.',
  },
  {
    title: 'Type or Tap',
    icon: '⌨️',
    description: 'Type any command at the prompt, or use quick actions from the bottom nav. Try "help" to see all commands.',
  },
  {
    title: 'Swipe & Explore',
    icon: '📊',
    description: 'Swipe left for command history, tap ↑↓ to recall past commands. The terminal is your command center.',
  },
]

const STORAGE_KEY = 'miau:onboarding_seen'

export default function MobileOnboarding() {
  const [step, setStep] = useState(0)
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const seen = localStorage.getItem(STORAGE_KEY)
    if (!seen && window.innerWidth < 768) {
      setVisible(true)
    }
  }, [])

  const dismiss = useCallback(() => {
    localStorage.setItem(STORAGE_KEY, '1')
    setVisible(false)
  }, [])

  const next = useCallback(() => {
    if (step < STEPS.length - 1) {
      setStep(s => s + 1)
    } else {
      dismiss()
    }
  }, [step, dismiss])

  if (!visible) return null

  const s = STEPS[step]

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center" style={{ background: 'rgba(10,26,20,0.95)' }}>
      <div className="glass-panel rounded-2xl p-6 mx-4 max-w-sm w-full text-center">
        <div className="text-5xl mb-4">{s.icon}</div>
        <h2 className="text-green text-lg font-bold mb-2">{s.title}</h2>
        <p className="text-dim text-sm mb-6 leading-relaxed">{s.description}</p>

        <div className="flex justify-center gap-2 mb-6">
          {STEPS.map((_, i) => (
            <div
              key={i}
              className={`w-2 h-2 rounded-full transition-colors ${
                i === step ? 'bg-green' : 'bg-[#1a3a2a]'
              }`}
            />
          ))}
        </div>

        <div className="flex gap-3">
          <button
            onClick={dismiss}
            className="flex-1 px-4 py-2 text-xs rounded border border-[#1a3a2a] text-dim hover:text-green hover:border-green/30 transition-colors"
          >
            Skip
          </button>
          <button
            onClick={next}
            className="flex-1 px-4 py-2 text-xs rounded border border-green text-green hover:bg-green/10 transition-colors font-semibold"
          >
            {step < STEPS.length - 1 ? 'Next' : 'Get Started'}
          </button>
        </div>
      </div>
    </div>
  )
}
