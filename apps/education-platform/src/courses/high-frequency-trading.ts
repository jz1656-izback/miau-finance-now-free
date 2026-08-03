import type { Course } from '../lib/types'

export const highFrequencyTrading: Course = {
  id: 'high-frequency-trading',
  slug: 'high-frequency-trading',
  title: 'High-Frequency Trading',
  description: 'Latency arb, colocation, market making, and statistical arbitrage — the cat trades faster than you can blink.',
  category: 'Trading',
  difficulty: 'advanced',
  icon: '⚡',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'hft-basics',
      slug: 'hft-fundamentals',
      title: 'HFT Fundamentals',
      description: 'What makes HFT different from regular trading.',
      commands: ['hft latency', 'hft strategy'],
      steps: [
        { instruction: 'Check your current connection latency: `hft latency --server ny4`', command: 'hft latency --server ny4', expectedOutput: 'Latency to NY4: 12.4ms — too slow for HFT. Target: <100μs' },
        { instruction: 'HFT relies on speed — microseconds matter. A 1ms advantage can be worth $100M/year.' },
        { instruction: 'List available HFT strategies: `hft strategy --list`', command: 'hft strategy --list', expectedOutput: 'Strategies: market-making, latency-arb, stat-arb, momentum-ignition, cross-exchange-arb' },
        { instruction: 'The cat\'s HFT strategy is "pounce first, ask questions later."' },
      ],
      quiz: [
        { question: 'What is the typical latency target for HFT?', options: ['Under 100 microseconds', 'Under 1 second', 'Under 1 millisecond', 'Under 1 nanosecond'], correctIndex: 0, explanation: 'HFT firms target sub-100 microsecond latency. Every microsecond of delay is lost opportunity and lost profit.' },
      ],
    },
    {
      id: 'colocation',
      slug: 'exchange-colocation',
      title: 'Exchange Colocation',
      description: 'Placing servers physically near exchange matching engines.',
      commands: ['hft colo', 'hft colo --list'],
      steps: [
        { instruction: 'Check colocation availability at CME: `hft colo --exchange cme --location aurora`', command: 'hft colo --exchange cme --location aurora', expectedOutput: 'CME Aurora colo: rack space available in Pod B (2ft from matching engine). Latency: 4μs. Monthly: $15,000' },
        { instruction: 'Colocation reduces physical distance, cutting latency from milliseconds to microseconds.' },
        { instruction: 'List all colo sites: `hft colo --list`', command: 'hft colo --list', expectedOutput: 'NY4 (NYSE), NJ2 (NASDAQ), Aurora (CME), Basildon (LSE), Bergamo (BATS Europe)' },
        { instruction: 'The cat\'s servers are in NY4. The cat pays rent in tuna. It is a very expensive location.' },
      ],
      quiz: [
        { question: 'Why do HFT firms use colocation?', options: ['To reduce physical distance to the exchange matching engine, minimizing latency', 'To save on electricity costs', 'To be closer to other traders for networking', 'To access better coffee machines'], correctIndex: 0, explanation: 'Colocation places trading servers as close as possible to exchange matching engines, reducing physical cable length and therefore signal propagation time.' },
      ],
    },
    {
      id: 'market-making',
      slug: 'electronic-market-making',
      title: 'Electronic Market Making',
      description: 'Providing liquidity through automated bid-ask quotes.',
      commands: ['hft mm', 'hft mm --symbol SPY'],
      steps: [
        { instruction: 'Check current market making stats for SPY: `hft mm --symbol SPY`', command: 'hft mm --symbol SPY', expectedOutput: 'SPY MM: Spread $0.01, Volume 12M shares, Quote frequency 850/s, Fill rate 62%, P&L +$42,350 today' },
        { instruction: 'Market makers earn the spread by simultaneously bidding and asking. Speed determines who gets filled.' },
        { instruction: 'The cat\'s market making algo is "buy the dip, sell the rip, nap at noon."' },
        { instruction: 'Start a market making strategy: `hft mm --start --symbol SPY --risk 100000`', command: 'hft mm --start --symbol SPY --risk 100000', expectedOutput: 'MM engine started for SPY. Max position: $100,000. Target spread: $0.01. Quote frequency: 1,000/s' },
      ],
      quiz: [
        { question: 'How do electronic market makers profit?', options: ['By earning the bid-ask spread on high-frequency quotes', 'By predicting stock prices', 'By holding positions overnight', 'By charging subscription fees'], correctIndex: 0, explanation: 'Market makers earn the spread by simultaneously posting bid and ask quotes. They profit when they buy at the bid and sell at the ask more frequently than the adverse selection costs.' },
      ],
    },
    {
      id: 'stat-arb',
      slug: 'statistical-arbitrage-hft',
      title: 'Statistical Arbitrage',
      description: 'Pairs trading and mean reversion at high frequency.',
      commands: ['hft pairs', 'hft arb'],
      steps: [
        { instruction: 'Scan for cointegrated pairs: `hft pairs --scan --universe sp500`', command: 'hft pairs --scan --universe sp500', expectedOutput: 'Top pairs: XOM-CVX (z-score 0.3), JPM-GS (z-score 0.8), MSFT-AAPL (z-score 1.2). Mean reversion horizon: 2-5 minutes' },
        { instruction: 'Statistical arbitrage exploits temporary price dislocations between related securities.' },
        { instruction: 'Run a pairs trade: `hft arb --pair XOM-CVX --entry-z 2 --exit-z 0 --capital 50000`', command: 'hft arb --pair XOM-CVX --entry-z 2 --exit-z 0 --capital 50000', expectedOutput: 'Pairs trade opened: Long XOM, Short CVX. Entry z-score: 2.1. Position: +$50,000 / -$50,000. Expected horizon: 3min' },
        { instruction: 'The cat\'s pairs trading strategy pairs "tuna" with "more tuna."' },
      ],
      quiz: [
        { question: 'What is the key statistical concept behind pairs trading?', options: ['Cointegration — two assets maintain a stationary spread over time', 'Correlation — two assets move in the same direction', 'Standard deviation — one asset is more volatile', 'Beta — one asset amplifies market moves'], correctIndex: 0, explanation: 'Pairs trading relies on cointegration: two assets whose price spread is mean-reverting. When the spread widens beyond a threshold, you bet on convergence.' },
      ],
    },
  ],
}
