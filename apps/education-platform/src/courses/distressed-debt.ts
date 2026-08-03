import type { Course } from '../lib/types'

export const distressedDebt: Course = {
  id: 'distressed-debt',
  slug: 'distressed-debt-restructuring',
  title: 'Distressed Debt & Restructuring',
  description: 'Bankruptcy, DIP financing, restructuring, and distressed valuations — the cat turns trash into treasure.',
  category: 'Corporate Finance',
  difficulty: 'advanced',
  icon: '🔄',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'distressed-basics',
      slug: 'distressed-debt-basics',
      title: 'Distressed Debt Basics',
      description: 'Understanding distressed securities and bankruptcy.',
      commands: ['distressed', 'distressed search'],
      steps: [
        { instruction: 'Search for distressed companies: `distressed search --criteria "debt > 5x ebitda, cash < 100m, maturity < 1yr"`', command: 'distressed search --criteria "debt > 5x ebitda, cash < 100m, maturity < 1yr"', expectedOutput: 'Matches: 12 companies. Top: Company A (debt/EBITDA 8x, cash $45M, maturity 6mo), Company B (6x, $80M, 8mo)' },
        { instruction: 'Distressed debt trades at deep discounts to par — often 20-60 cents on the dollar.' },
        { instruction: 'The cat sniffs out distressed debt like a shark smells blood in the water. Also tuna.' },
      ],
      quiz: [
        { question: 'What does "trading at 40 cents on the dollar" mean for a distressed bond?', options: ['The bond trades at 40% of its face value, implying significant distress', 'The bond pays 40% interest', 'The bond has 40 days to maturity', 'The bond is rated 40 out of 100'], correctIndex: 0, explanation: 'A bond trading at 40 cents on the dollar is priced at 40% of its par value, indicating the market expects significant default risk or restructuring.' },
      ],
    },
    {
      id: 'chapter-11',
      slug: 'chapter-11-bankruptcy',
      title: 'Chapter 11 & Restructuring Process',
      description: 'Navigating the US bankruptcy process.',
      commands: ['distressed bankruptcy', 'distressed docket'],
      steps: [
        { instruction: 'Check the bankruptcy docket for a company: `distressed docket --company "Company A" --recent 10`', command: 'distressed docket --company "Company A" --recent 10', expectedOutput: 'Recent filings: 1) DIP motion approved, 2) First day motions, 3) Creditor committee formed, 4) Auction scheduled Dec 15' },
        { instruction: 'Chapter 11 gives companies protection from creditors while they reorganize.' },
        { instruction: 'The cat filed for Chapter 11 after a tuna market crash. It emerged leaner, meaner, and hungrier.' },
        { instruction: 'Analyze the restructuring plan: `distressed plan --company "Company A" --summary`', command: 'distressed plan --company "Company A" --summary', expectedOutput: 'Plan: Debt-to-equity swap ($500M), New money ($200M DIP), Unsecured recovery 35%, Equity to existing holders 5%' },
      ],
      quiz: [
        { question: 'What is DIP financing?', options: ['Debtor-in-Possession financing — new loans given to a company in Chapter 11 that have super-priority status', 'Default Interest Protection — insurance against missed payments', 'Debt Incubation Period — time before debt matures', 'Dividend Increase Plan — raising dividends to attract investors'], correctIndex: 0, explanation: 'DIP (Debtor-in-Possession) financing provides capital to companies in Chapter 11, giving lenders super-priority claim over existing debt to fund operations during restructuring.' },
      ],
    },
    {
      id: 'distressed-valuation',
      slug: 'distressed-valuation',
      title: 'Distressed Valuation',
      description: 'Valuing companies in or near bankruptcy.',
      commands: ['distressed value', 'distressed waterfall'],
      steps: [
        { instruction: 'Run a distressed DCF with probability weighting: `distressed value --ticker TICKR --scenarios base,down,up --probs 40,40,20`', command: 'distressed value --ticker TICKR --scenarios base,down,up --probs 40,40,20', expectedOutput: 'Probability-weighted EV: $420M. Base: $600M (40%), Down: $200M (40%), Up: $900M (20%). Implied equity: $0 in base case' },
        { instruction: 'Run a waterfall analysis to see who gets paid: `distressed waterfall --ticker TICKR --debt-structure`', command: 'distressed waterfall --ticker TICKR --debt-structure', expectedOutput: 'Waterfall: Senior Secured ($300M) → 100% recovery. Senior Unsecured ($400M) → 35% recovery. Subordinated ($200M) → 0% recovery. Equity → $0' },
        { instruction: 'The cat\'s distressed valuation model accounts for "what if the company pivots to catnip?"' },
      ],
      quiz: [
        { question: 'What does a waterfall analysis show in distressed investing?', options: ['The order and amount of recovery for each creditor class in a liquidation', 'The company revenue projections', 'The management bonus structure', 'The marketing budget allocation'], correctIndex: 0, explanation: 'A waterfall analysis models the distribution of value in a bankruptcy, showing which creditor classes get paid and how much based on their priority in the capital structure.' },
      ],
    },
    {
      id: 'distressed-strategies',
      slug: 'distressed-investing-strategies',
      title: 'Distressed Investing Strategies',
      description: 'Active vs passive distressed investing approaches.',
      commands: ['distressed strategy', 'distressed trade'],
      steps: [
        { instruction: 'Evaluate distressed strategies: `distressed strategy --type "loan-to-own" --target TICKR`', command: 'distressed strategy --type "loan-to-own" --target TICKR', expectedOutput: 'Loan-to-own analysis: Buy senior debt at 65c/$ → convert to equity in restructuring → control 51% of reorganized company. Cost: $195M. Potential equity value: $350M' },
        { instruction: 'Loan-to-own involves buying debt to gain control of the company in restructuring.' },
        { instruction: 'The cat prefers "tuna-to-own" — lend tuna, own the can factory.' },
        { instruction: 'Simulate a distressed trade: `distressed trade --buy "TICKR 8.5% 2026" --price 45 --target 85 --horizon 18mo`', command: 'distressed trade --buy "TICKR 8.5% 2026" --price 45 --target 85 --horizon 18mo', expectedOutput: 'Distressed trade: Buy TICKR 8.5% 2026 at 45 → Exit at 85 in 18mo → IRR 52% (successful restructuring scenario)' },
      ],
      quiz: [
        { question: 'What is a "loan-to-own" strategy in distressed investing?', options: ['Buying distressed debt to convert into equity and gain control during restructuring', 'Borrowing money to buy distressed assets', 'Taking out a loan to start a business', 'Lending money to distressed companies at high rates'], correctIndex: 0, explanation: 'Loan-to-own is a strategy where an investor purchases distressed debt with the intention of converting it to equity in a restructuring to gain majority control of the company.' },
      ],
    },
  ],
}
