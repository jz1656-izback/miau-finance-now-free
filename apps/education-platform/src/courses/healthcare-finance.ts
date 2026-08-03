import type { Course } from '../lib/types'

export const healthcareFinance: Course = {
  id: 'healthcare-finance',
  slug: 'healthcare-biotech-finance',
  title: 'Healthcare & Biotech Finance',
  description: 'Biotech valuation, pipeline analysis, and pharma economics — the cat invests in healthcare because nine lives need good medical coverage.',
  category: 'Industry Analysis',
  difficulty: 'advanced',
  icon: '💊',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'biotech-valuation',
      slug: 'biotech-valuation-methods',
      title: 'Biotech Valuation Methods',
      description: 'Valuing pre-revenue biotech companies.',
      commands: ['biotech', 'healthcare', 'pipeline', 'pharma'],
      steps: [
        { instruction: 'Value a biotech pipeline: `biotech --rNPV --drug "ALZ-101" --phase "Phase 2" --probability 0.45 --peak-sales 2000000000 --launch-year 2028`', command: 'biotech --rNPV --drug "ALZ-101" --phase "Phase 2" --probability 0.45 --peak-sales 2000000000 --launch-year 2028', expectedOutput: 'rNPV for ALZ-101: $450M. Probability-adjusted peak sales: $900M. Phase 2 success rate: 45%. Discount rate: 12%. Time to market: 3 years. Risk-adjusted value: $450M' },
        { instruction: 'rNPV (risk-adjusted Net Present Value) is the standard for biotech valuation.' },
        { instruction: 'The cat biotech portfolio includes a gene therapy for hairball reduction — high risk, high reward.' },
      ],
      quiz: [
        { question: 'What is the probability of success for a drug entering Phase 2 clinical trials?', options: ['Approximately 30-45% success rate for advancing to Phase 3', '90% success rate', '5% success rate', '100% success rate'], correctIndex: 0, explanation: 'Drugs entering Phase 2 trials have roughly a 30-45% probability of eventually reaching the market, with significant attrition at each stage.' },
      ],
    },
    {
      id: 'pipeline-analysis',
      slug: 'drug-pipeline-analysis',
      title: 'Drug Pipeline Analysis',
      description: 'Analyzing pharmaceutical development pipelines.',
      commands: ['pipeline', 'biotech', 'pharma'],
      steps: [
        { instruction: 'Analyze pharma pipeline: `pipeline --analyze --company "Pfizer" --therapy-area oncology,immunology`', command: 'pipeline --analyze --company "Pfizer" --therapy-area oncology,immunology', expectedOutput: 'Pfizer pipeline: 95 programs (oncology 45, immunology 22, rare disease 15, vaccines 13). Phase 3: 8. NMEs: 12. Expected launches next 18mo: 3 (combined peak sales $8B)' },
        { instruction: 'Pipeline analysis evaluates the quantity, quality, and commercial potential of drug candidates.' },
        { instruction: 'The cat analyzed the feline medicine pipeline — there is a promising new catnip formulation.' },
      ],
      quiz: [
        { question: 'What is an NME (New Molecular Entity) in pharmaceutical pipelines?', options: ['A novel chemical compound not previously approved for any indication', 'A new marketing executive', 'A new manufacturing equipment', 'A new medical equipment'], correctIndex: 0, explanation: 'An NME is a drug containing a new chemical compound that has never been approved for any medical use, representing genuine innovation.' },
      ],
    },
    {
      id: 'pharma-economics',
      slug: 'pharmaceutical-economics',
      title: 'Pharmaceutical Economics',
      description: 'Understanding drug pricing and market dynamics.',
      commands: ['pharma', 'healthcare', 'pipeline'],
      steps: [
        { instruction: 'Analyze drug pricing model: `pharma --pricing --drug "Humira" --market US --competition 5 biosimilars`', command: 'pharma --pricing --drug "Humira" --market US --competition 5 biosimilars', expectedOutput: 'Humira US pricing: $80K/year list price. Net price after rebates: $45K (44% discount). Biosimilar erosion: -55% market share to biosimilars. 5 competitors in market' },
        { instruction: 'Drug pricing involves complex rebate and discount structures between manufacturers and payers.' },
        { instruction: 'The cat prescription catnip pricing involves similar rebates — but the cat pays in purrs.' },
      ],
      quiz: [
        { question: 'What is a biosimilar?', options: ['A nearly identical copy of an approved biologic drug, similar to a generic for small-molecule drugs', 'A similar chemical compound', 'A cheaper version of a vaccine', 'A new drug category'], correctIndex: 0, explanation: 'Biosimilars are highly similar versions of approved biologic drugs that enter the market after patent expiration, offering lower-cost alternatives.' },
      ],
    },
    {
      id: 'healthcare-investing',
      slug: 'healthcare-investing-strategies',
      title: 'Healthcare Investing Strategies',
      description: 'Building a healthcare-focused investment portfolio.',
      commands: ['healthcare', 'biotech', 'pharma'],
      steps: [
        { instruction: 'Build a healthcare allocation: `healthcare --allocate --capital 100000 --segments "pharma:40,biotech:25,medtech:20,healthcare-services:15"`', command: 'healthcare --allocate --capital 100000 --segments "pharma:40,biotech:25,medtech:20,healthcare-services:15"', expectedOutput: 'Healthcare portfolio: $40K pharma (12% CAGR, 15% vol), $25K biotech (18% CAGR, 35% vol), $20K medtech (10%, 18%), $15K services (8%, 12%)' },
        { instruction: 'Healthcare investing spans pharma, biotech, medtech, and services subsectors.' },
        { instruction: 'The cat healthcare portfolio is overweight veterinary stocks — insider knowledge.' },
      ],
      quiz: [
        { question: 'Why does biotech typically have higher volatility than pharma?', options: ['Biotech companies are smaller, pre-revenue, and driven by binary clinical trial outcomes', 'Biotech has lower margins', 'Biotech is less regulated', 'Biotech companies have more cash'], correctIndex: 0, explanation: 'Biotech stocks exhibit higher volatility because many are pre-revenue and their valuations swing dramatically on clinical trial results and FDA decisions.' },
      ],
    },
  ],
}
