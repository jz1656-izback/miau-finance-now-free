import type { Course } from '../lib/types'

export const macroEconomics: Course = {
  id: 'macro-economics',
  slug: 'macro-economics',
  title: 'Macro Economics & Central Banking',
  description: 'GDP, inflation, interest rates, central bank policy, and how macro moves markets.',
  category: 'Economics',
  difficulty: 'intermediate',
  icon: '🏛️',
  lessonCount: 5,
  estimatedMinutes: 30,
  lessons: [
    {
      id: 'macro-gdp',
      slug: 'gdp-growth',
      title: 'GDP & Economic Growth',
      description: 'Understand GDP components and what drives economic growth.',
      commands: ['economics', 'economics gdp'],
      steps: [
        { instruction: 'View US GDP data: `economics gdp US`', command: 'economics gdp US', expectedOutput: 'GDP breakdown by component (C+I+G+NX)' },
        { instruction: 'GDP = Consumption + Investment + Government + Net Exports. Each tells a different story.' },
        { instruction: 'Compare GDP growth rates: `economics gdp US EU CN --compare`', command: 'economics gdp US EU CN --compare', expectedOutput: 'GDP growth comparison chart' },
      ],
      quiz: [
        { question: 'What does GDP stand for?', options: ['Gross Domestic Product', 'Gross Demand Product', 'General Domestic Price', 'Government Debt Premium'], correctIndex: 0, explanation: 'Gross Domestic Product — the total value of goods and services produced in a country.' },
      ],
    },
    {
      id: 'macro-inflation',
      slug: 'inflation',
      title: 'Inflation & Price Stability',
      description: 'CPI, PCE, core inflation, and how central banks target price stability.',
      commands: ['economics inflation', 'economics cpi'],
      steps: [
        { instruction: 'Check inflation data: `economics inflation US`', command: 'economics inflation US', expectedOutput: 'CPI, Core CPI, PCE, Core PCE' },
        { instruction: 'Core inflation excludes food and energy — used by central banks as the true signal.' },
        { instruction: 'Compare inflation globally: `economics inflation --top5`', command: 'economics inflation --top5', expectedOutput: 'Top 5 highest/lowest inflation countries' },
      ],
      quiz: [
        { question: 'What does core inflation exclude?', options: ['Food and energy', 'Housing and healthcare', 'Imports and exports', 'Services and goods'], correctIndex: 0, explanation: 'Core inflation strips out volatile food and energy prices to show the underlying inflation trend.' },
      ],
    },
    {
      id: 'macro-interest',
      slug: 'interest-rates',
      title: 'Interest Rates & Monetary Policy',
      description: 'Fed funds rate, yield curve, QT, and the tools central banks use.',
      commands: ['economics fed', 'economics yield-curve'],
      steps: [
        { instruction: 'View Fed rate decisions: `economics fed`', command: 'economics fed', expectedOutput: 'Current Fed funds rate and meeting calendar' },
        { instruction: 'Yield curve inversion = long-term rates lower than short-term. Historically predicts recessions.' },
        { instruction: 'View yield curve: `economics yield-curve US`', command: 'economics yield-curve US', expectedOutput: 'Treasury yield curve with historical comparison' },
      ],
      quiz: [
        { question: 'What does an inverted yield curve historically signal?', options: ['Upcoming recession', 'Strong economic growth', 'Low inflation', 'Bull market'], correctIndex: 0, explanation: 'An inverted yield curve (short rates > long rates) has preceded most recessions.' },
      ],
    },
    {
      id: 'macro-central-banks',
      slug: 'central-banks',
      title: 'Central Banks & Policy Tools',
      description: 'Fed, ECB, BOJ, BOE — their tools, mandates, and market impact.',
      commands: ['economics central-bank', 'economics policy'],
      steps: [
        { instruction: 'Compare central bank policies: `economics central-bank --all`', command: 'economics central-bank --all', expectedOutput: 'Current policy rates for all major central banks' },
        { instruction: 'The Fed has a dual mandate: maximum employment and stable prices (2% inflation).' },
        { instruction: 'The ECB\'s primary mandate is price stability. The BOJ has fought deflation for decades.' },
      ],
      quiz: [
        { question: 'What is the Fed\'s dual mandate?', options: ['Max employment + stable prices', 'Low inflation + strong dollar', 'Growth + low debt', 'Trade balance + employment'], correctIndex: 0, explanation: 'The Federal Reserve targets both maximum employment and price stability (2% inflation).' },
      ],
    },
    {
      id: 'macro-trading',
      slug: 'macro-trading',
      title: 'Macro-Driven Trading',
      description: 'Trade macro events — NFP, CPI, FOMC — and understand how data moves markets.',
      commands: ['economics calendar', 'economics event'],
      steps: [
        { instruction: 'View economic calendar: `economics calendar --week`', command: 'economics calendar --week', expectedOutput: 'Upcoming economic events with consensus estimates' },
        { instruction: 'NFP (Non-Farm Payrolls) is the biggest monthly market mover. Released first Friday of every month.' },
        { instruction: 'CPI surprise = instant market repricing. Know the consensus before the release.' },
      ],
      quiz: [
        { question: 'When is NFP released?', options: ['First Friday of each month', 'Every Monday', 'Last day of each month', 'Every Thursday'], correctIndex: 0, explanation: 'Non-Farm Payrolls are released on the first Friday of every month at 8:30 AM ET.' },
      ],
    },
  ],
}
