import type { Course } from '../lib/types'

export const tradingOrders: Course = {
  id: 'trading-orders',
  slug: 'trading-orders',
  title: 'Trading & Orders',
  description: 'Place market, limit, stop orders and manage your order book.',
  category: 'Trading',
  difficulty: 'intermediate',
  icon: '📋',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'to-create',
      slug: 'create',
      title: 'Creating Orders',
      description: 'Place orders with different types.',
      commands: ['order create'],
      steps: [
        { instruction: 'Place a market buy: `order create AAPL buy 10 market`', command: 'order create AAPL buy 10 market', expectedOutput: 'Order confirmation with ID' },
        { instruction: 'Place a limit buy: `order create TSLA buy 5 limit 250`', command: 'order create TSLA buy 5 limit 250', expectedOutput: 'Limit order created' },
        { instruction: 'Try a stop order: `order create NVDA sell 3 stop 800`' },
      ],
      quiz: [
        { question: 'What order type executes immediately at the best available price?', options: ['market', 'limit', 'stop', 'trailing'], correctIndex: 0, explanation: 'Market orders execute immediately at the current best price.' },
      ],
    },
    {
      id: 'to-manage',
      slug: 'manage',
      title: 'Managing Orders',
      description: 'List, check status, and cancel orders.',
      commands: ['order list', 'order status', 'order cancel', 'trades', 'ps'],
      steps: [
        { instruction: 'List all orders: `order list`', command: 'order list', expectedOutput: 'Order book displayed' },
        { instruction: 'Check order status: `order status <id>`', command: 'order status 1', expectedOutput: 'Order status, fill details' },
        { instruction: 'Cancel an order: `order cancel <id>`', command: 'order cancel 1', expectedOutput: 'Order cancelled' },
        { instruction: 'View recent trades: `trades` or `ps`', command: 'trades', expectedOutput: 'Recent filled orders' },
      ],
      quiz: [
        { question: 'Which command shows your recent filled orders?', options: ['trades', 'order list', 'fills', 'history'], correctIndex: 0, explanation: '`trades` (or its alias `ps`) shows recent filled trades.' },
      ],
    },
    {
      id: 'to-signals',
      slug: 'signals',
      title: 'Trading Signals',
      description: 'Use technical signals to identify entry and exit points.',
      commands: ['signals', 'multisig'],
      steps: [
        { instruction: 'Get signals: `signals AAPL`', command: 'signals AAPL', expectedOutput: 'Buy/sell/hold signals with indicators' },
        { instruction: 'Multi-asset signals: `multisig AAPL,MSFT`', command: 'multisig TSLA,NVDA', expectedOutput: 'Signals for multiple tickers' },
      ],
      quiz: [
        { question: 'What does `multisig` do?', options: ['Signals for multiple tickers', 'Multiple signal types', 'Multi-factor analysis', 'Nothing special'], correctIndex: 0, explanation: '`multisig ticker1,ticker2,...` shows signals for multiple assets at once.' },
      ],
    },
    {
      id: 'to-greeks',
      slug: 'greeks',
      title: 'Options Greeks',
      description: 'Analyze option sensitivities.',
      commands: ['greeks'],
      steps: [
        { instruction: 'View Greeks: `greeks`', command: 'greeks', expectedOutput: 'Delta, gamma, theta, vega, rho displayed' },
        { instruction: 'Use Greeks to understand how options prices change with the underlying, time, and volatility.' },
      ],
      quiz: [
        { question: 'Which Greek measures sensitivity to time decay?', options: ['Theta', 'Delta', 'Gamma', 'Vega'], correctIndex: 0, explanation: 'Theta measures the rate of time decay in an option.' },
      ],
    },
  ],
}
