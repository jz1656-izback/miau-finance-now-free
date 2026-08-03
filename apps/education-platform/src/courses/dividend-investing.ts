import type { Course } from '../lib/types'

export const dividendInvesting: Course = {
  id: 'dividend-investing',
  slug: 'dividend-investing-strategies',
  title: 'Dividend Investing',
  description: 'Dividend growth, yield, DRIP, payout ratio, and dividend aristocrats — the cat loves dividends because they pay for its tuna addiction.',
  category: 'Investment Strategies',
  difficulty: 'beginner',
  icon: '💵',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'dividend-basics',
      slug: 'dividend-investing-basics',
      title: 'Dividend Investing Basics',
      description: 'Understanding dividends and dividend metrics.',
      commands: ['dividend', 'yield'],
      steps: [
        { instruction: 'Analyze a dividend stock: `dividend --analyze --ticker KO`', command: 'dividend --analyze --ticker KO', expectedOutput: 'KO (Coca-Cola): Dividend $1.94/share, yield 3.15%, payout ratio 75%, 62 consecutive years of increases, ex-div date quarterly' },
        { instruction: 'Dividends are payments made by companies to shareholders from profits.' },
        { instruction: 'The cat drinks Coca-Cola just for the dividend — actually, it just likes the bubbles.' },
      ],
      quiz: [
        { question: 'What does dividend yield measure?', options: ['Annual dividend per share divided by stock price', 'Total dividends paid divided by net income', 'Dividend growth rate over time', 'Number of consecutive dividend increases'], correctIndex: 0, explanation: 'Dividend yield is calculated as the annual dividend per share divided by the current stock price, expressed as a percentage.' },
      ],
    },
    {
      id: 'dividend-growth',
      slug: 'dividend-growth-strategies',
      title: 'Dividend Growth Strategies',
      description: 'Finding and investing in growing dividends.',
      commands: ['dividend', 'aristocrat'],
      steps: [
        { instruction: 'Screen for dividend aristocrats: `aristocrat --screen --yield-min 2.5 --growth-min 5yr-6pct`', command: 'aristocrat --screen --yield-min 2.5 --growth-min 5yr-6pct', expectedOutput: 'Dividend aristocrats meeting criteria: JNJ (3.0% yield, 6.2% 5yr growth), PG (2.8%, 5.5%), PEP (3.1%, 7.1%), LOW (2.6%, 18.5%)' },
        { instruction: 'Dividend aristocrats are S&P 500 stocks with 25+ years of consecutive dividend increases.' },
        { instruction: 'The cat is a dividend aristocrat in its own right — 25+ years of demanding tuna every morning.' },
      ],
      quiz: [
        { question: 'What qualifies a company as a Dividend Aristocrat?', options: ['S&P 500 member with 25+ consecutive years of dividend increases', 'Any company with a 5% dividend yield', 'A company that pays dividends quarterly', 'A company with no debt'], correctIndex: 0, explanation: 'Dividend Aristocrats are S&P 500 companies that have consistently increased their dividend payments for at least 25 consecutive years.' },
      ],
    },
    {
      id: 'drip',
      slug: 'dividend-reinvestment-plans',
      title: 'DRIP — Dividend Reinvestment Plans',
      description: 'Using DRIP to compound dividend returns.',
      commands: ['drip', 'dividend'],
      steps: [
        { instruction: 'Simulate DRIP compounding: `drip --simulate --initial 10000 --yield 3 --growth 6 --years 20`', command: 'drip --simulate --initial 10000 --yield 3 --growth 6 --years 20', expectedOutput: 'DRIP simulation: $10K → $42,300 after 20 years. Without DRIP: $22,100. DRIP advantage: $20,200 (91% more). Annual dividend income: $1,269' },
        { instruction: 'DRIP automatically reinvests dividends to purchase additional shares.' },
        { instruction: 'The cat\'s DRIP is set up — dividends buy more shares, which pay more dividends, which buy more tuna.' },
      ],
      quiz: [
        { question: 'What is the primary benefit of a DRIP (Dividend Reinvestment Plan)?', options: ['Automatic compounding of dividends into additional shares without commissions', 'Tax-free dividend income', 'Guaranteed dividend increases', 'Priority access to new stock issuances'], correctIndex: 0, explanation: 'DRIPs automatically reinvest cash dividends into additional shares, harnessing compound growth without trading fees.' },
      ],
    },
    {
      id: 'payout-ratio',
      slug: 'payout-ratio-analysis',
      title: 'Payout Ratio & Dividend Safety',
      description: 'Assessing dividend sustainability through payout ratios.',
      commands: ['dividend', 'yield'],
      steps: [
        { instruction: 'Analyze payout ratios: `dividend --payout --tickers O,KO,T,IBM`', command: 'dividend --payout --tickers O,KO,T,IBM', expectedOutput: 'O: 230% payout — UNSAFE (REIT, uses AFFO: 82% safe). KO: 75% — MODERATE. T: 58% — SAFE after spin-off. IBM: 54% — SAFE with room for growth' },
        { instruction: 'The payout ratio measures the percentage of earnings paid as dividends.' },
        { instruction: 'A cat with a payout ratio over 100% is spending its tuna before catching it — dangerously delicious.' },
      ],
      quiz: [
        { question: 'What does a payout ratio over 100% typically indicate?', options: ['The company is paying more in dividends than it earns, which is unsustainable long-term', 'The company is very profitable', 'The dividend is guaranteed to grow', 'The stock is undervalued'], correctIndex: 0, explanation: 'A payout ratio above 100% means the company is paying out more than it earns, which is generally unsustainable without borrowing or cutting dividends.' },
      ],
    },
  ],
}
