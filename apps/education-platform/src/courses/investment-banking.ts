import type { Course } from '../lib/types'

export const investmentBanking: Course = {
  id: 'investment-banking',
  slug: 'investment-banking',
  title: 'Investment Banking Toolkit',
  description: 'DCF, WACC, comparable analysis, and LBO — the cat has an MBA.',
  category: 'Analytics',
  difficulty: 'advanced',
  icon: '🏦',
  lessonCount: 4,
  estimatedMinutes: 30,
  lessons: [
    {
      id: 'ib-dcf',
      slug: 'dcf',
      title: 'Discounted Cash Flow',
      description: 'Value a company using DCF analysis.',
      commands: ['sheetz -dcf'],
      steps: [
        { instruction: 'Run a DCF: `sheetz -dcf AAPL`', command: 'sheetz -dcf AAPL', expectedOutput: 'DCF valuation with projected cash flows and terminal value' },
        { instruction: 'The output shows: free cash flows, WACC, terminal value, enterprise value, and fair value per share.' },
        { instruction: 'Compare the fair value to the current price for a BUY/HOLD/SELL verdict.' },
      ],
      quiz: [
        { question: 'What does DCF stand for?', options: ['Discounted Cash Flow', 'Direct Capital Funding', 'Debt Coverage Formula', 'Daily Cash Forecast'], correctIndex: 0, explanation: 'DCF = Discounted Cash Flow — projects future cash flows and discounts them to present value.' },
      ],
    },
    {
      id: 'ib-wacc',
      slug: 'wacc',
      title: 'WACC Calculation',
      description: 'Calculate the weighted average cost of capital.',
      commands: ['sheetz -wacc'],
      steps: [
        { instruction: 'Calculate WACC: `sheetz -wacc MSFT`', command: 'sheetz -wacc MSFT', expectedOutput: 'Cost of equity, cost of debt, and WACC' },
        { instruction: 'WACC is the blended cost of all capital — used as the discount rate in DCF.' },
      ],
      quiz: [
        { question: 'What does WACC represent?', options: ['Blended cost of capital', 'Stock price target', 'Dividend rate', 'Tax rate'], correctIndex: 0, explanation: 'WACC is the Weighted Average Cost of Capital — the blended cost of equity and debt.' },
      ],
    },
    {
      id: 'ib-comps',
      slug: 'comps',
      title: 'Comparable Company Analysis',
      description: 'Value a company relative to its peers.',
      commands: ['sheetz -comps'],
      steps: [
        { instruction: 'Run comps: `sheetz -comps GOOGL`', command: 'sheetz -comps GOOGL', expectedOutput: 'Peer multiples (P/E, EV/EBITDA, P/S) and implied valuation' },
        { instruction: 'Multiples give you a sense of whether a stock is cheap or expensive vs peers.' },
      ],
      quiz: [
        { question: 'What do comps compare?', options: ['Valuation multiples vs peers', 'Stock prices only', 'Dividend yields', 'Management quality'], correctIndex: 0, explanation: 'Comparable analysis compares valuation multiples (P/E, EV/EBITDA) against peer companies.' },
      ],
    },
    {
      id: 'ib-lbo',
      slug: 'lbo',
      title: 'Leveraged Buyout Model',
      description: 'Model an LBO scenario.',
      commands: ['sheetz -lbo', 'sheetz -all', 'sheetz miau'],
      steps: [
        { instruction: 'Run an LBO: `sheetz -lbo AAPL`', command: 'sheetz -lbo AAPL', expectedOutput: 'LBO model with debt schedule and IRR' },
        { instruction: 'Run all four models: `sheetz -all AAPL`', command: 'sheetz -all AAPL', expectedOutput: 'DCF, WACC, Comps, and LBO — all at once' },
        { instruction: 'Export to CSV: `sheetz miau -all AAPL`', command: 'sheetz miau -all AAPL', expectedOutput: 'All models downloaded as CSV' },
      ],
      quiz: [
        { question: 'What does `sheetz -all` do?', options: ['Runs all 4 valuation models', 'Shows all tickers', 'Lists all commands', 'Nothing special'], correctIndex: 0, explanation: '`sheetz -all` runs DCF, WACC, Comps, and LBO simultaneously.' },
      ],
    },
  ],
}
