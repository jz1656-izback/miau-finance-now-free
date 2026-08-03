import type { Course } from '../lib/types'

export const iposAndSpacs: Course = {
  id: 'ipos-and-spacs',
  slug: 'ipos-and-spacs',
  title: 'IPOs & SPACs',
  description: 'IPO process, SPAC structure, and blank check companies — the cat takes companies public.',
  category: 'Capital Markets',
  difficulty: 'intermediate',
  icon: '🚀',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'ipo-process',
      slug: 'ipo-process',
      title: 'The IPO Process',
      description: 'How a private company goes public.',
      commands: ['ipo', 'ipo process'],
      steps: [
        { instruction: 'Walk through an IPO: `ipo process --company "TechCo"`', command: 'ipo process --company "TechCo"', expectedOutput: 'IPO timeline: filing, roadshow, pricing, and listing' },
        { instruction: 'The company files an S-1 with the SEC, disclosing financials and risks.' },
        { instruction: 'Underwriters (investment banks) help price and sell the shares to investors.' },
      ],
      quiz: [
        { question: 'What is the S-1 filing?', options: ['The registration document filed with the SEC for an IPO', 'The final stock price', 'The underwriting agreement', 'The shareholder vote'], correctIndex: 0, explanation: 'The S-1 is a registration statement filed with the SEC that discloses the company\'s financials, business model, and risks before an IPO.' },
      ],
    },
    {
      id: 'ipo-pricing',
      slug: 'ipo-pricing',
      title: 'IPO Pricing & Allocation',
      description: 'How IPO price is set and shares are allocated.',
      commands: ['ipo pricing', 'ipo bookbuilding'],
      steps: [
        { instruction: 'Simulate IPO pricing: `ipo bookbuilding --demand 10B --shares 20M`', command: 'ipo bookbuilding --demand 10B --shares 20M', expectedOutput: 'Bookbuilding results showing demand at various price levels' },
        { instruction: 'The underwriter builds a book of investor orders to gauge demand.' },
        { instruction: 'The final price is set the night before listing based on demand.' },
      ],
      quiz: [
        { question: 'What is bookbuilding in an IPO?', options: ['Gathering investor orders to determine demand and price', 'Writing the prospectus', 'Building the company website', 'Constructing the exchange listing'], correctIndex: 0, explanation: 'Bookbuilding is the process where underwriters collect indications of interest from institutional investors to price the IPO.' },
      ],
    },
    {
      id: 'spac-structure',
      slug: 'spac-structure',
      title: 'SPAC Structure',
      description: 'Blank check companies and the SPAC merger process.',
      commands: ['spac', 'spac process'],
      steps: [
        { instruction: 'Analyze a SPAC: `spac process --ticker SPAC-X`', command: 'spac process --ticker SPAC-X', expectedOutput: 'SPAC structure: trust, sponsors, warrants, and merger timeline' },
        { instruction: 'A SPAC raises money in an IPO with no target — it must find one within 2 years.' },
        { instruction: 'If no deal is found, the trust is returned to shareholders.' },
      ],
      quiz: [
        { question: 'What happens if a SPAC does not find a target?', options: ['The trust is returned to shareholders', 'The SPAC converts to an operating company', 'Shareholders lose everything', 'The SEC extends the deadline'], correctIndex: 0, explanation: 'If a SPAC cannot complete a merger within its timeframe (typically 2 years), the funds in trust are returned to shareholders.' },
      ],
    },
    {
      id: 'spac-merger',
      slug: 'spac-merger-deal',
      title: 'SPAC Mergers & De-SPAC',
      description: 'How a SPAC merges with a target company.',
      commands: ['prospectus', 'prospectus read'],
      steps: [
        { instruction: 'Analyze a de-SPAC transaction: `spac merger --target "EV-Startup" --valuation 5B`', command: 'spac merger --target "EV-Startup" --valuation 5B', expectedOutput: 'De-SPAC analysis with dilution, redemptions, and pro-forma value' },
        { instruction: 'Shareholders can redeem their shares before the merger vote.' },
        { instruction: 'SPAC warrants give holders the right to buy more shares at a fixed price.' },
      ],
      quiz: [
        { question: 'What is a de-SPAC transaction?', options: ['The merger between a SPAC and its target company', 'The SPAC IPO process', 'The liquidation of a SPAC', 'The warrant exercise period'], correctIndex: 0, explanation: 'A de-SPAC transaction is the business combination where a SPAC merges with a private company to take it public.' },
      ],
    },
  ],
}
