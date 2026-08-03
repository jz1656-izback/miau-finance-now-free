import { useEffect, useState } from 'react'
import type { Lesson } from '../lib/types'

interface Props {
  lesson: Lesson
  onPractice: (command: string) => void
  onQuiz: () => void
  onNext: () => void
}

function highlightCommand(command: string) {
  const parts = command.split(/(\s+)/)
  return parts.map((part, i) => {
    if (part.startsWith('-')) {
      return <span key={i} className="text-miau-amber">{part}</span>
    }
    if (/^[A-Z][A-Z0-9_]+$/.test(part) || /^[a-z]+\..+$/.test(part)) {
      return <span key={i} className="text-miau-green">{part}</span>
    }
    if (i === 0) {
      return <span key={i} className="text-miau-text font-bold">{part}</span>
    }
    return <span key={i}>{part}</span>
  })
}

export function LessonViewer({ lesson, onPractice, onQuiz, onNext }: Props) {
  const [copiedId, setCopiedId] = useState<string | null>(null)

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return
      if (e.key === 'p') { e.preventDefault(); onPractice(lesson.commands[0] || '') }
      if (e.key === 'q') { e.preventDefault(); onQuiz() }
      if (e.key === 'n') { e.preventDefault(); onNext() }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [lesson, onPractice, onQuiz, onNext])

  const copyToClipboard = async (text: string, id: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedId(id)
      setTimeout(() => setCopiedId(null), 2000)
    } catch {}
  }

  return (
    <div className="max-w-3xl mx-auto p-6">
      {/* Lesson Header */}
      <div className="mb-6">
        <div className="text-xs text-miau-text-dim mb-1">LESSON</div>
        <h1 className="text-lg font-bold text-miau-green text-glow-green mb-2">{lesson.title}</h1>
        <p className="text-sm text-miau-text-dim">{lesson.description}</p>
      </div>

      {/* Commands */}
      <div className="mb-6 p-3 bg-miau-border/20 rounded border border-miau-border/50">
        <div className="text-xs text-miau-text-dim mb-2">COMMANDS COVERED</div>
        <div className="flex flex-wrap gap-2">
          {lesson.commands.map((cmd) => (
            <code
              key={cmd}
              className="px-2 py-1 bg-miau-bg border border-miau-border rounded text-xs text-miau-green font-mono cursor-pointer hover:bg-miau-border/40 transition-colors"
              onClick={() => onPractice(cmd)}
            >
              {highlightCommand(cmd)}
            </code>
          ))}
        </div>
      </div>

      {/* Steps */}
      <div className="space-y-4 mb-8">
        <div className="text-xs text-miau-text-dim mb-1">STEP-BY-STEP</div>
        {lesson.steps.map((step, i) => (
          <div
            key={i}
            className="p-3 bg-miau-surface rounded border border-miau-border/30 hover:border-miau-border transition-colors"
          >
            <div className="flex items-start gap-3">
              <span className="text-xs font-bold text-miau-green bg-miau-border/30 px-2 py-0.5 rounded shrink-0 font-mono">
                {i + 1}
              </span>
              <div className="flex-1">
                <p className="text-sm text-miau-text mb-1">{step.instruction}</p>
                {step.command && (
                  <div className="flex items-center gap-2 mt-2">
                    <code
                      className="flex-1 block px-3 py-2 bg-miau-bg border border-miau-border/50 rounded text-xs text-miau-amber font-mono font-mono"
                    >
                      {highlightCommand(step.command)}
                    </code>
                    <button
                      onClick={() => copyToClipboard(step.command!, `step-${i}`)}
                      className="px-2 py-2 text-xs font-mono text-miau-text-dim border border-miau-border/50 rounded hover:text-miau-green hover:border-miau-green/50 transition-colors"
                      title="Copy to clipboard"
                    >
                      {copiedId === `step-${i}` ? '✓' : '📋'}
                    </button>
                  </div>
                )}
                {step.expectedOutput && (
                  <p className="text-xs text-miau-text-dim mt-1">
                    Expected: <span className="text-miau-text-dim/60">{step.expectedOutput}</span>
                  </p>
                )}
                {step.hint && (
                  <p className="text-xs text-miau-amber mt-1">Hint: {step.hint}</p>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Action Buttons */}
      <div className="flex items-center gap-3 pt-4 border-t border-miau-border">
        <button
          onClick={() => onPractice(lesson.commands[0] || '')}
          className="px-4 py-2 bg-miau-green/10 border border-miau-green/30 text-miau-green rounded text-sm font-mono hover:bg-miau-green/20 transition-colors"
        >
          → Open Practice Terminal
        </button>
        <button
          onClick={onQuiz}
          className="px-4 py-2 bg-miau-amber/10 border border-miau-amber/30 text-miau-amber rounded text-sm font-mono hover:bg-miau-amber/20 transition-colors"
        >
          ? Take Quiz
        </button>
        <button
          onClick={onNext}
          className="px-4 py-2 bg-miau-border/20 border border-miau-border/50 text-miau-text-dim rounded text-sm font-mono hover:text-miau-text hover:border-miau-border transition-colors"
        >
          Next Lesson →
        </button>
      </div>

      {/* Keyboard Shortcuts Hint */}
      <div className="mt-6 p-3 bg-miau-border/10 border border-miau-border/30 rounded text-[10px] text-miau-text-dim font-mono flex items-center gap-4">
        <span className="text-miau-green">⌨ Shortcuts:</span>
        <span><kbd className="px-1 py-0.5 bg-miau-bg border border-miau-border/50 rounded text-miau-amber">P</kbd> Practice</span>
        <span><kbd className="px-1 py-0.5 bg-miau-bg border border-miau-border/50 rounded text-miau-amber">Q</kbd> Quiz</span>
        <span><kbd className="px-1 py-0.5 bg-miau-bg border border-miau-border/50 rounded text-miau-amber">N</kbd> Next Lesson</span>
      </div>
    </div>
  )
}
