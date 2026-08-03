import type { Course } from '../lib/types'

export const growthInvesting: Course = {
  id: 'growth-investing',
  slug: 'growth-investing-strategies',
  title: 'Growth Investing',
  description: 'PEG ratio, TAM, growth at reasonable price, and moats — the cat invests in companies that grow as fast as its appetite.',
  category: 'Investment Strategies',
  difficulty: 'intermediate',
  icon: '🚀',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'growth-basics',
      slug: 'growth-investing-basics',
      title: 'Growth Investing Basics',
      description: 'Core principles of growth investing.',
      commands: ['growth', 'peg'],
      steps: [
        { instruction: 'Screen for growth stocks: `growth --screen --revenue-growth 20 --earnings-growth 15 --market-cap-min 10b`', command: 'growth --screen --revenue-growth 20 --earnings-growth 15 --market-cap-min 10b', expectedOutput: 'Growth screen results: CRWD (rev +36%, EPS +45%), DDOG (+27%, +32%), SNOW (+30%, -5%), NOW (+22%, +18%)' },
        { instruction: 'Growth investing focuses on companies with above-average revenue and earnings growth.' },
        { instruction: 'The cat screens for growth stocks — it filters for companies that grow tuna revenue.' },
      ],
      quiz: [
        { question: 'What is the primary focus of growth investing?', options: ['Companies with above-average revenue and earnings growth potential', 'Companies with high dividend yields', 'Companies with low price-to-book ratios', 'Companies with large cash reserves'], correctIndex: 0, explanation: 'Growth investing targets companies that are expected to grow at an above-average rate compared to their industry or the market.' },
      ],
    },
    {
      id: 'peg-ratio',
      slug: 'peg-ratio-analysis',
      title: 'PEG Ratio & Valuation',
      description: 'Using the PEG ratio to value growth stocks.',
      commands: ['growth', 'peg'],
      steps: [
        { instruction: 'Calculate PEG ratio: `peg --calculate --ticker NVDA --pe 75 --growth-rate 0.50`', command: 'peg --calculate --ticker NVDA --pe 75 --growth-rate 0.50', expectedOutput: 'NVDA PEG ratio: 75 / 50 = 1.50. Interpretation: PEG < 1 = undervalued, PEG 1-2 = fair value, PEG > 2 = overvalued. NVDA: slightly overvalued' },
        { instruction: 'The PEG ratio divides the P/E ratio by the earnings growth rate.' },
        { instruction: 'The cat calculated the PEG ratio of its favorite tuna stock — it passed the smell test.' },
      ],
      quiz: [
        { question: 'What does a PEG ratio of 1.0 suggest about a stock?', options: ['The stock is fairly valued relative to its earnings growth rate', 'The stock is 100% overvalued', 'The stock has a P/E of exactly 1', 'The stock is guaranteed to grow 1%'], correctIndex: 0, explanation: 'A PEG ratio of 1.0 indicates the stock price is fairly valued relative to its earnings growth — P/E equals the growth rate.' },
      ],
    },
    {
      id: 'tam-analysis',
      slug: 'total-addressable-market',
      title: 'Total Addressable Market (TAM)',
      description: 'Evaluating growth potential through market sizing.',
      commands: ['tam', 'growth', 'moat'],
      steps: [
        { instruction: 'Analyze TAM for a company: `tam --analyze --company "Rivian" --segment "EV-trucks"`', command: 'tam --analyze --company "Rivian" --segment "EV-trucks"', expectedOutput: 'Rivian TAM: Global EV truck market $180B by 2030. Rivian revenue $4.4B (2.4% share). 10yr CAGR: 25%. Upside: Capture 5% = $9B revenue' },
        { instruction: 'TAM represents the total revenue opportunity for a product or service.' },
        { instruction: 'The cat calculated the TAM for catnip toys — it\'s in the billions, mostly from the cat itself.' },
      ],
      quiz: [
        { question: 'Why is TAM (Total Addressable Market) important for growth investing?', options: ['It helps estimate the long-term revenue potential and ceiling for a growth company', 'It predicts next quarter\'s earnings', 'It calculates the company\'s current market share', 'It determines the stock price'], correctIndex: 0, explanation: 'TAM helps investors understand the potential growth runway — a large TAM suggests a company can grow for longer before reaching market saturation.' },
      ],
    },
    {
      id: 'economic-moats',
      slug: 'economic-moat-analysis',
      title: 'Economic Moats',
      description: 'Identifying sustainable competitive advantages.',
      commands: ['moat', 'growth'],
      steps: [
        { instruction: 'Analyze moat strength: `moat --analyze --ticker MSFT`', command: 'moat --analyze --ticker MSFT', expectedOutput: 'MSFT moats: Strong — switching costs (Office/365 ecosystem), network effects (Teams/LinkedIn), intangible assets (patents, brand), scale advantages ($200B+ revenue)' },
        { instruction: 'An economic moat is a sustainable competitive advantage that protects a business.' },
        { instruction: 'The cat\'s economic moat? It\'s just too cute to compete against.' },
      ],
      quiz: [
        { question: 'Which of the following is NOT one of Morningstar\'s moat sources?', options: ['High employee satisfaction', 'Cost advantage', 'Network effects', 'Intangible assets'], correctIndex: 0, explanation: 'Morningstar identifies five moat sources: cost advantage, network effects, intangible assets, switching costs, and efficient scale.' },
      ],
    },
  ],
}
