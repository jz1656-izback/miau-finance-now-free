import type { Course } from '../lib/types'

export const financialNewsLiteracy: Course = {
  id: 'financial-news-literacy',
  slug: 'financial-news-literacy',
  title: 'Financial News Literacy',
  description: 'Reading between the lines, bias detection, and source verification — the cat sniffs out fake news like spoiled fish.',
  category: 'Literacy',
  difficulty: 'beginner',
  icon: '📰',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'news-reading',
      slug: 'reading-financial-news',
      title: 'Reading Financial News',
      description: 'Distinguishing signal from noise.',
      commands: ['news', 'news summary'],
      steps: [
        { instruction: 'Get a news summary for a ticker: `news summary --ticker AAPL --depth balanced`', command: 'news summary --ticker AAPL --depth balanced', expectedOutput: 'AAPL news summary: 3 positive, 2 neutral, 1 negative articles — key themes: AI, iPhone sales, China' },
        { instruction: 'Read multiple sources to get a complete picture.' },
        { instruction: 'The cat reads the Financial Times — mostly for the fish wrap section.' },
      ],
      quiz: [
        { question: 'Why should you read multiple news sources?', options: ['Each source has its own bias — triangulate for the truth', 'One source is always enough', 'News sources are all the same', 'Multiple sources confuse the picture'], correctIndex: 0, explanation: 'Different outlets have different editorial perspectives — comparing them reveals a more complete picture.' },
      ],
    },
    {
      id: 'news-bias',
      slug: 'detecting-bias',
      title: 'Detecting Media Bias',
      description: 'Recognizing slanted reporting.',
      commands: ['verify', 'verify claim'],
      steps: [
        { instruction: 'Verify a financial claim: `verify claim --url https://example.com/news/article --source factset`', command: 'verify claim --url https://example.com/news/article --source factset', expectedOutput: 'Claim verification: 3/5 statements factually accurate, 2 statements lack evidence' },
        { instruction: 'Look for loaded language, selective facts, and missing context.' },
        { instruction: 'The cat detects bias by ear — it always knows when you are hiding treat information.' },
      ],
      quiz: [
        { question: 'What is confirmation bias in news consumption?', options: ['Seeking information that confirms your existing beliefs', 'Confirming facts before publishing', 'Getting confirmation from multiple sources', 'The bias of news confirmations'], correctIndex: 0, explanation: 'Confirmation bias leads us to favor information that confirms our pre-existing beliefs while ignoring contradictory evidence.' },
      ],
    },
    {
      id: 'news-source',
      slug: 'source-verification',
      title: 'Source Verification',
      description: 'Checking credibility of information.',
      commands: ['bias', 'bias analyze'],
      steps: [
        { instruction: 'Analyze bias in a news article: `bias analyze --url https://example.com/finance-news`', command: 'bias analyze --url https://example.com/finance-news', expectedOutput: 'Bias analysis: left-leaning source, 60% factual accuracy, hyperbolic language detected' },
        { instruction: 'Check the author\'s track record and potential conflicts of interest.' },
        { instruction: 'The cat only trusts news sources approved by the International Cat Federation.' },
      ],
      quiz: [
        { question: 'What should you check when evaluating a news source?', options: ['Authorship, citations, funding, and track record', 'How many followers they have', 'The website design quality', 'The length of the article'], correctIndex: 0, explanation: 'Evaluate sources by checking who wrote it, what evidence they cite, who funds them, and their accuracy history.' },
      ],
    },
    {
      id: 'news-market',
      slug: 'news-market-impact',
      title: 'News & Market Impact',
      description: 'How news moves markets.',
      commands: ['source', 'source check'],
      steps: [
        { instruction: 'Check a source\'s credibility: `source check --name "Financial Times"`', command: 'source check --name "Financial Times"', expectedOutput: 'Financial Times: credibility score 92/100, founded 1888, ownership: Nikkei Inc.' },
        { instruction: 'Markets react to news instantly — be careful of trading on headlines.' },
        { instruction: 'The cat knows that "central bank hints at rate cut" is just clickbait for pigeons.' },
      ],
      quiz: [
        { question: 'Why should you avoid trading based on headlines alone?', options: ['Headlines often lack context and can be misleading', 'Headlines are always accurate', 'Markets ignore news entirely', 'Headlines are published too slowly'], correctIndex: 0, explanation: 'Headlines simplify complex stories and can be sensationalized — always read beyond the headline before acting.' },
      ],
    },
  ],
}
