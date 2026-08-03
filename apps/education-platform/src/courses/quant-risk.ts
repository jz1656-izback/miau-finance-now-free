import type { Course } from '../lib/types'

export const quantitativeRisk: Course = {
  id: 'quantitative-risk',
  slug: 'quantitative-risk-advanced',
  title: 'Quantitative Risk Advanced',
  description: 'Copulas, EVT, stress testing, and CCAR — the cat models tail risk because it has nine tails.',
  category: 'Risk Management',
  difficulty: 'advanced',
  icon: '📐',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'risk-copula',
      slug: 'copula-models',
      title: 'Copula Models',
      description: 'Modeling dependencies between assets.',
      commands: ['risk-model', 'risk-model copula'],
      steps: [
        { instruction: 'Fit a copula model to a portfolio: `risk-model copula --assets AAPL,MSFT,GOOGL --type clayton`', command: 'risk-model copula --assets AAPL,MSFT,GOOGL --type clayton', expectedOutput: 'Clayton copula fitted: theta=2.34, tail dependence lower=0.67' },
        { instruction: 'Copulas capture non-linear dependencies that correlation misses.' },
        { instruction: 'The cat uses a t-copula — sometimes it claws things to death.' },
      ],
      quiz: [
        { question: 'Why use copulas over simple correlation?', options: ['They capture non-linear dependencies and tail dependence', 'They are easier to calculate', 'They require less data', 'They always produce lower risk estimates'], correctIndex: 0, explanation: 'Copulas model the full dependence structure including tail events, unlike correlation which only captures linear relationships.' },
      ],
    },
    {
      id: 'risk-evt',
      slug: 'extreme-value-theory',
      title: 'Extreme Value Theory',
      description: 'Modeling rare but severe events.',
      commands: ['copula', 'copula simulate'],
      steps: [
        { instruction: 'Simulate tail risk scenarios: `copula simulate --model fitted-copula --scenarios 10000 --tail 0.01`', command: 'copula simulate --model fitted-copula --scenarios 10000 --tail 0.01', expectedOutput: '1% tail VaR: -18.7%, expected shortfall: -24.3%' },
        { instruction: 'EVT focuses on the statistical behavior of extreme values.' },
        { instruction: 'The cat\'s EVT model predicts a 5% chance of knocking over the vase.' },
      ],
      quiz: [
        { question: 'What does Extreme Value Theory model?', options: ['The statistical distribution of rare, extreme events', 'The average of all market events', 'The volatility of normal market conditions', 'The median return of a portfolio'], correctIndex: 0, explanation: 'EVT models the tail of a distribution to estimate the probability and magnitude of extreme events.' },
      ],
    },
    {
      id: 'risk-stress',
      slug: 'stress-testing-scenarios',
      title: 'Stress Testing & Scenarios',
      description: 'Historical and hypothetical scenarios.',
      commands: ['stress', 'stress test'],
      steps: [
        { instruction: 'Run a stress test: `stress test --scenario "2008 Financial Crisis" --portfolio my-portfolio`', command: 'stress test --scenario "2008 Financial Crisis" --portfolio my-portfolio', expectedOutput: 'Stress test result: portfolio loss -32.4% under 2008 scenario — VaR breach at 95% confidence' },
        { instruction: 'Stress tests reveal vulnerabilities that normal risk models miss.' },
        { instruction: 'The cat stress-tests its food supply by knocking over the bag.' },
      ],
      quiz: [
        { question: 'Why perform stress testing beyond VaR?', options: ['VaR does not capture extreme tail losses beyond the confidence level', 'Stress testing replaces VaR entirely', 'VaR is only for equities', 'Stress testing is a regulatory requirement only'], correctIndex: 0, explanation: 'VaR only shows the minimum loss at a confidence level; stress testing reveals how bad things can get in extreme scenarios.' },
      ],
    },
    {
      id: 'risk-ccar',
      slug: 'ccar-regulatory-capital',
      title: 'CCAR & Regulatory Capital',
      description: 'Comprehensive Capital Analysis and Review.',
      commands: ['stress', 'stress scenario'],
      steps: [
        { instruction: 'Generate CCAR-required stress scenarios: `stress scenario --framework ccar --year 2026`', command: 'stress scenario --framework ccar --year 2026', expectedOutput: 'CCAR 2026 stress scenarios: baseline, adverse, severely adverse — capital ratios projected' },
        { instruction: 'CCAR is the Fed\'s annual stress test for large US banks.' },
        { instruction: 'The cat\'s CCAR submission: "We have enough tuna for any scenario."' },
      ],
      quiz: [
        { question: 'What is the purpose of CCAR?', options: ['Ensure large banks maintain adequate capital through stress scenarios', 'Calculate corporate tax liability', 'Regulate cryptocurrency exchanges', 'Set interest rate policy'], correctIndex: 0, explanation: 'CCAR assesses whether large bank holding companies have sufficient capital to withstand adverse economic conditions.' },
      ],
    },
  ],
}
