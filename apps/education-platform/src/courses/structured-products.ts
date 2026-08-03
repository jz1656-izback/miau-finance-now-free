import type { Course } from '../lib/types'

export const structuredProducts: Course = {
  id: 'structured-products',
  slug: 'structured-products-strategies',
  title: 'Structured Products',
  description: 'Principal-protected notes, autocallables, and reverse convertibles — structured like a cat tower, complex but rewarding.',
  category: 'Advanced Finance',
  difficulty: 'advanced',
  icon: '🧩',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'structured-product-basics',
      slug: 'structured-product-fundamentals',
      title: 'Structured Product Fundamentals',
      description: 'Understanding structured product components.',
      commands: ['structured', 'ppn'],
      steps: [
        { instruction: 'Explore structured product types: `structured --types --list`', command: 'structured --types --list', expectedOutput: 'Types: Principal-Protected Notes (PPN), Autocallables, Reverse Convertibles, Capital-at-Risk Notes, Participation Notes' },
        { instruction: 'A structured product combines a bond with a derivative to create specific payoff profiles.' },
        { instruction: 'The cat tried to understand structured products — it got confused and knocked the keyboard off the desk.' },
        { instruction: 'Analyze a PPN structure: `ppn --analyze --principal 100000 --participation 0.8 --cap 1.5 --maturity 5`', command: 'ppn --analyze --principal 100000 --participation 0.8 --cap 1.5 --maturity 5', expectedOutput: 'PPN: $100K principal 100% protected. 80% participation in S&P 500 upside, capped at 50%. Best case: $150K. Worst case: $100K (principal returned)' },
      ],
      quiz: [
        { question: 'What is a principal-protected note (PPN)?', options: ['A structured product that guarantees the return of principal at maturity with variable upside', 'A type of insurance policy', 'A zero-coupon bond', 'A leveraged ETF'], correctIndex: 0, explanation: 'A PPN guarantees the full return of the initial investment at maturity while offering participation in the upside of an underlying asset.' },
      ],
    },
    {
      id: 'autocallables',
      slug: 'autocallable-structured-products',
      title: 'Autocallable Notes',
      description: 'Understanding autocallable structured products.',
      commands: ['autocall', 'structured'],
      steps: [
        { instruction: 'Model an autocallable: `autocall --model --underlying SPX --coupon 0.08 --barrier 0.7 --tenor 3`', command: 'autocall --model --underlying SPX --coupon 0.08 --barrier 0.7 --tenor 3', expectedOutput: 'Autocallable: 3yr tenor, 8% annual coupon, autocall trigger 100%, downside barrier 70%. Called automatically if SPX at 100%+ on observation dates' },
        { instruction: 'Autocallables are automatically redeemed if the underlying asset is at or above a trigger level.' },
        { instruction: 'The cat\'s autocallable note autocalled early — it spent the profit on a new feather wand.' },
      ],
      quiz: [
        { question: 'What triggers an autocallable note to redeem early?', options: ['The underlying asset reaches or exceeds a predetermined trigger level on an observation date', 'The investor requests redemption', 'The note reaches its coupon payment date', 'The underlying asset pays a dividend'], correctIndex: 0, explanation: 'Autocallable notes are automatically redeemed when the underlying asset closes at or above a predetermined trigger level on a scheduled observation date.' },
      ],
    },
    {
      id: 'reverse-convertibles',
      slug: 'reverse-convertible-notes',
      title: 'Reverse Convertibles',
      description: 'Understanding reverse convertible structures and risks.',
      commands: ['reverse-convertible', 'structured'],
      steps: [
        { instruction: 'Analyze a reverse convertible: `reverse-convertible --analyze --underlying AAPL --coupon 0.12 --barrier 0.8 --tenor 1`', command: 'reverse-convertible --analyze --underlying AAPL --coupon 0.12 --barrier 0.8 --tenor 1', expectedOutput: 'Reverse Convertible: 1yr, 12% coupon, barrier 80%. If AAPL stays above $180 (80% barrier): full principal + 12% returned. If below: receive shares worth $180K instead of $100K cash' },
        { instruction: 'Reverse convertibles pay high coupons but risk converting into shares if the underlying falls.' },
        { instruction: 'The cat\'s reverse convertible paid 12% — then the stock dropped and the cat got shares instead of tuna.' },
      ],
      quiz: [
        { question: 'What happens if the underlying asset falls below the barrier in a reverse convertible?', options: ['The investor receives shares instead of cash at maturity', 'The investor loses all principal', 'The coupon payment stops', 'The note converts to a bond'], correctIndex: 0, explanation: 'If the underlying breaches the barrier, the reverse convertible delivers physical shares instead of cash, exposing the investor to downside.' },
      ],
    },
    {
      id: 'structured-product-risks',
      slug: 'structured-product-risk-analysis',
      title: 'Structured Product Risks & Pricing',
      description: 'Assessing risks and fair pricing of structured products.',
      commands: ['structured', 'autocall'],
      steps: [
        { instruction: 'Calculate structured product fair value: `structured --price --type autocallable --parameters "vol:0.20,rates:0.05,div:0.02"`', command: 'structured --price --type autocallable --parameters "vol:0.20,rates:0.05,div:0.02"', expectedOutput: 'Fair value: 98.5% of par — implied issuer margin: 1.5%. Monte Carlo simulation: 65% probability of autocall in year 1, 85% by year 3' },
        { instruction: 'Structured products often embed issuer fees that reduce investor returns.' },
        { instruction: 'The cat calculated the fair value — then realized the issuer was making more than the cat.' },
      ],
      quiz: [
        { question: 'What is a key risk factor when investing in structured products?', options: ['Issuer credit risk — the bank could default, and the product is unsecured', 'Market open risk', 'Currency conversion risk', 'Inflation risk only'], correctIndex: 0, explanation: 'Structured products are unsecured obligations of the issuing bank, so investors face credit risk of the issuer defaulting.' },
      ],
    },
  ],
}
