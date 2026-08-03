import type { Course } from '../lib/types'

export const personalFinance: Course = {
  id: 'personal-finance',
  slug: 'personal-finance',
  title: 'Personal Finance & Budgeting',
  description: 'Budgeting, saving, emergency funds, and retirement planning — the cat manages your wallet.',
  category: 'Personal Finance',
  difficulty: 'beginner',
  icon: '💰',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'pf-budgeting',
      slug: 'budgeting-basics',
      title: 'Budgeting Basics',
      description: 'Track income, expenses, and build a budget that works.',
      commands: ['budget', 'budget overview'],
      steps: [
        { instruction: 'View your budget overview: `budget overview`', command: 'budget overview', expectedOutput: 'Monthly income vs expenses breakdown' },
        { instruction: 'The 50/30/20 rule: 50% needs, 30% wants, 20% savings.' },
        { instruction: 'Categorize expenses: `budget categories`', command: 'budget categories', expectedOutput: 'List of expense categories with amounts' },
      ],
      quiz: [
        { question: 'What percentage of income should go to savings per the 50/30/20 rule?', options: ['10%', '20%', '30%', '50%'], correctIndex: 1, explanation: 'The 50/30/20 rule allocates 20% of after-tax income to savings and debt repayment.' },
      ],
    },
    {
      id: 'pf-savings',
      slug: 'saving-strategies',
      title: 'Saving Strategies',
      description: 'Build savings habits that stick.',
      commands: ['budget savings', 'budget savings goal'],
      steps: [
        { instruction: 'Check your savings rate: `budget savings`', command: 'budget savings', expectedOutput: 'Current savings rate and recommendations' },
        { instruction: 'Set a savings goal: `budget savings goal --amount 10000 --name "Emergency Fund"`' },
        { instruction: 'Pay yourself first — automate a transfer to savings on payday.' },
      ],
      quiz: [
        { question: 'What is "pay yourself first"?', options: ['Automating savings before spending', 'Paying bills on time', 'Investing in yourself', 'Hiring a financial advisor'], correctIndex: 0, explanation: 'Pay yourself first means automatically transferring money to savings before you can spend it.' },
      ],
    },
    {
      id: 'pf-emergency',
      slug: 'emergency-funds',
      title: 'Emergency Funds',
      description: 'Why you need 3-6 months of expenses saved.',
      commands: ['budget emergency', 'budget emergency goal'],
      steps: [
        { instruction: 'Calculate your emergency fund target: `budget emergency`', command: 'budget emergency', expectedOutput: 'Recommended emergency fund amount based on expenses' },
        { instruction: 'An emergency fund covers 3-6 months of essential living expenses.' },
        { instruction: 'Keep emergency funds in a high-yield savings account, not the stock market.' },
      ],
      quiz: [
        { question: 'How many months of expenses should an emergency fund cover?', options: ['1-2 months', '3-6 months', '12-18 months', '24+ months'], correctIndex: 1, explanation: 'Financial experts recommend 3-6 months of essential living expenses in an emergency fund.' },
      ],
    },
    {
      id: 'pf-retirement',
      slug: 'retirement-planning',
      title: 'Retirement Planning',
      description: 'Start early, contribute consistently, and let compound interest work.',
      commands: ['budget retirement', 'budget retirement calc'],
      steps: [
        { instruction: 'Run a retirement calculator: `budget retirement calc --age 30 --income 60000`', command: 'budget retirement calc --age 30 --income 60000', expectedOutput: 'Projected retirement savings at age 65' },
        { instruction: 'The magic of compound interest — your money earns money on the money it earned.' },
        { instruction: 'Max out tax-advantaged accounts like 401(k) and IRA before taxable accounts.' },
      ],
      quiz: [
        { question: 'Why is starting early important for retirement?', options: ['Compound interest grows over time', 'You can take more risk', 'Fees are lower', 'You avoid taxes'], correctIndex: 0, explanation: 'Starting early lets compound interest work longer, exponentially growing your savings.' },
      ],
    },
  ],
}
