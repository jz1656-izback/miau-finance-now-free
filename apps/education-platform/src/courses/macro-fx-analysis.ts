import type { Course } from '../lib/types'

export const macroFxAnalysis: Course = {
  id: 'macro-fx-analysis',
  slug: 'macro-fx-analysis',
  title: 'Macro & FX Analysis',
  description: 'FX rates, currency conversion, historical trends, and macroeconomic indicators — the cat trades currencies globally.',
  category: 'Macro',
  difficulty: 'beginner',
  icon: '💱',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'fx-rates',
      slug: 'live-fx-rates',
      title: 'Live FX Rates',
      description: '200+ currency pairs from 55 central banks.',
      commands: ['fx USD', 'fx EUR', 'fx GBP'],
      steps: [
        { instruction: 'Get all FX rates: `fx USD` — 200+ pairs with USD as base', command: 'fx USD', expectedOutput: 'USD exchange rates with EUR, GBP, JPY, CHF, etc.' },
        { instruction: 'The FX market is the largest financial market in the world at $7.5T daily volume.' },
        { instruction: 'Try a different base: `fx EUR` — see all euro rates', command: 'fx EUR', expectedOutput: 'EUR exchange rates' },
        { instruction: 'The cat checked the USD/JPY rate and bought yen. It is now a samurai cat.' },
      ],
      quiz: [
        { question: 'What is the most traded currency pair in the world?', options: ['EUR/USD — the euro and US dollar pair accounts for ~25% of all FX trades', 'USD/JPY', 'GBP/USD', 'USD/CHF'], correctIndex: 0, explanation: 'EUR/USD is the most traded currency pair globally, representing approximately 25% of all daily FX transaction volume.' },
      ],
    },
    {
      id: 'fx-convert',
      slug: 'currency-converter',
      title: 'Currency Conversion',
      description: 'Convert any amount between any two currencies.',
      commands: ['fxconvert 100 USD EUR', 'fxconvert 50000 JPY USD'],
      steps: [
        { instruction: 'Convert currency: `fxconvert 100 USD EUR` — $100 to euros', command: 'fxconvert 100 USD EUR', expectedOutput: '100 USD = 91.50 EUR @ 0.9150 rate' },
        { instruction: 'Travel conversion: `fxconvert 50000 JPY USD` — how much is 50K yen in dollars?', command: 'fxconvert 50000 JPY USD', expectedOutput: '50000 JPY to USD conversion' },
        { instruction: 'The cat converted tuna to sardines. The spread was terrible. Never trade fish without checking FX.' },
        { instruction: 'Check historical rates: `fxhistory USD EUR 2024-01-01` to see how a pair has moved', command: 'fxhistory USD EUR 2024-01-01', expectedOutput: 'USD/EUR historical rates' },
      ],
      quiz: [
        { question: 'What does the "spread" mean in FX conversion?', options: ['The difference between the buy and sell price — the cost of converting currencies', 'The difference between two currency rates', 'The volatility of a currency pair', 'The central bank interest rate'], correctIndex: 0, explanation: 'The spread is the difference between the bid (buy) and ask (sell) price. A narrower spread means lower transaction costs for currency conversion.' },
      ],
    },
    {
      id: 'macro-indicators',
      slug: 'economic-indicators',
      title: 'Economic Indicators',
      description: 'GDP, CPI, employment, and central bank rates.',
      commands: ['cpi US', 'gdp US'],
      steps: [
        { instruction: 'Check CPI data: `cpi US` — inflation rate with YoY change', command: 'cpi US', expectedOutput: 'US CPI data with year-over-year change' },
        { instruction: 'CPI measures inflation — the rate at which prices for goods and services rise.' },
        { instruction: 'The cat tracks CPI because it directly affects tuna prices. Inflation is the enemy of tuna.' },
        { instruction: 'GDP shows economic growth: `gdp US` to see the overall health of the economy', command: 'gdp US', expectedOutput: 'US GDP quarterly and yearly data' },
      ],
      quiz: [
        { question: 'Why is CPI an important indicator for FX traders?', options: ['Central banks adjust interest rates based on inflation, which directly affects currency values', 'CPI determines stock prices', 'CPI only matters for commodities', 'CPI is irrelevant for currency trading'], correctIndex: 0, explanation: 'Central banks raise rates to combat high CPI (inflation), which strengthens the currency as higher rates attract foreign capital. Lower rates from low CPI weaken it.' },
      ],
    },
    {
      id: 'macro-workflow',
      slug: 'macro-trading-workflow',
      title: 'Macro Trading Workflow',
      description: 'Combine FX and macro for informed trading decisions.',
      commands: ['fx USD', 'fxconvert 1000 USD EUR', 'fxhistory USD EUR 2024-06-01'],
      steps: [
        { instruction: 'Start with rates: `fx USD` to see the landscape', command: 'fx USD', expectedOutput: 'Current FX rate landscape' },
        { instruction: 'Convert for a specific trade: `fxconvert 1000 USD EUR`', command: 'fxconvert 1000 USD EUR', expectedOutput: '1000 USD to EUR conversion' },
        { instruction: 'Check the trend: `fxhistory USD EUR 2024-01-01` to see direction', command: 'fxhistory USD EUR 2024-01-01', expectedOutput: 'Historical EUR/USD rate chart' },
        { instruction: 'The cat used this workflow to buy euros when EUR/USD hit a low. It saved 3 cans of tuna.' },
      ],
      quiz: [
        { question: 'What is the carry trade in FX?', options: ['Borrowing a low-interest-rate currency to invest in a high-interest-rate one, earning the rate differential', 'Carrying physical currency across borders', 'A type of futures contract', 'Trading currencies at a fixed rate'], correctIndex: 0, explanation: 'The carry trade borrows in a currency with a low interest rate (like JPY) and invests in one with a higher rate (like AUD or NZD), profiting from the interest rate differential.' },
      ],
    },
  ],
}
