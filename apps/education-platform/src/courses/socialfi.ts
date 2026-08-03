import type { Course } from '../lib/types'

export const socialfi: Course = {
  id: 'socialfi',
  slug: 'socialfi-creator-economy',
  title: 'SocialFi & Creator Economy',
  description: 'Social tokens, creator coins, fan tokens, and community ownership — the cat creates its own social token that can be earned by petting and spent on treats.',
  category: 'Crypto & Web3',
  difficulty: 'intermediate',
  icon: '👥',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'social-tokens',
      slug: 'social-token-basics',
      title: 'Social Token Basics',
      description: 'Understanding social and creator tokens.',
      commands: ['socialfi', 'creator-coin', 'fan-token'],
      steps: [
        { instruction: 'Explore social token types: `socialfi --types --list`', command: 'socialfi --types --list', expectedOutput: 'Social token types: Personal creator coins (Rally), Community tokens (Friends with Benefits), Fan tokens (Chiliz), Platform tokens (Mirror), NFT-based social tokens' },
        { instruction: 'Social tokens allow creators and communities to monetize directly.' },
        { instruction: 'The cat launched a personal social token — holders get exclusive access to purr videos.' },
      ],
      quiz: [
        { question: 'What is a social token?', options: ['A cryptocurrency issued by an individual or community to monetize and engage their audience', 'A token used for social media advertising', 'A government-issued digital currency for social programs', 'A token on social networks'], correctIndex: 0, explanation: 'Social tokens are creator- or community-issued cryptocurrencies that grant access to exclusive content, experiences, or community membership.' },
      ],
    },
    {
      id: 'creator-coins',
      slug: 'creator-coin-economics',
      title: 'Creator Coin Economics',
      description: 'How creators monetize through their own coins.',
      commands: ['creator-coin', 'socialfi', 'fan-token'],
      steps: [
        { instruction: 'Launch a creator coin: `creator-coin --launch --name "CAT" --supply 1000000 --initial-price 0.50 --benefits "exclusive-content,chat-access,voting"`', command: 'creator-coin --launch --name "CAT" --supply 1000000 --initial-price 0.50 --benefits "exclusive-content,chat-access,voting"', expectedOutput: 'CAT coin launched: 1M supply at $0.50 = $500K FDV. Creator allocation: 20% (locked 1yr). Benefits: exclusive purr videos, VIP chat, content voting rights' },
        { instruction: 'Creator coins let fans invest in a creator success while gaining access perks.' },
        { instruction: 'The cat creator coin CAT is trading at 2x — fans love the exclusive behind-the-scenes nap content.' },
      ],
      quiz: [
        { question: 'What value do creator coins provide to holders?', options: ['Access to exclusive content, community privileges, and potential financial upside from creator growth', 'Guaranteed dividends', 'Equity in the creator LLC', 'A salary from the creator'], correctIndex: 0, explanation: 'Creator coin holders gain access to exclusive content, community perks, and can benefit financially if the creator following and token value grows.' },
      ],
    },
    {
      id: 'fan-tokens',
      slug: 'fan-token-platforms',
      title: 'Fan Token Platforms',
      description: 'Sports and entertainment fan token ecosystems.',
      commands: ['fan-token', 'socialfi', 'creator-coin'],
      steps: [
        { instruction: 'Analyze fan token economics: `fan-token --analyze --club "FC Barcelona" --token BAR --market-cap 50M`', command: 'fan-token --analyze --club "FC Barcelona" --token BAR --market-cap 50M', expectedOutput: 'BAR fan token: $50M market cap, 10M tokens. Holders: 150K. Benefits: vote on kit design, goal celebration music, meet & greet. Revenue to club: $8M annually' },
        { instruction: 'Fan tokens give sports fans voting power on club decisions and access to experiences.' },
        { instruction: 'The cat bought fan tokens of its favorite cat sports league — now it votes on which catnip brand sponsors the matches.' },
      ],
      quiz: [
        { question: 'What can fan token holders typically vote on?', options: ['Club decisions like kit designs, celebration music, and community initiatives', 'Player transfers', 'Match results', 'Club ownership changes'], correctIndex: 0, explanation: 'Fan token holders typically vote on non-competitive club matters such as jersey designs, community initiatives, and match-day experiences.' },
      ],
    },
    {
      id: 'community-ownership',
      slug: 'community-ownership-socialfi',
      title: 'Community Ownership & DAOs',
      description: 'Community-owned social platforms and DAOs.',
      commands: ['socialfi', 'fan-token'],
      steps: [
        { instruction: 'Structure a community DAO: `socialfi --dao --name "CatLoversDAO" --token CATL --treasury 500000`', command: 'socialfi --dao --name "CatLoversDAO" --token CATL --treasury 500000', expectedOutput: 'CatLoversDAO: 10K members, $500K treasury in CATL tokens. Governance: 1 token = 1 vote. Proposals: content grants, platform upgrades, partnership votes' },
        { instruction: 'Community-owned platforms distribute governance and ownership to participants.' },
        { instruction: 'The CatLoversDAO voted to allocate 10% of treasury to a global cat video archive.' },
      ],
      quiz: [
        { question: 'How do community-owned social platforms differ from traditional social media?', options: ['Users have governance rights and share in the platform value through tokens', 'They are always free to use', 'They have no moderation', 'They are owned by a single corporation'], correctIndex: 0, explanation: 'Community-owned platforms distribute governance tokens to users, allowing them to vote on platform decisions and benefit from platform value appreciation.' },
      ],
    },
  ],
}
