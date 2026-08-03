import type { Course } from '../lib/types'

export const dataVisualization: Course = {
  id: 'data-viz-finance',
  slug: 'data-visualization-for-finance',
  title: 'Data Visualization for Finance',
  description: 'Charts, dashboards, plotting, and interpretation — the cat makes prettier charts than your CEO.',
  category: 'Data Science',
  difficulty: 'intermediate',
  icon: '📉',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'viz-charts',
      slug: 'financial-charts-basics',
      title: 'Financial Chart Types',
      description: 'Candlestick, line, bar, and area charts.',
      commands: ['chart', 'chart candlestick'],
      steps: [
        { instruction: 'Plot a candlestick chart: `chart candlestick --symbol AAPL --period 1mo`', command: 'chart candlestick --symbol AAPL --period 1mo', expectedOutput: 'Candlestick chart for AAPL with OHLC data for the last month' },
        { instruction: 'Candlestick charts show open, high, low, and close for each period.' },
        { instruction: 'The cat prefers wick dips — they look like whiskers.' },
      ],
      quiz: [
        { question: 'What does a candlestick body represent?', options: ['The open-to-close price range', 'The high-to-low range', 'The entire trading session', 'The volume traded'], correctIndex: 0, explanation: 'The body of a candlestick shows the range between the open and close prices for that period.' },
      ],
    },
    {
      id: 'viz-plotting',
      slug: 'advanced-plotting-techniques',
      title: 'Advanced Plotting Techniques',
      description: 'Overlays, subplots, and annotations.',
      commands: ['plot', 'plot overlay'],
      steps: [
        { instruction: 'Overlay moving averages on a price chart: `plot overlay --symbol AAPL --indicators sma20 sma50 ema12`', command: 'plot overlay --symbol AAPL --indicators sma20 sma50 ema12', expectedOutput: 'AAPL price chart with SMA20, SMA50, and EMA12 overlay' },
        { instruction: 'Use subplots to compare multiple tickers in one view.' },
        { instruction: 'The cat overlays nine lives on every chart — just in case.' },
      ],
      quiz: [
        { question: 'Why overlay multiple indicators on a chart?', options: ['To compare trends and identify confluences', 'To make charts look more complex', 'To hide the raw price action', 'To confuse other traders'], correctIndex: 0, explanation: 'Overlaying indicators helps identify where multiple signals align, strengthening the trading thesis.' },
      ],
    },
    {
      id: 'viz-dashboard',
      slug: 'building-financial-dashboards',
      title: 'Building Financial Dashboards',
      description: 'Real-time monitoring dashboards.',
      commands: ['dashboard', 'dashboard create'],
      steps: [
        { instruction: 'Create a portfolio dashboard: `dashboard create --portfolio my-portfolio --layout 2x2`', command: 'dashboard create --portfolio my-portfolio --layout 2x2', expectedOutput: 'Dashboard created with P&L, exposure, risk metrics, and performance charts' },
        { instruction: 'Good dashboards tell a story at a glance — keep it clean.' },
        { instruction: 'The cat\'s dashboard has one giant metric: tuna count.' },
      ],
      quiz: [
        { question: 'What makes a financial dashboard effective?', options: ['Clear hierarchy of information and actionable insights', 'Maximum number of charts per screen', 'Bright colors and animations', 'Real-time data refreshing every millisecond'], correctIndex: 0, explanation: 'An effective dashboard prioritizes key information hierarchically so users can quickly understand and act on the data.' },
      ],
    },
    {
      id: 'viz-interpretation',
      slug: 'chart-interpretation-patterns',
      title: 'Chart Interpretation & Patterns',
      description: 'Reading trends, support, resistance.',
      commands: ['visualize', 'visualize pattern'],
      steps: [
        { instruction: 'Identify patterns on a chart: `visualize pattern --symbol BTC --period 3mo`', command: 'visualize pattern --symbol BTC --period 3mo', expectedOutput: 'Pattern analysis: head-and-shoulders formation detected with 68% confidence' },
        { instruction: 'Support and resistance levels help identify entry and exit points.' },
        { instruction: 'The cat spotted a head-and-shoulders pattern in its yarn collection.' },
      ],
      quiz: [
        { question: 'What does a head-and-shoulders pattern typically indicate?', options: ['A trend reversal from bullish to bearish', 'A continuation of the current trend', 'A market crash is imminent', 'A breakout to new highs'], correctIndex: 0, explanation: 'The head-and-shoulders is a classic reversal pattern that signals a shift from an uptrend to a downtrend.' },
      ],
    },
  ],
}
