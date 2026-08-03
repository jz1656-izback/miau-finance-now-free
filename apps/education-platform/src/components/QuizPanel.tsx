import { useState } from 'react'
import type { Lesson } from '../lib/types'

interface Props {
  lesson: Lesson
  onBack: () => void
}

export function QuizPanel({ lesson, onBack }: Props) {
  const [currentQ, setCurrentQ] = useState(0)
  const [selected, setSelected] = useState<number | null>(null)
  const [submitted, setSubmitted] = useState(false)
  const [score, setScore] = useState(0)
  const [finished, setFinished] = useState(false)

  const questions = lesson.quiz

  if (questions.length === 0) {
    return (
      <div className="max-w-2xl mx-auto p-6 text-center">
        <p className="text-miau-text-dim text-sm">No quiz questions for this lesson yet.</p>
        <button
          onClick={onBack}
          className="mt-4 px-4 py-2 bg-miau-border/20 border border-miau-border/50 text-miau-text-dim rounded text-sm font-mono hover:text-miau-text"
        >
          ← Back to Lesson
        </button>
      </div>
    )
  }

  const q = questions[currentQ]

  const handleSelect = (index: number) => {
    if (submitted) return
    setSelected(index)
  }

  const handleSubmit = () => {
    if (selected === null) return
    setSubmitted(true)
    if (selected === q.correctIndex) {
      setScore((s) => s + 1)
    }
  }

  const handleNext = () => {
    if (currentQ < questions.length - 1) {
      setCurrentQ((i) => i + 1)
      setSelected(null)
      setSubmitted(false)
    } else {
      setFinished(true)
    }
  }

  if (finished) {
    const pct = Math.round((score / questions.length) * 100)
    const grade = pct >= 80 ? 'Meowster 🌟' : pct >= 60 ? 'Apprentice 🐱' : 'Kitten 📚'
    const perfect = pct === 100
    return (
      <div className="max-w-2xl mx-auto p-6 text-center relative">
        {perfect && (
          <div className="absolute inset-0 pointer-events-none overflow-hidden">
            {['🎉', '🌟', '✨', '🎊', '💫', '⭐', '🏆', '🥇', '🎆', '🌈', '💥', '🎯'].map((e, i) => (
              <span
                key={i}
                className="confetti-particle"
                style={{
                  left: `${5 + Math.random() * 90}%`,
                  top: `${20 + Math.random() * 60}%`,
                  animationDelay: `${i * 0.12}s`,
                  fontSize: `${1 + Math.random() * 1.8}rem`,
                }}
              >
                {e}
              </span>
            ))}
          </div>
        )}
        <div className="text-4xl mb-4">{perfect ? '🏆' : pct >= 80 ? '🎉' : pct >= 60 ? '👍' : '📚'}</div>
        <h2 className="text-lg font-bold text-miau-green mb-2">{perfect ? '✨ Perfect Score! ✨' : 'Quiz Complete!'}</h2>
        {perfect && <p className="text-sm text-miau-amber mb-1">Congratulations on completing "{lesson.title}" with a perfect score!</p>}
        <p className="text-sm text-miau-text-dim mb-1">
          {score} / {questions.length} correct ({pct}%)
        </p>
        <p className="text-sm text-miau-amber mb-6">{grade}</p>
        <button
          onClick={() => { setCurrentQ(0); setSelected(null); setSubmitted(false); setScore(0); setFinished(false) }}
          className="px-4 py-2 bg-miau-green/10 border border-miau-green/30 text-miau-green rounded text-sm font-mono mr-3 hover:bg-miau-green/20"
        >
          ↻ Retry Quiz
        </button>
        <button
          onClick={onBack}
          className="px-4 py-2 bg-miau-border/20 border border-miau-border/50 text-miau-text-dim rounded text-sm font-mono hover:text-miau-text"
        >
          ← Back to Lesson
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="flex items-center justify-between mb-4">
        <button onClick={onBack} className="text-miau-text-dim hover:text-miau-green text-xs font-mono">
          ← Back
        </button>
        <span className="text-xs text-miau-text-dim">Question {currentQ + 1} / {questions.length}</span>
        <span className="text-xs text-miau-amber">Score: {score}</span>
      </div>

      <div className="mb-6">
        <h3 className="text-sm font-bold text-miau-text mb-3">{q.question}</h3>
        <div className="space-y-2">
          {q.options.map((opt, i) => {
            let borderClass = 'border-miau-border/30 hover:border-miau-border'
            if (submitted && i === q.correctIndex) borderClass = 'border-miau-green bg-miau-green/5'
            if (submitted && i === selected && i !== q.correctIndex) borderClass = 'border-miau-red bg-miau-red/5'
            if (selected === i && !submitted) borderClass = 'border-miau-amber bg-miau-amber/5'

            return (
              <button
                key={i}
                onClick={() => handleSelect(i)}
                className={`w-full text-left px-4 py-3 border rounded text-sm font-mono transition-colors ${borderClass}`}
              >
                <span className="text-miau-text-dim mr-2">{String.fromCharCode(65 + i)}.</span>
                <span className={submitted && i === q.correctIndex ? 'text-miau-green' : submitted && i === selected && i !== q.correctIndex ? 'text-miau-red' : 'text-miau-text'}>
                  {opt}
                </span>
                {submitted && i === q.correctIndex && <span className="ml-2 text-miau-green">✓</span>}
                {submitted && i === selected && i !== q.correctIndex && <span className="ml-2 text-miau-red">✗</span>}
              </button>
            )
          })}
        </div>
      </div>

      {submitted && (
        <div className="mb-4 p-3 bg-miau-border/10 border border-miau-border/30 rounded text-xs text-miau-text-dim">
          <span className="text-miau-amber">Explanation:</span> {q.explanation}
        </div>
      )}

      <div className="flex gap-3">
        {!submitted ? (
          <button
            onClick={handleSubmit}
            disabled={selected === null}
            className={`px-4 py-2 rounded text-sm font-mono transition-colors ${
              selected !== null
                ? 'bg-miau-green/10 border border-miau-green/30 text-miau-green hover:bg-miau-green/20'
                : 'bg-miau-border/10 border border-miau-border/30 text-miau-text-dim/40 cursor-not-allowed'
            }`}
          >
            Submit Answer
          </button>
        ) : (
          <button
            onClick={handleNext}
            className="px-4 py-2 bg-miau-green/10 border border-miau-green/30 text-miau-green rounded text-sm font-mono hover:bg-miau-green/20"
          >
            {currentQ < questions.length - 1 ? 'Next Question →' : 'Finish Quiz'}
          </button>
        )}
      </div>
    </div>
  )
}
