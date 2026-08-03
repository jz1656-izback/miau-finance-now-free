import type { Course } from '../lib/types'

export const artAndCollectibles: Course = {
  id: 'art-and-collectibles',
  slug: 'art-collectibles-investing',
  title: 'Art & Collectibles Investing',
  description: 'Art market, appraisal, fractional ownership, and blue-chip art — the cat invests in paintings of fish and cardboard box sculptures.',
  category: 'Alternative Investments',
  difficulty: 'intermediate',
  icon: '🎨',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'art-market',
      slug: 'art-market-basics',
      title: 'Art Market Basics',
      description: 'Understanding the global art market.',
      commands: ['art', 'appraisal', 'collectible'],
      steps: [
        { instruction: 'Explore art market segments: `art --market --segments --year 2024`', command: 'art --market --segments --year 2024', expectedOutput: 'Global art market 2024: $65B total. Segments: Fine art $45B (69%), Decorative art $12B (18%), Digital art $8B (12%). Top markets: US 42%, China 19%, UK 17%' },
        { instruction: 'The art market is driven by galleries, auctions, and private sales.' },
        { instruction: 'The cat art collection is mostly finger paintings done by kittens — a niche market.' },
      ],
      quiz: [
        { question: 'What is the largest art market in the world by sales value?', options: ['United States (42% of global sales)', 'China', 'United Kingdom', 'France'], correctIndex: 0, explanation: 'The United States accounts for roughly 42% of global art sales by value, led by auction houses and galleries in New York.' },
      ],
    },
    {
      id: 'art-appraisal',
      slug: 'art-appraisal-valuation',
      title: 'Art Appraisal & Valuation',
      description: 'How art is appraised and valued.',
      commands: ['appraisal', 'art', 'collectible'],
      steps: [
        { instruction: 'Get an art appraisal: `appraisal --estimate --artist "Banksy" --work "Girl with Balloon" --condition excellent --provenance documented`', command: 'appraisal --estimate --artist "Banksy" --work "Girl with Balloon" --condition excellent --provenance documented', expectedOutput: 'Banksy "Girl with Balloon" appraisal: $12-18M. Factors: Artist market trend +22% YoY, provenance (original owner), exhibition history, condition 9/10' },
        { instruction: 'Art valuation considers artist reputation, provenance, condition, rarity, and market trends.' },
        { instruction: 'The cat had its cardboard box sculpture appraised — the appraiser said it was priceless (or worthless).' },
      ],
      quiz: [
        { question: 'What is provenance in the art world?', options: ['The documented history of ownership and authenticity of an artwork', 'The probability of the art appreciating', 'The price paid at the last auction', 'The artist biography'], correctIndex: 0, explanation: 'Provenance is the documented chain of ownership for an artwork, which significantly impacts its value and authenticity verification.' },
      ],
    },
    {
      id: 'fractional-ownership',
      slug: 'fractional-art-ownership',
      title: 'Fractional Art Ownership',
      description: 'Investing in art through fractional shares.',
      commands: ['fractional', 'art', 'collectible'],
      steps: [
        { instruction: 'Buy fractional art: `fractional --buy --asset "Banksy Print" --fraction 0.01 --total-value 100000`', command: 'fractional --buy --asset "Banksy Print" --fraction 0.01 --total-value 100000', expectedOutput: 'Fractional purchase: 1% of Banksy Print for $1,000. Platform fee: 1.5% annually. Liquidity: Secondary market only. Expected holding period: 3-5 years' },
        { instruction: 'Fractional ownership allows investors to buy shares of high-value artworks.' },
        { instruction: 'The cat owns 0.5% of a painting of a fish — it is now a fractional art collector.' },
      ],
      quiz: [
        { question: 'What is a key risk of fractional art ownership?', options: ['Limited liquidity — fractional shares can be hard to sell quickly at fair price', 'Guaranteed losses', 'No potential for appreciation', 'Unlimited liability'], correctIndex: 0, explanation: 'Fractional art investments typically have limited secondary market liquidity, meaning investors may struggle to sell their shares quickly.' },
      ],
    },
    {
      id: 'blue-chip-art',
      slug: 'blue-chip-art-investing',
      title: 'Blue-Chip Art Investing',
      description: 'Investing in established, high-value artists.',
      commands: ['art', 'collectible'],
      steps: [
        { instruction: 'Screen for blue-chip art: `art --blue-chip --artist-list --min-auction-price 1000000`', command: 'art --blue-chip --artist-list --min-auction-price 1000000', expectedOutput: 'Blue-chip artists: Picasso ($100M+), Warhol ($80M+), Basquiat ($45M+), Monet ($40M+), Richter ($35M+). Average 10yr return: 7.2% CAGR' },
        { instruction: 'Blue-chip art refers to works by established artists with strong auction track records.' },
        { instruction: 'The cat blue-chip investment is a signed photo of a famous cat from the internet — returns are purring.' },
      ],
      quiz: [
        { question: 'What characterizes blue-chip art?', options: ['Works by established artists with proven auction records and strong liquidity', 'Art that is colored blue', 'Art under $10,000', 'Digital art only'], correctIndex: 0, explanation: 'Blue-chip art represents works by historically significant artists with consistent auction performance and strong market demand.' },
      ],
    },
  ],
}
