import type { Course } from '../lib/types'

export const mevBlockchainTrading: Course = {
  id: 'mev-blockchain-trading',
  slug: 'mev-and-blockchain-trading',
  title: 'MEV & Blockchain Trading',
  description: 'MEV, sandwich attacks, arbitrage, and frontrunning — the cat extracts value faster than you can say "purr."',
  category: 'Web3',
  difficulty: 'advanced',
  icon: '🥷',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'mev-intro',
      slug: 'mev-fundamentals',
      title: 'Miner Extractable Value',
      description: 'What MEV is and how it works.',
      commands: ['mev', 'mev analyze'],
      steps: [
        { instruction: 'Analyze MEV opportunities: `mev analyze --mempool --strategy arbitrage`', command: 'mev analyze --mempool --strategy arbitrage', expectedOutput: 'MEV opportunities found: 12 arbitrage, 3 sandwich, 5 liquidations — estimated daily value $45k' },
        { instruction: 'MEV is profit extracted by reordering, including, or excluding transactions in blocks.' },
        { instruction: 'The cat extracts MEV from the treat jar — reordering the queue for maximum payoff.' },
      ],
      quiz: [
        { question: 'What is MEV?', options: ['Profit extracted by manipulating transaction order in blocks', 'A type of cryptocurrency token', 'A mining algorithm', 'A smart contract standard'], correctIndex: 0, explanation: 'Miner Extractable Value refers to profits miners or validators can earn by strategically ordering transactions within a block.' },
      ],
    },
    {
      id: 'mev-arbitrage',
      slug: 'on-chain-arbitrage',
      title: 'On-Chain Arbitrage',
      description: 'Profiting from price differences across DEXes.',
      commands: ['arbitrage', 'arbitrage scan'],
      steps: [
        { instruction: 'Scan for DEX arbitrage opportunities: `arbitrage scan --min-profit 0.5 --max-gas 100`', command: 'arbitrage scan --min-profit 0.5 --max-gas 100', expectedOutput: 'Arbitrage opportunities: 5 identified — best: ETH/USDC on Uniswap vs SushiSwap, profit $1,250' },
        { instruction: 'Flash loans enable arbitrage without upfront capital.' },
        { instruction: 'The cat arbitrages between the indoor and outdoor food bowls.' },
      ],
      quiz: [
        { question: 'How do flash loans enable arbitrage?', options: ['Borrow, execute trade, repay in same transaction — no capital needed', 'They provide interest-free loans for a month', 'They are government-backed loans', 'They require no collateral ever'], correctIndex: 0, explanation: 'Flash loans let you borrow any amount as long as you repay within the same transaction, enabling capital-free arbitrage.' },
      ],
    },
    {
      id: 'mev-sandwich',
      slug: 'sandwich-attacks',
      title: 'Sandwich Attacks',
      description: 'How traders get sandwiched and lose.',
      commands: ['sandwich', 'sandwich simulate'],
      steps: [
        { instruction: 'Simulate a sandwich attack: `sandwich simulate --target tx --slippage 2`', command: 'sandwich simulate --target tx --slippage 2', expectedOutput: 'Sandwich simulation: attacker profit $340, victim slippage loss $290' },
        { instruction: 'A sandwich attack places a buy before and sell after a target transaction.' },
        { instruction: 'The cat was once sandwiched — now it checks for MEV bots before trading.' },
      ],
      quiz: [
        { question: 'How does a sandwich attack work?', options: ['Front-run a buy then back-run it after the victim\'s trade pushes price up', 'Steal the victim\'s private keys', 'Hack the victim\'s wallet address', 'Exploit a smart contract bug'], correctIndex: 0, explanation: 'The attacker sees a pending buy, places their own buy first (pushing price up), then sells after the victim buys at the inflated price.' },
      ],
    },
    {
      id: 'mev-flashbots',
      slug: 'flashbots-searchers',
      title: 'Flashbots & Searchers',
      description: 'Democratizing MEV extraction.',
      commands: ['flashbots', 'flashbots send'],
      steps: [
        { instruction: 'Send a bundle via Flashbots: `flashbots send --tx bundle.json --priority low`', command: 'flashbots send --tx bundle.json --priority low', expectedOutput: 'Bundle sent to Flashbots relay — included in block #19,245,001' },
        { instruction: 'Flashbots provides a private channel for MEV transactions without public mempool leakage.' },
        { instruction: 'The cat uses Flashbots to keep its trading strategy top secret.' },
      ],
      quiz: [
        { question: 'What problem does Flashbots solve?', options: ['Public mempool frontrunning risk through private transaction relay', 'Slow block confirmation times', 'High gas fees on Ethereum', 'Smart contract vulnerabilities'], correctIndex: 0, explanation: 'Flashbots lets searchers submit bundles directly to miners, bypassing the public mempool where frontrunners can see pending trades.' },
      ],
    },
  ],
}
