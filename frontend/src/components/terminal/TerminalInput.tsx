// TerminalInput — command/password input area for the Terminal
import React from 'react'
import type { TerminalTheme } from '../../lib/themes'

interface TerminalInputProps {
  input: string
  setInput: (v: string) => void
  pwPrompt: null | { mode: 'username' | 'password'; username: string }
  suggestions: string[]
  handleKey: (e: React.KeyboardEvent) => void
  onVoiceClick: () => void
  voiceActive: boolean
  inputRef: React.Ref<HTMLInputElement>
  theme: TerminalTheme
}

const PROMPT = 'miau@finance'

export function TerminalInput({
  input, setInput, pwPrompt, suggestions,
  handleKey, onVoiceClick, voiceActive,
  inputRef, theme,
}: TerminalInputProps) {
  return (
    <div className="flex items-center px-4 py-3 border-t border-green-500/20" style={{ background: 'rgba(0,20,10,0.95)', boxShadow: '0 -2px 12px rgba(0,255,136,0.06)' }}>
      {pwPrompt?.mode === 'username' && (
        <span className="text-yellow shrink-0 font-mono text-sm">Username:</span>
      )}
      {pwPrompt?.mode === 'password' && (
        <span className="text-yellow shrink-0 font-mono text-sm">Password:</span>
      )}
      {!pwPrompt && (
        <>
          <span className="text-green shrink-0 font-mono text-sm">{PROMPT}</span>
          <span className="text-dim shrink-0 font-mono text-sm">:~$ </span>
        </>
      )}
      <input
        id="terminal-input"
        ref={inputRef}
        type={pwPrompt?.mode === 'password' ? 'password' : 'text'}
        value={input}
        onChange={e => { setInput(e.target.value) }}
        onKeyDown={handleKey}
        className="flex-1 bg-transparent border-none outline-none font-mono placeholder:text-green/30"
        style={{ caretColor: theme.colors.green, color: theme.colors.green, fontSize: '16px' }}
        autoFocus
        spellCheck={false}
        autoComplete="off"
        autoCapitalize="none"
        autoCorrect="off"
        placeholder={pwPrompt ? (pwPrompt.mode === 'username' ? 'username' : '••••••••') : "type 'help' for commands..."}
        aria-label={pwPrompt ? (pwPrompt.mode === 'username' ? 'Username input' : 'Password input') : 'Terminal command input'}
        {...(pwPrompt ? {} : { 'aria-autocomplete': 'list', role: 'combobox', 'aria-expanded': suggestions.length > 0 })}
      />
      <span className="terminal-cursor-smooth" />
      <button
        onClick={onVoiceClick}
        className="ml-2 px-2 py-1 text-xs rounded border transition-colors"
        style={{
          borderColor: voiceActive ? theme.colors.green : theme.colors.border,
          color: voiceActive ? theme.colors.green : theme.colors.textDim,
          background: voiceActive ? 'rgba(0,255,136,0.1)' : 'transparent',
        }}
        aria-label={voiceActive ? 'Stop voice input' : 'Start voice input'}
        title={voiceActive ? 'Click to stop listening' : 'Click to speak a command'}
      >
        {voiceActive ? '🔴' : '🎤'}
      </button>
    </div>
  )
}
