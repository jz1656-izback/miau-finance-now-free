import type { Course } from '../lib/types'

export const executionAlgorithms: Course = {
  id: 'execution-algorithms',
  slug: 'execution-algorithm-trading',
  title: 'Execution Algorithms',
  description: 'VWAP, TWAP, implementation shortfall, and iceberg orders — the cat executes trades with the stealth of a predator stalking a laser dot.',
  category: 'Trading',
  difficulty: 'advanced',
  icon: '⚙️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'vwap',
      slug: 'vwap-execution',
      title: 'VWAP Execution',
      description: 'Volume-Weighted Average Price algorithms.',
      commands: ['vwap', 'implementation'],
      steps: [
        { instruction: 'Run a VWAP execution simulation: `vwap --simulate --order-size 100000 --ticker AAPL --urgency medium`', command: 'vwap --simulate --order-size 100000 --ticker AAPL --urgency medium', expectedOutput: 'VWAP execution: 100K shares AAPL. Target: match VWAP. Estimated slippage: 2bps. Time horizon: 4 hours. Participation rate: 8% of volume' },
        { instruction: 'VWAP algorithms aim to execute at or better than the volume-weighted average price.' },
        { instruction: 'The cat\'s VWAP execution was so smooth the market didn\'t even notice it bought 100K shares of tuna.' },
      ],
      quiz: [
        { question: 'What is the primary goal of a VWAP execution algorithm?', options: ['To execute an order at a price at or near the volume-weighted average price for the period', 'To execute the entire order at the opening price', 'To maximize trading volume', 'To minimize the number of trades'], correctIndex: 0, explanation: 'VWAP algorithms slice orders to match or beat the volume-weighted average price over a specified time horizon.' },
      ],
    },
    {
      id: 'twap',
      slug: 'twap-execution',
      title: 'TWAP Execution',
      description: 'Time-Weighted Average Price algorithms.',
      commands: ['twap', 'implementation'],
      steps: [
        { instruction: 'Run a TWAP simulation: `twap --simulate --order-size 50000 --duration 120 --ticker MSFT`', command: 'twap --simulate --order-size 50000 --duration 120 --ticker MSFT', expectedOutput: 'TWAP execution: 50K shares MSFT over 120 minutes. Slice size: 417 shares/min. Estimated market impact: 1.5bps. Expected VWAP slippage: 3bps' },
        { instruction: 'TWAP executes equal-sized slices at regular time intervals.' },
        { instruction: 'The cat prefers TWAP — it\'s like portioning out tuna into equal meals throughout the day.' },
      ],
      quiz: [
        { question: 'How does a TWAP algorithm differ from VWAP?', options: ['TWAP slices orders evenly over time regardless of volume; VWAP follows volume patterns', 'TWAP is faster', 'TWAP is only for large orders', 'TWAP uses AI prediction'], correctIndex: 0, explanation: 'TWAP divides an order into equal time slices, while VWAP varies slice sizes based on historical volume patterns to track the volume-weighted price.' },
      ],
    },
    {
      id: 'implementation-shortfall',
      slug: 'implementation-shortfall',
      title: 'Implementation Shortfall',
      description: 'Minimizing the total cost of trading.',
      commands: ['implementation', 'vwap'],
      steps: [
        { instruction: 'Calculate implementation shortfall: `implementation --calculate --decision-price 100 --execution-price 101 --arrival-price 100.50 --commission 0.01`', command: 'implementation --calculate --decision-price 100 --execution-price 101 --arrival-price 100.50 --commission 0.01', expectedOutput: 'Implementation shortfall: $1.01/share (1.01%). Components: market impact $0.50, timing cost $0.50, commission $0.01. Total cost: $10,100 on 10K shares' },
        { instruction: 'Implementation shortfall measures the difference between the decision price and final execution price.' },
        { instruction: 'The cat\'s implementation shortfall was minimal — it pounced at exactly the right moment.' },
      ],
      quiz: [
        { question: 'What does implementation shortfall measure?', options: ['The total cost of executing a trade, including market impact, timing, and fees', 'The time taken to execute an order', 'The difference between bid and ask', 'The number of failed trades'], correctIndex: 0, explanation: 'Implementation shortfall quantifies the total cost of trade execution including market impact, timing costs, and explicit fees relative to the decision price.' },
      ],
    },
    {
      id: 'iceberg-orders',
      slug: 'iceberg-order-strategies',
      title: 'Iceberg Orders & Stealth Execution',
      description: 'Hiding large orders to minimize market impact.',
      commands: ['iceberg', 'implementation'],
      steps: [
        { instruction: 'Place an iceberg order: `iceberg --place --total-size 50000 --display-size 1000 --ticker SPY --type limit --limit 450`', command: 'iceberg --place --total-size 50000 --display-size 1000 --ticker SPY --type limit --limit 450', expectedOutput: 'Iceberg order placed: 50K shares SPY, showing 1K at a time, limit $450. 50 visible slices. Estimated completion: 2-3 hours depending on volume' },
        { instruction: 'Iceberg orders show only a small portion of the total order to the market.' },
        { instruction: 'The cat\'s iceberg order is like the tip of its tail — the rest is hidden under the couch.' },
      ],
      quiz: [
        { question: 'Why do traders use iceberg orders?', options: ['To hide the full order size and reduce market impact from large orders', 'To trade in frozen markets', 'To access lower exchange fees', 'To guarantee price improvement'], correctIndex: 0, explanation: 'Iceberg orders conceal the total order size by displaying only a small portion, preventing other traders from front-running the full order.' },
      ],
    },
  ],
}
