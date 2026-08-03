import type { Course } from '../lib/types'

export const technicalAnalysis: Course = {
  id: 'technical-analysis',
  slug: 'technical-analysis',
  title: 'Technical Analysis',
  description: 'Backtesting, strategy comparison, and rolling metrics.',
  category: 'Analytics',
  difficulty: 'intermediate',
  icon: '🔍',
  lessonCount: 3,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'ta-backtest',
      slug: 'backtest',
      title: 'Strategy Backtesting',
      description: 'Test trading strategies on historical data.',
      commands: ['backtest'],
      steps: [
        { instruction: 'Run a backtest: `backtest AAPL`', command: 'backtest AAPL', expectedOutput: 'Backtest results with metrics displayed' },
        { instruction: 'The backtest runs the selected strategy against historical price data.' },
        { instruction: 'Look at Sharpe ratio, max drawdown, and win rate in the output.' },
      ],
      quiz: [
        { question: 'What does `backtest` evaluate?', options: ['Strategy performance on historical data', 'Live trading signals', 'Market forecasts', 'Tax implications'], correctIndex: 0, explanation: '`backtest` runs a strategy against historical data to measure how it would have performed.' },
      ],
    },
    {
      id: 'ta-rolling',
      slug: 'rolling',
      title: 'Rolling Metrics',
      description: 'Track performance metrics over rolling windows.',
      commands: ['rolling'],
      steps: [
        { instruction: 'View rolling metrics: `rolling AAPL`', command: 'rolling AAPL', expectedOutput: 'Rolling Sharpe, beta, volatility over time' },
        { instruction: 'Rolling windows show how metrics change over different time periods.' },
        { instruction: 'Use this to spot trends in risk and return.' },
      ],
      quiz: [
        { question: 'What does `rolling` measure over time?', options: ['Sharpe, beta, and volatility', 'Price only', 'Volume only', 'News sentiment'], correctIndex: 0, explanation: '`rolling` tracks metrics like Sharpe ratio, beta, and volatility over rolling time windows.' },
      ],
    },
    {
      id: 'ta-scenario',
      slug: 'scenario',
      title: 'Scenario Analysis',
      description: 'See how assets perform in different market scenarios.',
      commands: ['scenario', 'dividends'],
      steps: [
        { instruction: 'Run scenario analysis: `scenario AAPL`', command: 'scenario AAPL', expectedOutput: 'Bear, base, and bull case projections' },
        { instruction: 'Check dividend data: `dividends AAPL`', command: 'dividends AAPL', expectedOutput: 'Dividend yield, payout ratio, history' },
      ],
      quiz: [
        { question: 'Which scenarios does `scenario` analyze?', options: ['Bear, base, and bull', 'Only bull', 'Only bear', 'Past scenarios'], correctIndex: 0, explanation: '`scenario` presents bear, base, and bull case projections for the asset.' },
      ],
    },
  ],
}
