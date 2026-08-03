import type { Course } from '../lib/types'

export const assetAllocation: Course = {
  id: 'asset-allocation',
  slug: 'asset-allocation-strategies',
  title: 'Asset Allocation',
  description: 'Strategic, tactical, dynamic allocation, and risk budgeting — the cat allocates its energy between napping, eating, and knocking things off tables.',
  category: 'Portfolio Management',
  difficulty: 'intermediate',
  icon: '🎯',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'strategic-allocation',
      slug: 'strategic-asset-allocation',
      title: 'Strategic Asset Allocation',
      description: 'Long-term target portfolio weights.',
      commands: ['allocation', 'strategic'],
      steps: [
        { instruction: 'Set strategic allocation: `strategic --allocate --risk-profile "moderate" --time-horizon 20`', command: 'strategic --allocate --risk-profile "moderate" --time-horizon 20', expectedOutput: 'Strategic allocation (moderate, 20yr): 55% equities (35% US, 15% intl, 5% EM), 30% bonds, 10% alternatives, 5% cash. Expected return: 7.2%, vol: 11.5%' },
        { instruction: 'Strategic asset allocation sets long-term target weights based on risk tolerance.' },
        { instruction: 'The cat strategic allocation is 60% nap time, 30% eating, 10% supervised awake hours.' },
      ],
      quiz: [
        { question: 'What is strategic asset allocation?', options: ['Setting long-term target portfolio weights based on risk tolerance and investment horizon', 'Daily portfolio rebalancing', 'Timing the market based on forecasts', 'Investing all assets in one security'], correctIndex: 0, explanation: 'Strategic asset allocation establishes fixed, long-term portfolio weights across asset classes aligned with the investor risk tolerance and goals.' },
      ],
    },
    {
      id: 'tactical-allocation',
      slug: 'tactical-asset-allocation',
      title: 'Tactical Asset Allocation',
      description: 'Short-term deviations from strategic targets.',
      commands: ['tactical', 'allocation'],
      steps: [
        { instruction: 'Generate tactical overlay: `tactical --overlay --strategic-weights "equities:60,bonds:40" --market-view "overweight-equities" --conviction 0.7`', command: 'tactical --overlay --strategic-weights "equities:60,bonds:40" --market-view "overweight-equities" --conviction 0.7', expectedOutput: 'Tactical overlay: Equities +5% (to 65%), Bonds -5% (to 35%). Reason: Strong economic momentum, easing Fed. Conviction: 70%. Tracking error: 1.5%' },
        { instruction: 'Tactical allocation involves short-term deviations from strategic weights based on market views.' },
        { instruction: 'The cat made a tactical decision to move from the couch to the sunny spot with higher expected return.' },
      ],
      quiz: [
        { question: 'What distinguishes tactical asset allocation from strategic asset allocation?', options: ['Tactical is short-term deviations from long-term targets based on market conditions', 'Tactical is long-term only', 'Tactical ignores market conditions', 'Tactical only applies to bonds'], correctIndex: 0, explanation: 'Tactical asset allocation makes shorter-term adjustments away from strategic targets to capitalize on perceived market opportunities.' },
      ],
    },
    {
      id: 'dynamic-allocation',
      slug: 'dynamic-asset-allocation',
      title: 'Dynamic Asset Allocation',
      description: 'Continuously adjusting to changing conditions.',
      commands: ['allocation', 'tactical'],
      steps: [
        { instruction: 'Run dynamic allocation model: `allocation --dynamic --signal "risk-on" --volatility-target 0.15`', command: 'allocation --dynamic --signal "risk-on" --volatility-target 0.15', expectedOutput: 'Dynamic allocation (risk-on): Equities 70%, bonds 15%, gold 10%, crypto 5%. Expected vol: 14.8%. VaR (95%): -3.2%. Rebalance trigger: vol > 16%' },
        { instruction: 'Dynamic allocation continuously adjusts portfolio weights based on market conditions.' },
        { instruction: 'The cat dynamic allocation adjusts between sunny spots and warm radiators based on temperature.' },
      ],
      quiz: [
        { question: 'How does dynamic asset allocation differ from tactical?', options: ['Dynamic uses continuous rule-based adjustments rather than discrete tactical tilts', 'Dynamic is the same as strategic', 'Dynamic only applies to fixed income', 'Dynamic allocation does not use rules'], correctIndex: 0, explanation: 'Dynamic asset allocation involves continuous systematic adjustments based on predefined rules or models.' },
      ],
    },
    {
      id: 'risk-budgeting',
      slug: 'risk-budgeting-portfolio',
      title: 'Risk Budgeting & Parity',
      description: 'Allocating risk rather than capital.',
      commands: ['risk-budget', 'allocation'],
      steps: [
        { instruction: 'Calculate risk contribution: `risk-budget --calculate --portfolio "equities:60,bonds:40" --volatilities "equities:0.16,bonds:0.06" --correlation 0.2`', command: 'risk-budget --calculate --portfolio "equities:60,bonds:40" --volatilities "equities:0.16,bonds:0.06" --correlation 0.2', expectedOutput: 'Risk contributions: Equities 60% allocation gets 89% of risk. Bonds 40% gets 11% of risk. Risk parity would require equities 23% bonds 77%' },
        { instruction: 'Risk budgeting allocates portfolio risk rather than capital across asset classes.' },
        { instruction: 'The cat risk budget is 90% from the unpredictability of the red dot movement.' },
      ],
      quiz: [
        { question: 'What is the key insight of risk budgeting?', options: ['Capital allocation does not equal risk allocation each asset risk contribution should be measured', 'All assets have equal risk', 'Risk can be eliminated through diversification alone', 'Risk budgeting ignores correlations'], correctIndex: 0, explanation: 'Risk budgeting recognizes that the percentage of capital allocated to an asset differs from its percentage contribution to total portfolio risk.' },
      ],
    },
  ],
}
