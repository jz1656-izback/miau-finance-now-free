import type { Course } from '../lib/types'

export const vcAngelInvesting: Course = {
  id: 'vc-angel-investing',
  slug: 'vc-angel-investing',
  title: 'VC & Angel Investing',
  description: 'Term sheets, cap tables, dilution, valuation, and exit strategies — the cat invests in the next big thing.',
  category: 'Investing',
  difficulty: 'intermediate',
  icon: '🦄',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'vc-basics',
      slug: 'venture-capital-basics',
      title: 'Venture Capital Fundamentals',
      description: 'Understanding VC stages, players, and economics.',
      commands: ['vc stages', 'vc landscape'],
      steps: [
        { instruction: 'Explore VC stages: `vc stages --overview`', command: 'vc stages --overview', expectedOutput: 'VC stages: Pre-seed ($500K-1M), Seed ($1M-5M), Series A ($5M-15M), Series B ($15M-50M), Growth ($50M+). Median ownership: Angel 10%, Seed 20%, Series A 25%, Series B 20%' },
        { instruction: 'VCs provide capital, connections, and expertise in exchange for equity.' },
        { instruction: 'The cat is a scout investor for Sequoia. Its deal flow is 100% catnip startups.' },
        { instruction: 'Check current VC landscape by sector: `vc landscape --sector ai`', command: 'vc landscape --sector ai', expectedOutput: 'AI VC activity Q3: Total deals $28.5B (+42% YoY). Median Series A: $12M. Top investors: A16Z, Sequoia, Index. Active subsectors: LLM infra, AI agents, vertical AI' },
      ],
      quiz: [
        { question: 'What is the typical ownership range for a Series A investor in a VC round?', options: ['15-25% of the company in exchange for $5-15M investment', '50-60% to gain control', 'Less than 5%', '100% via acquisition'], correctIndex: 0, explanation: 'Series A investors typically receive 15-25% ownership for investments of $5-15M. Founders and employees are diluted but retain majority control at this stage.' },
      ],
    },
    {
      id: 'term-sheets',
      slug: 'term-sheet-negotation',
      title: 'Term Sheet Negotiation',
      description: 'Key terms in VC term sheets.',
      commands: ['vc termsheet', 'vc termsheet --simulate'],
      steps: [
        { instruction: 'Generate a standard term sheet: `vc termsheet --series "seed" --amount 2m --valuation 10m`', command: 'vc termsheet --series "seed" --amount 2m --valuation 10m', expectedOutput: 'Term sheet: Pre-money $8M, Post-money $10M. Option pool: 15%. 1x non-participating liquidation preference. Pro-rata rights. Information rights. MFN clause. No board seat' },
        { instruction: 'Key terms: valuation, liquidation preference, anti-dilution, board composition, pro-rata rights.' },
        { instruction: 'Simulate term sheet negotiation: `vc termsheet --simulate --investor "Sequoia" --founder 60% --investor 20% --option-pool 20%`', command: 'vc termsheet --simulate --investor "Sequoia" --founder 60% --investor 20% --option-pool 20%', expectedOutput: 'Negotiation outcome: Founder 55%, Investor 22%, Pool 23%. Key term: Participating preferred → non-participating (founder win). Board: 2 founders, 1 investor, 1 independent' },
        { instruction: 'The cat negotiated a term sheet that includes "unlimited tuna supply" as a board observation right.' },
      ],
      quiz: [
        { question: 'What does a "1x non-participating liquidation preference" mean for investors?', options: ['Investors get back their investment amount (1x) before common holders, but do not participate in remaining proceeds — they choose between 1x or converting to common', 'Investors get 1x their investment plus participate pro-rata in remaining proceeds', 'Investors get nothing in a liquidation', 'The company must liquidate within 1 year'], correctIndex: 0, explanation: '1x non-participating liquidation preference gives investors the choice between getting their original investment back or converting to common stock and sharing in the proceeds. They do not get both.' },
      ],
    },
    {
      id: 'cap-tables',
      slug: 'cap-table-management',
      title: 'Cap Table & Dilution',
      description: 'Managing ownership percentages across rounds.',
      commands: ['vc captable', 'vc dilution'],
      steps: [
        { instruction: 'Build a cap table: `vc captable --founders "Alice 40%, Bob 30%, Charlie 20%, Pool 10%"`', command: 'vc captable --founders "Alice 40%, Bob 30%, Charlie 20%, Pool 10%"', expectedOutput: 'Cap table: Alice 4M (40%), Bob 3M (30%), Charlie 2M (20%), Option pool 1M (10%). Total shares: 10M. Fully diluted: 10M' },
        { instruction: 'Project dilution through Series A and B: `vc dilution --round-a 5m --val-a 20m --round-b 15m --val-b 60m`', command: 'vc dilution --round-a 5m --val-a 20m --round-b 15m --val-b 60m', expectedOutput: 'After Series A ($5M at $20M post): Founders diluted to 75%. After Series B ($15M at $60M post): Founders diluted to 56.25%. Alice stake: 40% → 30% → 22.5%' },
        { instruction: 'Dilution is natural in VC — smart founders plan for 50-60% dilution from seed to exit.' },
        { instruction: 'The cat experienced 90% dilution when it accepted "equity in catnip" as compensation.' },
      ],
      quiz: [
        { question: 'What is "option pool shuffle" in VC term sheets?', options: ['The practice of creating or expanding the employee option pool before a funding round, which dilutes existing shareholders (especially founders) but not the new investor', 'A pool of investment options for venture capitalists', 'A trading strategy for options markets', 'A game VCs play during negotiations'], correctIndex: 0, explanation: 'The option pool shuffle involves creating or increasing the employee stock option pool pre-money, diluting founders and existing shareholders while the new investor ownership percentage stays fixed.' },
      ],
    },
    {
      id: 'exits',
      slug: 'exit-strategies',
      title: 'Exit Strategies & Returns',
      description: 'IPOs, acquisitions, secondary sales, and returns analysis.',
      commands: ['vc exit', 'vc ipo', 'vc returns'],
      steps: [
        { instruction: 'Check exit landscape: `vc exit --landscape --year 2025`', command: 'vc exit --landscape --year 2025', expectedOutput: '2025 exits: 142 IPOs ($45B total), 342 M&A ($120B total). Median IPO return: 22% first-day pop. Median M&A multiple: 4.2x revenue. Top sector for exits: AI/ML' },
        { instruction: 'Analyze a potential exit scenario: `vc exit --simulate --type ipo --revenue 100m --growth 40% --margin 20%`', command: 'vc exit --simulate --type ipo --revenue 100m --growth 40% --margin 20%', expectedOutput: 'IPO estimate: Revenue $100M, 40% growth, 20% margin → P/S 8x (SaaS comps) → Valuation $800M. IPO proceeds: $200M primary + $100M secondary. Lockup: 180 days' },
        { instruction: 'The cat\'s exit strategy for its catnip startup is "IPO on the New York Stock Exchange followed by a world tour."' },
        { instruction: 'Calculate VC fund returns: `vc returns --fund-size 100m --investments 20 --exit-multiple 3x`', command: 'vc returns --fund-size 100m --investments 20 --exit-multiple 3x', expectedOutput: 'Fund: $100M, 20 investments. Targets: 5 failures ($0), 10 breakeven (1x), 3 good (3x), 2 home runs (10x). Gross return: 2.15x. Net to LPs (2/20): 1.65x. Net IRR: 18%' },
      ],
      quiz: [
        { question: 'What is the typical VC fund return distribution (power law)?', options: ['Most returns come from a small number of home runs — often 60-70% of fund returns from 10% of investments', 'Returns are evenly distributed across all investments', 'All investments return approximately the same amount', 'Losses are evenly distributed across investments'], correctIndex: 0, explanation: 'VC returns follow a power law distribution: the majority of fund returns come from a small number of outlier investments. A typical fund might have 50% failures, 30% partial returns, and 20% that generate all profits.' },
      ],
    },
  ],
}
