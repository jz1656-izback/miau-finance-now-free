import type { Course } from '../lib/types'

export const globalFxCurrency: Course = {
  id: 'global-fx-currency',
  slug: 'global-fx-currency',
  title: 'Global FX & Currency Markets',
  description: 'Navigate the foreign exchange market — the cat trades yen for tuna across international waters.',
  category: 'Forex',
  difficulty: 'intermediate',
  icon: '💱',
  lessonCount: 3,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'fx-rates', slug: 'fx-rates', title: 'Understanding FX Rates',
      description: 'Live currency rates and pairs.',
      commands: ['fx USD', 'fx EUR'],
      steps: [
        { instruction: 'Check USD rates: `fx USD`', command: 'fx USD', expectedOutput: 'Major currency pairs against USD' },
        { instruction: 'FX rates show how much of a quote currency you get for one unit of base currency.' },
        { instruction: 'The cat tracks the Tuna/USD cross rate. It is highly correlated with fish market open.' },
        { instruction: 'Try EUR: `fx EUR`', command: 'fx EUR', expectedOutput: 'Euro-based rates' },
      ],
      quiz: [{ question: 'What does EUR/USD = 1.10 mean?', options: ['1 Euro buys 1.10 US Dollars', '1 US Dollar buys 1.10 Euros', '10 Euros = 1 Dollar', 'The rate changed by 1.10%'], correctIndex: 0, explanation: 'EUR/USD is the number of US Dollars needed to buy one Euro. 1.10 means 1 Euro = $1.10.' }],
    },
    {
      id: 'fx-conversion', slug: 'fx-conversion', title: 'Currency Conversion',
      description: 'Convert amounts between currencies.',
      commands: ['fxconvert 100 USD EUR', 'fxconvert 500 EUR GBP'],
      steps: [
        { instruction: 'Convert $100 to EUR: `fxconvert 100 USD EUR`', command: 'fxconvert 100 USD EUR', expectedOutput: 'Converted amount and exchange rate' },
        { instruction: 'Always check both directions to avoid bad rates.' },
        { instruction: 'The cat converts USD to EUR for its Monaco summer home. The tax implications are complex.' },
      ],
      quiz: [{ question: 'If EUR/USD rises from 1.10 to 1.20, the dollar has...', options: ['Weakened against the euro', 'Strengthened against the euro', 'Stayed the same', 'Become more volatile'], correctIndex: 0, explanation: 'A higher EUR/USD means each Euro buys more dollars, so the dollar has weakened relative to the euro.' }],
    },
    {
      id: 'fx-strategies', slug: 'fx-strategies', title: 'Currency Trading Strategies',
      description: 'Basic FX trading approaches.',
      commands: ['fx GBP', 'fx JPY'],
      steps: [
        { instruction: 'Check GBP: `fx GBP`', command: 'fx GBP', expectedOutput: 'Sterling rates' },
        { instruction: 'Carry trade: borrow low-yield currency, buy high-yield currency.' },
        { instruction: 'The cat tried carry trade between Tuna (high yield) and Catnip (low yield). Results were fishy.' },
      ],
      quiz: [{ question: 'What is a carry trade in FX?', options: ['Borrowing a low-interest currency to buy a high-interest one', 'Trading currencies at the same price', 'Holding cash only', 'Shorting both currencies'], correctIndex: 0, explanation: 'A carry trade exploits interest rate differentials by borrowing in low-yield currencies and investing in high-yield ones.' }],
    },
  ],
}
