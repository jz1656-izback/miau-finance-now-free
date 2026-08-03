import { useState, useRef, useEffect } from 'react'
import type { Lesson } from '../lib/types'
import { executeTerminalCommand, getCSRFToken, getPawdentitySession } from '../lib/api'

interface Props {
  lesson: Lesson
  initialCommand?: string
  onBack: () => void
}

export function TerminalSimulator({ lesson, initialCommand, onBack }: Props) {
  const [input, setInput] = useState('')
  const [lines, setLines] = useState<{ text: string; className: string }[]>([])
  const [currentStep, setCurrentStep] = useState(0)
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set())
  const [celebration, setCelebration] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)
  // Pawdentity credential prompts — password is NEVER echoed or stored in history.
  const [pwPrompt, setPwPrompt] = useState<null | { mode: 'username' | 'password'; username: string }>(null)
  const [authUser, setAuthUser] = useState<string | null>(null)

  const storageKey = `progress-${lesson.id}`

  const saveProgress = () => {
    const data = { currentStep, completedSteps: [...completedSteps] }
    localStorage.setItem(storageKey, JSON.stringify(data))
  }

  const resetProgress = () => {
    localStorage.removeItem(storageKey)
    setLines([])
    setCurrentStep(0)
    setCompletedSteps(new Set())
    setCelebration(false)
    if (lesson.steps.length > 0) {
      addLine({ text: `╭─ ${lesson.title} ─ Practice Terminal ─`, className: 'text-miau-green text-xs' })
      addLine({ text: `│  Commands: ${lesson.commands.join(', ')}`, className: 'text-miau-text-dim text-xs' })
      addLine({ text: `│  Type 'hint' for help · 'next' to skip forward · 'back' to go back`, className: 'text-miau-text-dim text-xs' })
      addLine({ text: `╰─${'─'.repeat(40)}`, className: 'text-miau-green text-xs' })
      addLine({ text: `\n📋 Step 1/${lesson.steps.length}: ${lesson.steps[0].instruction}`, className: 'text-miau-yellow text-xs' })
      if (lesson.steps[0].command) {
        addLine({ text: `   └─ Try: ${lesson.steps[0].command}`, className: 'text-miau-text-dim text-xs' })
      }
    }
  }

  useEffect(() => {
    setLines([])
    setCelebration(false)
    const saved = localStorage.getItem(storageKey)
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        const restoredStep = parsed.currentStep ?? 0
        const restoredCompleted: number[] = parsed.completedSteps ?? []
        setCurrentStep(restoredStep)
        setCompletedSteps(new Set(restoredCompleted))
        if (lesson.steps.length > 0) {
          addLine({ text: `╭─ ${lesson.title} ─ Practice Terminal ─ (resumed)`, className: 'text-miau-green text-xs' })
          addLine({ text: `│  Commands: ${lesson.commands.join(', ')}`, className: 'text-miau-text-dim text-xs' })
          addLine({ text: `│  Type 'hint' for help · 'next' to skip forward · 'back' to go back`, className: 'text-miau-text-dim text-xs' })
          addLine({ text: `╰─${'─'.repeat(40)}`, className: 'text-miau-green text-xs' })
          addLine({ text: `\n📋 Step ${restoredStep + 1}/${lesson.steps.length}: ${lesson.steps[restoredStep].instruction}`, className: 'text-miau-yellow text-xs' })
          if (lesson.steps[restoredStep].command) {
            addLine({ text: `   └─ Try: ${lesson.steps[restoredStep].command}`, className: 'text-miau-text-dim text-xs' })
          }
        }
        return
      } catch {}
    }
    setCurrentStep(0)
    setCompletedSteps(new Set())
    if (lesson.steps.length > 0) {
      addLine({ text: `╭─ ${lesson.title} ─ Practice Terminal ─`, className: 'text-miau-green text-xs' })
      addLine({ text: `│  Commands: ${lesson.commands.join(', ')}`, className: 'text-miau-text-dim text-xs' })
      addLine({ text: `│  Type 'hint' for help · 'next' to skip forward · 'back' to go back`, className: 'text-miau-text-dim text-xs' })
      addLine({ text: `╰─${'─'.repeat(40)}`, className: 'text-miau-green text-xs' })
      addLine({ text: `\n📋 Step 1/${lesson.steps.length}: ${lesson.steps[0].instruction}`, className: 'text-miau-yellow text-xs' })
      if (lesson.steps[0].command) {
        addLine({ text: `   └─ Try: ${lesson.steps[0].command}`, className: 'text-miau-text-dim text-xs' })
      }
    }
  }, [lesson])

  useEffect(() => {
    saveProgress()
  }, [currentStep, completedSteps])

  // Restore pawdentity SSO session state on mount (shared cookie across all apps).
  useEffect(() => {
    getPawdentitySession().then((sess) => {
      if (sess.authenticated && sess.username) {
        setAuthUser(sess.username)
        addLine({ text: `🔐 Session active as ${sess.username}`, className: 'text-miau-text text-xs' })
      }
    })
  }, [])

  const addLine = (line: { text: string; className: string }) => {
    setLines((prev) => [...prev, line])
  }

  // Complete the current course step when its expected command matches the prefix
  // (e.g. `login`/`logout` steps in getting-started) after real pawdentity auth.
  const completeStepIfExpected = (commandPrefix: string) => {
    const step = lesson.steps[currentStep]
    const expectedCmd = step?.command?.toLowerCase().trim()
    if (!expectedCmd || (expectedCmd !== commandPrefix && !expectedCmd.startsWith(`${commandPrefix} `))) return
    if (step.expectedOutput) {
      addLine({ text: `  ✅ ${step.expectedOutput}`, className: 'text-miau-green text-xs' })
    } else {
      addLine({ text: '  ✅ Command executed successfully.', className: 'text-miau-green text-xs' })
    }
    setCompletedSteps((prev) => new Set([...prev, currentStep]))
    advanceStep()
  }

  const doPawdentityLogin = async (username: string, password: string) => {
    const user = username.trim()
    if (!user) {
      addLine({ text: '❌ login failed: no username', className: 'text-miau-red text-xs' })
      return
    }
    try {
      const headers: Record<string, string> = { 'Content-Type': 'application/json' }
      const csrf = getCSRFToken()
      if (csrf) headers['X-CSRF-Token'] = csrf
      const res = await fetch('/api/v1/pawdentity/login', {
        method: 'POST',
        credentials: 'include',
        headers,
        body: JSON.stringify({ username: user, password }),
      })
      const data = await res.json().catch(() => ({}))
      if (res.ok && data.authenticated) {
        const loggedInAs = data.username || user
        setAuthUser(loggedInAs)
        addLine({ text: `✅ Logged in as ${loggedInAs}`, className: 'text-miau-green text-xs' })
        completeStepIfExpected('login')
      } else {
        addLine({ text: `❌ login failed: ${data.detail || `HTTP ${res.status}`}`, className: 'text-miau-red text-xs' })
      }
    } catch (e) {
      addLine({ text: `❌ login failed: ${e instanceof Error ? e.message : 'network error'}`, className: 'text-miau-red text-xs' })
    }
    inputRef.current?.focus()
  }

  const doPawdentityLogout = async () => {
    try {
      await fetch('/api/v1/pawdentity/logout', { method: 'POST', credentials: 'include' })
    } catch {
      // Local logout still applies even if the backend is unreachable.
    }
    setAuthUser(null)
    addLine({ text: '🔒 logged out', className: 'text-miau-text text-xs' })
    completeStepIfExpected('logout')
  }

  const advanceStep = () => {
    if (currentStep < lesson.steps.length - 1) {
      const next = currentStep + 1
      setCurrentStep(next)
      addLine({ text: `\n📋 Step ${next + 1}/${lesson.steps.length}: ${lesson.steps[next].instruction}`, className: 'text-miau-yellow text-xs' })
      if (lesson.steps[next].command) {
        addLine({ text: `   └─ Try: ${lesson.steps[next].command}`, className: 'text-miau-text-dim text-xs' })
      }
    } else {
      setCelebration(true)
      addLine({ text: '\n🎉 All steps completed! You mastered these commands:\n   ' + lesson.commands.join(', '), className: 'text-miau-green text-xs' })
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // ── Pawdentity credential prompt flow (password is never echoed) ──────
    if (pwPrompt) {
      if (pwPrompt.mode === 'username') {
        const username = input.trim()
        if (!username) return
        setPwPrompt({ mode: 'password', username })
        setInput('')
        inputRef.current?.focus()
      } else {
        const password = input
        setInput('')
        setPwPrompt(null)
        await doPawdentityLogin(pwPrompt.username, password)
      }
      return
    }

    if (!input.trim()) return

    const rawInput = input.trim()
    const parts = rawInput.split(/\s+/)
    const cmd = parts[0].toLowerCase()

    // ── Secure login: intercept BEFORE the echo so a password is never shown ──
    if (cmd === 'login') {
      const username = parts[1] || ''
      addLine({ text: username ? `$ login ${username}` : '$ login', className: 'text-miau-text' })
      setPwPrompt({ mode: username ? 'password' : 'username', username })
      setInput('')
      inputRef.current?.focus()
      return
    }

    // ── Logout: real pawdentity logout instead of the backend stub ──
    if (cmd === 'logout') {
      addLine({ text: '$ logout', className: 'text-miau-text' })
      setInput('')
      await doPawdentityLogout()
      return
    }

    addLine({ text: `$ ${rawInput}`, className: 'text-miau-text' })

    if (cmd === 'hint') {
      const hint = lesson.steps[currentStep]?.hint || 'No hint available. Try the suggested command!'
      addLine({ text: `💡 ${hint}`, className: 'text-miau-amber text-xs' })
    } else if (cmd === 'next') {
      setCompletedSteps((prev) => new Set([...prev, currentStep]))
      advanceStep()
    } else if (cmd === 'back') {
      onBack()
      setInput('')
      return
    } else if (cmd === 'clear') {
      setLines([])
      setInput('')
      const step = lesson.steps[currentStep]
      const expectedCmd = step.command?.toLowerCase().trim()
      if (expectedCmd === 'clear') {
        if (step.expectedOutput) {
          setTimeout(() => addLine({ text: `  ✅ ${step.expectedOutput}`, className: 'text-miau-green text-xs' }), 50)
        }
        setCompletedSteps((prev) => new Set([...prev, currentStep]))
        advanceStep()
      }
      return
    } else {
      const step = lesson.steps[currentStep]
      const expectedCmd = step.command?.toLowerCase().trim()
      const typedFull = rawInput.toLowerCase().trim()
      const matchedExact = expectedCmd && typedFull === expectedCmd
      const matchedSimilar = expectedCmd && (typedFull.startsWith(expectedCmd.split(' ')[0]))

      if (matchedExact) {
        // Exact match — show expected output and advance
        if (step.expectedOutput) {
          addLine({ text: `  ✅ ${step.expectedOutput}`, className: 'text-miau-green text-xs' })
        } else {
          addLine({ text: `  ✅ Command executed successfully.`, className: 'text-miau-green text-xs' })
        }
        setCompletedSteps((prev) => new Set([...prev, currentStep]))
        advanceStep()
      } else if (matchedSimilar) {
        // Close match — still advance but be transparent
        if (step.expectedOutput) {
          addLine({ text: `  ${step.expectedOutput}`, className: 'text-miau-text text-xs' })
        }
        setCompletedSteps((prev) => new Set([...prev, currentStep]))
        advanceStep()
      } else {
        // Not a step command — try the backend for general commands
        const result = await executeTerminalCommand(cmd, parts.slice(1).join(' '))
        if (result.output) {
          for (const line of result.output.split('\n')) {
            addLine({ text: `  ${line}`, className: result.status === 'error' ? 'text-miau-red text-xs' : 'text-miau-text text-xs' })
          }
        }
        if (result.status === 'ok') {
          setCompletedSteps((prev) => new Set([...prev, currentStep]))
          advanceStep()
        } else {
          // Backend didn't know it either — suggest the step command
          if (step.command) {
            addLine({ text: `  💡 Try the step command: ${step.command}`, className: 'text-miau-amber text-xs' })
          }
        }
      }
    }
    setInput('')
  }

  const progress = lesson.steps.length > 0 ? (completedSteps.size / lesson.steps.length) * 100 : 0

  return (
    <div className="h-full flex flex-col relative">
      {celebration && (
        <div className="absolute inset-0 pointer-events-none overflow-hidden z-10">
          {['🎉', '🌟', '✨', '🎊', '💫', '⭐', '🏆', '🥇'].map((e, i) => (
            <span
              key={i}
              className="confetti-particle"
              style={{
                left: `${10 + Math.random() * 80}%`,
                top: `${30 + Math.random() * 40}%`,
                animationDelay: `${i * 0.15}s`,
                fontSize: `${1 + Math.random() * 1.5}rem`,
              }}
            >
              {e}
            </span>
          ))}
        </div>
      )}
      <div className="px-4 py-1 border-b border-miau-border shrink-0">
        <div className="flex items-center gap-2">
          <button onClick={onBack} className="text-miau-text-dim hover:text-miau-green text-xs font-mono">
            ← Back to lesson
          </button>
          <div className="flex-1 h-1 bg-miau-border rounded-full overflow-hidden">
            <div
              className="h-full bg-miau-green transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
          <span className="text-miau-text-dim text-xs">{completedSteps.size}/{lesson.steps.length}</span>
          {authUser && (
            <span className="text-[10px] text-miau-green font-mono" title="Signed in via pawdentity">🔐 {authUser}</span>
          )}
          <button onClick={resetProgress} className="text-[10px] text-miau-text-dim/40 hover:text-miau-red font-mono transition-colors" title="Reset progress">
            ↺
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 font-mono text-xs leading-relaxed" ref={(el) => { if (el) el.scrollTop = el.scrollHeight }}>
        {lines.map((line, i) => (
          <div key={i} className={line.className}>{line.text}</div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="p-3 border-t border-miau-border shrink-0 flex items-center gap-2">
        <span className="text-miau-green font-mono text-sm">
          {pwPrompt ? (pwPrompt.mode === 'password' ? 'Password:' : 'Username:') : '$'}
        </span>
        <input
          ref={inputRef}
          type={pwPrompt?.mode === 'password' ? 'password' : 'text'}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 bg-transparent border-none outline-none text-miau-text font-mono text-sm placeholder:text-miau-text-dim/30"
          placeholder={pwPrompt ? (pwPrompt.mode === 'password' ? '••••••••' : 'username') : (lesson.steps[currentStep]?.command || 'Type a command...')}
          autoFocus
          spellCheck={false}
          autoComplete={pwPrompt?.mode === 'password' ? 'current-password' : 'off'}
        />
        {!pwPrompt && <span className="text-miau-text-dim text-xs">hint · next · back</span>}
      </form>
    </div>
  )
}
