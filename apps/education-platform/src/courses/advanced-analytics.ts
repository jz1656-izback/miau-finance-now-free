import type { Course } from '../lib/types'

export const advancedAnalytics: Course = {
  id: 'advanced-analytics',
  slug: 'advanced-analytics',
  title: 'Advanced Analytics',
  description: 'Factor analysis, watchlists, and deep portfolio insights.',
  category: 'Analytics',
  difficulty: 'advanced',
  icon: '🔬',
  lessonCount: 3,
  estimatedMinutes: 15,
  lessons: [
    {
      id: 'aa-watchlist',
      slug: 'watchlist',
      title: 'Watchlist Management',
      description: 'Track assets you care about.',
      commands: ['watch list', 'watch add', 'watch rm'],
      steps: [
        { instruction: 'View watchlist: `watch list`', command: 'watch list', expectedOutput: 'Your tracked tickers with current prices' },
        { instruction: 'Add to watchlist: `watch add AAPL`', command: 'watch add TSLA', expectedOutput: 'Ticker added' },
        { instruction: 'Remove: `watch rm AAPL`', command: 'watch rm AAPL', expectedOutput: 'Ticker removed' },
      ],
      quiz: [
        { question: 'How do you add a ticker to your watchlist?', options: ['watch add <ticker>', 'add watch <ticker>', 'track <ticker>', 'follow <ticker>'], correctIndex: 0, explanation: '`watch add <ticker>` adds an asset to your watchlist.' },
      ],
    },
    {
      id: 'aa-factors',
      slug: 'factors',
      title: 'Factor & Sector Analysis',
      description: 'Understand factor exposures and sector dynamics.',
      commands: ['factors', 'sectorsexposure', 'anportfolio', 'anrisk'],
      steps: [
        { instruction: 'Factor analysis: `factors AAPL`', command: 'factors AAPL', expectedOutput: 'Size, value, momentum, quality, low-vol factor scores' },
        { instruction: 'Portfolio analytics: `anportfolio 1`', command: 'anportfolio 1', expectedOutput: 'Full portfolio analytics report' },
        { instruction: 'Risk analytics: `anrisk 1`', command: 'anrisk 1', expectedOutput: 'Portfolio risk decomposition' },
      ],
      quiz: [
        { question: 'What does `factors` analyze?', options: ['Fama-French factor exposures', 'Company fundamentals', 'Technical indicators', 'Sector weights'], correctIndex: 0, explanation: '`factors` shows Fama-French factor exposures: size, value, momentum, quality, and low volatility.' },
      ],
    },
    {
      id: 'aa-calc',
      slug: 'calc',
      title: 'Custom Calculations',
      description: 'Compute P&L and run pipeline analytics.',
      commands: ['calc pnl', 'pipelines', 'optperf'],
      steps: [
        { instruction: 'Calculate P&L: `calc pnl`', command: 'calc pnl', expectedOutput: 'Realized and unrealized P&L breakdown' },
        { instruction: 'Pipeline runs: `pipelines`', command: 'pipelines', expectedOutput: 'Data pipeline execution log' },
        { instruction: 'Optimizer performance: `optperf`', command: 'optperf', expectedOutput: 'Rust optimizer speed and accuracy benchmarks' },
      ],
      quiz: [
        { question: 'What is the Rust optimizer used for?', options: ['Portfolio optimization', 'Market data', 'Order execution', 'News parsing'], correctIndex: 0, explanation: 'The Rust PyO3 optimizer performs high-speed portfolio optimization calculations.' },
      ],
    },
  ],
}
