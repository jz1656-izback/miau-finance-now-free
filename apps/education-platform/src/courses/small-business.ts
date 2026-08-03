import type { Course } from '../lib/types'

export const smallBusinessFinance: Course = {
  id: 'small-business-finance',
  slug: 'small-business-finance',
  title: 'Small Business Finance',
  description: 'Startup funding, cash flow management, and business valuation — the cat runs a small catnip empire and needs to manage its finances.',
  category: 'Business Finance',
  difficulty: 'intermediate',
  icon: '🏪',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'startup-funding',
      slug: 'startup-funding-sources',
      title: 'Startup Funding Sources',
      description: 'Understanding funding options for new businesses.',
      commands: ['startup', 'business-plan'],
      steps: [
        { instruction: 'Explore funding options: `startup --funding --type "bootstrapping vs angel vs vc" --amount-needed 250000`', command: 'startup --funding --type "bootstrapping vs angel vs vc" --amount-needed 250000', expectedOutput: 'Funding comparison: Bootstrapping (0% dilution, slow growth), Angel ($25K-100K, 10-20% equity), VC ($500K+, 20-40% equity, board control)' },
        { instruction: 'Each funding source comes with different trade-offs between capital, control, and dilution.' },
        { instruction: 'The cat bootstrapped its catnip business — no investors, just pure feline entrepreneurship.' },
      ],
      quiz: [
        { question: 'What is the main trade-off when accepting venture capital funding?', options: ['Capital and expertise in exchange for equity dilution and board control', 'No strings attached capital', 'Guaranteed profits', 'Free marketing'], correctIndex: 0, explanation: 'VC funding provides capital and strategic support but requires giving up equity, board seats, and some control over business decisions.' },
      ],
    },
    {
      id: 'business-cashflow',
      slug: 'small-business-cashflow',
      title: 'Cash Flow Management for Business',
      description: 'Keeping your business solvent with proper cash flow.',
      commands: ['cashflow', 'business-plan'],
      steps: [
        { instruction: 'Project business cash flow: `cashflow --project --revenue 50000 --expenses 35000 --receivables-avg 30 --payables-avg 45`', command: 'cashflow --project --revenue 50000 --expenses 35000 --receivables-avg 30 --payables-avg 45', expectedOutput: 'Monthly cash flow: +$15K operating. Cash conversion cycle: 55 days (inventory 40 + receivables 30 - payables 15). Working capital needed: $27,500' },
        { instruction: 'Cash is king in small business — profit does not equal cash in the bank.' },
        { instruction: 'The cat learned about cash flow the hard way: lots of catnip sales on credit but no cash for tuna.' },
      ],
      quiz: [
        { question: 'What is the cash conversion cycle?', options: ['The time between paying suppliers and collecting cash from customers', 'The time to convert cash to inventory and back to cash', 'The monthly accounting period', 'The time to process payments'], correctIndex: 0, explanation: 'The cash conversion cycle measures how long cash is tied up in operations from paying suppliers to collecting from customers.' },
      ],
    },
    {
      id: 'business-valuation',
      slug: 'small-business-valuation',
      title: 'Small Business Valuation',
      description: 'Methods for valuing a small business.',
      commands: ['valuation', 'business-plan'],
      steps: [
        { instruction: 'Value a small business: `valuation --small-biz --revenue 500000 --ebitda 120000 --industry "retail" --growth 0.05`', command: 'valuation --small-biz --revenue 500000 --ebitda 120000 --industry "retail" --growth 0.05', expectedOutput: 'Valuation range: $600K-$840K (5-7x EBITDA). Market comps: 1.2-1.8x revenue. DCF value: $720K (10% WACC, 3% terminal growth)' },
        { instruction: 'Small businesses are often valued on EBITDA multiples or revenue multiples.' },
        { instruction: 'The cat catnip business is valued at 8x EBITDA — premium for the purr factor.' },
      ],
      quiz: [
        { question: 'What is the most common valuation multiple for small businesses?', options: ['EBITDA multiple (typically 3-8x depending on industry and size)', 'Price-to-earnings ratio', 'Book value multiple', 'Dividend yield'], correctIndex: 0, explanation: 'Small businesses are most commonly valued using EBITDA multiples, with typical ranges of 3-8x depending on industry, size, and growth.' },
      ],
    },
    {
      id: 'business-plan',
      slug: 'business-plan-writing',
      title: 'Business Planning & Strategy',
      description: 'Creating a business plan for success.',
      commands: ['business-plan', 'startup'],
      steps: [
        { instruction: 'Create a business plan outline: `business-plan --create --name "Catnip Delights" --industry "pet-supplies" --funding 50000`', command: 'business-plan --create --name "Catnip Delights" --industry "pet-supplies" --funding 50000', expectedOutput: 'Business plan: Executive summary, company description, market analysis ($2B catnip market, 8% CAGR), product line, marketing strategy, financial projections ($120K Y1 revenue, 35% margin)' },
        { instruction: 'A business plan outlines the strategy, market, and financial projections for a business.' },
        { instruction: 'The cat business plan for "Catnip Delights" was written entirely in paw prints — investors were confused.' },
      ],
      quiz: [
        { question: 'What are the key components of a business plan?', options: ['Executive summary, market analysis, product/service, marketing, financial projections, team', 'Only financial projections', 'Only marketing strategy', 'Only product description'], correctIndex: 0, explanation: 'A comprehensive business plan includes executive summary, market analysis, product description, marketing strategy, financial projections, and management team.' },
      ],
    },
  ],
}
