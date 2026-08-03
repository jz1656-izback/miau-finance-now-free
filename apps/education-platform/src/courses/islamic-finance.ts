import type { Course } from '../lib/types'

export const islamicFinance: Course = {
  id: 'islamic-finance',
  slug: 'islamic-finance-sharia',
  title: 'Islamic Finance',
  description: 'Sharia-compliant finance, sukuk, murabaha, and riba prohibition — the cat follows halal investing even if it means fewer tuna futures.',
  category: 'Ethical Finance',
  difficulty: 'intermediate',
  icon: '☪️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'sharia-principles',
      slug: 'sharia-finance-principles',
      title: 'Sharia Finance Principles',
      description: 'Core principles of Islamic finance.',
      commands: ['islamic', 'sharia'],
      steps: [
        { instruction: 'Explore Sharia principles: `sharia --principles --list`', command: 'sharia --principles --list', expectedOutput: 'Core principles: Prohibition of riba (interest), gharar (excessive uncertainty), haram activities — must have asset backing, profit/loss sharing' },
        { instruction: 'Riba (interest) is strictly prohibited in Islamic finance.' },
        { instruction: 'The cat checked if its bank account is halal — no interest, just extra catnip as a gift.' },
      ],
      quiz: [
        { question: 'What does "riba" mean in Islamic finance?', options: ['Interest or usury, which is prohibited', 'Charitable giving', 'Profit sharing', 'Asset backing'], correctIndex: 0, explanation: 'Riba refers to any predetermined interest payment on loans and is strictly prohibited in Islamic finance.' },
      ],
    },
    {
      id: 'sukuk',
      slug: 'sukuk-islamic-bonds',
      title: 'Sukuk — Islamic Bonds',
      description: 'Understanding sukuk as asset-backed securities.',
      commands: ['sukuk', 'islamic'],
      steps: [
        { instruction: 'Analyze a sukuk structure: `sukuk --analyze --type ijara --value 500000000 --tenor 5`', command: 'sukuk --analyze --type ijara --value 500000000 --tenor 5', expectedOutput: 'Ijara Sukuk: $500M, 5-year, asset-backed (real estate), variable rental returns (SOFR + 1.2%), principal repaid at maturity' },
        { instruction: 'Sukuk represent ownership in an underlying asset rather than a debt obligation.' },
        { instruction: 'The cat bought sukuk — it now owns 0.0001% of a halal tuna fishing boat.' },
      ],
      quiz: [
        { question: 'How does a sukuk differ from a conventional bond?', options: ['Sukuk represents ownership in an underlying asset; a bond represents debt', 'Sukuk pays higher interest', 'Sukuk has no maturity date', 'There is no difference'], correctIndex: 0, explanation: 'A sukuk grants the holder ownership in an underlying tangible asset with returns tied to that asset, while a conventional bond is a pure debt instrument.' },
      ],
    },
    {
      id: 'murabaha',
      slug: 'murabaha-financing',
      title: 'Murabaha & Cost-Plus Financing',
      description: 'Understanding murabaha as a common Islamic finance structure.',
      commands: ['murabaha', 'islamic'],
      steps: [
        { instruction: 'Structure a murabaha transaction: `murabaha --structure --asset-price 100000 --profit-margin 0.05 --tenor 24-months`', command: 'murabaha --structure --asset-price 100000 --profit-margin 0.05 --tenor 24-months', expectedOutput: 'Murabaha: Bank buys asset for $100K, sells to client for $105K over 24 months — $4,375/month, no interest, fully Sharia-compliant' },
        { instruction: 'Murabaha is a cost-plus sale where the bank discloses its profit margin upfront.' },
        { instruction: 'The cat used murabaha to buy a new cat tree — the bank made 5% profit, halal-approved.' },
      ],
      quiz: [
        { question: 'In a murabaha transaction, how does the financial institution earn income?', options: ['By selling the asset at a disclosed markup over cost', 'By charging interest on the loan', 'Through late payment fees', 'Through service charges'], correctIndex: 0, explanation: 'Murabaha uses a cost-plus sale where the bank discloses its profit margin upfront and sells the asset above cost.' },
      ],
    },
    {
      id: 'islamic-investing',
      slug: 'islamic-investing-strategies',
      title: 'Islamic Investing & Screening',
      description: 'Sharia-compliant stock screening and investing.',
      commands: ['islamic', 'sharia'],
      steps: [
        { instruction: 'Screen stocks for Sharia compliance: `islamic --screen --tickers AAPL,MSFT,JPM,BAC`', command: 'islamic --screen --tickers AAPL,MSFT,JPM,BAC', expectedOutput: 'Sharia screening: AAPL ✅ (debt ratio 32% < 33%), MSFT ✅ (debt ratio 29%), JPM ❌ (interest income > 5%), BAC ❌ (interest-based business)' },
        { instruction: 'Sharia screening filters out companies with excessive debt or interest-based income.' },
        { instruction: 'The cat\'s halal portfolio includes Apple — even cats know the iPhone is essential.' },
      ],
      quiz: [
        { question: 'What financial ratio is commonly used in Sharia stock screening?', options: ['Debt-to-asset ratio must be below 33%', 'P/E ratio above 15', 'Dividend yield above 2%', 'Market cap above $1 billion'], correctIndex: 0, explanation: 'Sharia screening typically requires total debt divided by total assets to be less than 33% to ensure the company is not overly leveraged with interest-bearing debt.' },
      ],
    },
  ],
}
