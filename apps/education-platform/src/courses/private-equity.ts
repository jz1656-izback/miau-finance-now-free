import type { Course } from '../lib/types'

export const privateEquity: Course = {
  id: 'private-equity',
  slug: 'private-equity',
  title: 'Private Equity & VC',
  description: 'PE fund structure, LBOs, carried interest, and venture valuation — the cat hunts returns.',
  category: 'Alternative Investments',
  difficulty: 'advanced',
  icon: '💎',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'pe-structure',
      slug: 'fund-structure',
      title: 'PE Fund Structure',
      description: 'How private equity funds are organized.',
      commands: ['pe', 'pe structure'],
      steps: [
        { instruction: 'View PE fund structure: `pe structure`', command: 'pe structure', expectedOutput: 'Diagram of GP/LP fund structure with fee breakdown' },
        { instruction: 'Limited Partners (LPs) provide capital. General Partners (GPs) manage the fund.' },
        { instruction: 'Typical fee structure: 2% management fee and 20% carried interest.' },
      ],
      quiz: [
        { question: 'Who manages a private equity fund?', options: ['General Partner (GP)', 'Limited Partner (LP)', 'The government', 'The bank'], correctIndex: 0, explanation: 'The General Partner (GP) manages the fund\'s investments and operations, while LPs are passive investors.' },
      ],
    },
    {
      id: 'pe-lbo',
      slug: 'leveraged-buyouts',
      title: 'Leveraged Buyouts (LBOs)',
      description: 'Buying companies using borrowed money.',
      commands: ['pe lbo', 'pe lbo model'],
      steps: [
        { instruction: 'Run an LBO model: `pe lbo model --ebitda 100M --multiple 8x --debt 500M`', command: 'pe lbo model --ebitda 100M --multiple 8x --debt 500M', expectedOutput: 'LBO returns analysis with IRR and MOIC' },
        { instruction: 'In an LBO, 60-70% of the purchase price is typically funded with debt.' },
        { instruction: 'The target company\'s cash flows pay down the debt over time.' },
      ],
      quiz: [
        { question: 'What does LBO stand for?', options: ['Leveraged Buyout', 'Limited Buyout Option', 'Large Business Operation', 'Liability Buyout'], correctIndex: 0, explanation: 'LBO stands for Leveraged Buyout — acquiring a company primarily with borrowed money.' },
      ],
    },
    {
      id: 'pe-carried',
      slug: 'carried-interest',
      title: 'Carried Interest',
      description: 'How PE managers get paid — the 20% carry.',
      commands: ['pe carry', 'pe carry calc'],
      steps: [
        { instruction: 'Calculate carried interest: `pe carry calc --fund 500M --return 2x`', command: 'pe carry calc --fund 500M --return 2x', expectedOutput: 'Carried interest calculation with GP/LP waterfall' },
        { instruction: 'Carried interest is the GP\'s share of profits, typically 20% above a hurdle rate.' },
        { instruction: 'The hurdle rate (usually 8%) must be achieved before the GP receives carry.' },
      ],
      quiz: [
        { question: 'What is typical carried interest in PE?', options: ['20% of profits', '2% of assets', '30% of profits', '10% of profits'], correctIndex: 0, explanation: 'Standard carried interest is 20% of profits above the hurdle rate, aligning GP and LP interests.' },
      ],
    },
    {
      id: 'pe-venture',
      slug: 'venture-valuation',
      title: 'Venture Capital Valuation',
      description: 'How VCs value early-stage companies.',
      commands: ['vc', 'vc valuation'],
      steps: [
        { instruction: 'Run a VC valuation: `vc valuation --revenue 5M --growth 100 --market 50B`', command: 'vc valuation --revenue 5M --growth 100 --market 50B', expectedOutput: 'VC valuation with revenue multiple and market comparison' },
        { instruction: 'VCs use scorecard, venture capital method, and comparable analysis for startups.' },
        { instruction: 'Term sheets outline valuation, liquidation preferences, and board seats.' },
      ],
      quiz: [
        { question: 'What is a liquidation preference in VC?', options: ['Investors get paid before common shareholders in an exit', 'The company must liquidate assets', 'A tax preference for startups', 'The order of hiring'], correctIndex: 0, explanation: 'Liquidation preference ensures VCs get their investment back before common shareholders receive any proceeds.' },
      ],
    },
  ],
}
