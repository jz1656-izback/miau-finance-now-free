import type { Course } from '../lib/types'

export const projectFinance: Course = {
  id: 'project-finance',
  slug: 'project-finance',
  title: 'Project Finance',
  description: 'Infrastructure PPPs, project valuation, risk allocation, and off-balance-sheet financing — the cat builds toll roads.',
  category: 'Corporate Finance',
  difficulty: 'intermediate',
  icon: '🏗️',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'project-basics',
      slug: 'project-finance-basics',
      title: 'Project Finance Fundamentals',
      description: 'What makes project finance different from corporate finance.',
      commands: ['project finance', 'project spv'],
      steps: [
        { instruction: 'Create a project SPV structure: `project spv --name "Highway 401 Expansion" --equity 300m --debt 700m`', command: 'project spv --name "Highway 401 Expansion" --equity 300m --debt 700m', expectedOutput: 'SPV: Highway 401 Expansion LP. Equity: $300M (sponsor). Debt: $700M (non-recourse). Total: $1B. Debt/Equity: 70/30' },
        { instruction: 'Project finance uses non-recourse debt — lenders can only claim the project assets, not the sponsor.' },
        { instruction: 'The cat formed an SPV for a catnip highway. The tolls are paid in treats.' },
      ],
      quiz: [
        { question: 'What does "non-recourse" mean in project finance?', options: ['Lenders can only claim the project assets if the borrower defaults, not the sponsor parent', 'The borrower has no legal obligation to repay', 'The loan has zero interest', 'The project has no revenue risk'], correctIndex: 0, explanation: 'Non-recourse debt means lenders can only seize the project assets and cash flows in default, with no claim against the parent company sponsors.' },
      ],
    },
    {
      id: 'project-risks',
      slug: 'project-risk-allocation',
      title: 'Project Risk Allocation',
      description: 'Identifying and allocating risks in infrastructure projects.',
      commands: ['project risk', 'project allocate'],
      steps: [
        { instruction: 'Run a risk matrix for a project: `project risk --name "Solar Farm 500MW" --phase construction`', command: 'project risk --name "Solar Farm 500MW" --phase construction', expectedOutput: 'Top risks: 1) Construction delay (P60: 3mo overrun, $50M cost), 2) Panel price escalation (P80: +15%, $30M), 3) Permitting delay (P40: 6mo, $20M)' },
        { instruction: 'Key project risks: construction, completion, revenue, currency, political, force majeure.' },
        { instruction: 'Allocate risk to the party best able to manage it: `project allocate --risk "construction delay" --to contractor --penalty 100k/day`', command: 'project allocate --risk "construction delay" --to contractor --penalty 100k/day', expectedOutput: 'Risk allocated: construction delay → EPC contractor. Liquidated damages: $100K/day. Cap: 10% of contract value' },
        { instruction: 'The cat allocates the risk of running out of tuna to "future self."' },
      ],
      quiz: [
        { question: 'What is the most common risk allocation mechanism for construction delays in project finance?', options: ['Liquidated damages in the EPC contract — the contractor pays a daily penalty for delays', 'Government guarantees', 'Revenue sharing agreements', 'Interest rate swaps'], correctIndex: 0, explanation: 'Construction delay risk is typically allocated through liquidated damages in the EPC contract, requiring the contractor to pay a predetermined daily penalty for delays.' },
      ],
    },
    {
      id: 'project-valuation',
      slug: 'project-valuation-models',
      title: 'Project Valuation & Cash Flow Modeling',
      description: 'Building project finance cash flow models.',
      commands: ['project model', 'project irr'],
      steps: [
        { instruction: 'Build a project cash flow model: `project model --name "Wind Farm" --capex 500m --opex 20m/year --revenue 80m/year --tenor 25yr`', command: 'project model --name "Wind Farm" --capex 500m --opex 20m/year --revenue 80m/year --tenor 25yr', expectedOutput: 'Wind Farm model: EBITDA $60M/yr, Debt service $35M/yr, DSCR 1.71x, LLCR 1.52x, Project IRR 9.8%, Equity IRR 14.2%' },
        { instruction: 'Key metrics: DSCR (Debt Service Coverage Ratio) and LLCR (Loan Life Coverage Ratio).' },
        { instruction: 'Run sensitivity analysis: `project model --sensitivity --variable "electricity price" --range -20%,+20%`', command: 'project model --sensitivity --variable "electricity price" --range -20%,+20%', expectedOutput: 'Electricity -20%: IRR 6.5%, DSCR 1.25x. Base: IRR 9.8%, DSCR 1.71x. +20%: IRR 13.1%, DSCR 2.15x' },
        { instruction: 'The cat\'s wind farm model assumes wind speeds are "sufficient for napping-induced turbulence."' },
      ],
      quiz: [
        { question: 'What does DSCR (Debt Service Coverage Ratio) measure in project finance?', options: ['Project EBITDA divided by total debt service — measures ability to pay debt', 'The discount rate used in NPV calculations', 'The ratio of equity to debt in the project', 'The project internal rate of return'], correctIndex: 0, explanation: 'DSCR = EBITDA / Total Debt Service. It measures how many times the project cash flow covers its debt obligations. Lenders typically require DSCR > 1.20x.' },
      ],
    },
    {
      id: 'ppp-structures',
      slug: 'public-private-partnerships',
      title: 'Public-Private Partnerships (PPPs)',
      description: 'Government partnership structures for infrastructure.',
      commands: ['project ppp', 'project bid'],
      steps: [
        { instruction: 'Analyze a PPP structure: `project ppp --type "availability" --value 2b --term 30yr`', command: 'project ppp --type "availability" --value 2b --term 30yr', expectedOutput: 'Availability PPP: $2B, 30yr. Government pays monthly availability charge: $8.5M/mo. Performance deductions for non-compliance. No demand risk for private partner' },
        { instruction: 'PPP types: Availability (gov pays fixed), Concession (user pays tolls), Hybrid (both).' },
        { instruction: 'Bid on a PPP project: `project bid --name "Bridge Project" --irr 12 --equity 100m`', command: 'project bid --name "Bridge Project" --irr 12 --equity 100m', expectedOutput: 'Bid submitted: Bridge Project. Equity IRR 12%. Bid score: Technical 82/100, Financial 91/100. Combined: 86.5/100. Competitor bids: 3' },
        { instruction: 'The cat bid on a bridge PPP — tolls paid in tuna. The cat calls it "Tuna Bridge."' },
      ],
      quiz: [
        { question: 'In an Availability PPP, how does the private partner get paid?', options: ['Fixed periodic payments from the government based on asset availability, regardless of usage', 'Tolls collected directly from users', 'A percentage of government tax revenue', 'One-time lump sum at project completion'], correctIndex: 0, explanation: 'In an Availability PPP, the government makes regular payments to the private partner for making the asset available and meeting performance standards, removing demand/usage risk from the private sector.' },
      ],
    },
  ],
}
