import { Component, ErrorInfo, ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export default class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('[ErrorBoundary]', error, info.componentStack)
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="flex items-center justify-center h-screen w-screen" style={{ background: '#0a1a14' }}>
          <div className="text-center font-mono p-8">
            <div className="text-6xl mb-4">😿</div>
            <div className="text-red text-lg mb-2">critical error</div>
            <pre className="text-dim text-xs mb-4 max-w-xl mx-auto overflow-auto" style={{ whiteSpace: 'pre-wrap' }}>
              {this.state.error?.message}
            </pre>
            <button
              onClick={() => this.setState({ hasError: false, error: null })}
              className="px-4 py-2 text-sm rounded cursor-pointer"
              style={{ background: '#00ff88', color: '#0a1a14', border: 'none' }}
            >
              retry
            </button>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}