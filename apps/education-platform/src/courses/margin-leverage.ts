import type { Course } from '../lib/types'

export const marginLeverage: Course = {
  id: 'margin-leverage',
  slug: 'margin-leverage',
  title: 'Margin & Leverage Trading',
  description: 'Understand margin requirements, liquidation prices, and how leverage amplifies both gains and losses — the cat shows you how not to get liquidated.',
  category: 'Calculators',
  difficulty: 'intermediate',
  icon: '⚠️',
  lessonCount: 3,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'margin-basics',
      slug: 'margin-basics',
      title: 'Margin Trading Basics',
      description: 'How margin works: borrowing money to trade larger positions.',
      commands: ['margin 150 100 2', 'margin 200 50 3'],
      steps: [
        { instruction: 'Run a margin calc: `margin 150 100 2` — 100 shares at $150 with 2x leverage', command: 'margin 150 100 2', expectedOutput: 'Total value, equity, liquidation price, margin call price' },
        { instruction: 'The liquidation price is where the broker closes your position. Lower leverage = safer.' },
        { instruction: 'Cats use 1.5x leverage max. They have 9 lives but only 1 portfolio.' },
        { instruction: 'Try 3x leverage: `margin 150 100 3` and see how much closer the liquidation price gets', command: 'margin 150 100 3', expectedOutput: 'Higher liquidation price — less room for the trade to move' },
      ],
      quiz: [
        { question: 'What happens when the stock price hits your liquidation price?', options: ['The broker closes your position to limit losses', 'You get a warning but can keep the position', 'Your leverage automatically increases', 'Nothing happens until you sell'], correctIndex: 0, explanation: 'If the price drops to your liquidation level, the broker will close the position to protect their loan. You lose your equity.' },
      ],
    },
    {
      id: 'leverage-risk',
      slug: 'leverage-risk',
      title: 'Leverage & Risk Management',
      description: 'How leverage amplifies returns and risk.',
      commands: ['margin 100 1000 1', 'margin 100 1000 4'],
      steps: [
        { instruction: 'No leverage: `margin 100 1000 1` — $100K position with your own money', command: 'margin 100 1000 1', expectedOutput: 'Same as buying outright, no liquidation risk' },
        { instruction: 'High leverage: `margin 100 1000 4` — $100K with 4x leverage', command: 'margin 100 1000 4', expectedOutput: 'Liquidation price much closer to entry' },
        { instruction: 'The cat asks: are you willing to lose everything for 4x the gain? Neither is the cat.' },
      ],
      quiz: [
        { question: 'With 4x leverage, a 25% drop in price causes what?', options: ['100% loss of equity (complete liquidation)', '25% loss', '50% loss', 'No loss, margin covers it'], correctIndex: 0, explanation: 'With 4x leverage, you only have 25% equity. A 25% drop wipes out your entire equity, triggering liquidation.' },
      ],
    },
    {
      id: 'margin-call-scenarios',
      slug: 'margin-call-scenarios',
      title: 'Margin Call Scenarios',
      description: 'Plan for different market conditions.',
      commands: ['margin 50 500 2', 'margin 50 500 1.5'],
      steps: [
        { instruction: 'Run a conservative margin scenario: `margin 50 500 1.5`', command: 'margin 50 500 1.5', expectedOutput: 'Lower leverage = safer liquidation buffer' },
        { instruction: 'Always know your liquidation price before entering a margin trade.' },
        { instruction: 'Cats keep a 50% buffer above their liquidation price. You should too.' },
      ],
      quiz: [
        { question: 'What is the safest leverage ratio?', options: ['1x (no leverage)', '2x', '3x', '5x'], correctIndex: 0, explanation: '1x leverage means no borrowed money and zero liquidation risk. You can only lose what you put in.' },
      ],
    },
  ],
}
