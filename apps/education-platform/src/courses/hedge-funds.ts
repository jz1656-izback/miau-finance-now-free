import type { Course } from '../lib/types'

export const hedgeFunds: Course = {
  id: 'hedge-funds',
  slug: 'hedge-funds',
  title: 'Hedge Fund Strategies',
  description: 'Long/short, global macro, event-driven, and relative value — the cat hedges its bets.',
  category: 'Hedge Funds',
  difficulty: 'advanced',
  icon: '🦈',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'hf-long-short',
      slug: 'long-short-equity',
      title: 'Long/Short Equity',
      description: 'The classic hedge fund strategy — buy winners, short losers.',
      commands: ['hedge-fund', 'hedge-fund long-short'],
      steps: [
        { instruction: 'Analyze a long/short portfolio: `hedge-fund long-short --long AAPL MSFT --short TSLA`', command: 'hedge-fund long-short --long AAPL MSFT --short TSLA', expectedOutput: 'Portfolio breakdown with net and gross exposure' },
        { instruction: 'Net exposure = long % - short %. Gross exposure = long % + short %.' },
        { instruction: 'Market-neutral funds target near-zero net exposure to isolate stock selection alpha.' },
      ],
      quiz: [
        { question: 'What is gross exposure in a long/short fund?', options: ['Long % + Short %', 'Long % - Short %', 'Short % - Long %', 'Absolute value of net exposure'], correctIndex: 0, explanation: 'Gross exposure is the sum of long and short positions as a percentage of capital, measuring total market exposure.' },
      ],
    },
    {
      id: 'hf-macro',
      slug: 'global-macro',
      title: 'Global Macro',
      description: 'Trade based on macroeconomic trends across asset classes.',
      commands: ['long-short', 'long-short macro'],
      steps: [
        { instruction: 'View macro indicators: `global-macro --indicators gdp inflation rates`', command: 'global-macro --indicators gdp inflation rates', expectedOutput: 'Macro dashboard with GDP, inflation, and interest rate trends' },
        { instruction: 'Global macro funds trade currencies, bonds, equities, and commodities based on macro views.' },
        { instruction: 'George Soros famously "broke the Bank of England" with a macro trade in 1992.' },
      ],
      quiz: [
        { question: 'What do global macro funds trade based on?', options: ['Macroeconomic trends and policies', 'Individual stock analysis', 'Technical chart patterns', 'Corporate earnings'], correctIndex: 0, explanation: 'Global macro funds make directional bets based on macroeconomic analysis of interest rates, currencies, and economic policies.' },
      ],
    },
    {
      id: 'hf-event',
      slug: 'event-driven',
      title: 'Event-Driven Strategies',
      description: 'Profit from corporate events like mergers, bankruptcies, and spin-offs.',
      commands: ['global-macro', 'global-macro trade'],
      steps: [
        { instruction: 'Find event-driven opportunities: `event --list --type merger`', command: 'event --list --type merger', expectedOutput: 'Merger arbitrage opportunities with spread and probability' },
        { instruction: 'Merger arbitrage buys the target and shorts the acquirer to capture the spread.' },
        { instruction: 'Distressed debt funds buy bonds of companies in or near bankruptcy.' },
      ],
      quiz: [
        { question: 'How does merger arbitrage profit?', options: ['By capturing the spread between target price and deal price', 'By predicting the next merger', 'By shorting the overall market', 'By buying call options'], correctIndex: 0, explanation: 'Merger arbitrage captures the price spread between the target\'s current stock price and the acquisition price offered.' },
      ],
    },
    {
      id: 'hf-relative',
      slug: 'relative-value',
      title: 'Relative Value & Arbitrage',
      description: 'Exploit price discrepancies between related securities.',
      commands: ['event', 'event arbitrage'],
      steps: [
        { instruction: 'Find relative value opportunities: `relative-value --pairs`', command: 'relative-value --pairs', expectedOutput: 'Pairs trading opportunities with z-score and hedge ratio' },
        { instruction: 'Convertible arbitrage buys convertible bonds and shorts the underlying stock.' },
        { instruction: 'Statistical arbitrage uses mean reversion models to trade baskets of stocks.' },
      ],
      quiz: [
        { question: 'What is pairs trading?', options: ['Going long one stock and short a correlated stock', 'Trading two of the same stock', 'Buying a pair of options', 'Trading in pairs of currencies'], correctIndex: 0, explanation: 'Pairs trading involves taking a long position in one stock and a short position in a correlated stock to profit from convergence.' },
      ],
    },
  ],
}
