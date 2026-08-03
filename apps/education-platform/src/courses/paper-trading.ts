import type { Course } from '../lib/types'

export const paperTrading: Course = {
  id: 'paper-trading',
  slug: 'paper-trading',
  title: 'Paper Trading',
  description: 'Practice trading with virtual money — no risk, real learning.',
  category: 'Trading',
  difficulty: 'beginner',
  icon: '📝',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'pt-create',
      slug: 'create',
      title: 'Creating a Paper Account',
      description: 'Set up a virtual trading account with fake money.',
      commands: ['paper create', 'paper list'],
      steps: [
        { instruction: 'Create a paper account: `paper create "My First Account" 100000`', command: 'paper create Learning 50000', expectedOutput: 'Paper portfolio created with $50,000' },
        { instruction: 'Or with default cash: `paper create Beginner`' },
        { instruction: 'List your paper accounts: `paper list`', command: 'paper list', expectedOutput: 'All paper portfolios listed' },
      ],
      quiz: [
        { question: 'What is the default starting cash for a paper account?', options: ['$100,000', '$10,000', '$1,000,000', '$0'], correctIndex: 0, explanation: 'The default starting cash is $100,000 if not specified.' },
      ],
    },
    {
      id: 'pt-trade',
      slug: 'trade',
      title: 'Placing Paper Trades',
      description: 'Buy and sell with virtual money.',
      commands: ['paper buy', 'paper sell'],
      steps: [
        { instruction: 'Buy shares: `paper buy AAPL 10`', command: 'paper buy AAPL 10', expectedOutput: 'Paper buy order filled with fill price' },
        { instruction: 'Sell shares: `paper sell AAPL 5`', command: 'paper sell AAPL 5', expectedOutput: 'Paper sell order executed' },
        { instruction: 'Trades are simulated realistically — you will see slippage and commissions.' },
      ],
      quiz: [
        { question: 'Do paper trades cost real money?', options: ['No, it is virtual', 'Yes, a small fee', 'Only if you lose', 'It depends'], correctIndex: 0, explanation: 'Paper trading uses virtual money — completely risk-free practice.' },
      ],
    },
    {
      id: 'pt-positions',
      slug: 'positions',
      title: 'Position Tracking',
      description: 'Monitor your virtual holdings.',
      commands: ['paper positions'],
      steps: [
        { instruction: 'View your holdings: `paper positions`', command: 'paper positions', expectedOutput: 'Current holdings with market value and P&L' },
        { instruction: 'See how much cash you have left and total portfolio value.' },
      ],
      quiz: [
        { question: 'How do you view your paper holdings?', options: ['paper positions', 'paper list', 'paper portfolio', 'paper holdings'], correctIndex: 0, explanation: '`paper positions` shows your current virtual holdings.' },
      ],
    },
    {
      id: 'pt-pnl',
      slug: 'pnl',
      title: 'Paper P&L',
      description: 'Track your virtual profit and loss.',
      commands: ['paper pnl'],
      steps: [
        { instruction: 'Check performance: `paper pnl`', command: 'paper pnl', expectedOutput: 'Total P&L, realized and unrealized' },
        { instruction: 'Compare your paper trading performance against benchmarks.' },
      ],
      quiz: [
        { question: 'What does `paper pnl` display?', options: ['Virtual profit and loss', 'Real account P&L', 'Tax calculations', 'Nothing'], correctIndex: 0, explanation: '`paper pnl` shows your virtual trading gains and losses.' },
      ],
    },
  ],
}
