import type { Course } from '../lib/types'

export const aiInvestmentResearch: Course = {
  id: 'ai-investment-research',
  slug: 'ai-investment-research',
  title: 'AI-Powered Investment Research',
  description: 'Leverage data-driven analytics for investment research — mega charts, quant health scores, DCF fair value, automated discovery, and predictive models. The cat analyzes data so you can make decisions.',
  category: 'AI',
  difficulty: 'intermediate',
  icon: '🤖',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'ai-mega-charts',
      slug: 'mega-chart-analysis',
      title: 'Mega Chart Analysis',
      description: 'Full display charts with RSI, MACD, predictions, and market context.',
      commands: ['chartz AAPL', 'chartz AAPL -l', 'chartz AAPL -lm'],
      steps: [
        { instruction: 'Generate a mega chart: `chartz AAPL` — 16-row ASCII chart with indicators', command: 'chartz AAPL', expectedOutput: 'Full chart with RSI, MACD, SMA, prediction' },
        { instruction: 'Add live data and news: `chartz AAPL -l` — market context, P/E, news', command: 'chartz AAPL -l', expectedOutput: 'Chart + market context + news stories' },
        { instruction: 'Max mode: `chartz AAPL -lm` — everything including cats', command: 'chartz AAPL -lm', expectedOutput: 'Chart + mega indicators + news + cats' },
        { instruction: 'The cat uses mega charts to analyze stocks. It looks for patterns. Also tuna.' },
      ],
      quiz: [
        { question: 'What does the RSI indicator above 70 typically suggest?', options: ['The stock may be overbought and due for a pullback', 'The stock is a strong buy', 'The stock is oversold', 'The market is closed'], correctIndex: 0, explanation: 'RSI above 70 is considered overbought, suggesting the stock may have risen too far too fast and could be due for a correction or consolidation.' },
      ],
    },
    {
      id: 'ai-quant-scores',
      slug: 'quant-scores-health',
      title: 'Quant Health & Fair Value',
      description: 'Fundamental health scores and intrinsic valuation.',
      commands: ['quanthealth AAPL', 'fairvalue AAPL'],
      steps: [
        { instruction: 'Run quant health: `quanthealth AAPL` — Piotroski F-Score, Altman Z', command: 'quanthealth AAPL', expectedOutput: 'Financial health metrics' },
        { instruction: 'The Piotroski F-Score (0-9) measures financial strength using 9 fundamental signals.' },
        { instruction: 'Check fair value: `fairvalue AAPL` — DCF intrinsic value vs current price', command: 'fairvalue AAPL', expectedOutput: 'Current price vs fair value with upside %' },
        { instruction: 'The cat combines quant health plus fair value to make buy/sell decisions. It is very scientific.' },
      ],
      quiz: [
        { question: 'What does a Piotroski F-Score of 7-9 indicate?', options: ['Strong financial health — the company scores well on most fundamental signals', 'The company is about to go bankrupt', 'The stock is overvalued', 'The company has poor earnings quality'], correctIndex: 0, explanation: 'A Piotroski F-Score of 7-9 indicates strong financial health based on 9 fundamental signals including profitability, leverage, liquidity, and operating efficiency.' },
      ],
    },
    {
      id: 'ai-predictions',
      slug: 'predictions-forecasts',
      title: 'Predictions & Forecasting',
      description: 'Linear regression forecasts and predictive analytics.',
      commands: ['chartz SPY', 'montecarlo SPY 1000 252', 'fairvalue SPY'],
      steps: [
        { instruction: 'Get the forecast: `chartz SPY` — includes 20-period linear regression prediction', command: 'chartz SPY', expectedOutput: 'Chart with price prediction' },
        { instruction: 'Run Monte Carlo: `montecarlo SPY 1000 252` — 1000 simulated price paths', command: 'montecarlo SPY 1000 252', expectedOutput: 'Monte Carlo simulation with percentiles' },
        { instruction: 'The cat\'s favorite prediction: 87% chance of tuna price increase.' },
        { instruction: 'Combine with fundamentals: `fairvalue SPY` for DCF-based intrinsic value', command: 'fairvalue SPY', expectedOutput: 'SPY fair value' },
      ],
      quiz: [
        { question: 'What does a Monte Carlo simulation show in investing?', options: ['A range of possible outcomes with probability percentiles based on historical volatility', 'The exact future price of a stock', 'The best day to buy', 'The guaranteed minimum return'], correctIndex: 0, explanation: 'Monte Carlo runs thousands of random simulations based on historical mean and volatility, giving a probability distribution of potential outcomes rather than a single prediction.' },
      ],
    },
    {
      id: 'ai-workflow',
      slug: 'ai-research-workflow',
      title: 'AI Research Workflow',
      description: 'Put it all together — an AI-powered research pipeline.',
      commands: ['chartz AAPL -lm', 'quanthealth AAPL', 'fairvalue AAPL', 'correlation AAPL,MSFT,GOOGL'],
      steps: [
        { instruction: 'Step 1: Macro view — `chartz AAPL -lm` for full technical picture', command: 'chartz AAPL -lm', expectedOutput: 'Full mega chart with technicals and news' },
        { instruction: 'Step 2: Fundamentals — `quanthealth AAPL` for financial health', command: 'quanthealth AAPL', expectedOutput: 'Quant health scores' },
        { instruction: 'Step 3: Valuation — `fairvalue AAPL` for intrinsic value', command: 'fairvalue AAPL', expectedOutput: 'Fair value comparison' },
        { instruction: 'Step 4: Correlation — `correlation AAPL,MSFT,GOOGL` for market relationships', command: 'correlation AAPL,MSFT,GOOGL', expectedOutput: 'Asset correlation matrix' },
        { instruction: 'The cat completed the AI research workflow. It recommends investing in more catnip.' },
      ],
      quiz: [
        { question: 'What is the recommended order for AI-powered investment research?', options: ['1) Technical chart (chartz), 2) Financial health (quanthealth), 3) Valuation (fairvalue), 4) Market context (correlation)', '1) Buy first, 2) Research later', '1) Only check the price', '1) Read news, 2) Follow tips'], correctIndex: 0, explanation: 'A systematic approach: start with the technical picture, assess fundamental health, determine fair value, then understand market context through correlations and news.' },
      ],
    },
  ],
}
