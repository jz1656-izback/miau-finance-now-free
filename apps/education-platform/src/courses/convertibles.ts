import type { Course } from '../lib/types'

export const convertibles: Course = {
  id: 'convertibles',
  slug: 'convertible-bonds-warrants',
  title: 'Convertible Bonds & Warrants',
  description: 'Convertible valuation, conversion premium, and warrant trading — the cat converts its tuna bonds into equity for the ultimate seafood portfolio.',
  category: 'Advanced Finance',
  difficulty: 'advanced',
  icon: '🔄',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'convertible-basics',
      slug: 'convertible-bond-fundamentals',
      title: 'Convertible Bond Fundamentals',
      description: 'Understanding convertible bond structures.',
      commands: ['convertible', 'conversion'],
      steps: [
        { instruction: 'Analyze a convertible bond: `convertible --analyze --ticker TSLA --issue-date 2024 --maturity 2029`', command: 'convertible --analyze --ticker TSLA --issue-date 2024 --maturity 2029', expectedOutput: 'TSLA 0.25% 2029: $2B issue, 0.25% coupon, conversion ratio 1.2, conversion price $833.33, 5yr maturity, callable after year 3' },
        { instruction: 'A convertible bond can be exchanged for a fixed number of shares of the issuer.' },
        { instruction: 'The cat bought a convertible bond — if the stock goes up, the cat gets shares. If not, the cat keeps the bond and buys tuna anyway.' },
      ],
      quiz: [
        { question: 'What is a convertible bond?', options: ['A bond that can be converted into a predetermined number of shares of the issuer', 'A bond that converts from fixed to floating rate', 'A bond that matures early', 'A bond that pays interest in stock'], correctIndex: 0, explanation: 'A convertible bond gives the holder the right to convert the bond into a specified number of common shares of the issuing company.' },
      ],
    },
    {
      id: 'conversion-premium',
      slug: 'conversion-premium-analysis',
      title: 'Conversion Premium & Parity',
      description: 'Calculating conversion premium and parity value.',
      commands: ['convertible', 'conversion', 'parity'],
      steps: [
        { instruction: 'Calculate conversion premium: `convertible --premium --bond-price 1200 --parity 1100`', command: 'convertible --premium --bond-price 1200 --parity 1100', expectedOutput: 'Conversion premium: (1200 - 1100) / 1100 = 9.09%. Parity value: $1,100. Bond price: $1,200. Premium above parity: 9.09%' },
        { instruction: 'Conversion premium measures how much extra you pay for the bond vs. the conversion value.' },
        { instruction: 'The cat calculated a 9% premium and decided the conversion feature was worth the extra kibble.' },
      ],
      quiz: [
        { question: 'What does the conversion premium measure?', options: ['The percentage by which the bond price exceeds its conversion value', 'The interest rate premium over Treasuries', 'The premium paid for early conversion', 'The premium of the stock over the bond'], correctIndex: 0, explanation: 'Conversion premium measures how much more an investor pays for the convertible bond compared to its conversion value (the value if converted immediately).' },
      ],
    },
    {
      id: 'warrant-trading',
      slug: 'warrant-trading-strategies',
      title: 'Warrant Trading & Strategies',
      description: 'Understanding warrants and their differences from options.',
      commands: ['warrant', 'convertible'],
      steps: [
        { instruction: 'Analyze a warrant: `warrant --analyze --ticker GME --strike 20 --expiry 2028 --warrant-price 8`', command: 'warrant --analyze --ticker GME --strike 20 --expiry 2028 --warrant-price 8', expectedOutput: 'GME warrant: Strike $20, expires 2028, warrant price $8. Stock $28 — intrinsic value $8, time value $0. At $22 — intrinsic $2, time value $6' },
        { instruction: 'Warrants are issued by the company and typically have longer maturities than options.' },
        { instruction: 'The cat bought warrants — it likes the stock, and the warrants are like catnip for leverage.' },
        { instruction: 'Compare warrants vs options: `warrant --compare --type warrants,options --tenor 2yr`', command: 'warrant --compare --type warrants,options --tenor 2yr', expectedOutput: 'Warrants: Company-issued, 2-5yr tenor, dilutive, OTC. Options: Exchange-traded, <2yr tenor, non-dilutive, standardized' },
      ],
      quiz: [
        { question: 'How do warrants differ from exchange-traded options?', options: ['Warrants are issued by the company and are dilutive; options are standardized contracts', 'Warrants have shorter maturities', 'Warrants never have a strike price', 'There is no difference'], correctIndex: 0, explanation: 'Warrants are issued directly by the company and create new shares upon exercise (dilution), while options are standardized contracts between third parties.' },
      ],
    },
    {
      id: 'convertible-arbitrage',
      slug: 'convertible-arbitrage-strategies',
      title: 'Convertible Arbitrage',
      description: 'Hedging and arbitrage strategies with convertibles.',
      commands: ['convertible', 'arb'],
      steps: [
        { instruction: 'Model a convertible arbitrage trade: `convertible --arb --bond-price 105 --delta 0.75 --stock-price 50 --shares-per-bond 20`', command: 'convertible --arb --bond-price 105 --delta 0.75 --stock-price 50 --shares-per-bond 20', expectedOutput: 'Convertible arb: Buy $1.05M bond, short 15,000 shares ($750K). Delta-neutral hedge — profit from mispricing and carry. Target return: 8-12% annualized' },
        { instruction: 'Convertible arbitrage involves buying the bond and shorting the stock to capture mispricing.' },
        { instruction: 'The cat set up a convertible arb trade — it\'s now a hedge fund cat with a bow tie.' },
      ],
      quiz: [
        { question: 'What is the basic premise of convertible arbitrage?', options: ['Buy the convertible bond and short the underlying stock to capture pricing inefficiencies', 'Short the bond and buy the stock', 'Buy both the bond and stock', 'Trade options on the convertible'], correctIndex: 0, explanation: 'Convertible arbitrage exploits mispricing between a convertible bond and the underlying stock by going long the bond and short the stock to achieve a delta-neutral position.' },
      ],
    },
  ],
}
