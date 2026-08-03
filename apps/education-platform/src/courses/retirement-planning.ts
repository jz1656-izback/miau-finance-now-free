import type { Course } from '../lib/types'

export const retirementPlanning: Course = {
  id: 'retirement-planning',
  slug: 'retirement-planning-basics',
  title: 'Retirement Planning',
  description: '401k, IRA, Roth, pension, Social Security, and withdrawal strategies — because even cats dream of a sunny retirement with endless tuna.',
  category: 'Personal Finance',
  difficulty: 'beginner',
  icon: '🌅',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'retirement-accounts',
      slug: 'retirement-account-types',
      title: 'Retirement Account Types',
      description: 'Understanding 401k, IRA, and Roth accounts.',
      commands: ['retirement', '401k', 'ira'],
      steps: [
        { instruction: 'Compare retirement accounts: `retirement --compare --accounts 401k,traditional-ira,roth-ira`', command: 'retirement --compare --accounts 401k,traditional-ira,roth-ira', expectedOutput: '401k: $23K limit, employer match, pre-tax. Traditional IRA: $7K limit, pre-tax, income limits. Roth IRA: $7K limit, after-tax, tax-free growth' },
        { instruction: 'A 401k is an employer-sponsored retirement account with tax advantages.' },
        { instruction: 'The cat contributes to its 401(k) — the employer match is paid in tuna cans.' },
        { instruction: 'Check your contribution limits: `retirement --limits --year 2025 --age 35`', command: 'retirement --limits --year 2025 --age 35', expectedOutput: 'Your 2025 limits: 401k $23,500 ($31K with catch-up after 50), IRA $7K ($8K catch-up), Total $30,500' },
      ],
      quiz: [
        { question: 'What is the key difference between a Traditional IRA and a Roth IRA?', options: ['Traditional IRA offers tax-deductible contributions now and taxes on withdrawal; Roth is after-tax now and tax-free later', 'Traditional IRA has no income limit', 'Roth IRA has higher contribution limits', 'There is no difference'], correctIndex: 0, explanation: 'Traditional IRAs provide upfront tax deductions but tax withdrawals, while Roth IRAs use after-tax contributions for tax-free growth and withdrawals.' },
      ],
    },
    {
      id: 'social-security',
      slug: 'social-security-basics',
      title: 'Social Security & Pensions',
      description: 'Understanding Social Security benefits and pension plans.',
      commands: ['retirement', '401k'],
      steps: [
        { instruction: 'Estimate Social Security: `retirement --social-security --age 35 --income 85000`', command: 'retirement --social-security --age 35 --income 85000', expectedOutput: 'Estimated monthly benefit at 67: $2,845/month. At 70 (delayed): $3,528/month. At 62 (early): $1,993/month' },
        { instruction: 'Social Security replaces about 40% of pre-retirement income for average earners.' },
        { instruction: 'The cat\'s pension is paid in premium kibble — the 401(k) is for the good stuff.' },
      ],
      quiz: [
        { question: 'At what full retirement age (FRA) do you receive 100% of your Social Security benefit?', options: ['67 for those born after 1960', '62 for everyone', '65 for everyone', '70 for everyone'], correctIndex: 0, explanation: 'Full retirement age is 67 for those born in 1960 or later, with reduced benefits available at 62 and increased benefits up to age 70.' },
      ],
    },
    {
      id: 'withdrawal-strategies',
      slug: 'retirement-withdrawal-strategies',
      title: 'Withdrawal Strategies',
      description: 'Strategies for sustainable retirement income.',
      commands: ['retirement', 'ira'],
      steps: [
        { instruction: 'Simulate the 4% rule: `retirement --withdraw --rule 4 --portfolio 1000000 --years 30`', command: 'retirement --withdraw --rule 4 --portfolio 1000000 --years 30', expectedOutput: '4% rule: $40K/year initial withdrawal, adjusted for inflation. Portfolio survives 30 years with 96% probability, median ending value $1.8M' },
        { instruction: 'The 4% rule suggests withdrawing 4% of your portfolio in the first year of retirement.' },
        { instruction: 'The cat\'s withdrawal strategy: 4% for tuna, 3% for catnip, 93% for napping expenses.' },
      ],
      quiz: [
        { question: 'What does the 4% rule in retirement planning recommend?', options: ['Withdraw 4% of your portfolio in the first year and adjust for inflation annually', 'Save 4% of your income each year', 'Invest 4% in bonds', 'Keep 4% of assets in cash'], correctIndex: 0, explanation: 'The 4% rule suggests withdrawing 4% of your portfolio in your first retirement year, then adjusting that dollar amount for inflation each subsequent year.' },
      ],
    },
    {
      id: 'retirement-goals',
      slug: 'retirement-goal-planning',
      title: 'Retirement Goal Planning',
      description: 'Setting and tracking retirement savings goals.',
      commands: ['retirement', 'plan'],
      steps: [
        { instruction: 'Calculate retirement goal: `retirement --goal --current-age 30 --retire-age 65 --desired-income 80000`', command: 'retirement --goal --current-age 30 --retire-age 65 --desired-income 80000', expectedOutput: 'Retirement goal: $2M needed (25x $80K). Monthly savings required: $1,450 at 7% return. Current progress: $0 (start saving!)' },
        { instruction: 'A common rule of thumb is to save 15% of your income for retirement.' },
        { instruction: 'The cat started saving late but made up for it with aggressive tuna investing.' },
      ],
      quiz: [
        { question: 'How much do you need saved for retirement using the 25x rule?', options: ['25 times your desired annual retirement income', '25 times your current salary', '$25 million', '25% of your current net worth'], correctIndex: 0, explanation: 'The 25x rule means you need 25 times your desired annual retirement income, based on the 4% withdrawal rule.' },
      ],
    },
  ],
}
