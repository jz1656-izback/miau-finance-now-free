import type { Course } from '../lib/types'

export const bankingInstitutions: Course = {
  id: 'banking-institutions',
  slug: 'banking-institutions',
  title: 'Banking & Financial Institutions',
  description: 'Bank financials, regulation, and capital requirements — the cat audits the vault.',
  category: 'Banking',
  difficulty: 'intermediate',
  icon: '🏦',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'bk-financials',
      slug: 'bank-financials',
      title: 'Bank Financial Statements',
      description: 'Understand how banks make and report money.',
      commands: ['bank', 'bank financials'],
      steps: [
        { instruction: 'View bank financials: `bank financials --ticker JPM`', command: 'bank financials --ticker JPM', expectedOutput: 'Net interest income, provisions, and efficiency ratio' },
        { instruction: 'Net Interest Income (NII) = interest earned on loans minus interest paid on deposits.' },
        { instruction: 'The efficiency ratio measures non-interest expenses as a percentage of revenue.' },
      ],
      quiz: [
        { question: 'What is Net Interest Income?', options: ['Interest earned minus interest paid', 'Total bank revenue', 'Profit after taxes', 'Loan loss provisions'], correctIndex: 0, explanation: 'Net Interest Income is the difference between interest income earned on assets and interest paid on liabilities.' },
      ],
    },
    {
      id: 'bk-regulation',
      slug: 'bank-regulation',
      title: 'Bank Regulation',
      description: 'Basel III, Dodd-Frank, and how banks are regulated.',
      commands: ['financials', 'financials statement'],
      steps: [
        { instruction: 'Check regulatory compliance: `bank regulation --standard basel3`', command: 'bank regulation --standard basel3', expectedOutput: 'Basel III capital ratios: CET1, Tier 1, and Total Capital' },
        { instruction: 'Basel III requires banks to maintain minimum capital ratios and liquidity coverage.' },
        { instruction: 'Stress tests simulate adverse economic scenarios to ensure bank resilience.' },
      ],
      quiz: [
        { question: 'What is the minimum CET1 capital ratio under Basel III?', options: ['4.5%', '6%', '8%', '10%'], correctIndex: 0, explanation: 'Basel III requires banks to maintain a minimum Common Equity Tier 1 (CET1) capital ratio of 4.5% of risk-weighted assets.' },
      ],
    },
    {
      id: 'bk-capital',
      slug: 'capital-requirements',
      title: 'Capital Requirements',
      description: 'How much capital banks must hold and why.',
      commands: ['capital', 'capital ratio'],
      steps: [
        { instruction: 'Calculate capital ratios: `capital ratio --ticker JPM`', command: 'capital ratio --ticker JPM', expectedOutput: 'CET1, Tier 1, and Total Capital ratios with regulatory minimums' },
        { instruction: 'Risk-weighted assets (RWA) assign higher weights to riskier loans.' },
        { instruction: 'CCAR and DFAST are the US regulatory stress test frameworks.' },
      ],
      quiz: [
        { question: 'What are risk-weighted assets?', options: ['Assets weighted by their risk level', 'Total bank assets', 'Assets that are insured', 'Assets generating losses'], correctIndex: 0, explanation: 'Risk-weighted assets assign higher capital requirements to riskier asset classes like corporate loans vs government bonds.' },
      ],
    },
    {
      id: 'bk-risk',
      slug: 'bank-risk-management',
      title: 'Bank Risk Management',
      description: 'Credit, market, operational, and liquidity risk at banks.',
      commands: ['regulation', 'regulation stress-test'],
      steps: [
        { instruction: 'Run a bank stress test: `regulation stress-test --ticker JPM --scenario adverse`', command: 'regulation stress-test --ticker JPM --scenario adverse', expectedOutput: 'Stress test results: capital ratios under adverse scenario' },
        { instruction: 'Credit risk is the biggest risk — borrowers might default on loans.' },
        { instruction: 'Liquidity Coverage Ratio (LCR) ensures banks have enough liquid assets to survive 30 days of stress.' },
      ],
      quiz: [
        { question: 'What does the Liquidity Coverage Ratio measure?', options: ['Ability to survive 30 days of stress', 'Long-term profitability', 'Loan growth rate', 'Deposit insurance coverage'], correctIndex: 0, explanation: 'LCR requires banks to hold enough high-quality liquid assets to cover net cash outflows over 30 stress days.' },
      ],
    },
  ],
}
