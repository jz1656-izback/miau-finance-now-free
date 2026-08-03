import type { Course } from '../lib/types'

export const pythonForFinance: Course = {
  id: 'python-for-finance',
  slug: 'python-for-finance',
  title: 'Python for Finance',
  description: 'Pandas, data analysis, backtesting, and APIs — the cat writes Pythonic portfolios.',
  category: 'Programming',
  difficulty: 'intermediate',
  icon: '🐍',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'py-pandas',
      slug: 'pandas-basics',
      title: 'Pandas for Financial Data',
      description: 'Manipulate time series data with pandas.',
      commands: ['python', 'python pandas'],
      steps: [
        { instruction: 'Load financial data with pandas: `python pandas --load AAPL --start 2023-01-01`', command: 'python pandas --load AAPL --start 2023-01-01', expectedOutput: 'DataFrame with OHLCV data for AAPL' },
        { instruction: 'Pandas DataFrame is the core structure for financial data analysis.' },
        { instruction: 'Use `.resample()` to convert daily data to weekly or monthly.' },
      ],
      quiz: [
        { question: 'Which pandas method resamples time series data?', options: ['.resample()', '.groupby()', '.aggregate()', '.transform()'], correctIndex: 0, explanation: 'The .resample() method in pandas is used to change the frequency of time series data.' },
      ],
    },
    {
      id: 'py-analysis',
      slug: 'financial-analysis',
      title: 'Financial Data Analysis',
      description: 'Calculate returns, volatility, and correlations.',
      commands: ['python analyze', 'python metrics'],
      steps: [
        { instruction: 'Analyze a stock: `python analyze --symbol AAPL --metrics all`', command: 'python analyze --symbol AAPL --metrics all', expectedOutput: 'Returns, volatility, Sharpe ratio, and correlation matrix' },
        { instruction: 'Daily returns = (Price_today / Price_yesterday) - 1. Volatility = standard deviation of returns.' },
        { instruction: 'Correlation matrix shows how assets move relative to each other.' },
      ],
      quiz: [
        { question: 'What does a Sharpe ratio above 1 indicate?', options: ['Good risk-adjusted returns', 'Poor risk-adjusted returns', 'High volatility', 'Negative returns'], correctIndex: 0, explanation: 'A Sharpe ratio above 1 indicates that the investment\'s returns exceed the risk-free rate by more than its volatility.' },
      ],
    },
    {
      id: 'py-backtest',
      slug: 'backtesting-basics',
      title: 'Backtesting Strategies',
      description: 'Test trading strategies on historical data.',
      commands: ['backtest', 'backtest run'],
      steps: [
        { instruction: 'Run a backtest: `backtest run --strategy "SMA Crossover" --symbol AAPL`', command: 'backtest run --strategy "SMA Crossover" --symbol AAPL', expectedOutput: 'Backtest results with returns, drawdown, and trade log' },
        { instruction: 'Backtesting evaluates a strategy on historical data before risking real money.' },
        { instruction: 'Watch for look-ahead bias and survivorship bias in backtests.' },
      ],
      quiz: [
        { question: 'What is look-ahead bias in backtesting?', options: ['Using future data that would not have been available', 'Looking at past performance', 'Forward testing a strategy', 'Ignoring transaction costs'], correctIndex: 0, explanation: 'Look-ahead bias occurs when a backtest uses information that was not available at the time of the trade.' },
      ],
    },
    {
      id: 'py-apis',
      slug: 'financial-apis',
      title: 'Financial Data APIs',
      description: 'Fetch live and historical data from APIs.',
      commands: ['data', 'data fetch'],
      steps: [
        { instruction: 'Fetch data from an API: `data fetch --symbol AAPL --source yahoo`', command: 'data fetch --symbol AAPL --source yahoo', expectedOutput: 'OHLCV data from Yahoo Finance API' },
        { instruction: 'Popular APIs: Yahoo Finance, Alpha Vantage, IEX Cloud, Polygon.' },
        { instruction: 'Most financial APIs require an API key and have rate limits.' },
      ],
      quiz: [
        { question: 'What is typically needed to use a financial data API?', options: ['An API key', 'A brokerage account', 'A trading license', 'A minimum balance'], correctIndex: 0, explanation: 'Financial data APIs typically require registration for an API key, which authenticates your requests.' },
      ],
    },
  ],
}
