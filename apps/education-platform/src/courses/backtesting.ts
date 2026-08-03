import type { Course } from '../lib/types'

export const backtesting: Course = {
  id: 'backtesting',
  slug: 'backtesting',
  title: 'Backtesting Strategies',
  description: 'Methodology, pitfalls, overfitting, and walk-forward analysis — the cat validates your edge.',
  category: 'Trading',
  difficulty: 'advanced',
  icon: '🔬',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'bt-methodology',
      slug: 'backtesting-methodology',
      title: 'Backtesting Methodology',
      description: 'Proper structure for reliable backtests.',
      commands: ['backtest', 'backtest setup'],
      steps: [
        { instruction: 'Set up a backtest: `backtest setup --strategy "Momentum" --symbols AAPL MSFT GOOGL`', command: 'backtest setup --strategy "Momentum" --symbols AAPL MSFT GOOGL', expectedOutput: 'Backtest configuration with parameters and date range' },
        { instruction: 'A backtest simulates trades on historical data to evaluate strategy performance.' },
        { instruction: 'Include transaction costs, slippage, and market impact for realistic results.' },
      ],
      quiz: [
        { question: 'Why include transaction costs in backtests?', options: ['Realistic results reflect actual trading frictions', 'Costs are always negligible', 'Backtests ignore costs automatically', 'Costs only matter in live trading'], correctIndex: 0, explanation: 'Transaction costs, slippage, and market impact significantly affect real returns and must be modeled in backtests.' },
      ],
    },
    {
      id: 'bt-pitfalls',
      slug: 'backtesting-pitfalls',
      title: 'Common Backtesting Pitfalls',
      description: 'Survivorship bias, look-ahead bias, and data snooping.',
      commands: ['optimize', 'optimize parameters'],
      steps: [
        { instruction: 'Check for biases: `backtest audit --results`', command: 'backtest audit --results', expectedOutput: 'Backtest audit report: identified biases and recommendations' },
        { instruction: 'Survivorship bias = only looking at stocks that still exist today.' },
        { instruction: 'Data snooping = testing many strategies until one works by chance.' },
      ],
      quiz: [
        { question: 'What is survivorship bias in backtesting?', options: ['Ignoring stocks that delisted or went bankrupt', 'Only testing surviving companies', 'Using survivor data', 'Testing long-term strategies'], correctIndex: 0, explanation: 'Survivorship bias occurs when backtests only include stocks that survived, ignoring failed companies that would have appeared in a real portfolio.' },
      ],
    },
    {
      id: 'bt-overfitting',
      slug: 'overfitting-strategies',
      title: 'Overfitting & Curve-Fitting',
      description: 'When a strategy looks amazing in backtest but fails live.',
      commands: ['walk-forward', 'walk-forward run'],
      steps: [
        { instruction: 'Run an overfitting analysis: `backtest overfit --strategy momentum`', command: 'backtest overfit --strategy momentum', expectedOutput: 'Overfitting analysis with out-of-sample performance comparison' },
        { instruction: 'Curve-fitting = optimizing parameters to fit historical data perfectly.' },
        { instruction: 'A strategy that works across many parameter values is more robust.' },
      ],
      quiz: [
        { question: 'What is curve-fitting in strategy development?', options: ['Over-optimizing parameters to fit historical data', 'Fitting a yield curve model', 'Building a learning curve', 'Plotting equity curves'], correctIndex: 0, explanation: 'Curve-fitting means choosing parameters that maximize past returns but may not generalize to future data.' },
      ],
    },
    {
      id: 'bt-metrics',
      slug: 'performance-metrics',
      title: 'Performance Metrics & Validation',
      description: 'Sharpe ratio, max drawdown, and walk-forward analysis.',
      commands: ['metrics', 'metrics sharpe'],
      steps: [
        { instruction: 'Calculate performance metrics: `metrics sharpe --strategy momentum --risk-free 5`', command: 'metrics sharpe --strategy momentum --risk-free 5', expectedOutput: 'Sharpe ratio, Sortino ratio, max drawdown, and Calmar ratio' },
        { instruction: 'Walk-forward analysis retrains the model periodically, testing on out-of-sample data.' },
        { instruction: 'Monte Carlo simulation tests strategy robustness by randomizing trade sequences.' },
      ],
      quiz: [
        { question: 'What does walk-forward analysis do?', options: ['Periodically retrains and tests on out-of-sample data', 'Walks forward through trades one by one', 'Forwards testing on walk data', 'Analysis of forward contracts'], correctIndex: 0, explanation: 'Walk-forward analysis repeatedly trains on a rolling window and tests on the next period to simulate real-world performance.' },
      ],
    },
  ],
}
