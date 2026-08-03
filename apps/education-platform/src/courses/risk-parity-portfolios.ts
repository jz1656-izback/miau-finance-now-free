import type { Course } from '../lib/types'

export const riskParityPortfolios: Course = {
  id: 'risk-parity-portfolios',
  slug: 'risk-parity-portfolios',
  title: 'Risk Parity Portfolio Construction',
  description: 'Build portfolios where each asset contributes equally to risk — the cat balances its risk across tuna, salmon, and catnip.',
  category: 'Portfolio Management',
  difficulty: 'advanced',
  icon: '⚖️',
  lessonCount: 3,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'rp-intro', slug: 'rp-intro', title: 'Risk Parity Basics',
      description: 'Equal risk contribution across assets.',
      commands: ['riskparity SPY,TLT,GLD'],
      steps: [
        { instruction: 'Run risk parity: `riskparity SPY,TLT,GLD`', command: 'riskparity SPY,TLT,GLD', expectedOutput: 'Weights and risk contributions for each asset' },
        { instruction: 'Traditional portfolios allocate by dollar amount. Risk parity allocates by risk contribution.' },
        { instruction: 'The cat practices risk parity: 50% of risk from tuna, 50% from naps.' },
      ],
      quiz: [{ question: 'What does risk parity aim to achieve?', options: ['Equal risk contribution from each asset', 'Equal dollar allocation', 'Maximum returns', 'Minimum volatility'], correctIndex: 0, explanation: 'Risk parity balances risk contributions so no single asset dominates portfolio risk.' }],
    },
    {
      id: 'rp-construction', slug: 'rp-construction', title: 'Portfolio Construction',
      description: 'Building a risk parity portfolio step by step.',
      commands: ['riskparity SPY,TLT,GLD,IAU'],
      steps: [
        { instruction: 'Add assets: `riskparity SPY,TLT,GLD,IAU`', command: 'riskparity SPY,TLT,GLD,IAU', expectedOutput: 'Weights for 4-asset risk parity' },
        { instruction: 'Low-volatility assets (bonds) get higher dollar weights to match risk contributions of volatile assets.' },
        { instruction: 'The cat bonds (catnip futures) have lower volatility than stocks (tuna).' },
      ],
      quiz: [{ question: 'In a risk parity portfolio, which asset typically gets the highest dollar allocation?', options: ['Low-volatility assets like bonds', 'High-volatility assets like stocks', 'Cash', 'The asset with highest returns'], correctIndex: 0, explanation: 'Low-volatility assets need larger dollar weights to match the risk contribution of high-volatility assets.' }],
    },
    {
      id: 'rp-vs-traditional', slug: 'rp-vs-traditional', title: 'Risk Parity vs Traditional Allocation',
      description: 'Compare approaches.',
      commands: ['riskparity SPY,TLT', 'riskparity SPY,TLT,GLD,IAU,TLT'],
      steps: [
        { instruction: 'Two-asset risk parity: `riskparity SPY,TLT`', command: 'riskparity SPY,TLT', expectedOutput: 'Bonds get higher weight to match equity risk' },
        { instruction: 'Risk parity portfolios tend to be more resilient during equity drawdowns.' },
      ],
      quiz: [{ question: 'When does risk parity typically outperform a 60/40 portfolio?', options: ['During bear markets when equities fall sharply', 'During strong bull markets', 'Every year', 'During low volatility periods'], correctIndex: 0, explanation: 'Risk parity overweights bonds relative to 60/40, so it tends to hold up better when stocks crash.' }],
    },
  ],
}
