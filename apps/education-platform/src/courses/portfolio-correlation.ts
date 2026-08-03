import type { Course } from '../lib/types'

export const portfolioCorrelation: Course = {
  id: 'portfolio-correlation',
  slug: 'portfolio-correlation',
  title: 'Portfolio Correlation & Benchmarking',
  description: 'Measure how assets move together, compare against benchmarks, and analyze drawdowns — the cat tracks everything.',
  category: 'Analytics',
  difficulty: 'intermediate',
  icon: '📊',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'correlation-matrix',
      slug: 'correlation-matrix',
      title: 'Correlation Matrices',
      description: 'Understand how assets relate to each other.',
      commands: ['correlation AAPL,MSFT,GOOGL', 'correlation SPY,TLT,GLD'],
      steps: [
        { instruction: 'Run a correlation matrix: `correlation AAPL,MSFT,GOOGL`', command: 'correlation AAPL,MSFT,GOOGL', expectedOutput: 'NxN table of correlation coefficients' },
        { instruction: 'Values near 1 = move together, near 0 = unrelated, near -1 = opposite directions.' },
        { instruction: 'The cat diversifies: stocks AND tuna cans (correlation: -0.8 on Fridays).' },
        { instruction: 'Try bonds vs stocks: `correlation SPY,TLT,GLD`', command: 'correlation SPY,TLT,GLD', expectedOutput: 'Lower correlations = better diversification' },
      ],
      quiz: [
        { question: 'What does a correlation of -0.5 between two assets mean?', options: ['They tend to move in opposite directions moderately', 'They move together perfectly', 'They are completely unrelated', 'One is double the other'], correctIndex: 0, explanation: 'Negative correlation means assets tend to move in opposite directions. -0.5 is a moderate inverse relationship.' },
      ],
    },
    {
      id: 'pairs-trading',
      slug: 'pairs-trading',
      title: 'Pairs Trading Analysis',
      description: 'Find cointegrated pairs for mean-reversion strategies.',
      commands: ['pairtrade XOM CVX', 'pairtrade AAPL MSFT'],
      steps: [
        { instruction: 'Analyze a pair: `pairtrade XOM CVX` — Exxon vs Chevron', command: 'pairtrade XOM CVX', expectedOutput: 'Cointegration test, hedge ratio, z-score, signals' },
        { instruction: 'Cointegrated pairs share a long-run equilibrium. When they diverge, they tend to revert.' },
        { instruction: 'The cat pairs tuna with salmon. When tuna is cheap, buy tuna, sell salmon. Meow-reversion.' },
        { instruction: 'Try tech: `pairtrade AAPL MSFT`', command: 'pairtrade AAPL MSFT', expectedOutput: 'Z-scores and cointegration stats for tech giants' },
      ],
      quiz: [
        { question: 'What does cointegration mean for two stocks?', options: ['They share a long-term equilibrium relationship', 'They have the same price', 'They are in the same industry', 'They always move together'], correctIndex: 0, explanation: 'Cointegration means the spread between two assets is mean-reverting — when they diverge, they tend to come back together.' },
      ],
    },
    {
      id: 'benchmark-comparison',
      slug: 'benchmark-comparison',
      title: 'Benchmark Comparison',
      description: 'Measure alpha, beta, and performance vs benchmarks.',
      commands: ['benchmark AAPL SPY', 'benchmark TSLA QQQ'],
      steps: [
        { instruction: 'Compare AAPL to SPY: `benchmark AAPL SPY`', command: 'benchmark AAPL SPY', expectedOutput: 'Alpha, beta, tracking error, Sharpe ratio, R-squared' },
        { instruction: 'Positive alpha means the stock outperformed its benchmark on a risk-adjusted basis.' },
        { instruction: 'The cat has alpha in tuna picking. Beta is just following the fish market.' },
        { instruction: 'Try TSLA vs QQQ: `benchmark TSLA QQQ`', command: 'benchmark TSLA QQQ', expectedOutput: 'Higher beta = more volatility than the benchmark' },
      ],
      quiz: [
        { question: 'What does a beta of 1.5 mean?', options: ['The stock moves 50% more than the benchmark', 'The stock is 50% less volatile', 'The stock has 1.5% alpha', 'The stock trades at $1.50'], correctIndex: 0, explanation: 'A beta of 1.5 means if the benchmark moves 1%, the stock tends to move 1.5% in the same direction.' },
      ],
    },
    {
      id: 'drawdown-analysis',
      slug: 'drawdown-analysis',
      title: 'Drawdown Analysis',
      description: 'Understand the worst losses in historical context.',
      commands: ['drawdown AAPL', 'drawdown SPY'],
      steps: [
        { instruction: 'Analyze drawdown: `drawdown AAPL`', command: 'drawdown AAPL', expectedOutput: 'Max drawdown %, start/end dates, top 10 drawdowns' },
        { instruction: 'Max drawdown shows the largest peak-to-trough decline. Lower is better.' },
        { instruction: 'The cat once experienced a 50% drawdown in tuna supply. It was a dark winter.' },
        { instruction: 'Check the S&P 500: `drawdown SPY`', command: 'drawdown SPY', expectedOutput: 'Historical drawdowns — 2008, 2020, 2022' },
      ],
      quiz: [
        { question: 'Why is max drawdown important?', options: ['It shows the worst-case historical loss, helping you size positions appropriately', 'It predicts future returns', 'It measures trading volume', 'It shows the average gain'], correctIndex: 0, explanation: 'Max drawdown helps you understand the worst pain you might experience, which is crucial for position sizing and risk management.' },
      ],
    },
  ],
}
