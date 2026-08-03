// Miau Finance i18n — Internationalization Framework

import en from '../locales/en'
import de from '../locales/de'
import fr from '../locales/fr'
import es from '../locales/es'
import ja from '../locales/ja'
import zh from '../locales/zh'
import ko from '../locales/ko'
import pt from '../locales/pt'
import ru from '../locales/ru'

export type LocaleCode = 'en' | 'de' | 'fr' | 'es' | 'ja' | 'zh' | 'ko' | 'pt' | 'ru'

const LOCALES: Record<LocaleCode, Record<string, string>> = { en, de, fr, es, ja, zh, ko, pt, ru }

const NAMES: Record<LocaleCode, string> = {
  en: 'English', de: 'Deutsch', fr: 'Français', es: 'Español',
  ja: '日本語', zh: '中文', ko: '한국어', pt: 'Português', ru: 'Русский',
}

let _current: LocaleCode = 'en'
let _listeners: Array<(locale: LocaleCode) => void> = []

function detect(): LocaleCode {
  if (typeof navigator === 'undefined') return 'en'
  const lang = navigator.language?.slice(0, 2) || ''
  return (lang in LOCALES ? lang : 'en') as LocaleCode
}

function loadSaved(): LocaleCode {
  try {
    const saved = localStorage.getItem('miau-locale') as LocaleCode | null
    if (saved && saved in LOCALES) return saved
  } catch {}
  return detect()
}

function save(locale: LocaleCode) {
  try { localStorage.setItem('miau-locale', locale) } catch {}
}

export function getLocale(): LocaleCode {
  return _current
}

export const getCurrentLocale = getLocale

export function getLocaleName(code?: LocaleCode): string {
  return NAMES[code || _current] || 'English'
}

export const LOCALE_NATIVE = NAMES

export function setLocale(code: LocaleCode) {
  if (!(code in LOCALES)) return
  _current = code
  save(code)
  document.documentElement.lang = code
  _listeners.forEach(fn => fn(code))
}

export function onLocaleChange(fn: (locale: LocaleCode) => void) {
  _listeners.push(fn)
  return () => { _listeners = _listeners.filter(f => f !== fn) }
}

export function t(key: string, ...args: (string | number)[]): string {
  const dict = LOCALES[_current] || LOCALES.en
  let template = dict[key] || key
  args.forEach((arg, i) => {
    template = template.replace(`{${i}}`, String(arg))
  })
  return template
}

export function formatNumber(n: number): string {
  return new Intl.NumberFormat(_current).format(n)
}

export function registerTranslations(code: LocaleCode, translations: Record<string, string>) {
  LOCALES[code] = translations
}

export function formatCurrency(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat(_current, { style: 'currency', currency }).format(amount)
}

export function formatPercent(n: number, decimals = 1): string {
  return new Intl.NumberFormat(_current, { style: 'percent', minimumFractionDigits: decimals, maximumFractionDigits: decimals }).format(n)
}

export function formatDate(date: Date | string): string {
  return new Intl.DateTimeFormat(_current).format(typeof date === 'string' ? new Date(date) : date)
}

export const SUPPORTED_LOCALES = Object.keys(LOCALES)

export function listLocales(): { code: LocaleCode; name: string; native: string }[] {
  return Object.keys(LOCALES).map(code => ({
    code: code as LocaleCode,
    name: NAMES[code as LocaleCode],
    native: NAMES[code as LocaleCode],
  }))
}

// Initialize
_current = loadSaved()
document.documentElement.lang = _current || 'en'
