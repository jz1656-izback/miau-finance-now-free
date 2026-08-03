import type { Course } from '../lib/types'

export const nftsDigitalAssets: Course = {
  id: 'nfts-digital-assets',
  slug: 'nfts-and-digital-assets',
  title: 'NFTs & Digital Assets',
  description: 'NFT valuation, digital art, collectibles, and royalties — the cat mints its whiskers as NFTs.',
  category: 'Web3',
  difficulty: 'intermediate',
  icon: '🎨',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'nft-intro',
      slug: 'nft-fundamentals',
      title: 'NFT Fundamentals',
      description: 'What NFTs are and how they work.',
      commands: ['nft', 'nft info'],
      steps: [
        { instruction: 'Look up an NFT collection: `nft info --collection "Bored Ape Yacht Club"`', command: 'nft info --collection "Bored Ape Yacht Club"', expectedOutput: 'Collection: Bored Ape Yacht Club — floor price 32.5 ETH, volume 1,240 ETH (7d)' },
        { instruction: 'NFTs are unique digital tokens verified on a blockchain.' },
        { instruction: 'The cat owns NFT #1 — a portrait titled "Distinguished Gentleman."' },
      ],
      quiz: [
        { question: 'What makes an NFT different from a fungible token?', options: ['Each NFT is unique and cannot be exchanged 1:1', 'NFTs are always worth more than fungible tokens', 'NFTs cannot be traded', 'NFTs are stored off-chain'], correctIndex: 0, explanation: 'Non-fungible tokens are unique digital assets that cannot be exchanged on a one-to-one basis like cryptocurrencies.' },
      ],
    },
    {
      id: 'nft-minting',
      slug: 'minting-nfts',
      title: 'Minting NFTs',
      description: 'Creating and launching NFT collections.',
      commands: ['mint', 'mint nft'],
      steps: [
        { instruction: 'Mint a new NFT: `mint nft --image whiskers.jpg --name "Cat Whiskers #1" --royalty 5`', command: 'mint nft --image whiskers.jpg --name "Cat Whiskers #1" --royalty 5', expectedOutput: 'NFT minted: Cat Whiskers #1 (0xabcd...ef01) — 5% royalty set on secondary sales' },
        { instruction: 'Royalties pay the original creator a percentage of each secondary sale.' },
        { instruction: 'The cat mints a new selfie every morning. The internet deserves it.' },
      ],
      quiz: [
        { question: 'What are NFT royalties?', options: ['Ongoing payments to the original creator on secondary sales', 'The initial minting fee paid to the blockchain', 'Tax paid to the government on NFT sales', 'Revenue share for the marketplace'], correctIndex: 0, explanation: 'Royalties automatically pay the original creator a percentage (typically 5-10%) every time the NFT resells.' },
      ],
    },
    {
      id: 'nft-collections',
      slug: 'nft-collections-valuation',
      title: 'Collections & Valuation',
      description: 'Evaluating NFT projects and floors.',
      commands: ['collection', 'collection analyze'],
      steps: [
        { instruction: 'Analyze an NFT collection: `collection analyze --collection "CryptoPunks" --metric floor,volume,holders`', command: 'collection analyze --collection "CryptoPunks" --metric floor,volume,holders', expectedOutput: 'CryptoPunks: floor 49.9 ETH, volume 890 ETH (7d), 2,340 unique holders' },
        { instruction: 'Floor price is the cheapest NFT in a collection — a key valuation metric.' },
        { instruction: 'The cat\'s NFT collection valuation: priceless + one tuna.' },
      ],
      quiz: [
        { question: 'What does NFT floor price represent?', options: ['The lowest listed price for any item in the collection', 'The average price of all sales', 'The highest price ever paid', 'The minimum bid across all listings'], correctIndex: 0, explanation: 'Floor price is the minimum asking price for any NFT in a collection, serving as a baseline valuation metric.' },
      ],
    },
    {
      id: 'nft-royalties',
      slug: 'nft-royalties-licensing',
      title: 'Royalties & Licensing',
      description: 'Earning from digital creations.',
      commands: ['royalty', 'royalty claim'],
      steps: [
        { instruction: 'Claim accumulated royalties: `royalty claim --wallet 0xabcd...ef01`', command: 'royalty claim --wallet 0xabcd...ef01', expectedOutput: '3.42 ETH royalties claimed and transferred to wallet 0xabcd...ef01' },
        { instruction: 'Smart contracts automatically enforce royalty payments on every resale.' },
        { instruction: 'The cat\'s royalties buy exactly one tuna can per month. Sustainable.' },
      ],
      quiz: [
        { question: 'How do NFT smart contracts enforce royalties?', options: ['The contract code automatically deducts royalties on secondary sales', 'Marketplaces manually send payments to creators', 'Buyers voluntarily pay creators', 'Royalties are enforced by law'], correctIndex: 0, explanation: 'NFT smart contracts encode royalty logic that automatically diverts a percentage of each sale to the creator\'s wallet.' },
      ],
    },
  ],
}
