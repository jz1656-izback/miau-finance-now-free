import type { Course } from '../lib/types'

export const momentumTrading: Course = {
  id: 'momentum-trading',
  slug: 'momentum-trend-following',
  title: 'Momentum & Trend Following',
  description: 'Relative strength, trend following, and moving average crossovers — the cat rides the trend like a wave of cream.',
  category: 'Trading',
  difficulty: 'intermediate',
  icon: '📈',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'momentum-basics',
      slug: 'momentum-trading-fundamentals',
      title: 'Momentum Trading Fundamentals',
      description: 'Core concepts of momentum trading.',
      commands: ['momentum', 'relative-strength', 'trend'],
      steps: [
        { instruction: 'Calculate relative strength: `relative-strength --calculate --ticker NVDA --benchmark SPY --period 12mo`', command: 'relative-strength --calculate --ticker NVDA --benchmark SPY --period 12mo', expectedOutput: 'NVDA relative strength: 2.45 (NVDA +145% vs SPY +22%). RS rating: 98 out of 100. Trend status: STRONG UPTREND' },
        { instruction: 'Relative strength compares a stock\'s performance to a benchmark index.' },
        { instruction: 'The cat\'s relative strength is off the charts — it can knock things off tables with 99% accuracy.' },
      ],
      quiz: [
        { question: 'What does relative strength (RS) measure in momentum trading?', options: ['A stock\'s price performance relative to a benchmark index', 'The physical strength of a company\'s management', 'The correlation between two stocks', 'The volatility of a stock'], correctIndex: 0, explanation: 'Relative strength compares a stock\'s percentage return to that of a benchmark (like the S&P 500) over a specific period to gauge momentum.' },
      ],
    },
    {
      id: 'moving-averages',
      slug: 'moving-average-crossovers',
      title: 'Moving Average Crossovers',
      description: 'Using moving averages to identify trend changes.',
      commands: ['cross-over', 'trend', 'momentum'],
      steps: [
        { instruction: 'Detect crossover signals: `cross-over --detect --ticker AAPL --fast 50 --slow 200`', command: 'cross-over --detect --ticker AAPL --fast 50 --slow 200', expectedOutput: 'AAPL: 50-day MA ($178) ABOVE 200-day MA ($165). Golden cross detected. Signal: BULLISH. Next support: 200-day MA at $165. Resistance: $195 (52-week high)' },
        { instruction: 'A golden cross occurs when the 50-day MA crosses above the 200-day MA.' },
        { instruction: 'The cat spotted a golden cross on the tuna futures chart — time to load up the bowl.' },
      ],
      quiz: [
        { question: 'What does a "golden cross" signal in technical analysis?', options: ['A bullish signal when the 50-day moving average crosses above the 200-day moving average', 'A sell signal at market peaks', 'When gold prices cross above oil', 'When two stocks have the same moving average'], correctIndex: 0, explanation: 'A golden cross forms when a shorter-term moving average (typically 50-day) crosses above a longer-term moving average (200-day), indicating a potential bull market.' },
      ],
    },
    {
      id: 'trend-following',
      slug: 'trend-following-strategies',
      title: 'Trend Following Strategies',
      description: 'Systematic trend following approaches.',
      commands: ['trend', 'momentum'],
      steps: [
        { instruction: 'Run a trend following backtest: `trend --backtest --strategy "dual-momentum" --universe SP500 --period 2000-2025`', command: 'trend --backtest --strategy "dual-momentum" --universe SP500 --period 2000-2025', expectedOutput: 'Dual Momentum backtest: 10.8% CAGR vs SPY 7.2%. Max drawdown: -28% vs -51%. Win rate: 62%. Sharpe ratio: 0.85 vs 0.45' },
        { instruction: 'Trend following strategies buy assets in uptrends and sell or short in downtrends.' },
        { instruction: 'The cat follows the trend — when the sunbeam moves, the cat follows it.' },
      ],
      quiz: [
        { question: 'What is the core premise of trend following?', options: ['Markets tend to move in persistent directions that can be captured systematically', 'All trends reverse at predictable points', 'Fundamental analysis drives all trends', 'Trends only exist in bull markets'], correctIndex: 0, explanation: 'Trend following is based on the observation that financial markets exhibit persistent directional movements that can be captured through systematic rules.' },
      ],
    },
    {
      id: 'momentum-risk',
      slug: 'momentum-risk-management',
      title: 'Momentum Risk Management',
      description: 'Managing risks specific to momentum strategies.',
      commands: ['momentum', 'trend'],
      steps: [
        { instruction: 'Set momentum stop-losses: `momentum --stops --type "trailing" --percent 15 --position NVDA`', command: 'momentum --stops --type "trailing" --percent 15 --position NVDA', expectedOutput: 'Trailing stop set: NVDA at $175, stop at $148.75 (15% trail). Current trail distance: $26.25. Max risk per trade: $2,625 on $17,500 position' },
        { instruction: 'Trailing stops protect profits by adjusting the stop-loss as the price rises.' },
        { instruction: 'The cat uses a trailing stop — if the stock falls, the cat bounces. If it rises, the cat chases.' },
      ],
      quiz: [
        { question: 'How does a trailing stop-loss work?', options: ['It automatically adjusts upward as the stock price rises, locking in profits', 'It stays fixed regardless of price movement', 'It trails behind the market by exactly one day', 'It only triggers at market close'], correctIndex: 0, explanation: 'A trailing stop-loss moves up with the stock price at a set percentage distance, protecting profits while allowing room for continued growth.' },
      ],
    },
  ],
}
