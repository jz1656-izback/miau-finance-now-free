/**
 * 🐱 CAT SOUND EFFECTS LIBRARY — REAL WEBAUDIO PURRS
 * Synthesizes cat sounds directly in your browser. No audio files needed.
 */

type SoundType = 'login' | 'trade' | 'optimize' | 'error' | 'achievement' | 'notification' | 'purr' | 'meow' | 'chirp'

let _audioCtx: AudioContext | null = null
let _volume = 0.5

export function setVolume(v: number) { _volume = v }

function getCtx(): AudioContext {
  if (!_audioCtx) _audioCtx = new AudioContext()
  return _audioCtx
}

function meow(freq: number = 500, duration: number = 0.4): void {
  try {
    const ctx = getCtx()
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.type = 'sawtooth'
    osc.frequency.setValueAtTime(freq, ctx.currentTime)
    osc.frequency.exponentialRampToValueAtTime(freq * 1.8, ctx.currentTime + duration * 0.5)
    osc.frequency.exponentialRampToValueAtTime(freq * 0.7, ctx.currentTime + duration)
    gain.gain.setValueAtTime(0.08 * _volume, ctx.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.01 * _volume, ctx.currentTime + duration)
    osc.connect(gain).connect(ctx.destination)
    osc.start(ctx.currentTime)
    osc.stop(ctx.currentTime + duration)
  } catch {}
}

function purr(freq: number = 25, duration: number = 1.0): void {
  try {
    const ctx = getCtx()
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.type = 'sawtooth'
    osc.frequency.setValueAtTime(freq, ctx.currentTime)
    osc.frequency.setValueAtTime(freq * 2, ctx.currentTime + duration * 0.5)
    gain.gain.setValueAtTime(0.04 * _volume, ctx.currentTime)
    gain.gain.setValueAtTime(0.04 * _volume, ctx.currentTime + duration * 0.8)
    gain.gain.exponentialRampToValueAtTime(0.01 * _volume, ctx.currentTime + duration)
    osc.connect(gain).connect(ctx.destination)
    osc.start(ctx.currentTime)
    osc.stop(ctx.currentTime + duration)
  } catch {}
}

function chirp(): void {
  try {
    const ctx = getCtx()
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.type = 'sine'
    osc.frequency.setValueAtTime(800, ctx.currentTime)
    osc.frequency.exponentialRampToValueAtTime(1600, ctx.currentTime + 0.08)
    gain.gain.setValueAtTime(0.06 * _volume, ctx.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.01 * _volume, ctx.currentTime + 0.12)
    osc.connect(gain).connect(ctx.destination)
    osc.start(ctx.currentTime)
    osc.stop(ctx.currentTime + 0.12)
  } catch {}
}

function hiss(): void {
  try {
    const ctx = getCtx()
    const bufferSize = ctx.sampleRate * 0.2
    const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate)
    const data = buffer.getChannelData(0)
    for (let i = 0; i < bufferSize; i++) data[i] = (Math.random() * 2 - 1) * 0.04 * _volume
    const source = ctx.createBufferSource()
    source.buffer = buffer
    const gain = ctx.createGain()
    gain.gain.setValueAtTime(0.06 * _volume, ctx.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.01 * _volume, ctx.currentTime + 0.2)
    source.connect(gain).connect(ctx.destination)
    source.start(ctx.currentTime)
  } catch {}
}

function celebratoryMeow(): void {
  meow(600, 0.3)
  setTimeout(() => meow(800, 0.3), 150)
  setTimeout(() => meow(1000, 0.5), 300)
}

const SOUND_FN: Record<SoundType, () => void> = {
  login: () => { purr(28, 1.5) },
  trade: () => { meow(500, 0.35) },
  optimize: () => { purr(25, 2.0) },
  error: () => { hiss() },
  achievement: () => { celebratoryMeow() },
  notification: () => { chirp() },
  purr: () => { purr(20 + Math.random() * 20, 1.0 + Math.random() * 2.0) },
  meow: () => { meow(400 + Math.random() * 300, 0.3 + Math.random() * 0.3) },
  chirp: () => { chirp() },
}

export function playCatSound(type: SoundType, volume: number = 0.5): void {
  _volume = Math.max(0, Math.min(1, volume))
  SOUND_FN[type]()
}

export function playRandomMeow(): void {
  const sounds: SoundType[] = ['meow', 'purr', 'chirp']
  const type = sounds[Math.floor(Math.random() * sounds.length)]
  SOUND_FN[type]()
}

export function getCatSoundText(type: SoundType): string {
  const sounds: Record<SoundType, string[]> = {
    login: ['Meow~', 'mew mew', 'purr'],
    trade: ['MEOW!', 'mrrow!', 'hiss (just kidding!)'],
    optimize: ['prrrrr', 'purr~', 'mrow~'],
    error: ['HISSS!', 'meow...', 'yowl'],
    achievement: ['MEOW MEOW!', 'MRROW!', 'purr purr PURR!'],
    notification: ['mew', 'chirp', 'bleep-bloop I mean meow'],
    purr: ['prrrrr', 'purr~', 'rrrrrow'],
    meow: ['Meow!', 'Mew!', 'Mrrow!'],
    chirp: ['Chirp!', 'chirp chirp', 'mew chirp!'],
  }
  const options = sounds[type]
  return options[Math.floor(Math.random() * options.length)]
}

export const CAT_SOUND_PRESETS = {
  success: { type: 'trade' as const, text: 'Trade executed - Meow! 🐱' },
  error: { type: 'error' as const, text: 'Oops! Meoow? 😿' },
  achievement: { type: 'achievement' as const, text: 'Achievement unlocked! MEOW MEOW! 😻' },
  optimization: { type: 'optimize' as const, text: 'Portfolio optimized - prrrrr 😸' },
}

export async function fetchWithCatSound<T>(
  url: string,
  options?: RequestInit,
  successSound?: SoundType,
  errorSound?: SoundType
): Promise<T> {
  try {
    const response = await fetch(url, options)
    if (!response.ok) throw new Error(response.statusText)
    if (successSound) playCatSound(successSound)
    return await response.json()
  } catch (error) {
    if (errorSound) playCatSound(errorSound)
    throw error
  }
}

export function getCatEncouragement(): string {
  const encouragements = [
    '🐱 You got this, whisker!',
    '😸 Pawsome work!',
    '😻 You\'re purr-fect!',
    '🐱 That\'s the cat\'s meow!',
    '😼 Clever kitten!',
    '😹 ROFL (Rolling Over Feline Laughter)',
    '🐱 9 lives of productivity!',
    '😺 Keep up the good work, cat!',
  ]
  return encouragements[Math.floor(Math.random() * encouragements.length)]
}

export function getCatErrorMessage(error: string): string {
  const prefix = ['Meoow,', 'Meow...', 'Oh noes!', 'Cat got your error message!', 'Hissss!'][
    Math.floor(Math.random() * 5)
  ]
  return `${prefix} ${error}`
}
