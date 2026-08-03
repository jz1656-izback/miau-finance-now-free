import type { Course } from '../lib/types'

export const corporateFinance: Course = {
  id: 'corporate-finance',
  slug: 'corporate-finance',
  title: 'Corporate Finance',
  description: 'Capital structure, dividend policy, and cost of capital — the cat runs the CFO office.',
  category: 'Corporate Finance',
  difficulty: 'intermediate',
  icon: '🏢',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'cf-capital-structure',
      slug: 'capital-structure',
      title: 'Capital Structure',
      description: 'Debt vs equity — how companies finance themselves.',
      commands: ['corp-finance', 'corp-finance structure'],
      steps: [
        { instruction: 'View capital structure: `corp-finance structure --ticker AAPL`', command: 'corp-finance structure --ticker AAPL', expectedOutput: 'Debt-to-equity ratio, components of capital' },
        { instruction: 'Debt is cheaper than equity because interest is tax-deductible but adds financial risk.' },
        { instruction: 'The optimal capital structure balances the tax benefit of debt against bankruptcy risk.' },
      ],
      quiz: [
        { question: 'Why is debt typically cheaper than equity?', options: ['Interest payments are tax-deductible', 'Debt has higher returns', 'Debt never defaults', 'Equity is subsidized'], correctIndex: 0, explanation: 'Interest payments on debt are tax-deductible, reducing the effective cost of debt compared to equity.' },
      ],
    },
    {
      id: 'cf-dividend',
      slug: 'dividend-policy',
      title: 'Dividend Policy',
      description: 'How companies decide to pay dividends or reinvest.',
      commands: ['capital', 'capital dividend'],
      steps: [
        { instruction: 'Check dividend policy: `capital dividend --ticker AAPL`', command: 'capital dividend --ticker AAPL', expectedOutput: 'Dividend history, payout ratio, and yield' },
        { instruction: 'Dividends signal confidence. Cutting dividends often signals trouble.' },
        { instruction: 'Share buybacks are an alternative way to return capital to shareholders.' },
      ],
      quiz: [
        { question: 'What does a high dividend payout ratio indicate?', options: ['The company returns most earnings as dividends', 'The company is growing fast', 'The company has no profits', 'The company is in bankruptcy'], correctIndex: 0, explanation: 'A high payout ratio means the company pays out a large portion of earnings as dividends, leaving less for reinvestment.' },
      ],
    },
    {
      id: 'cf-wacc',
      slug: 'cost-of-capital',
      title: 'Cost of Capital (WACC)',
      description: 'Calculate the weighted average cost of capital.',
      commands: ['dividend', 'dividend calc'],
      steps: [
        { instruction: 'Calculate WACC: `wacc calc --ticker AAPL`', command: 'wacc calc --ticker AAPL', expectedOutput: 'WACC breakdown with cost of equity, cost of debt, and weights' },
        { instruction: 'WACC = (E/V × Re) + (D/V × Rd × (1 - Tc)). It is the minimum return a company must earn.' },
        { instruction: 'CAPM is used to estimate cost of equity: Re = Rf + β × (Rm - Rf).' },
      ],
      quiz: [
        { question: 'What does CAPM stand for?', options: ['Capital Asset Pricing Model', 'Corporate Asset Pricing Model', 'Capital Allocation Pricing Method', 'Compound Asset Portfolio Model'], correctIndex: 0, explanation: 'CAPM stands for Capital Asset Pricing Model, which calculates the expected return of an asset based on its risk.' },
      ],
    },
    {
      id: 'cf-project',
      slug: 'project-finance',
      title: 'Project Finance & Capital Budgeting',
      description: 'Evaluate investment projects using NPV, IRR, and payback.',
      commands: ['wacc', 'wacc calc'],
      steps: [
        { instruction: 'Evaluate a project: `npv calc --investment 10M --cashflows 2M/3M/4M/3M --wacc 10`', command: 'npv calc --investment 10M --cashflows 2M/3M/4M/3M --wacc 10', expectedOutput: 'NPV, IRR, and payback period' },
        { instruction: 'NPV > 0 means the project adds value. IRR > WACC means the project beats the cost of capital.' },
        { instruction: 'Payback period is simple but ignores time value of money.' },
      ],
      quiz: [
        { question: 'What does a positive NPV indicate?', options: ['The project adds value above its cost', 'The project loses money', 'The project breaks even', 'The project is too risky'], correctIndex: 0, explanation: 'A positive Net Present Value means the project\'s expected returns exceed its cost, creating shareholder value.' },
      ],
    },
  ],
}
