import type { Course } from '../lib/types'

export const alternativeData: Course = {
  id: 'alternative-data',
  slug: 'alternative-data',
  title: 'Alternative Data',
  description: 'Satellite imagery, credit card transactions, web scraping, and sentiment analysis — the cat sees what others miss.',
  category: 'Data Science',
  difficulty: 'advanced',
  icon: '📡',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'altdata-intro',
      slug: 'alternative-data-introduction',
      title: 'Introduction to Alternative Data',
      description: 'What alt data is and why it matters.',
      commands: ['alt-data', 'alt-data search'],
      steps: [
        { instruction: 'Search for alternative data sources: `alt-data search --category foot-traffic`', command: 'alt-data search --category foot-traffic', expectedOutput: 'List of foot traffic data providers with coverage and pricing' },
        { instruction: 'Alternative data gives you an edge before traditional data catches up.' },
        { instruction: 'The cat tracks foot traffic via satellite — no more guessing which stores are busy.' },
      ],
      quiz: [
        { question: 'What makes alternative data valuable for investors?', options: ['It provides non-traditional signals not yet priced in', 'It replaces financial statements entirely', 'It is always free to access', 'It is regulated by the SEC'], correctIndex: 0, explanation: 'Alternative data offers unique insights that traditional financial data sources do not capture, giving early signals.' },
      ],
    },
    {
      id: 'altdata-satellite',
      slug: 'satellite-imagery-data',
      title: 'Satellite Imagery & Geospatial',
      description: 'Counting cars in parking lots from space.',
      commands: ['satellite', 'satellite track'],
      steps: [
        { instruction: 'Track retail traffic via satellite: `satellite track --target WMT --region us-east`', command: 'satellite track --target WMT --region us-east', expectedOutput: 'Satellite imagery analysis: car count trends for Walmart since last quarter' },
        { instruction: 'Satellite data can estimate crop yields, oil tank levels, and retail foot traffic.' },
        { instruction: 'The cat\'s eye in the sky operates 24/7 — clouds are the only enemy.' },
      ],
      quiz: [
        { question: 'How can satellite imagery predict retail earnings?', options: ['Counting cars in parking lots estimates store traffic', 'Reading store signs from orbit', 'Measuring building heights', 'Tracking weather patterns'], correctIndex: 0, explanation: 'Satellite images of parking lots reveal customer traffic patterns before earnings are reported.' },
      ],
    },
    {
      id: 'altdata-web',
      slug: 'web-scraping-sentiment',
      title: 'Web Scraping & Sentiment',
      description: 'Extracting signals from the public web.',
      commands: ['web-scrape', 'web-scrape product'],
      steps: [
        { instruction: 'Scrape product prices from retailers: `web-scrape product --url https://example.com/products --interval 1h`', command: 'web-scrape product --url https://example.com/products --interval 1h', expectedOutput: 'Web scraping pipeline started — tracking 150 products hourly' },
        { instruction: 'Sentiment analysis scores news and social media for bullish or bearish signals.' },
        { instruction: 'The cat reads every tweet so you do not have to.' },
      ],
      quiz: [
        { question: 'Why use web scraping for investment research?', options: ['Track pricing, inventory, and reviews in real-time', 'Steal competitor trade secrets', 'Replace fundamental analysis entirely', 'Automate insider trading'], correctIndex: 0, explanation: 'Web scraping captures real-time pricing, product availability, and customer sentiment from e-commerce sites.' },
      ],
    },
    {
      id: 'altdata-processing',
      slug: 'processing-alternative-data',
      title: 'Processing & Validation',
      description: 'Cleaning noise from messy datasets.',
      commands: ['sentiment', 'sentiment analyze'],
      steps: [
        { instruction: 'Analyze sentiment for a stock: `sentiment analyze --ticker TSLA --source twitter`', command: 'sentiment analyze --ticker TSLA --source twitter', expectedOutput: 'Sentiment score: 0.72 (bullish) based on 15,432 mentions in last 24 hours' },
        { instruction: 'Always validate alt data against known benchmarks before trading on it.' },
        { instruction: 'The cat filters out bot tweets — real sentiment only, no robot gossip.' },
      ],
      quiz: [
        { question: 'What is the biggest challenge with alternative data?', options: ['Data quality and signal-to-noise ratio', 'Getting SEC approval for use', 'Finding free data sources', 'Storing large image files'], correctIndex: 0, explanation: 'Alternative data is often noisy, unstructured, and requires significant cleaning and validation before it becomes actionable.' },
      ],
    },
  ],
}
