import type { Course } from '../lib/types'

export const depin: Course = {
  id: 'depin',
  slug: 'depin-physical-infrastructure',
  title: 'DePIN & Physical Infrastructure',
  description: 'Decentralized physical infrastructure, wireless, compute, and storage — the cat contributes its spare computing power (when not napping) to the DePIN network.',
  category: 'Crypto & Web3',
  difficulty: 'advanced',
  icon: '🏗️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'depin-basics',
      slug: 'depin-fundamentals',
      title: 'DePIN Fundamentals',
      description: 'Understanding decentralized physical infrastructure networks.',
      commands: ['depin', 'infrastructure', 'wireless', 'compute'],
      steps: [
        { instruction: 'Explore DePIN sectors: `depin --sectors --list`', command: 'depin --sectors --list', expectedOutput: 'DePIN sectors: Wireless (Helium, Pollen), Compute (Akash, Golem), Storage (Filecoin, Arweave), Sensors (Hivemapper, DIMO), Energy (React, Powerledger)' },
        { instruction: 'DePIN uses token incentives to build and maintain physical infrastructure networks.' },
        { instruction: 'The cat joined a DePIN wireless network — its collar now earns tokens as a hotspot.' },
      ],
      quiz: [
        { question: 'What is DePIN (Decentralized Physical Infrastructure Networks)?', options: ['Token-incentivized networks where participants deploy real-world physical infrastructure', 'A type of blockchain consensus mechanism', 'A DeFi protocol for lending', 'A new programming language'], correctIndex: 0, explanation: 'DePIN projects use token rewards to incentivize individuals and businesses to deploy physical infrastructure like wireless hotspots, sensors, and compute nodes.' },
      ],
    },
    {
      id: 'wireless-networks',
      slug: 'decentralized-wireless-networks',
      title: 'Decentralized Wireless Networks',
      description: 'Building wireless coverage through token incentives.',
      commands: ['wireless', 'depin', 'infrastructure'],
      steps: [
        { instruction: 'Analyze Helium network economics: `wireless --analyze --network helium --hotspots 1000000 --data-credits-usage 5000000`', command: 'wireless --analyze --network helium --hotspots 1000000 --data-credits-usage 5000000', expectedOutput: 'Helium network: 1M hotspots, 5M data credits used. Monthly earnings per hotspot: $12-45. Network coverage: 195 countries. IoT data transfer: 100M+ packets/day' },
        { instruction: 'Decentralized wireless networks reward hotspot operators for providing coverage.' },
        { instruction: 'The cat hotspot is on its cat tree — best coverage at the highest altitude in the house.' },
      ],
      quiz: [
        { question: 'How do participants earn rewards in decentralized wireless networks like Helium?', options: ['By deploying hotspots that provide wireless coverage and transfer data', 'By mining Bitcoin', 'By staking tokens only', 'By running a validator node'], correctIndex: 0, explanation: 'Participants deploy wireless hotspots that provide IoT or 5G coverage and are rewarded with network tokens for the coverage and data transfer they facilitate.' },
      ],
    },
    {
      id: 'compute-storage',
      slug: 'decentralized-compute-storage',
      title: 'Decentralized Compute & Storage',
      description: 'Renting and providing compute and storage resources.',
      commands: ['compute', 'depin', 'infrastructure'],
      steps: [
        { instruction: 'Compare decentralized storage costs: `compute --storage --compare --providers filecoin,arweave,sia --storage-size 1TB --duration 12mo`', command: 'compute --storage --compare --providers filecoin,arweave,sia --storage-size 1TB --duration 12mo', expectedOutput: 'Decentralized storage (1TB, 12mo): Filecoin $5-15/mo, Arweave $10-20 (one-time payment), Sia $3-8/mo. Cost vs AWS S3: 60-80% cheaper. Replication: 6-10x' },
        { instruction: 'Decentralized compute and storage networks offer cheaper alternatives to cloud providers.' },
        { instruction: 'The cat rents out its spare hard drive space for filecoin — mostly storing photos of cats.' },
      ],
      quiz: [
        { question: 'How do decentralized storage networks ensure data reliability?', options: ['Through cryptographic proofs and redundant replication across multiple independent nodes', 'By storing data on a single central server', 'Through blockchain consensus only', 'By relying on a single provider'], correctIndex: 0, explanation: 'Decentralized storage networks use proof-of-replication and proof-of-spacetime to verify that data is being stored redundantly across nodes.' },
      ],
    },
    {
      id: 'depin-investing',
      slug: 'depin-investing-strategies',
      title: 'Depin Investing & Token Economics',
      description: 'Evaluating DePIN projects as investments.',
      commands: ['depin', 'infrastructure'],
      steps: [
        { instruction: 'Evaluate a DePIN project: `depin --evaluate --project "Helium" --metrics "nodes,revenue,usage,team"`', command: 'depin --evaluate --project "Helium" --metrics "nodes,revenue,usage,team"', expectedOutput: 'Helium evaluation: Nodes 1M+ ✅, Revenue $5M/mo growing, Usage 100M packets/day ✅, Team strong ✅, Tokenomics inflationary ⚠️, Competition from WiFi ⚠️' },
        { instruction: 'DePIN investments require evaluating both token economics and real-world adoption metrics.' },
        { instruction: 'The cat evaluated a DePIN project — strong node growth but the tokenomics needed more catnip.' },
      ],
      quiz: [
        { question: 'What metrics are most important when evaluating DePIN projects?', options: ['Node count, revenue/usage growth, token economics, and real-world adoption', 'Only the token price', 'Only the number of Twitter followers', 'Only the founding team background'], correctIndex: 0, explanation: 'DePIN projects should be evaluated on real-world adoption (node count, usage), revenue generation, sustainable tokenomics, and team quality.' },
      ],
    },
  ],
}
