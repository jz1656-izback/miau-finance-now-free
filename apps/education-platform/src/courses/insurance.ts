import type { Course } from '../lib/types'

export const insurance: Course = {
  id: 'insurance',
  slug: 'insurance',
  title: 'Insurance & Risk Pooling',
  description: 'Actuarial science, risk pooling, pricing, and reinsurance — the cat insures your tail.',
  category: 'Insurance',
  difficulty: 'intermediate',
  icon: '🛡️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'ins-actuarial',
      slug: 'actuarial-science',
      title: 'Actuarial Science',
      description: 'The math behind insurance pricing.',
      commands: ['insurance', 'insurance actuarial'],
      steps: [
        { instruction: 'Run actuarial analysis: `insurance actuarial --risk mortality --age 30`', command: 'insurance actuarial --risk mortality --age 30', expectedOutput: 'Mortality probability table and premium calculation' },
        { instruction: 'Actuaries use probability theory and statistics to calculate risk and set premiums.' },
        { instruction: 'Life tables show mortality rates at each age — the foundation of life insurance.' },
      ],
      quiz: [
        { question: 'What do actuaries calculate?', options: ['Risk probabilities and insurance premiums', 'Stock market returns', 'Real estate values', 'Tax liabilities'], correctIndex: 0, explanation: 'Actuaries use mathematical and statistical methods to assess risk and calculate insurance premiums.' },
      ],
    },
    {
      id: 'ins-pooling',
      slug: 'risk-pooling',
      title: 'Risk Pooling',
      description: 'How insurance spreads risk across many policyholders.',
      commands: ['actuarial', 'actuarial model'],
      steps: [
        { instruction: 'Simulate risk pooling: `insurance risk-pool --policies 10000 --premium 1000`', command: 'insurance risk-pool --policies 10000 --premium 1000', expectedOutput: 'Risk pooling simulation with loss distribution' },
        { instruction: 'Risk pooling works because not everyone experiences a loss at the same time.' },
        { instruction: 'Law of large numbers makes aggregate losses more predictable as pool size grows.' },
      ],
      quiz: [
        { question: 'Why does risk pooling work for insurers?', options: ['Individual losses are uncorrelated across the pool', 'Everyone claims at once', 'Insurers never pay claims', 'Premiums are always higher than losses'], correctIndex: 0, explanation: 'Risk pooling works because individual losses are largely independent, making aggregate losses predictable via the law of large numbers.' },
      ],
    },
    {
      id: 'ins-pricing',
      slug: 'insurance-pricing',
      title: 'Insurance Pricing',
      description: 'How premiums, deductibles, and coverage limits are set.',
      commands: ['premium', 'premium calc'],
      steps: [
        { instruction: 'Calculate a premium: `premium calc --coverage 500000 --risk-factor 1.2`', command: 'premium calc --coverage 500000 --risk-factor 1.2', expectedOutput: 'Annual premium breakdown with loading and expense components' },
        { instruction: 'Premium = expected loss + expense loading + profit margin.' },
        { instruction: 'Deductibles reduce premiums by shifting some risk to the policyholder.' },
      ],
      quiz: [
        { question: 'What happens to premiums when deductibles increase?', options: ['Premiums decrease', 'Premiums increase', 'Premiums stay the same', 'Coverage is cancelled'], correctIndex: 0, explanation: 'Higher deductibles mean the policyholder bears more initial risk, so insurance companies charge lower premiums.' },
      ],
    },
    {
      id: 'ins-reinsurance',
      slug: 'reinsurance',
      title: 'Reinsurance',
      description: 'Insurance for insurance companies.',
      commands: ['risk-pool', 'risk-pool analysis'],
      steps: [
        { instruction: 'Analyze reinsurance structures: `insurance reinsurance --type excess-of-loss`', command: 'insurance reinsurance --type excess-of-loss', expectedOutput: 'Reinsurance structure with attachment points and limits' },
        { instruction: 'Primary insurers buy reinsurance to protect against catastrophic losses.' },
        { instruction: 'Reinsurance comes in two main forms: treaty (automatic) and facultative (per-risk).' },
      ],
      quiz: [
        { question: 'What is the purpose of reinsurance?', options: ['To protect insurers from catastrophic losses', 'To insure individual policyholders', 'To provide health insurance', 'To replace primary insurance'], correctIndex: 0, explanation: 'Reinsurance transfers risk from primary insurers to reinsurers, protecting against losses too large for one company to bear.' },
      ],
    },
  ],
}
