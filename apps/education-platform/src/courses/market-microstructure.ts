import type { Course } from '../lib/types'

export const marketMicrostructure: Course = {
  id: 'market-microstructure',
  slug: 'market-microstructure',
  title: 'Market Microstructure',
  description: 'Order book, HFT, dark pools, and spreads — the cat sees the tape.',
  category: 'Market Structure',
  difficulty: 'advanced',
  icon: '⚡',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'mm-orderbook',
      slug: 'order-book',
      title: 'The Order Book',
      description: 'Understand how buy and sell orders match.',
      commands: ['orderbook', 'orderbook view'],
      steps: [
        { instruction: 'View the order book: `orderbook view --symbol AAPL`', command: 'orderbook view --symbol AAPL', expectedOutput: 'Order book with bid/ask levels, sizes, and depth chart' },
        { instruction: 'Bids are buy orders at various price levels. Asks are sell orders.' },
        { instruction: 'The spread is the difference between the best bid and best ask.' },
      ],
      quiz: [
        { question: 'What does the "spread" represent in the order book?', options: ['Difference between best bid and best ask', 'Total volume of orders', 'Number of market participants', 'Trading speed'], correctIndex: 0, explanation: 'The spread is the difference between the highest bid and the lowest ask price in the order book.' },
      ],
    },
    {
      id: 'mm-hft',
      slug: 'high-frequency-trading',
      title: 'High-Frequency Trading (HFT)',
      description: 'How algorithms trade in microseconds.',
      commands: ['microstructure', 'microstructure hft'],
      steps: [
        { instruction: 'Analyze HFT activity: `microstructure hft --symbol AAPL`', command: 'microstructure hft --symbol AAPL', expectedOutput: 'HFT activity metrics: order-to-trade ratio, cancel rates' },
        { instruction: 'HFT firms use co-location and ultra-low latency infrastructure.' },
        { instruction: 'HFT provides liquidity but also raises concerns about market fairness.' },
      ],
      quiz: [
        { question: 'What is co-location in HFT?', options: ['Placing servers next to exchange data centers for speed', 'Trading from multiple locations', 'Sharing order flow with other firms', 'Using cloud computing for trading'], correctIndex: 0, explanation: 'Co-location means HFT firms place their trading servers physically near exchange servers to minimize latency.' },
      ],
    },
    {
      id: 'mm-dark-pools',
      slug: 'dark-pools',
      title: 'Dark Pools & Off-Exchange Trading',
      description: 'Private exchanges where large blocks trade anonymously.',
      commands: ['liquidity', 'liquidity dark-pool'],
      steps: [
        { instruction: 'View dark pool activity: `liquidity dark-pool --list`', command: 'liquidity dark-pool --list', expectedOutput: 'List of dark pools with volume metrics' },
        { instruction: 'Dark pools allow large institutional orders without revealing intent to the public market.' },
        { instruction: 'Over 40% of US equity volume now trades off-exchange.' },
      ],
      quiz: [
        { question: 'Why do institutions use dark pools?', options: ['To hide large orders and avoid market impact', 'To get better prices than exchanges', 'To trade faster', 'To avoid regulations'], correctIndex: 0, explanation: 'Dark pools let institutions trade large blocks without signaling their intent, reducing market impact.' },
      ],
    },
    {
      id: 'mm-liquidity',
      slug: 'liquidity-spread',
      title: 'Liquidity & Transaction Costs',
      description: 'Measure and minimize trading costs.',
      commands: ['spread', 'spread analysis'],
      steps: [
        { instruction: 'Analyze transaction costs: `spread analysis --symbol AAPL --size 10000`', command: 'spread analysis --symbol AAPL --size 10000', expectedOutput: 'Estimated transaction costs including spread, fees, and market impact' },
        { instruction: 'Liquidity = ability to trade large size without moving the price.' },
        { instruction: 'Market impact is the price movement caused by your own order.' },
      ],
      quiz: [
        { question: 'What is market impact?', options: ['Price movement caused by your own trade', 'The bid-ask spread', 'Exchange trading fees', 'News impact on stock price'], correctIndex: 0, explanation: 'Market impact is the adverse price movement that occurs when a large order moves the market against itself.' },
      ],
    },
  ],
}
