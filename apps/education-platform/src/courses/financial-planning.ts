import type { Course } from '../lib/types'

export const financialPlanning: Course = {
  id: 'financial-planning',
  slug: 'financial-planning-basics',
  title: 'Financial Planning',
  description: 'Goal-based planning, net worth, cash flow, and budgeting — the cat plans its finances better than it plans its heists of the kitchen counter.',
  category: 'Personal Finance',
  difficulty: 'beginner',
  icon: '📋',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'goal-planning',
      slug: 'goal-based-financial-planning',
      title: 'Goal-Based Financial Planning',
      description: 'Setting and achieving financial goals.',
      commands: ['plan', 'goal'],
      steps: [
        { instruction: 'Set a financial goal: `goal --set --name "buy-house" --target 500000 --timeframe 10 --monthly-savings 3000`', command: 'goal --set --name "buy-house" --target 500000 --timeframe 10 --monthly-savings 3000', expectedOutput: 'Goal: Buy house — $500K in 10 years. Required monthly savings: $2,890 at 7% return. Current savings: $3,000. ON TRACK. Projected: $520K (4% surplus)' },
        { instruction: 'Goal-based planning starts with specific financial objectives and works backward.' },
        { instruction: 'The cat financial goal is to buy a tuna fishing boat by age 10 — currently on track.' },
      ],
      quiz: [
        { question: 'What is the first step in goal-based financial planning?', options: ['Defining specific goals with timeframes and target amounts', 'Buying stocks', 'Opening a bank account', 'Getting a credit card'], correctIndex: 0, explanation: 'Goal-based planning begins with clearly defined, specific goals including target amounts and target dates.' },
      ],
    },
    {
      id: 'net-worth',
      slug: 'net-worth-tracking',
      title: 'Net Worth & Tracking',
      description: 'Calculating and tracking your net worth.',
      commands: ['net-worth', 'plan'],
      steps: [
        { instruction: 'Calculate net worth: `net-worth --calculate --assets "house:500000,investments:200000,cash:50000" --liabilities "mortgage:300000,loans:25000"`', command: 'net-worth --calculate --assets "house:500000,investments:200000,cash:50000" --liabilities "mortgage:300000,loans:25000"', expectedOutput: 'Net worth: $425,000 (Assets: $750K - Liabilities: $325K). Liquidity ratio: 15%. Debt-to-asset ratio: 43%. Trend: +$25K vs last month' },
        { instruction: 'Net worth is the difference between what you own and what you owe.' },
        { instruction: 'The cat net worth is mostly canned tuna (liquid assets) and scratching posts (fixed assets).' },
      ],
      quiz: [
        { question: 'How is net worth calculated?', options: ['Total assets minus total liabilities', 'Total income minus total expenses', 'Total savings divided by total debt', 'Total investments times expected return'], correctIndex: 0, explanation: 'Net worth is calculated by subtracting all liabilities from all assets, providing a snapshot of financial health.' },
      ],
    },
    {
      id: 'cashflow',
      slug: 'cashflow-management',
      title: 'Cash Flow Management',
      description: 'Managing income and expenses effectively.',
      commands: ['cashflow', 'plan'],
      steps: [
        { instruction: 'Create cash flow statement: `cashflow --create --income "salary:8000,side:1500" --expenses "rent:2000,food:600,utilities:300,transport:400,fun:500"`', command: 'cashflow --create --income "salary:8000,side:1500" --expenses "rent:2000,food:600,utilities:300,transport:400,fun:500"', expectedOutput: 'Monthly cash flow: Income $9,500, Expenses $3,800, Surplus $5,700. Savings rate: 60%. Debt payments: $0. Recommended: Emergency fund 3-6 months' },
        { instruction: 'Positive cash flow means income exceeds expenses — the foundation of financial health.' },
        { instruction: 'The cat cash flow is positive: tuna income exceeds kibble expenses with room for catnip treats.' },
      ],
      quiz: [
        { question: 'What is a healthy savings rate for most households?', options: ['At least 15-20% of gross income is a strong target', '5% is sufficient', '50% is required', 'Any positive amount is fine'], correctIndex: 0, explanation: 'Financial experts typically recommend saving at least 15-20% of gross income for long-term financial health and retirement.' },
      ],
    },
    {
      id: 'budgeting',
      slug: 'budgeting-basics',
      title: 'Budgeting Methods',
      description: 'Different approaches to budgeting.',
      commands: ['plan', 'cashflow'],
      steps: [
        { instruction: 'Apply the 50/30/20 budget rule: `plan --budget-rule --income 6000 --fifty "needs" --thirty "wants" --twenty "savings"`', command: 'plan --budget-rule --income 6000 --fifty "needs" --thirty "wants" --twenty "savings"', expectedOutput: '50/30/20 Budget: Needs $3,000 (50%), Wants $1,800 (30%), Savings $1,200 (20%). Needs: rent, food, utilities. Wants: dining, entertainment, shopping' },
        { instruction: 'The 50/30/20 rule allocates 50% to needs, 30% to wants, and 20% to savings.' },
        { instruction: 'The cat budget: 50% for tuna (needs), 30% for catnip (wants), 20% for scratching post fund (savings).' },
      ],
      quiz: [
        { question: 'What does the 50/30/20 budgeting rule recommend?', options: ['50% on needs, 30% on wants, 20% on savings and debt repayment', '50% on housing, 30% on food, 20% on everything else', '50% savings, 30% needs, 20% wants', '50% wants, 30% needs, 20% savings'], correctIndex: 0, explanation: 'The 50/30/20 rule allocates 50% of after-tax income to needs, 30% to wants, and 20% to savings and debt repayment.' },
      ],
    },
  ],
}
