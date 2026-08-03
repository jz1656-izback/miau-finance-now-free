import type { Course } from '../lib/types'

export const realEstate: Course = {
  id: 'real-estate',
  slug: 'real-estate',
  title: 'Real Estate Investing',
  description: 'REITs, property valuation, mortgages, and cap rates — the cat flips houses.',
  category: 'Real Estate',
  difficulty: 'intermediate',
  icon: '🏠',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 're-reits',
      slug: 'reits',
      title: 'REITs — Real Estate Investment Trusts',
      description: 'Invest in real estate without buying property.',
      commands: ['reits', 'reits list'],
      steps: [
        { instruction: 'List available REITs: `reits list`', command: 'reits list', expectedOutput: 'Table of REITs with ticker, sector, yield, and price' },
        { instruction: 'REITs must distribute 90% of taxable income as dividends.' },
        { instruction: 'REIT sectors include residential, commercial, healthcare, and data centers.' },
      ],
      quiz: [
        { question: 'What percentage of income must REITs distribute as dividends?', options: ['50%', '75%', '90%', '100%'], correctIndex: 2, explanation: 'REITs are required by law to distribute at least 90% of taxable income to shareholders.' },
      ],
    },
    {
      id: 're-valuation',
      slug: 'property-valuation',
      title: 'Property Valuation Methods',
      description: 'Learn how to value real estate properties.',
      commands: ['realestate', 'realestate comps'],
      steps: [
        { instruction: 'Run comparable market analysis: `realestate comps --address "123 Main St"`', command: 'realestate comps --address "123 Main St"', expectedOutput: 'Comparable sales in the area with price per sq ft' },
        { instruction: 'Three approaches: sales comparison, cost approach, and income approach.' },
        { instruction: 'Location is the most important factor in property value.' },
      ],
      quiz: [
        { question: 'Which valuation approach is most common for residential real estate?', options: ['Income approach', 'Cost approach', 'Sales comparison approach', 'Discounted cash flow'], correctIndex: 2, explanation: 'The sales comparison approach, which compares to similar recently sold properties, is most common for residential.' },
      ],
    },
    {
      id: 're-mortgage',
      slug: 'mortgages',
      title: 'Mortgages & Financing',
      description: 'Understand mortgage types, rates, and affordability.',
      commands: ['mortgage', 'mortgage calc'],
      steps: [
        { instruction: 'Calculate a mortgage payment: `mortgage calc --principal 300000 --rate 6.5 --term 30`', command: 'mortgage calc --principal 300000 --rate 6.5 --term 30', expectedOutput: 'Monthly payment with amortization schedule' },
        { instruction: 'Fixed-rate vs adjustable-rate mortgages — fixed locks in your rate, ARM adjusts periodically.' },
        { instruction: 'A 20% down payment avoids private mortgage insurance (PMI).' },
      ],
      quiz: [
        { question: 'What is PMI?', options: ['Private Mortgage Insurance — required when down payment is under 20%', 'Property Market Index', 'Prime Mortgage Interest', 'Principal Monthly Installment'], correctIndex: 0, explanation: 'PMI protects the lender when your down payment is less than 20% of the home value.' },
      ],
    },
    {
      id: 're-cap-rate',
      slug: 'cap-rates',
      title: 'Cap Rates & Investment Analysis',
      description: 'Use cap rates to compare real estate investments.',
      commands: ['property', 'property analysis'],
      steps: [
        { instruction: 'Analyze a property: `property analysis --price 500000 --income 60000`', command: 'property analysis --price 500000 --income 60000', expectedOutput: 'Cap rate of 12% with investment analysis' },
        { instruction: 'Cap rate = Net Operating Income / Property Value. Higher cap rates mean higher returns and higher risk.' },
        { instruction: 'A "good" cap rate depends on the market — 4-6% in hot markets, 8-12% in secondary markets.' },
      ],
      quiz: [
        { question: 'How is cap rate calculated?', options: ['NOI / Property Value', 'Rent / Mortgage Payment', 'Property Value / NOI', 'Income / Expenses'], correctIndex: 0, explanation: 'Cap rate = Net Operating Income divided by Property Value, expressed as a percentage.' },
      ],
    },
  ],
}
