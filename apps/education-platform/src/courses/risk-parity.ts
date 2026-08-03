import type { Course } from '../lib/types'

export const riskParity: Course = {
  id: 'risk-parity',
  slug: 'risk-parity-volatility-targeting',
  title: 'Risk Parity & Volatility Targeting',
  description: 'Volatility targeting, risk contribution, leverage, and diversification — the cat balances risk like it balances on the edge of a bookshelf.',
  category: 'Portfolio Management',
  difficulty: 'advanced',
  icon: '⚖️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'risk-parity-basics',
      slug: 'risk-parity-fundamentals',
      title: 'Risk Parity Fundamentals',
      description: 'Core concepts of risk parity investing.',
      commands: ['risk-parity', 'diversification', 'contribution'],
      steps: [
        { instruction: 'Build a risk parity portfolio: `risk-parity --build --assets "equities,bonds,commodities" --target-vol 0.10`', command: 'risk-parity --build --assets "equities,bonds,commodities" --target-vol 0.10', expectedOutput: 'Risk parity weights: Bonds 55%, Equities 25%, Commodities 20%. Each contributes ~33% of total risk. Leverage factor: 1.5x. Expected return: 8.5%, vol: 10%' },
        { instruction: 'Risk parity equalizes risk contribution across asset classes rather than capital.' },
        { instruction: 'The cat practices risk parity by distributing its weight evenly across all four paws.' },
      ],
      quiz: [
        { question: 'What is the main goal of a risk parity strategy?', options: ['To equalize the risk contribution from each asset class in the portfolio', 'To maximize returns regardless of risk', 'To minimize the number of assets held', 'To match the S&P 500'], correctIndex: 0, explanation: 'Risk parity aims to construct a portfolio where each asset class contributes equally to total portfolio risk.' },
      ],
    },
    {
      id: 'volatility-targeting',
      slug: 'volatility-targeting-strategies',
      title: 'Volatility Targeting',
      description: 'Keeping portfolio volatility at a target level.',
      commands: ['vol-target', 'risk-parity'],
      steps: [
        { instruction: 'Implement volatility targeting: `vol-target --target 0.12 --current-portfolio-vol 0.08 --max-leverage 2.0`', command: 'vol-target --target 0.12 --current-portfolio-vol 0.08 --max-leverage 2.0', expectedOutput: 'Vol target: 12%. Current vol: 8%. Leverage required: 1.5x. Apply 50% leverage to reach target. Risk budget: 12% VaR (95%): -2.8% daily' },
        { instruction: 'Volatility targeting adjusts portfolio leverage to maintain a target volatility level.' },
        { instruction: 'The cat targets volatility — it prefers the steady purr of contentment over wild zoomies.' },
      ],
      quiz: [
        { question: 'How does volatility targeting work?', options: ['It adjusts leverage up when volatility is low and down when volatility is high to maintain a target vol level', 'It targets a specific stock price', 'It only works in bull markets', 'It eliminates all risk'], correctIndex: 0, explanation: 'Volatility targeting dynamically adjusts leverage inversely to realized volatility to keep portfolio volatility at a predetermined target level.' },
      ],
    },
    {
      id: 'risk-contribution',
      slug: 'risk-contribution-analysis',
      title: 'Risk Contribution Analysis',
      description: 'Measuring and analyzing risk contributions.',
      commands: ['contribution', 'risk-parity'],
      steps: [
        { instruction: 'Analyze risk contributions: `contribution --analyze --portfolio "bonds:60,equities:40" --correlation 0.3`', command: 'contribution --analyze --portfolio "bonds:60,equities:40" --correlation 0.3', expectedOutput: 'Risk decomposition: Equities (40% capital): 72% of risk. Bonds (60% capital): 28% of risk. Marginal contribution: equities 0.18, bonds 0.04' },
        { instruction: 'Risk contribution analysis shows how much each asset contributes to total portfolio risk.' },
        { instruction: 'The cat contribution to household risk is 100% despite being only 10% of the household.' },
      ],
      quiz: [
        { question: 'What is marginal contribution to risk (MCTR)?', options: ['The change in total portfolio risk from a small increase in an asset weight', 'The total risk of the portfolio', 'The correlation between assets', 'The beta of the portfolio'], correctIndex: 0, explanation: 'MCTR measures how much total portfolio risk changes when a small additional amount of an asset is added to the portfolio.' },
      ],
    },
    {
      id: 'risk-parity-implementation',
      slug: 'risk-parity-implementation',
      title: 'Risk Parity Implementation',
      description: 'Practical considerations for risk parity portfolios.',
      commands: ['risk-parity', 'diversification'],
      steps: [
        { instruction: 'Implement a risk parity strategy: `risk-parity --implement --capital 10000000 --rebalance quarterly --benchmark 60/40`', command: 'risk-parity --implement --capital 10000000 --rebalance quarterly --benchmark 60/40', expectedOutput: 'Risk parity portfolio ($10M): Leverage 1.8x. Expected tracking error vs 60/40: 5.2%. Historical Sharpe: 0.65 vs 0.45. Drawdown in 2022: -12% vs -18%' },
        { instruction: 'Risk parity typically requires leverage to achieve competitive returns from bond-heavy allocations.' },
        { instruction: 'The cat risk parity implementation uses leverage — a low-interest tuna loan from the bank.' },
      ],
      quiz: [
        { question: 'Why does risk parity typically require leverage?', options: ['Because bonds (low risk, low return) get large allocations and need leverage to match equity return targets', 'Because risk parity avoids stocks entirely', 'Because leverage is the main source of returns', 'Because regulators require it'], correctIndex: 0, explanation: 'Risk parity allocates heavily to lower-risk assets like bonds, requiring leverage to achieve return levels comparable to equity-heavy portfolios.' },
      ],
    },
  ],
}
