type LogLevel = 'debug' | 'info' | 'warn' | 'error'

interface LogEntry {
  timestamp: string
  level: LogLevel
  module: string
  message: string
  data?: Record<string, unknown>
  error?: string
}

const LOG_LEVELS: Record<LogLevel, number> = { debug: 0, info: 1, warn: 2, error: 3 }
const CURRENT_LEVEL: LogLevel = (typeof window !== 'undefined' && (window as any).__LOG_LEVEL__) || 
  'debug'

class Logger {
  private module: string

  constructor(module: string) {
    this.module = module
  }

  private log(level: LogLevel, message: string, data?: Record<string, unknown>, error?: Error) {
    if (LOG_LEVELS[level] < LOG_LEVELS[CURRENT_LEVEL]) return
    
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      module: this.module,
      message,
      data,
      error: error?.message || error?.stack,
    }

    const prefix = `[${entry.timestamp}] [${level.toUpperCase()}] [${this.module}]`
    
    switch (level) {
      case 'debug':
        console.debug(prefix, message, data || '', error || '')
        break
      case 'info':
        console.info(prefix, message, data || '', error || '')
        break
      case 'warn':
        console.warn(prefix, message, data || '', error || '')
        break
      case 'error':
        console.error(prefix, message, data || '', error || '')
        break
    }

    // Store in memory ring buffer for log viewer
    if (typeof window !== 'undefined') {
      const w = window as any
      if (!w.__logs) w.__logs = []
      w.__logs.push(entry)
      if (w.__logs.length > 1000) w.__logs.shift()
    }
  }

  debug(message: string, data?: Record<string, unknown>) { this.log('debug', message, data) }
  info(message: string, data?: Record<string, unknown>) { this.log('info', message, data) }
  warn(message: string, data?: Record<string, unknown>) { this.log('warn', message, data) }
  error(message: string, data?: Record<string, unknown>, error?: Error) { this.log('error', message, data, error) }

  // Convenience for API calls
  apiCall(method: string, url: string, status?: number, durationMs?: number) {
    const level = status && status >= 400 ? 'warn' : 'info'
    this.log(level, `${method} ${url}`, { status, duration_ms: durationMs })
  }

  apiError(method: string, url: string, status: number, error?: Error) {
    this.log('error', `${method} ${url} → ${status}`, { status }, error)
  }

  command(cmd: string, args: string[], success: boolean) {
    this.log(success ? 'info' : 'warn', `cmd: ${cmd} ${args.join(' ')}`, { success })
  }
}

export function getLogger(module: string): Logger {
  return new Logger(module)
}

export const logger = getLogger('app')
