import type { Course } from '../lib/types'

export const arbitrage: Course = {
  id: 'arbitrage-strategies',
  slug: 'arbitrage-strategies-overview',
  title: 'Arbitrage Strategies',
  description: 'Merger arb, convertible arb, statistical arb, and triangular arb — the cat spots price discrepancies faster than it spots a laser pointer.',
  category: 'Trading',
  difficulty: 'advanced',
  icon: '⚡',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'merger-arb',
      slug: 'merger-arbitrage',
      title: 'Merger Arbitrage',
      description: 'Capturing spreads in M&A transactions.',
      commands: ['arb', 'merger-arb'],
      steps: [
        { instruction: 'Analyze a merger arb opportunity: `merger-arb --analyze --target "Company A" --acquirer "Company B" --offer 50 --stock-price 48`', command: 'merger-arb --analyze --target "Company A" --acquirer "Company B" --offer 50 --stock-price 48', expectedOutput: 'Merger arb spread: 4.2% ($2 difference). Annualized (3mo close): 16.8%. Risk: regulatory hurdles, shareholder vote. Probability of close: 85%' },
        { instruction: 'Merger arbitrage involves buying the target stock after an acquisition is announced.' },
        { instruction: 'The cat trades merger arb — it buys companies that are about to be acquired by bigger fish.' },
      ],
      quiz: [
        { question: 'What is the main risk in merger arbitrage?', options: ['The deal fails to close due to regulatory, financing, or shareholder issues', 'The stock market crashes', 'The acquirer runs out of cash', 'The target company rejects the offer'], correctIndex: 0, explanation: 'Deal risk is the primary concern — if the acquisition falls through, the target stock typically drops below the pre-announcement price.' },
      ],
    },
    {
      id: 'statistical-arb',
      slug: 'statistical-arbitrage',
      title: 'Statistical Arbitrage',
      description: 'Pairs trading and mean reversion strategies.',
      commands: ['stat-arb', 'arb'],
      steps: [
        { instruction: 'Find cointegrated pairs: `stat-arb --pairs --universe SP100 --lookback 252`', command: 'stat-arb --pairs --universe SP100 --lookback 252', expectedOutput: 'Top cointegrated pairs: PEP/KO (z-score -2.1, hedge ratio 0.85), JPM/BAC (z-score 1.8, hedge ratio 1.2), XOM/CVX (z-score -1.5, hedge ratio 0.7)' },
        { instruction: 'Pairs trading involves finding two stocks that move together and trading the divergence.' },
        { instruction: 'The cat found a cointegrated pair of tuna brands — when one dips, the other follows.' },
        { instruction: 'Execute a pairs trade: `stat-arb --trade --pair PEP/KO --z-threshold 2 --position-size 50000`', command: 'stat-arb --trade --pair PEP/KO --z-threshold 2 --position-size 50000', expectedOutput: 'Pairs trade opened: Long PEP, short KO (hedge ratio 0.85). $50K position, z-score -2.1. Mean reversion target: z-score 0 — profit target: $1,800' },
      ],
      quiz: [
        { question: 'What is cointegration in statistical arbitrage?', options: ['A statistical property where two time series move together with a stable long-term relationship', 'When two stocks have the same price', 'When stocks are listed on the same exchange', 'When stocks have the same beta'], correctIndex: 0, explanation: 'Cointegration means two securities have a statistically stable long-term relationship, making them suitable for pairs trading strategies.' },
      ],
    },
    {
      id: 'triangular-arb',
      slug: 'triangular-arbitrage',
      title: 'Triangular Arbitrage',
      description: 'Exploiting FX cross-rate discrepancies.',
      commands: ['triangular', 'arb'],
      steps: [
        { instruction: 'Detect triangular arbitrage: `triangular --detect --pairs EUR/USD,GBP/USD,EUR/GBP`', command: 'triangular --detect --pairs EUR/USD,GBP/USD,EUR/GBP', expectedOutput: 'Triangular arb detected: EUR/USD 1.08, GBP/USD 1.26, EUR/GBP 0.857. Implied EUR/GBP: 0.8571 vs actual 0.8570 — spread too small (<0.1%)' },
        { instruction: 'Triangular arbitrage exploits pricing discrepancies between three currency pairs.' },
        { instruction: 'The cat tried triangular arb — got dizzy converting tuna dollars to sardine pounds to kibble euros.' },
      ],
      quiz: [
        { question: 'Why has triangular arbitrage become rare in modern markets?', options: ['High-frequency trading and algorithmic systems quickly eliminate discrepancies', 'Central banks prohibit it', 'Currency markets are too small', 'Transaction costs are zero'], correctIndex: 0, explanation: 'HFT algorithms and sophisticated trading systems instantly detect and exploit triangular arbitrage opportunities, keeping markets efficient.' },
      ],
    },
    {
      id: 'arb-risk',
      slug: 'arbitrage-risk-management',
      title: 'Arbitrage Risk & Execution',
      description: 'Managing risks and executing arbitrage strategies.',
      commands: ['arb', 'merger-arb'],
      steps: [
        { instruction: 'Assess arb trade risk: `arb --risk --type merger-arb --spread 0.05 --probability-close 0.85`', command: 'arb --risk --type merger-arb --spread 0.05 --probability-close 0.85', expectedOutput: 'Risk-adjusted return: 4.2% × 85% = 3.57% expected return. Downside: 15% chance of -15% gap = -2.25% expected loss. Net expected value: +1.32%' },
        { instruction: 'Arbitrage strategies are often called "picking up nickels in front of steamrollers."' },
        { instruction: 'The cat learned about arb risk the hard way — it picked up a nickel and the steamroller was a vacuum cleaner.' },
      ],
      quiz: [
        { question: 'Why is arbitrage often described as "picking up nickels in front of steamrollers"?', options: ['Arb trades offer small, frequent gains but risk rare, catastrophic losses', 'Arb trades are extremely profitable', 'Arb trades involve nickels', 'Arb traders are reckless'], correctIndex: 0, explanation: 'This phrase captures how arbitrage strategies generate many small profits but occasionally suffer devastating losses when normal market relationships break down.' },
      ],
    },
  ],
}
