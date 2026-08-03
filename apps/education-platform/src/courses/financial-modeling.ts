import type { Course } from '../lib/types'

export const financialModeling: Course = {
  id: 'financial-modeling',
  slug: 'financial-modeling',
  title: 'Financial Modeling',
  description: '3-statement models, DCF, and scenario analysis — the cat builds spreadsheets of doom.',
  category: 'Valuation',
  difficulty: 'advanced',
  icon: '📊',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'fm-3statement',
      slug: 'three-statement-model',
      title: 'The 3-Statement Model',
      description: 'Link income statement, balance sheet, and cash flow statement.',
      commands: ['model', 'model build'],
      steps: [
        { instruction: 'Build a 3-statement model: `model build --ticker AAPL`', command: 'model build --ticker AAPL', expectedOutput: 'Integrated 3-statement financial model' },
        { instruction: 'The income statement flows into retained earnings on the balance sheet.' },
        { instruction: 'Cash from operations, investing, and financing sum to the change in cash.' },
      ],
      quiz: [
        { question: 'Which financial statement connects the income statement to the balance sheet?', options: ['Cash flow statement', 'Statement of equity', 'Notes to financials', 'Audit report'], correctIndex: 0, explanation: 'The cash flow statement bridges net income (from income statement) to the cash balance (on the balance sheet).' },
      ],
    },
    {
      id: 'fm-dcf',
      slug: 'dcf-valuation',
      title: 'DCF Valuation',
      description: 'Discounted cash flow analysis — the gold standard of valuation.',
      commands: ['dcf', 'dcf calc'],
      steps: [
        { instruction: 'Run a DCF valuation: `dcf calc --ticker AAPL`', command: 'dcf calc --ticker AAPL', expectedOutput: 'DCF model with FCF projections, terminal value, and implied share price' },
        { instruction: 'DCF = sum of projected free cash flows discounted back to present value.' },
        { instruction: 'The terminal value typically represents 60-80% of the total DCF value.' },
      ],
      quiz: [
        { question: 'What does WACC represent in a DCF?', options: ['The discount rate reflecting cost of capital', 'The growth rate of cash flows', 'The terminal multiple', 'The tax rate'], correctIndex: 0, explanation: 'WACC (Weighted Average Cost of Capital) is the discount rate used in DCF to reflect the company\'s cost of all capital.' },
      ],
    },
    {
      id: 'fm-scenario',
      slug: 'scenario-analysis',
      title: 'Scenario Analysis',
      description: 'Model different outcomes with sensitivity analysis.',
      commands: ['scenario', 'scenario create'],
      steps: [
        { instruction: 'Create a scenario: `scenario create --base bear bull`', command: 'scenario create --base bear bull', expectedOutput: 'Scenario comparison table with base, bear, and bull cases' },
        { instruction: 'Base case = most likely. Bear case = pessimistic. Bull case = optimistic.' },
        { instruction: 'Assign probabilities to each scenario to get an expected value.' },
      ],
      quiz: [
        { question: 'What is scenario analysis used for?', options: ['Evaluating different possible outcomes', 'Predicting the exact future', 'Guaranteeing returns', 'Eliminating all risk'], correctIndex: 0, explanation: 'Scenario analysis models different possible future outcomes to understand the range of potential results.' },
      ],
    },
    {
      id: 'fm-sensitivity',
      slug: 'sensitivity-analysis',
      title: 'Sensitivity Analysis',
      description: 'See how changes in assumptions affect valuation.',
      commands: ['sensitivity', 'sensitivity table'],
      steps: [
        { instruction: 'Run sensitivity analysis: `sensitivity table --variable growth --range -2-5`', command: 'sensitivity table --variable growth --range -2-5', expectedOutput: 'Data table showing valuation sensitivity to growth assumptions' },
        { instruction: 'Tornado charts show which variables have the biggest impact on valuation.' },
        { instruction: 'Common sensitivities: revenue growth, margins, discount rate, terminal multiple.' },
      ],
      quiz: [
        { question: 'What does a tornado chart display?', options: ['Which variables most impact the output', 'Actual vs forecast', 'Historical stock prices', 'Market volatility'], correctIndex: 0, explanation: 'A tornado chart ranks variables by how much they impact the output, showing the range of outcomes for each.' },
      ],
    },
  ],
}
