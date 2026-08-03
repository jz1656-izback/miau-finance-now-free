import type { Course } from '../lib/types'

export const financialCalculators: Course = {
  id: 'financial-calculators',
  slug: 'financial-calculators',
  title: 'Financial Calculators & Planning',
  description: 'DCA, compound interest, loan amortization, retirement planning, margin analysis, and Monte Carlo simulations — the cat crunches numbers so you do not have to.',
  category: 'Calculators',
  difficulty: 'beginner',
  icon: '🧮',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'calc-dca',
      slug: 'dca-calculator',
      title: 'Dollar-Cost Averaging Backtest',
      description: 'See how regular investing into a ticker would have performed.',
      commands: ['dca 500 monthly 20 7', 'dca 1000 yearly 10 10'],
      steps: [
        { instruction: 'Run a DCA backtest: `dca 500 monthly 20 7` — invest $500 monthly for 20 years at 7% return', command: 'dca 500 monthly 20 7', expectedOutput: 'Total Invested, Final Value, Total Return, CAGR' },
        { instruction: 'DCA smooths out market volatility by investing fixed amounts at regular intervals.' },
        { instruction: 'The cat DCA\'s into a tuna ETF every Friday. It is called "Fishy Friday."' },
        { instruction: 'Try different periods: `dca 1000 yearly 30 8` for a 30-year annual investment', command: 'dca 1000 yearly 30 8', expectedOutput: 'CAGR and final value for annual DCA' },
      ],
      quiz: [
        { question: 'What is the main advantage of dollar-cost averaging?', options: ['Reduces timing risk by spreading purchases across regular intervals', 'Guarantees higher returns than lump-sum investing', 'Eliminates all market risk', 'Only works in bull markets'], correctIndex: 0, explanation: 'DCA reduces the risk of investing a lump sum at a market peak by spreading purchases over time, smoothing out volatility.' },
      ],
    },
    {
      id: 'calc-compound',
      slug: 'compound-interest',
      title: 'Compound Interest & Growth',
      description: 'Watch your money grow with the power of compounding.',
      commands: ['compound 10000 7 30 500', 'compound 5000 10 20 200'],
      steps: [
        { instruction: 'Project compound growth: `compound 10000 7 30 500` — $10K @ 7% for 30 years, adding $500/mo', command: 'compound 10000 7 30 500', expectedOutput: 'Final Value, Total Interest, yearly schedule' },
        { instruction: 'Compound interest is "interest on interest" — Einstein called it the eighth wonder of the world.' },
        { instruction: 'The cat understands compound interest because its tuna stash keeps growing.' },
        { instruction: 'Check without monthly contributions: `compound 50000 8 20`', command: 'compound 50000 8 20', expectedOutput: 'Compound growth on principal only' },
      ],
      quiz: [
        { question: 'What is the Rule of 72?', options: ['72 divided by annual return % estimates years to double your money', 'You need 72% of your income saved for retirement', 'A stock must return 72% to be worth buying', '72 is the magic number of trades per year'], correctIndex: 0, explanation: 'The Rule of 72 estimates how long an investment takes to double: divide 72 by the annual return rate. At 8%, money doubles in ~9 years.' },
      ],
    },
    {
      id: 'calc-loan',
      slug: 'loan-amortization',
      title: 'Loan Amortization & Planning',
      description: 'Understand the true cost of borrowing.',
      commands: ['loan 500000 6.5 30', 'loan 30000 5 5'],
      steps: [
        { instruction: 'Run a loan amortization: `loan 500000 6.5 30` — $500K mortgage at 6.5% for 30 years', command: 'loan 500000 6.5 30', expectedOutput: 'Monthly payment, total interest, amortization schedule' },
        { instruction: 'Total interest on a 30-year mortgage often exceeds half the loan amount at current rates.' },
        { instruction: 'The cat took out a mortgage on a cat tree. The interest rate was 3 cans of tuna per month.' },
        { instruction: 'Try a shorter term: `loan 500000 6.5 15` — see how much interest you save with 15 years', command: 'loan 500000 6.5 15', expectedOutput: 'Higher monthly payment but much less total interest' },
      ],
      quiz: [
        { question: 'How does shortening a loan term from 30 to 15 years affect total interest?', options: ['Significantly reduces total interest paid despite higher monthly payments', 'Increases total interest since you pay faster', 'Has no effect on total interest', 'Doubles the total interest'], correctIndex: 0, explanation: 'A 15-year mortgage typically has a lower rate and half the interest accrual period, dramatically reducing total interest despite higher monthly payments.' },
      ],
    },
    {
      id: 'calc-retirement-montecarlo',
      slug: 'retirement-monte-carlo',
      title: 'Retirement Planning & Monte Carlo',
      description: 'Plan for the future and simulate thousands of possible outcomes.',
      commands: ['retirement 30 50000 1000 7 65', 'montecarlo SPY 1000 252'],
      steps: [
        { instruction: 'Project retirement: `retirement 30 50000 1000 7 65` — age 30, $50K saved, $1000/mo, 7% return, retire at 65', command: 'retirement 30 50000 1000 7 65', expectedOutput: 'Projected balance, annual income, yearly schedule' },
        { instruction: 'The 4% rule suggests you can withdraw 4% of your portfolio annually in retirement.' },
        { instruction: 'The cat plans to retire at 7 (cat years) on a beach with unlimited tuna.' },
        { instruction: 'Run a Monte Carlo simulation: `montecarlo SPY 1000 252` — 1000 simulations over 1 year', command: 'montecarlo SPY 1000 252', expectedOutput: 'Expected price, percentiles, probability of loss' },
      ],
      quiz: [
        { question: 'What does a Monte Carlo simulation show in financial planning?', options: ['Thousands of possible outcomes based on random price paths, showing you the range of potential results and probability of success', 'The exact future price of a stock', 'The best possible investment strategy', 'The maximum guaranteed return'], correctIndex: 0, explanation: 'Monte Carlo simulation runs thousands of random price paths based on historical volatility and drift, giving a probability distribution of potential outcomes.' },
      ],
    },
  ],
}
