import type { Course } from '../lib/types'

export const forexTrading: Course = {
  id: 'forex-trading',
  slug: 'forex-trading',
  title: 'Forex & Currency Trading',
  description: 'Currency pairs, pips, carry trade, and central bank FX — the cat trades currencies.',
  category: 'Forex',
  difficulty: 'intermediate',
  icon: '💱',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'fx-pairs',
      slug: 'currency-pairs',
      title: 'Currency Pairs',
      description: 'Understand how currency pairs work.',
      commands: ['forex', 'forex pairs'],
      steps: [
        { instruction: 'List currency pairs: `forex pairs`', command: 'forex pairs', expectedOutput: 'Table of major, minor, and exotic currency pairs with current rates' },
        { instruction: 'Major pairs include EUR/USD, GBP/USD, USD/JPY — the most liquid and tightest spreads.' },
        { instruction: 'The base currency is first (EUR/USD), quote currency is second. Price = how much quote currency for 1 base.' },
      ],
      quiz: [
        { question: 'In EUR/USD, which currency is the base?', options: ['EUR', 'USD', 'Both', 'Neither'], correctIndex: 0, explanation: 'EUR is the base currency in EUR/USD — the price shows how many US dollars one euro buys.' },
      ],
    },
    {
      id: 'fx-pips',
      slug: 'pips-lots',
      title: 'Pips, Lots & Leverage',
      description: 'Calculate profit, loss, and position sizes in forex.',
      commands: ['forex calc', 'forex pip'],
      steps: [
        { instruction: 'Calculate pip value: `forex pip --pair EUR/USD --lots 1`', command: 'forex pip --pair EUR/USD --lots 1', expectedOutput: 'Pip value of $10 for 1 standard lot of EUR/USD' },
        { instruction: 'A pip is the smallest price move, usually 0.0001 for most pairs.' },
        { instruction: 'Leverage in forex can be 50:1 or higher — it amplifies both gains and losses.' },
      ],
      quiz: [
        { question: 'What is a pip in forex trading?', options: ['The smallest price movement in a currency pair', 'A percentage point', 'A type of order', 'A trading strategy'], correctIndex: 0, explanation: 'A pip (percentage in point) is the smallest standardized price movement in forex, typically 0.0001.' },
      ],
    },
    {
      id: 'fx-carry',
      slug: 'carry-trade',
      title: 'Carry Trade Strategy',
      description: 'Profit from interest rate differences between currencies.',
      commands: ['carry', 'carry trade'],
      steps: [
        { instruction: 'Find carry trade opportunities: `carry trade --list`', command: 'carry trade --list', expectedOutput: 'Currency pairs ranked by interest rate differential' },
        { instruction: 'A carry trade borrows a low-interest currency to buy a high-interest one.' },
        { instruction: 'The risk is that exchange rate moves can wipe out interest profits.' },
      ],
      quiz: [
        { question: 'How does a carry trade profit?', options: ['From interest rate differentials between currencies', 'From currency appreciation only', 'From low spreads', 'From high leverage'], correctIndex: 0, explanation: 'A carry trade profits from the interest rate differential — earning more interest on the bought currency than paid on the sold one.' },
      ],
    },
    {
      id: 'fx-central-bank',
      slug: 'central-bank-fx',
      title: 'Central Banks & FX',
      description: 'How central bank policies drive currency markets.',
      commands: ['fx', 'fx central-bank'],
      steps: [
        { instruction: 'Check central bank calendar: `fx central-bank --calendar`', command: 'fx central-bank --calendar', expectedOutput: 'Upcoming central bank meetings and rate decisions' },
        { instruction: 'Higher interest rates attract foreign capital, strengthening the currency.' },
        { instruction: 'Central bank forward guidance can move currency markets even before rate changes.' },
      ],
      quiz: [
        { question: 'What typically happens to a currency when its central bank raises rates?', options: ['The currency tends to strengthen', 'The currency tends to weaken', 'No effect on currency', 'The currency becomes fixed'], correctIndex: 0, explanation: 'Higher interest rates attract foreign investment seeking yield, increasing demand for the currency and strengthening it.' },
      ],
    },
  ],
}
