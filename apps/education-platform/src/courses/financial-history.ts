import type { Course } from '../lib/types'

export const financialHistory: Course = {
  id: 'financial-history',
  slug: 'financial-history',
  title: 'Financial History',
  description: 'Market crashes, bubbles, and lessons from history — the cat learns from the past.',
  category: 'History',
  difficulty: 'beginner',
  icon: '📜',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'fh-crashes',
      slug: 'market-crashes',
      title: 'Famous Market Crashes',
      description: '1929, 1987, 2008, and what caused them.',
      commands: ['history', 'history crashes'],
      steps: [
        { instruction: 'Explore market crashes: `history crashes --year 1929`', command: 'history crashes --year 1929', expectedOutput: 'Details of the 1929 crash: causes, timeline, and aftermath' },
        { instruction: 'The 1929 crash was fueled by excessive leverage and speculative mania.' },
        { instruction: 'The 2008 financial crisis was triggered by subprime mortgage defaults and systemic risk.' },
      ],
      quiz: [
        { question: 'What triggered the 2008 financial crisis?', options: ['Subprime mortgage defaults and systemic risk', 'The dot-com bubble bursting', 'Oil price collapse', 'Currency devaluation'], correctIndex: 0, explanation: 'The 2008 crisis was triggered by widespread defaults on subprime mortgages, which cascaded through the financial system.' },
      ],
    },
    {
      id: 'fh-bubbles',
      slug: 'famous-bubbles',
      title: 'Speculative Bubbles',
      description: 'Tulip mania, dot-com, housing, and the psychology of bubbles.',
      commands: ['crisis', 'crisis timeline'],
      steps: [
        { instruction: 'Study speculative bubbles: `history bubbles --list`', command: 'history bubbles --list', expectedOutput: 'Timeline of major speculative bubbles with common characteristics' },
        { instruction: 'Tulip mania (1637) is often cited as the first recorded speculative bubble.' },
        { instruction: 'The dot-com bubble (2000) saw the NASDAQ rise 400% and then fall 78%.' },
      ],
      quiz: [
        { question: 'What common pattern do speculative bubbles follow?', options: ['Displacement → boom → euphoria → distress → panic', 'Steady growth → crash → recovery', 'Random price movements', 'Gradual decline'], correctIndex: 0, explanation: 'Bubbles follow a pattern: displacement (new paradigm), boom, euphoria, distress, and finally panic/crash.' },
      ],
    },
    {
      id: 'fh-lessons',
      slug: 'lessons-from-history',
      title: 'Lessons from Financial History',
      description: 'What every investor should know from past crises.',
      commands: ['bubble', 'bubble analysis'],
      steps: [
        { instruction: 'Review key lessons: `history lessons`', command: 'history lessons', expectedOutput: 'Top 10 lessons from financial history' },
        { instruction: '"This time is different" is the four most expensive words in investing.' },
        { instruction: 'Diversification, risk management, and long-term thinking survive every crisis.' },
      ],
      quiz: [
        { question: 'What is the most dangerous phrase in investing?', options: ['"This time is different"', '"Buy low, sell high"', '"Diversify your portfolio"', '"Cut your losses"'], correctIndex: 0, explanation: '"This time is different" leads investors to ignore historical patterns and take excessive risks, often right before a crash.' },
      ],
    },
    {
      id: 'fh-investors',
      slug: 'great-investors',
      title: 'Great Investors of History',
      description: 'Lessons from Buffett, Graham, Lynch, and Soros.',
      commands: ['crash', 'crash analysis'],
      steps: [
        { instruction: 'Learn from the greats: `history investors`', command: 'history investors', expectedOutput: 'Profiles of legendary investors with their key principles' },
        { instruction: 'Warren Buffett: "Be fearful when others are greedy, greedy when others are fearful."' },
        { instruction: 'Benjamin Graham invented value investing — buying stocks for less than their intrinsic value.' },
      ],
      quiz: [
        { question: 'What is Benjamin Graham known for?', options: ['Founding value investing', 'Founding growth investing', 'Creating the first hedge fund', 'Predicting the 2008 crisis'], correctIndex: 0, explanation: 'Benjamin Graham, author of "The Intelligent Investor," is considered the father of value investing.' },
      ],
    },
  ],
}
