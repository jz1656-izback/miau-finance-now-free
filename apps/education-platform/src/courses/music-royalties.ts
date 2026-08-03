import type { Course } from '../lib/types'

export const musicRoyalties: Course = {
  id: 'music-royalties',
  slug: 'music-entertainment-finance',
  title: 'Music & Entertainment Finance',
  description: 'Streaming economics, catalog valuation, and royalty rates — the cat invests in the mewsic industry and collects royalties every time a cat video is played.',
  category: 'Alternative Investments',
  difficulty: 'intermediate',
  icon: '🎵',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'streaming-economics',
      slug: 'music-streaming-economics',
      title: 'Streaming Economics',
      description: 'How streaming platforms generate and distribute revenue.',
      commands: ['music', 'streaming', 'royalty'],
      steps: [
        { instruction: 'Analyze streaming payout model: `streaming --payouts --platform spotify --streams 1000000 --artist-tier independent`', command: 'streaming --payouts --platform spotify --streams 1000000 --artist-tier independent', expectedOutput: 'Spotify payout: 1M streams = $3,500-$5,000. Per-stream rate: $0.003-$0.005. Label cut: 50-70%. Artist net: $1,050-$2,500. Publisher: additional $500-$1,000' },
        { instruction: 'Streaming platforms pay rights holders based on pro-rata share of total streams.' },
        { instruction: 'The cat mewsic streams generated enough royalties to buy one can of tuna per quarter.' },
      ],
      quiz: [
        { question: 'What is the approximate per-stream payout range on Spotify?', options: ['$0.003 to $0.005 per stream', '$0.10 per stream', '$0.50 per stream', '$1.00 per stream'], correctIndex: 0, explanation: 'Spotify pays between $0.003 and $0.005 per stream on average, varying by listener country and subscription type.' },
      ],
    },
    {
      id: 'catalog-valuation',
      slug: 'music-catalog-valuation',
      title: 'Music Catalog Valuation',
      description: 'Valuing music publishing and recording catalogs.',
      commands: ['catalog', 'music', 'royalty'],
      steps: [
        { instruction: 'Value a music catalog: `catalog --value --annual-revenue 500000 --growth 0.03 --royalty-type publishing --artist-risk low`', command: 'catalog --value --annual-revenue 500000 --growth 0.03 --royalty-type publishing --artist-risk low', expectedOutput: 'Catalog valuation: $5M-7.5M (10-15x net publisher share). DCF: $6.2M. Synch income: $50K/yr. Catalog age: 20+ years. Risk factor: low (diversified writer pool)' },
        { instruction: 'Music catalogs are valued on multiples of net publisher share or net artist royalty.' },
        { instruction: 'The cat mewsic catalog includes the hit single "Meow Meow Meow" — valuation is classified.' },
      ],
      quiz: [
        { question: 'What multiple is commonly used to value music publishing catalogs?', options: ['10-15x annual net publisher share for established catalogs', '1-2x annual revenue', '50x annual revenue', 'Based solely on hit singles'], correctIndex: 0, explanation: 'Established music publishing catalogs typically trade at 10-15x annual net publisher share, varying by catalog age and revenue stability.' },
      ],
    },
    {
      id: 'royalty-rates',
      slug: 'music-royalty-rate-structures',
      title: 'Royalty Rate Structures',
      description: 'Understanding different royalty types in music.',
      commands: ['royalty', 'music', 'catalog'],
      steps: [
        { instruction: 'Compare royalty types: `royalty --compare --types mechanical,performance,sync,print`', command: 'royalty --compare --types mechanical,performance,sync,print', expectedOutput: 'Mechanical: 9.1c per physical copy/sale. Performance: $0.02-0.05 per stream (PRO). Sync: $5K-$500K per use (negotiated). Print: 10-20% of sheet music retail' },
        { instruction: 'Music royalties come in multiple forms: mechanical, performance, synchronization, and print.' },
        { instruction: 'The cat collects performance royalties every time its purr is streamed on Calm app.' },
      ],
      quiz: [
        { question: 'What is a sync (synchronization) royalty?', options: ['Payment for using music in visual media like TV, film, or advertisements', 'Synchronization of royalty payments across platforms', 'A royalty for live performances', 'A royalty for streaming only'], correctIndex: 0, explanation: 'Sync royalties are paid when music is used in synchronization with visual media such as movies, TV shows, commercials, or video games.' },
      ],
    },
    {
      id: 'entertainment-investing',
      slug: 'entertainment-investing-strategies',
      title: 'Entertainment Investing Strategies',
      description: 'Investing in music rights and entertainment assets.',
      commands: ['music', 'royalty', 'catalog'],
      steps: [
        { instruction: 'Build an entertainment portfolio: `royalty --portfolio --allocate "catalogs:60,royalty-funds:30,film-slate:10" --capital 500000`', command: 'royalty --portfolio --allocate "catalogs:60,royalty-funds:30,film-slate:10" --capital 500000', expectedOutput: 'Entertainment portfolio: $300K catalogs (8-12% target return), $150K royalty funds (7-9%, liquid), $50K film slate (15-25%, high risk, 3yr lock-up)' },
        { instruction: 'Entertainment assets offer diversification with low correlation to traditional markets.' },
        { instruction: 'The cat entertainment portfolio includes royalties from cat video compilations — evergreen content.' },
      ],
      quiz: [
        { question: 'What makes entertainment assets attractive for portfolio diversification?', options: ['Low correlation with traditional equity and bond markets', 'Guaranteed returns', 'High liquidity', 'Government backing'], correctIndex: 0, explanation: 'Entertainment assets like music royalties have low correlation to traditional financial markets, providing diversification benefits.' },
      ],
    },
  ],
}
