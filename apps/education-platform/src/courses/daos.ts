import type { Course } from '../lib/types'

export const daosGovernance: Course = {
  id: 'daos-governance',
  slug: 'daos-and-governance',
  title: 'DAOs & Governance',
  description: 'DAO structure, token voting, and treasury management — the cat runs a DAO where every vote is "more tuna."',
  category: 'Web3',
  difficulty: 'advanced',
  icon: '🗳️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'dao-intro',
      slug: 'dao-fundamentals',
      title: 'DAO Fundamentals',
      description: 'What DAOs are and how they work.',
      commands: ['dao', 'dao info'],
      steps: [
        { instruction: 'Look up a DAO: `dao info --name "Uniswap DAO"`', command: 'dao info --name "Uniswap DAO"', expectedOutput: 'Uniswap DAO: 245k members, 480M UNI staked, treasury $4.2B' },
        { instruction: 'DAOs are organizations governed by code and token votes, not people.' },
        { instruction: 'The cat\'s DAO is called PurrDAO — all decisions require 51% catnip majority.' },
      ],
      quiz: [
        { question: 'What is a DAO?', options: ['A decentralized autonomous organization governed by smart contracts', 'A traditional company with digital shares', 'A type of cryptocurrency exchange', 'A government regulatory body'], correctIndex: 0, explanation: 'A DAO is an organization represented by rules encoded as smart contracts, controlled by token-holder votes rather than central leadership.' },
      ],
    },
    {
      id: 'dao-voting',
      slug: 'token-voting-mechanisms',
      title: 'Token Voting Mechanisms',
      description: 'How proposals pass and fail.',
      commands: ['proposal', 'proposal create'],
      steps: [
        { instruction: 'Create a governance proposal: `proposal create --dao "PurrDAO" --title "Increase Tuna Budget" --description "Allocate 10% of treasury to tuna procurement"`', command: 'proposal create --dao "PurrDAO" --title "Increase Tuna Budget" --description "Allocate 10% of treasury to tuna procurement"', expectedOutput: 'Proposal #42 created — voting opens in 24 hours, quorum required: 4M tokens' },
        { instruction: 'Most DAOs require a minimum quorum of token votes for proposals to pass.' },
        { instruction: 'The cat votes YES on every proposal. Yes, even the questionable ones.' },
      ],
      quiz: [
        { question: 'What is quorum in DAO voting?', options: ['The minimum number of votes required for a proposal to be valid', 'The maximum number of votes allowed', 'The percentage of yes votes needed to pass', 'The time window for voting'], correctIndex: 0, explanation: 'Quorum ensures decisions have sufficient participation by requiring a minimum threshold of token votes.' },
      ],
    },
    {
      id: 'dao-treasury',
      slug: 'treasury-management',
      title: 'Treasury Management',
      description: 'Managing DAO funds and assets.',
      commands: ['vote', 'vote cast'],
      steps: [
        { instruction: 'Cast your vote on a proposal: `vote cast --proposal 42 --option yes --amount 10000`', command: 'vote cast --proposal 42 --option yes --amount 10000', expectedOutput: 'Vote cast: Proposal #42 — YES (10,000 tokens). Current tally: 2.1M YES, 890k NO' },
        { instruction: 'DAOs use multi-sig wallets for treasury security.' },
        { instruction: 'The cat\'s treasury holds 100% tuna-backed assets.' },
      ],
      quiz: [
        { question: 'Why do DAOs use multi-sig wallets?', options: ['Require multiple signers to approve transactions for security', 'Allow anyone to spend treasury funds', 'Speed up transaction processing', 'Reduce gas fees on transactions'], correctIndex: 0, explanation: 'Multi-signature wallets require several authorized signers to approve any transaction, preventing unilateral fund movement.' },
      ],
    },
    {
      id: 'dao-governance',
      slug: 'governance-best-practices',
      title: 'Governance Best Practices',
      description: 'Running effective decentralized orgs.',
      commands: ['treasury', 'treasury report'],
      steps: [
        { instruction: 'Generate a treasury report: `treasury report --dao "PurrDAO" --format json`', command: 'treasury report --dao "PurrDAO" --format json', expectedOutput: 'Treasury report: 500 ETH, 1.2M stablecoins, 50 NFTs, 10,000 tuna cans (in-kind)' },
        { instruction: 'Good governance requires transparent treasury reporting and clear proposal processes.' },
        { instruction: 'The cat delegates its votes to a trusted feline representative.' },
      ],
      quiz: [
        { question: 'What is a common challenge for DAO governance?', options: ['Low voter participation and concentration of voting power', 'Too many people wanting to vote', 'Excessive transparency in operations', 'Overabundance of treasury funds'], correctIndex: 0, explanation: 'Many DAOs face low voter turnout and concentration of tokens among few holders, creating centralization risks.' },
      ],
    },
  ],
}
