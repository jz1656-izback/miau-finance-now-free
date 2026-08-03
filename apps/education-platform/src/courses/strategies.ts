import type { Course } from '../lib/types'

export const strategies: Course = {
  id: 'strategies',
  slug: 'strategies',
  title: 'Trading Strategies',
  description: 'Deploy, backtest, and compare algorithmic strategies.',
  category: 'Trading',
  difficulty: 'advanced',
  icon: '🧠',
  lessonCount: 3,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'st-list',
      slug: 'list',
      title: 'Strategy Overview',
      description: 'See available strategies and their descriptions.',
      commands: ['strategy list'],
      steps: [
        { instruction: 'List strategies: `strategy list`', command: 'strategy list', expectedOutput: 'SMA, RSI, MACD, Bollinger, Mean Reversion, Momentum' },
        { instruction: 'Each strategy has different parameters and logic.' },
        { instruction: 'Strategies run on paper accounts to test before going live.' },
      ],
      quiz: [
        { question: 'How many built-in strategies are available?', options: ['6 core strategies', '3', '10', '20'], correctIndex: 0, explanation: 'Six core strategies: SMA, RSI, MACD, Bollinger, Mean Reversion, and Momentum.' },
      ],
    },
    {
      id: 'st-backtest',
      slug: 'backtest',
      title: 'Strategy Backtesting',
      description: 'Test any strategy against historical data.',
      commands: ['strategy backtest'],
      steps: [
        { instruction: 'Backtest: `strategy backtest SMA AAPL`', command: 'strategy backtest SMA AAPL', expectedOutput: 'Performance metrics: Sharpe, drawdown, win rate, CAGR' },
        { instruction: 'The backtest simulates the strategy over the past year of data.' },
        { instruction: 'Results include equity curve, trade log, and risk metrics.' },
      ],
      quiz: [
        { question: 'What metrics does a strategy backtest show?', options: ['Sharpe, drawdown, win rate, CAGR', 'Only P&L', 'Sentiment score', 'News analysis'], correctIndex: 0, explanation: 'Strategy backtests provide comprehensive metrics including risk-adjusted returns.' },
      ],
    },
    {
      id: 'st-compare',
      slug: 'compare',
      title: 'Strategy Comparison',
      description: 'Compare multiple strategies side by side.',
      commands: ['strategy compare'],
      steps: [
        { instruction: 'Compare: `strategy compare SMA,MACD AAPL`', command: 'strategy compare SMA,MACD AAPL', expectedOutput: 'Head-to-head comparison table' },
        { instruction: 'See which strategy works best for a specific ticker.' },
        { instruction: 'Use this to select the optimal strategy before deploying.' },
      ],
      quiz: [
        { question: 'What does `strategy compare` help you do?', options: ['Evaulate multiple strategies on one ticker', 'Compare tickers', 'View market data', 'Analyze sectors'], correctIndex: 0, explanation: '`strategy compare` runs multiple strategies on the same ticker for direct comparison.' },
      ],
    },
  ],
}
