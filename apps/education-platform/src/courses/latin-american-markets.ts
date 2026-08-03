import type { Course } from '../lib/types'

export const latinAmericanMarkets: Course = {
  id: 'latin-american-markets',
  slug: 'latin-american-markets',
  title: 'Latin American Markets',
  description: 'Bovespa, Mexico, Argentina, FX risk, and emerging market dynamics — the cat sambas with the bulls.',
  category: 'Global Markets',
  difficulty: 'intermediate',
  icon: '💃',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'brazil-markets',
      slug: 'brazil-bovespa',
      title: 'Brazil & Bovespa',
      description: 'South America largest equity market.',
      commands: ['latam brazil', 'latam brazil --index'],
      steps: [
        { instruction: 'Check Brazil market: `latam brazil --index ibovespa`', command: 'latam brazil --index ibovespa', expectedOutput: 'Ibovespa: 128,450 (+0.6%). BRL/USD: 4.95. Selic rate: 11.25%. Petrobras: +1.2%, Vale: +0.8%. Foreign flow: +$180M' },
        { instruction: 'Brazil is a commodity-driven economy — iron ore, oil, soy, beef. Also the cat loves Brazilian catnip.' },
        { instruction: 'Check sector breakdown: `latam brazil --sectors`', command: 'latam brazil --sectors', expectedOutput: 'Ibovespa sectors: Financials 25%, Materials 18%, Energy 15%, Utilities 12%, Consumer 10%, Other 20%' },
        { instruction: 'The cat tracks Brazilian real like a hawk tracks a mouse — volatile, unpredictable, fascinating.' },
      ],
      quiz: [
        { question: 'What is the Selic rate and why does it matter for Brazilian markets?', options: ['Brazil\'s benchmark interest rate — it drives bond yields, currency values, and equity valuations in the region largest economy', 'The Brazilian stock exchange trading fee', 'A tax on foreign investments', 'The minimum wage adjustment rate'], correctIndex: 0, explanation: 'The Selic is Brazil\'s benchmark interest rate set by the Central Bank. It affects everything from bond yields to currency valuation to equity risk premiums in Latin America largest economy.' },
      ],
    },
    {
      id: 'mexico-markets',
      slug: 'mexico-bmv',
      title: 'Mexico & BMV',
      description: 'Nearshoring beneficiary and US trade partner.',
      commands: ['latam mexico', 'latam mexico --index'],
      steps: [
        { instruction: 'Check Mexico market: `latam mexico --index bmv`', command: 'latam mexico --index bmv', expectedOutput: 'BMV IPC: 56,800 (+0.4%). MXN/USD: 17.20. Mexico 10Y: 9.85%. Remittances: $5.5B this month. Trade balance: +$850M' },
        { instruction: 'Mexico benefits from nearshoring as companies move production from China to North America.' },
        { instruction: 'Check nearshoring flows: `latam mexico --nearshoring --sector automotive`', command: 'latam mexico --nearshoring --sector automotive', expectedOutput: 'Nearshoring Q3: Automotive FDI +$2.1B (+35% YoY). Top investors: Tesla suppliers, BMW, KIA. New plants: 12' },
        { instruction: 'The cat is bullish on Mexico — shorter supply chains mean faster tuna delivery.' },
      ],
      quiz: [
        { question: 'What is "nearshoring" and why is Mexico a primary beneficiary?', options: ['Relocating manufacturing closer to the consumer market — Mexico benefits from US proximity and USMCA trade agreement', 'Moving factories to neighboring countries for lower wages', 'Offshoring services to nearby time zones', 'Building factories near natural resources'], correctIndex: 0, explanation: 'Nearshoring relocates production closer to end consumers. Mexico is the top beneficiary as companies move supply chains from Asia to North America, leveraging USMCA trade benefits and geographic proximity.' },
      ],
    },
    {
      id: 'argentina-markets',
      slug: 'argentina-crisis',
      title: 'Argentina & Crisis Markets',
      description: 'Navigating high-inflation, default-risk markets.',
      commands: ['latam argentina', 'latam argentina --fx'],
      steps: [
        { instruction: 'Check Argentina situation: `latam argentina --overview`', command: 'latam argentina --overview', expectedOutput: 'Merval: 1,245,000 (+2.1% in ARS, -0.3% in USD). Inflation: 143% YoY. ARS official: 850/$1. ARS blue: 1,320/$1. GDP: -2.8%' },
        { instruction: 'Argentina has parallel exchange rates (official vs "blue" market) — a classic emerging market dynamic.' },
        { instruction: 'The cat tried to understand Argentine inflation. The cat gave up and bought more tuna instead.' },
        { instruction: 'Check Argentina bond market: `latam argentina --bonds`', command: 'latam argentina --bonds', expectedOutput: 'Argentina 2030 (GD30D): 42.5c. 2035 (GD35D): 35.2c. 2041 (GD41D): 28.8c. Yields: 25-35%. Credit rating: CCC' },
      ],
      quiz: [
        { question: 'What is the "blue dollar" in Argentina?', options: ['An unofficial parallel exchange rate reflecting the market rate beyond government capital controls', 'A special currency for tourists only', 'The official central bank exchange rate', 'A digital currency issued by Argentine banks'], correctIndex: 0, explanation: 'The "dólar blue" is Argentina unofficial parallel exchange rate that trades outside government capital controls, typically reflecting a significantly weaker Argentine peso than the official rate.' },
      ],
    },
    {
      id: 'latam-risk',
      slug: 'latam-fx-risk',
      title: 'LatAm FX & Political Risk',
      description: 'Managing currency and political risk in Latin America.',
      commands: ['latam risk', 'latam hedge'],
      steps: [
        { instruction: 'Run LatAm FX risk analysis: `latam risk --fx --portfolio "BRL 5M, MXN 3M, ARS 1M"`', command: 'latam risk --fx --portfolio "BRL 5M, MXN 3M, ARS 1M"', expectedOutput: 'FX risk: BRL 5M (VaR 95%: -8.2%), MXN 3M (VaR 95%: -5.5%), ARS 1M (VaR 95%: -22%). Total VaR: -$680K. Correlation benefit: -12%' },
        { instruction: 'Latin American currencies are volatile — the BRL can move 2-3% in a single day.' },
        { instruction: 'The cat hedges FX risk by holding a diversified basket of international tuna futures.' },
        { instruction: 'Run a political risk assessment: `latam risk --political --country brazil --election-year 2026`', command: 'latam risk --political --country brazil --election-year 2026', expectedOutput: 'Brazil political risk: Medium-High. Election year 2026. Key risks: fiscal policy shift, regulatory change in oil/mining, social spending expansion. Historical volatility increase: +15% in election months' },
      ],
      quiz: [
        { question: 'What makes Latin American FX risk management particularly challenging?', options: ['High volatility combined with capital controls, parallel exchange rates, and political-driven currency swings', 'Low volatility makes it hard to trade', 'All LatAm currencies are pegged to the dollar', 'Only Brazil has FX risk'], correctIndex: 0, explanation: 'LatAm FX combines high realized volatility, frequent government capital controls, parallel market rates in some countries (Argentina, Venezuela), and political event risk that can cause sudden 10-20% devaluations.' },
      ],
    },
  ],
}
