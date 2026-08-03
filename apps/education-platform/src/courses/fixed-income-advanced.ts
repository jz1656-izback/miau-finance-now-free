import type { Course } from '../lib/types'

export const fixedIncomeAdvanced: Course = {
  id: 'fixed-income-advanced',
  slug: 'fixed-income-advanced',
  title: 'Fixed Income Advanced',
  description: 'MBS, CDS, structured products, and CLOs — the cat finds fixed income more exciting than a laser pointer.',
  category: 'Fixed Income',
  difficulty: 'advanced',
  icon: '📈',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'fi-mbs',
      slug: 'mortgage-backed-securities',
      title: 'Mortgage-Backed Securities',
      description: 'Pools of mortgages sliced and diced.',
      commands: ['mbs', 'mbs analyze'],
      steps: [
        { instruction: 'Analyze an MBS pool: `mbs analyze --pool FNMA1234 --factors wac,wam,cpr`', command: 'mbs analyze --pool FNMA1234 --factors wac,wam,cpr', expectedOutput: 'MBS pool FNMA1234: WAC 4.25%, WAM 320mo, CPR 8.5% — OAS 65bps' },
        { instruction: 'MBS cash flows depend on homeowner prepayment behavior.' },
        { instruction: 'The cat models prepayment risk — sometimes humans pay off mortgages early, it is unpredictable.' },
      ],
      quiz: [
        { question: 'What is prepayment risk in MBS?', options: ['Homeowners may pay off mortgages early, altering cash flows', 'Homeowners never pay on time', 'The bank can call the loan at any time', 'Interest rates are fixed forever'], correctIndex: 0, explanation: 'When homeowners refinance or sell, they prepay mortgages, returning principal earlier than expected and changing MBS yields.' },
      ],
    },
    {
      id: 'fi-cds',
      slug: 'credit-default-swaps',
      title: 'Credit Default Swaps',
      description: 'Insurance against default.',
      commands: ['cds', 'cds price'],
      steps: [
        { instruction: 'Price a CDS contract: `cds price --reference AAPL --tenor 5y --recovery 40`', command: 'cds price --reference AAPL --tenor 5y --recovery 40', expectedOutput: 'CDS spread: 35bps — annual premium $35k per $10M notional, PV of protection leg $120k' },
        { instruction: 'CDS are insurance contracts that pay out if a reference entity defaults.' },
        { instruction: 'The cat bought CDS on the tuna supply chain — just in case of a fish shortage.' },
      ],
      quiz: [
        { question: 'What is the CDS spread?', options: ['The annual premium as a percentage of notional value', 'The difference between bid and ask prices', 'The spread between CDS and bond yields', 'The default probability'], correctIndex: 0, explanation: 'The CDS spread is the annual premium paid by the protection buyer, expressed in basis points of the notional amount.' },
      ],
    },
    {
      id: 'fi-structured',
      slug: 'structured-products',
      title: 'Structured Products',
      description: 'Engineered fixed-income instruments.',
      commands: ['structured', 'structured analyze'],
      steps: [
        { instruction: 'Analyze a structured product: `structured analyze --ticker ABC-2026-1 --tranches senior,mezz,equity`', command: 'structured analyze --ticker ABC-2026-1 --tranches senior,mezz,equity', expectedOutput: 'ABC-2026-1: senior AAA (3.5%), mezz A (5.2%), equity (12.8% expected)' },
        { instruction: 'Tranching creates different risk-return profiles from the same pool of assets.' },
        { instruction: 'The cat invested in the equity tranche — highest risk, highest reward, most catnip.' },
      ],
      quiz: [
        { question: 'Why do structured products create tranches?', options: ['To offer different risk-return profiles from the same asset pool', 'To hide risky assets from investors', 'To reduce the number of investors needed', 'To avoid regulatory oversight'], correctIndex: 0, explanation: 'Tranching lets investors choose different risk levels, with senior tranches safer but lower-yielding than equity tranches.' },
      ],
    },
    {
      id: 'fi-clo',
      slug: 'collateralized-loan-obligations',
      title: 'Collateralized Loan Obligations',
      description: 'CLOs — the comeback kid of structured credit.',
      commands: ['clo', 'clo waterfall'],
      steps: [
        { instruction: 'Run a CLO waterfall analysis: `clo waterfall --deal CLO-2025-1 --default-rate 3`', command: 'clo waterfall --deal CLO-2025-1 --default-rate 3', expectedOutput: 'CLO waterfall: senior paid 100%, mezz paid 100%, equity IRR 8.2% at 3% default rate' },
        { instruction: 'CLOs pool leveraged loans and issue tranched securities.' },
        { instruction: 'The cat owns a CLO equity tranche — it is basically a lottery ticket with extra steps.' },
      ],
      quiz: [
        { question: 'What is the primary risk in CLO equity tranches?', options: ['Loan defaults reduce cash flow available to the lowest tranche', 'Interest rate increases always help equity', 'Equity tranches have the lowest yield', 'CLO managers cannot trade loans'], correctIndex: 0, explanation: 'Equity is the first-loss tranche — when loans default, equity absorbs losses before senior or mezzanine tranches.' },
      ],
    },
  ],
}
