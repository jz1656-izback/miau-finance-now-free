import type { Course } from '../lib/types'

export const riskAnalytics: Course = {
  id: 'risk-analytics',
  slug: 'risk-analytics',
  title: 'Risk Analytics',
  description: 'VaR, beta, stress tests, correlation, and factor attribution.',
  category: 'Analytics',
  difficulty: 'advanced',
  icon: '⚠️',
  lessonCount: 5,
  estimatedMinutes: 30,
  lessons: [
    {
      id: 'ra-risk',
      slug: 'risk',
      title: 'Risk Assessment',
      description: 'Full risk reports for any asset.',
      commands: ['risk', 'var'],
      steps: [
        { instruction: 'Full risk report: `risk AAPL`', command: 'risk AAPL', expectedOutput: 'VaR, beta, volatility, Sharpe, max drawdown' },
        { instruction: 'Value at Risk: `var AAPL`', command: 'var AAPL', expectedOutput: '95% and 99% VaR values' },
        { instruction: 'VaR tells you the maximum expected loss at a given confidence level.' },
      ],
      quiz: [
        { question: 'What does VaR stand for?', options: ['Value at Risk', 'Variance', 'Volatility and Return', 'Very Aggressive Risk'], correctIndex: 0, explanation: 'VaR = Value at Risk — the maximum expected loss at a confidence level.' },
      ],
    },
    {
      id: 'ra-beta',
      slug: 'beta',
      title: 'Beta & Correlation',
      description: 'Measure how an asset moves with the market.',
      commands: ['beta', 'correlation', 'factors'],
      steps: [
        { instruction: 'Get beta: `beta AAPL`', command: 'beta AAPL', expectedOutput: 'Beta value and interpretation' },
        { instruction: 'Correlation matrix: `correlation`', command: 'correlation', expectedOutput: 'Asset correlation table' },
        { instruction: 'Factor analysis: `factors AAPL`', command: 'factors AAPL', expectedOutput: 'Fama-French factor exposures' },
      ],
      quiz: [
        { question: 'What does a beta of 1.0 mean?', options: ['Moves with the market', 'Twice the market', 'Half the market', 'No correlation'], correctIndex: 0, explanation: 'A beta of 1.0 means the asset moves in line with the overall market.' },
      ],
    },
    {
      id: 'ra-stress',
      slug: 'stress',
      title: 'Stress Testing',
      description: 'Simulate extreme market events.',
      commands: ['stress'],
      steps: [
        { instruction: 'Run a stress test: `stress AAPL`', command: 'stress AAPL', expectedOutput: 'Projected loss under crisis scenarios' },
        { instruction: 'Stress tests simulate: 2008 crash, 2020 COVID crash, rate hikes, etc.' },
      ],
      quiz: [
        { question: 'What does `stress` simulate?', options: ['Extreme market scenarios', 'Daily price movements', 'Order book depth', 'Your anxiety'], correctIndex: 0, explanation: '`stress` tests asset performance under extreme scenarios like crashes and crises.' },
      ],
    },
    {
      id: 'ra-attrib',
      slug: 'attrib',
      title: 'Performance Attribution',
      description: 'Understand what drives your returns.',
      commands: ['attrib', 'attrib sector', 'attrib security', 'attrib factor'],
      steps: [
        { instruction: 'Full attribution: `attrib <pid>`', command: 'attrib 1', expectedOutput: 'Brinson sector + security attribution' },
        { instruction: 'Sector only: `attrib sector 1`' },
        { instruction: 'Factor attribution: `attrib factor 1`' },
      ],
      quiz: [
        { question: 'What does performance attribution answer?', options: ['What drove portfolio returns', 'What stocks to buy', 'Market direction', 'Tax liability'], correctIndex: 0, explanation: 'Attribution breaks down returns into allocation and selection effects.' },
      ],
    },
    {
      id: 'ra-optimize',
      slug: 'optimize',
      title: 'Portfolio Optimization',
      description: 'Find the best portfolio weights.',
      commands: ['optimize', 'minvar', 'eqweight'],
      steps: [
        { instruction: 'Max Sharpe optimization: `optimize AAPL MSFT GOOGL`', command: 'optimize AAPL MSFT GOOGL', expectedOutput: 'Optimal weights for max risk-adjusted return' },
        { instruction: 'Minimum variance: `minvar AAPL MSFT TSLA`', command: 'minvar AAPL MSFT GOOGL', expectedOutput: 'Weights for lowest volatility' },
        { instruction: 'Equal weight: `eqweight AAPL MSFT GOOGL TSLA NVDA`', command: 'eqweight AAPL MSFT GOOGL TSLA NVDA', expectedOutput: 'Equal allocation across all assets' },
      ],
      quiz: [
        { question: 'What does `optimize` maximize?', options: ['Sharpe ratio', 'Returns only', 'Diversification', 'Dividends'], correctIndex: 0, explanation: '`optimize` finds the portfolio with the highest Sharpe ratio (risk-adjusted return).' },
      ],
    },
  ],
}
