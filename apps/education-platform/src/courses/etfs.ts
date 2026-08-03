import type { Course } from '../lib/types'

export const etfsDeepDive: Course = {
  id: 'etfs-deep-dive',
  slug: 'etfs-passive-investing',
  title: 'ETFs & Passive Investing',
  description: 'ETF creation/redemption, tracking error, synthetic vs physical, and index funds — the cat tracks the market one paw at a time.',
  category: 'Investment Strategies',
  difficulty: 'intermediate',
  icon: '📊',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'etf-structure',
      slug: 'etf-structure-basics',
      title: 'ETF Structure & Mechanics',
      description: 'How ETFs are created, traded, and redeemed.',
      commands: ['etf', 'creation'],
      steps: [
        { instruction: 'Explore ETF creation process: `etf --creation --ticker SPY`', command: 'etf --creation --ticker SPY', expectedOutput: 'SPY creation: Authorized Participant deposits basket of 500 S&P 500 stocks → receives 50,000 ETF shares. Creation unit: 50,000 shares. In-kind transfer: no taxable event' },
        { instruction: 'Authorized Participants (APs) create and redeem ETF shares to keep prices aligned with NAV.' },
        { instruction: 'The cat watched an AP create ETF shares — it was like watching a magician pull tuna from a hat.' },
      ],
      quiz: [
        { question: 'What is the role of an Authorized Participant in the ETF ecosystem?', options: ['To create and redeem ETF shares to maintain price alignment with NAV', 'To trade the ETF on the exchange', 'To manage the ETF portfolio', 'To audit the ETF holdings'], correctIndex: 0, explanation: 'APs are financial institutions that create and redeem ETF shares directly with the ETF issuer to keep the market price close to the NAV.' },
      ],
    },
    {
      id: 'tracking-error',
      slug: 'etf-tracking-error',
      title: 'Tracking Error & Performance',
      description: 'Understanding and measuring ETF tracking error.',
      commands: ['etf', 'tracking'],
      steps: [
        { instruction: 'Calculate tracking error: `etf --tracking --ticker QQQ --period 3yr`', command: 'etf --tracking --ticker QQQ --period 3yr', expectedOutput: 'QQQ tracking vs NDX: Annual tracking error 0.08%, cumulative return difference: -0.32% (fees + drag), expense ratio 0.20%' },
        { instruction: 'Tracking error measures how closely an ETF follows its benchmark index.' },
        { instruction: 'The cat\'s tracking error analysis shows the ETF is off by 0.32% — that\'s 3 fewer cans of tuna per year.' },
      ],
      quiz: [
        { question: 'What is tracking error in the context of ETFs?', options: ['The standard deviation of the difference between ETF returns and benchmark returns', 'The expense ratio of the ETF', 'The bid-ask spread of the ETF', 'The dividend yield difference'], correctIndex: 0, explanation: 'Tracking error measures the consistency of an ETF\'s returns relative to its benchmark index, calculated as the standard deviation of return differences.' },
      ],
    },
    {
      id: 'synthetic-vs-physical',
      slug: 'synthetic-vs-physical-etfs',
      title: 'Synthetic vs Physical ETFs',
      description: 'Comparing replication methods for ETFs.',
      commands: ['etf', 'index-fund'],
      steps: [
        { instruction: 'Compare replication methods: `etf --compare --type synthetic,physical --region europe`', command: 'etf --compare --type synthetic,physical --region europe', expectedOutput: 'Physical: Directly holds underlying securities, lower counterparty risk, higher tracking error. Synthetic: Uses swaps, lower tracking error, counterparty risk, may be more tax-efficient' },
        { instruction: 'Physical ETFs hold the actual securities; synthetic ETFs use derivatives to replicate returns.' },
        { instruction: 'The cat prefers physical ETFs — it doesn\'t trust swap counterparties, especially not dogs.' },
      ],
      quiz: [
        { question: 'What is a key difference between physical and synthetic ETFs?', options: ['Physical ETFs hold the underlying assets; synthetic ETFs use swaps to replicate returns', 'Synthetic ETFs are always cheaper', 'Physical ETFs are riskier', 'Synthetic ETFs don\'t track an index'], correctIndex: 0, explanation: 'Physical ETFs directly own the securities in the index, while synthetic ETFs use total return swaps or other derivatives to replicate index performance.' },
      ],
    },
    {
      id: 'index-fund-strategies',
      slug: 'index-fund-investing-strategies',
      title: 'Index Fund Investing Strategies',
      description: 'Building passive portfolios with index funds.',
      commands: ['index-fund', 'etf'],
      steps: [
        { instruction: 'Build a three-fund portfolio: `index-fund --three-fund --allocation "US:60,International:30,Bonds:10" --amount 100000`', command: 'index-fund --three-fund --allocation "US:60,International:30,Bonds:10" --amount 100000', expectedOutput: 'Three-fund portfolio: $60K VTI, $30K VXUS, $10K BND. Weighted expense ratio: 0.05%. Estimated annual cost: $50. Historical return: 8.2%' },
        { instruction: 'The three-fund portfolio uses total US stock, international stock, and US bond index funds.' },
        { instruction: 'The cat\'s three-fund portfolio is 60% tuna stocks, 30% salmon stocks, 10% kibble bonds.' },
      ],
      quiz: [
        { question: 'What does the classic three-fund portfolio consist of?', options: ['US total stock market, international total stock market, and US total bond market index funds', 'Growth, value, and dividend stock funds', 'Large-cap, mid-cap, and small-cap funds', 'Stock, bond, and real estate funds'], correctIndex: 0, explanation: 'The three-fund portfolio consists of three broad market index funds: US stocks, international stocks, and US bonds for complete diversification.' },
      ],
    },
  ],
}
