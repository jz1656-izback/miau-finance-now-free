import type { Course } from '../lib/types'

export const desci: Course = {
  id: 'desci',
  slug: 'decentralized-science',
  title: 'Decentralized Science (DeSci)',
  description: 'Research funding, IP-NFTs, science DAOs, and decentralized research — the cat funds the cure for catnip addiction.',
  category: 'Web3',
  difficulty: 'advanced',
  icon: '🔬',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'desci-basics',
      slug: 'desci-introduction',
      title: 'DeSci Fundamentals',
      description: 'What DeSci is and why it matters for research.',
      commands: ['desci overview', 'desci landscape'],
      steps: [
        { instruction: 'Get DeSci overview: `desci overview`', command: 'desci overview', expectedOutput: 'DeSci is a movement using Web3 to fund, conduct, and share scientific research. Key problems solved: closed access (80% of research behind paywalls), slow funding (18mo grant cycles), reproducibility crisis (70% of studies fail to replicate)' },
        { instruction: 'Traditional science is slow, opaque, and exclusionary. DeSci uses DAOs, tokens, and NFTs to fix this.' },
        { instruction: 'The cat believes DeSci will cure "catnip tolerance syndrome" within 5 years.' },
        { instruction: 'Check the DeSci landscape: `desci landscape`', command: 'desci landscape', expectedOutput: 'Top DeSci projects: VitaDAO (longevity, $50M treasury), Molecule (IP-NFTs, $20M), ResearchHub (decentralized peer review), BioDAO (biotech funding), AthenaDAO (women health research)' },
      ],
      quiz: [
        { question: 'What core problem does DeSci aim to solve in scientific research?', options: ['Slow funding cycles, closed-access publishing, reproducibility crisis, and lack of researcher incentives aligned with open science', 'Lack of scientists', 'Too much government regulation', 'Excessive research funding'], correctIndex: 0, explanation: 'DeSci addresses systemic issues: grant cycles take 12-18 months, 80% of research is behind paywalls, 70% of studies fail to replicate, and researchers lack incentives to share data and methods openly.' },
      ],
    },
    {
      id: 'ip-nfts',
      slug: 'ip-nfts-research',
      title: 'IP-NFTs & Research Funding',
      description: 'Tokenizing intellectual property for research.',
      commands: ['desci ipnft', 'desci ipnft --mint'],
      steps: [
        { instruction: 'Explore IP-NFT marketplace: `desci ipnft --marketplace`', command: 'desci ipnft --marketplace', expectedOutput: 'Available IP-NFTs: 1) Longevity Drug Target XYZ (VitaDAO, $500K), 2) ALS Gene Therapy (Molecule, $350K), 3) Psychedelic Depression Trial (PsyDAO, $200K). Avg yield: 12% from license royalties' },
        { instruction: 'IP-NFTs represent future royalty streams from licensed research — like patent-backed tokens.' },
        { instruction: 'Mint an IP-NFT for a research project: `desci ipnft --mint --project "Catnip Addiction Cure" --funding 100k --royalty 15%`', command: 'desci ipnft --mint --project "Catnip Addiction Cure" --funding 100k --royalty 15%', expectedOutput: 'IP-NFT minted: "Catnip Addiction Cure Research IP". Funding target: $100K (100,000 DESCI tokens at $1). Backers: 47 supporters. Royalty: 15% of future licensing. IP stored on IPFS: QmXyZ...' },
        { instruction: 'The cat owns an IP-NFT for a vibrating scratching post. The royalties fund more catnip research.' },
      ],
      quiz: [
        { question: 'How does an IP-NFT work for research funding?', options: ['An NFT that represents ownership of future royalty streams from a research project IP, allowing the public to fund science and earn returns', 'A digital certificate for attending a science conference', 'A token representing a PhD degree', 'A collectible image of a scientist'], correctIndex: 0, explanation: 'IP-NFTs (Intellectual Property NFTs) tokenize research IP, allowing backers to fund projects in exchange for future royalty streams from licensing, similar to how musicians tokenize future album royalties.' },
      ],
    },
    {
      id: 'science-daos',
      slug: 'science-daos-governance',
      title: 'Science DAOs & Governance',
      description: 'Decentralized research funding organizations.',
      commands: ['desci dao', 'desci dao --proposals'],
      steps: [
        { instruction: 'Check a science DAO treasury: `desci dao --name "VitaDAO" --treasury`', command: 'desci dao --name "VitaDAO" --treasury', expectedOutput: 'VitaDAO treasury: $52M total. $18M in stablecoins, $22M in tokens, $12M in IP-NFTs. Monthly research funding: $850K. Active proposals: 8. VITA token price: $4.20' },
        { instruction: 'Science DAOs pool capital to fund research and govern the IP portfolio through token voting.' },
        { instruction: 'Vote on a research proposal: `desci dao --vote --proposal 42 --decision for --rationale "promising mechanism"`', command: 'desci dao --vote --proposal 42 --decision for --rationale "promising mechanism"', expectedOutput: 'Vote cast: Proposal #42 — "Longevity drug screening pipeline" → FOR. Your voting power: 1,200 VITA. Current tally: 78% FOR, 15% AGAINST, 7% ABSTAIN. Quorum: reached (65%). Proposal likely to pass' },
        { instruction: 'The cat votes FOR any proposal that mentions "cat lifespan extension."' },
      ],
      quiz: [
        { question: 'How do Science DAOs decide which research to fund?', options: ['Token holders vote on research proposals, with funding allocated based on community governance and peer review within the DAO', 'A centralized committee of scientists decides', 'The government decides', 'Research is funded randomly through a lottery system'], correctIndex: 0, explanation: 'Science DAOs use token-based governance where holders vote on research proposals. Proposals typically go through community discussion, peer review by domain experts, and final token voting before funding is released.' },
      ],
    },
    {
      id: 'desci-future',
      slug: 'desci-future-impact',
      title: 'DeSci Impact & Future',
      description: 'How DeSci transforms research and biotech investing.',
      commands: ['desci impact', 'desci portfolio'],
      steps: [
        { instruction: 'Analyze DeSci investment portfolio: `desci portfolio --build --risk medium --capital 50k`', command: 'desci portfolio --build --risk medium --capital 50k', expectedOutput: 'DeSci portfolio ($50K): 40% IP-NFTs (early-stage research), 30% DAO tokens (VITA, BIO, RSC), 20% research tokens (specific projects), 10% stablecoin yield. Expected return: 25-40% IRR (venture-like)' },
        { instruction: 'DeSci creates liquid markets for research funding — previously only accessible to VCs and grants.' },
        { instruction: 'Track DeSci milestones: `desci impact --milestones --year 2025`', command: 'desci impact --milestones --year 2025', expectedOutput: '2025 milestones: 15 IP-NFTs reached clinical trials, 3 DAO-funded drugs received FDA approval, 200+ research papers published with open access via DeSci platforms, $500M total research funding through DAOs' },
        { instruction: 'The cat predicts DeSci will fund the cure for "Monday morning lack of motivation."' },
      ],
      quiz: [
        { question: 'What makes DeSci potentially transformative for biotech investing?', options: ['It creates liquid markets for early-stage research IP, allows retail investors to fund drug development, and aligns researcher incentives with open science', 'It replaces pharmaceutical companies entirely', 'It makes all drugs free', 'It eliminates the need for clinical trials'], correctIndex: 0, explanation: 'DeSci democratizes biotech investing by tokenizing research IP (IP-NFTs), creating liquid secondary markets, allowing retail participation in early-stage drug development, and using token incentives to promote open data and reproducible research.' },
      ],
    },
  ],
}
