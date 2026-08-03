import type { Course } from '../lib/types'

export const asianMarkets: Course = {
  id: 'asian-markets',
  slug: 'asian-markets',
  title: 'Asian Markets',
  description: 'China A-shares, Japan, India, SE Asia exchanges, and regional trading dynamics — the cat goes east.',
  category: 'Global Markets',
  difficulty: 'intermediate',
  icon: '🏯',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'china-markets',
      slug: 'china-a-shares',
      title: 'China A-Shares & Hong Kong',
      description: 'Navigating Chinese equity markets.',
      commands: ['asia china', 'asia china --index'],
      steps: [
        { instruction: 'Check China market overview: `asia china --index shanghai`', command: 'asia china --index shanghai', expectedOutput: 'Shanghai Composite: 3,285 (+0.8%). Shenzhen: 10,842 (+1.2%). Hang Seng: 18,420 (-0.3%). A-share turnover: $85B. Northbound: +$1.2B' },
        { instruction: 'China has A-shares (Shanghai/Shenzhen, local currency) and H-shares (Hong Kong, foreign accessible).' },
        { instruction: 'Check Stock Connect flows: `asia china --connect`', command: 'asia china --connect', expectedOutput: 'Northbound (HK→Shanghai): +$450M. Northbound (HK→Shenzhen): +$320M. Southbound (Shanghai→HK): -$180M' },
        { instruction: 'The cat trades A-shares through Stock Connect — it is a very sophisticated feline.' },
      ],
      quiz: [
        { question: 'What is the difference between China A-shares and H-shares?', options: ['A-shares trade in Shanghai/Shenzhen in CNY, H-shares trade in Hong Kong in HKD', 'A-shares are for domestic investors only, H-shares are for everyone', 'A-shares are stocks, H-shares are bonds', 'There is no difference'], correctIndex: 0, explanation: 'A-shares are Chinese companies listed in Shanghai or Shenzhen, traded in CNY. H-shares are Chinese companies listed in Hong Kong, traded in HKD and accessible to international investors.' },
      ],
    },
    {
      id: 'japan-markets',
      slug: 'japan-korea-markets',
      title: 'Japan & Korea Markets',
      description: 'Nikkei, KOSPI, and regional dynamics.',
      commands: ['asia japan', 'asia korea'],
      steps: [
        { instruction: 'Check Japan market data: `asia japan --index nikkei`', command: 'asia japan --index nikkei', expectedOutput: 'Nikkei 225: 39,420 (+0.5%). TOPIX: 2,745 (+0.3%). JPY/USD: 149.20. 10Y JGB: 0.85%. BoJ policy rate: 0.25%' },
        { instruction: 'Japan has negative interest rates until recently — the cat remembers when banks paid to lend money.' },
        { instruction: 'Check Korea market: `asia korea --index kospi`', command: 'asia korea --index kospi', expectedOutput: 'KOSPI: 2,685 (-0.2%). KOSDAQ: 845 (+0.6%). KRW/USD: 1,320. Samsung: +0.8%, SK Hynix: -1.2%' },
        { instruction: 'The cat follows Japan\'s "lost decades" and wonders if the tuna market could experience the same.' },
      ],
      quiz: [
        { question: 'What was significant about the Bank of Japan monetary policy for most of the 2010s and 2020s?', options: ['Negative interest rates and Yield Curve Control to combat deflation', 'The highest interest rates in the developed world', 'A gold standard peg', 'Complete digital currency adoption'], correctIndex: 0, explanation: 'The BoJ maintained negative interest rates and Yield Curve Control to fight decades of deflation and stimulate economic growth, making Japan an outlier in global monetary policy.' },
      ],
    },
    {
      id: 'india-markets',
      slug: 'india-se-asia',
      title: 'India & Southeast Asia',
      description: 'Nifty, SET, IDX, and high-growth markets.',
      commands: ['asia india', 'asia se'],
      steps: [
        { instruction: 'Check India market: `asia india --index nifty`', command: 'asia india --index nifty', expectedOutput: 'Nifty 50: 22,450 (+0.9%). Sensex: 74,200 (+0.7%). INR/USD: 83.20. FII flows: +$320M. GDP growth: 6.8%' },
        { instruction: 'India is the fastest-growing major economy — the cat is long Indian catnip futures.' },
        { instruction: 'Check SE Asia markets: `asia se --index all`', command: 'asia se --index all', expectedOutput: 'SET (Thailand): 1,380 (+0.4%). IDX (Indonesia): 7,220 (+0.6%). PSEi (Philippines): 6,450 (-0.1%). VN30 (Vietnam): 1,185 (+0.9%)' },
        { instruction: 'SE Asia benefits from supply chain diversification — the cat calls it "China Plus Pounce."' },
      ],
      quiz: [
        { question: 'What is driving the recent growth of Indian and SE Asian equity markets?', options: ['Supply chain diversification from China, demographic dividends, and digital adoption', 'Oil price increases', 'Declining global trade', 'Rising interest rates in developed markets'], correctIndex: 0, explanation: 'India and SE Asia benefit from companies diversifying supply chains away from China (China Plus One), young populations, rapid digital adoption, and growing middle classes.' },
      ],
    },
    {
      id: 'asia-trading',
      slug: 'asia-trading-hours',
      title: 'Asian Trading Hours & Settlement',
      description: 'Navigating time zones, holidays, and settlement differences.',
      commands: ['asia hours', 'asia calendar'],
      steps: [
        { instruction: 'Check current trading hours across Asia: `asia hours --now`', command: 'asia hours --now', expectedOutput: 'Current (14:30 UTC): Tokyo closed (08:00-14:30 JST), Shanghai closed (09:30-15:00 CST), Mumbai open (09:15-15:30 IST), Seoul open (09:00-15:30 KST)' },
        { instruction: 'Asian markets have different lunch breaks, holidays, and settlement conventions (T+2 vs T+1).' },
        { instruction: 'Check upcoming Asian market holidays: `asia calendar --month 10`', command: 'asia calendar --month 10', expectedOutput: 'Oct 1-7: China National Day (closed). Oct 3: Korea Foundation Day (closed). Oct 9: Korea Hangul Day (closed). Oct 31: India Diwali (early close)' },
        { instruction: 'The cat tracks Asian holidays because nothing ruins a trade like a closed market.' },
      ],
      quiz: [
        { question: 'Why is tracking Asian market holidays critical for global traders?', options: ['Asian markets have different holiday calendars that can cause liquidity gaps and settlement delays for cross-border trades', 'Holidays determine when you can deposit money', 'Markets always close early on holidays', 'Trading is banned during holiday seasons'], correctIndex: 0, explanation: 'Asia has many unique holidays (Chinese New Year, Golden Week, Diwali) that close markets when other regions are open, creating liquidity gaps and cross-border settlement timing issues.' },
      ],
    },
  ],
}
