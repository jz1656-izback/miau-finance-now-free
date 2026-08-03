import type { Course } from '../lib/types'

export const aiAdvisor: Course = {
  id: 'ai-advisor',
  slug: 'ai-advisor',
  title: 'AI Portfolio Advisor',
  description: 'Get AI-powered insights on your portfolio, markets, and risks.',
  category: 'AI',
  difficulty: 'intermediate',
  icon: '🤖',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'ai-portfolio',
      slug: 'portfolio',
      title: 'AI Portfolio Analysis',
      description: 'Let AI analyze your portfolio.',
      commands: ['ai portfolio'],
      steps: [
        { instruction: 'Analyze a portfolio: `ai portfolio 1`', command: 'ai portfolio 1', expectedOutput: 'AI-generated analysis with strengths and weaknesses' },
        { instruction: 'The AI looks at allocation, concentration, risk, and diversification.' },
      ],
      quiz: [
        { question: 'What does `ai portfolio` analyze?', options: ['Portfolio allocation and risk', 'Market news', 'Stock prices only', 'Your trading history'], correctIndex: 0, explanation: '`ai portfolio` provides comprehensive analysis including allocation, risk, and diversification.' },
      ],
    },
    {
      id: 'ai-market',
      slug: 'market',
      title: 'AI Market Overview',
      description: 'Get AI market commentary and insights.',
      commands: ['ai market'],
      steps: [
        { instruction: 'Market overview: `ai market`', command: 'ai market', expectedOutput: 'AI analysis of current market conditions' },
        { instruction: 'Includes sector rotation, sentiment, and potential opportunities.' },
      ],
      quiz: [
        { question: 'What does `ai market` provide?', options: ['AI-powered market analysis', 'Raw price data', 'Order book', 'Historical data'], correctIndex: 0, explanation: '`ai market` gives an AI overview of current market conditions and sentiment.' },
      ],
    },
    {
      id: 'ai-risk',
      slug: 'risk',
      title: 'AI Risk Assessment',
      description: 'AI evaluates your portfolio risks.',
      commands: ['ai risk'],
      steps: [
        { instruction: 'Risk assessment: `ai risk 1`', command: 'ai risk 1', expectedOutput: 'AI identifying key risk factors' },
        { instruction: 'The AI flags concentration risk, sector exposure, and tail risks.' },
      ],
      quiz: [
        { question: 'What does `ai risk` identify?', options: ['Key risk factors in a portfolio', 'Stock prices', 'Market hours', 'News headlines'], correctIndex: 0, explanation: '`ai risk` flags risks like concentration, sector exposure, and tail events.' },
      ],
    },
    {
      id: 'ai-query',
      slug: 'query',
      title: 'Natural Language Queries',
      description: 'Ask the AI anything in plain English.',
      commands: ['ai query', 'ask'],
      steps: [
        { instruction: 'Ask a question: `ask what is the best performing sector this month?`', command: 'ask what sectors are doing well today', expectedOutput: 'AI response to your question' },
        { instruction: 'Formal syntax: `ai query <text>`', command: 'ai query explain value investing', expectedOutput: 'AI explanation' },
        { instruction: 'You can ask about markets, strategies, definitions, and more.' },
      ],
      quiz: [
        { question: 'Which command lets you ask AI in plain English?', options: ['ask', 'ai portfolio', 'ai market', 'ai risk'], correctIndex: 0, explanation: '`ask <question>` lets you query the AI in natural language.' },
      ],
    },
  ],
}
