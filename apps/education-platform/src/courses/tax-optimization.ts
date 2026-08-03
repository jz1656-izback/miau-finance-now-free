import type { Course } from '../lib/types'

export const taxOptimization: Course = {
  id: 'tax-optimization',
  slug: 'tax-optimization',
  title: 'Tax Optimization',
  description: 'Capital gains, tax-loss harvesting, and retirement accounts — the cat minimizes your tax bill.',
  category: 'Tax',
  difficulty: 'beginner',
  icon: '🧾',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'tax-gains',
      slug: 'capital-gains',
      title: 'Capital Gains Tax',
      description: 'Short-term vs long-term capital gains and how they are taxed.',
      commands: ['tax', 'tax gains'],
      steps: [
        { instruction: 'Calculate capital gains tax: `tax gains --gain 10000 --held 400`', command: 'tax gains --gain 10000 --held 400', expectedOutput: 'Estimated capital gains tax: $0 long-term rate' },
        { instruction: 'Long-term gains (held > 1 year) are taxed at 0%, 15%, or 20% depending on income.' },
        { instruction: 'Short-term gains are taxed as ordinary income — up to 37%.' },
      ],
      quiz: [
        { question: 'How long must you hold an asset for long-term capital gains treatment?', options: ['More than 1 year', 'More than 6 months', 'More than 2 years', 'More than 30 days'], correctIndex: 0, explanation: 'Assets held for more than 1 year qualify for long-term capital gains tax rates, which are lower than short-term rates.' },
      ],
    },
    {
      id: 'tax-harvesting',
      slug: 'tax-loss-harvesting',
      title: 'Tax-Loss Harvesting',
      description: 'Use losses to offset gains and reduce your tax bill.',
      commands: ['tax harvest', 'tax harvest --list'],
      steps: [
        { instruction: 'Find harvesting opportunities: `tax harvest --list --portfolio`', command: 'tax harvest --list --portfolio', expectedOutput: 'List of losing positions with unrealized losses' },
        { instruction: 'Sell losing positions to offset capital gains. You can deduct up to $3,000 of net losses against ordinary income.' },
        { instruction: 'Watch out for wash sale rules — you cannot buy back the same security within 30 days.' },
      ],
      quiz: [
        { question: 'What is the wash sale rule?', options: ['You cannot repurchase the same security within 30 days of selling at a loss', 'You must wash all securities before selling', 'You can only harvest losses once per year', 'Losses cannot be deducted'], correctIndex: 0, explanation: 'The wash sale rule disallows the loss deduction if you buy a substantially identical security within 30 days before or after the sale.' },
      ],
    },
    {
      id: 'tax-retirement',
      slug: 'retirement-accounts',
      title: 'Tax-Advantaged Retirement Accounts',
      description: '401(k), IRA, Roth IRA, and HSA — the tax shelters.',
      commands: ['tax roth', 'tax roth calc'],
      steps: [
        { instruction: 'Compare retirement accounts: `tax roth calc --income 80000 --contribution 6000`', command: 'tax roth calc --income 80000 --contribution 6000', expectedOutput: 'Comparison of traditional vs Roth IRA tax treatment' },
        { instruction: 'Traditional 401(k)/IRA: tax deduction now, pay taxes on withdrawals in retirement.' },
        { instruction: 'Roth IRA: pay taxes now, tax-free withdrawals in retirement.' },
      ],
      quiz: [
        { question: 'When are Roth IRA contributions taxed?', options: ['When contributed (after-tax)', 'When withdrawn in retirement', 'Never — they are tax-free', 'At the end of each year'], correctIndex: 0, explanation: 'Roth IRA contributions are made with after-tax dollars, so withdrawals in retirement are tax-free.' },
      ],
    },
    {
      id: 'tax-strategies',
      slug: 'tax-strategies',
      title: 'Advanced Tax Strategies',
      description: 'Bond placement, qualified dividends, and AMT awareness.',
      commands: ['capital-gains', 'capital-gains calc'],
      steps: [
        { instruction: 'Run a tax strategy analysis: `tax harvest strategy --income 200000 --portfolio 500000`', command: 'tax harvest strategy --income 200000 --portfolio 500000', expectedOutput: 'Tax optimization strategy report' },
        { instruction: 'Place bonds in tax-advantaged accounts (they generate ordinary income).' },
        { instruction: 'Qualified dividends are taxed at long-term capital gains rates, not ordinary income rates.' },
      ],
      quiz: [
        { question: 'How are qualified dividends taxed?', options: ['At long-term capital gains rates', 'As ordinary income', 'They are tax-free', 'At short-term capital gains rates'], correctIndex: 0, explanation: 'Qualified dividends receive preferential tax treatment and are taxed at the lower long-term capital gains rates.' },
      ],
    },
  ],
}
