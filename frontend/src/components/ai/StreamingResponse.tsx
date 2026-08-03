import { useState, useEffect, useRef, useCallback } from 'react'

interface StreamingResponseProps {
  content: string
  streaming?: boolean
  onComplete?: () => void
}

export default function StreamingResponse({ content, streaming = false, onComplete }: StreamingResponseProps) {
  const [displayedChars, setDisplayedChars] = useState(0)
  const [copied, setCopied] = useState(false)
  const textRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!streaming) {
      setDisplayedChars(content.length)
      onComplete?.()
      return
    }
    setDisplayedChars(0)
    const interval = setInterval(() => {
      setDisplayedChars(prev => {
        if (prev >= content.length) {
          clearInterval(interval)
          onComplete?.()
          return content.length
        }
        return prev + 3
      })
    }, 30)
    return () => clearInterval(interval)
  }, [content, streaming, onComplete])

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {}
  }, [content])

  const displayed = content.slice(0, displayedChars)
  const isComplete = displayedChars >= content.length

  return (
    <div className="glass-panel rounded-lg p-4 my-2">
      <div className="flex items-start gap-3">
        <span className="text-yellow font-bold shrink-0">AI:</span>
        <div className="flex-1 min-w-0">
          <div
            ref={textRef}
            className="text-green whitespace-pre-wrap break-words text-sm leading-relaxed"
          >
            {displayed}
            {streaming && !isComplete && (
              <span className="terminal-cursor-smooth inline-block ml-0.5" />
            )}
          </div>
          {isComplete && !streaming && (
            <div className="flex items-center gap-2 mt-2">
              <button
                onClick={handleCopy}
                className="text-xs text-dim hover:text-green transition-colors px-2 py-1 rounded border border-[#1a3a2a] hover:border-green/30"
              >
                {copied ? '✓ Copied' : 'Copy'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
