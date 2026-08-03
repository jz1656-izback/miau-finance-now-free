import type { Course } from '../lib/types'

export const defiWeb3: Course = {
  id: 'defi-web3',
  slug: 'defi-web3',
  title: 'DeFi & Web3',
  description: 'Connect wallets, explore DeFi protocols, and track NFT portfolios.',
  category: 'DeFi',
  difficulty: 'advanced',
  icon: '⛓️',
  lessonCount: 3,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'dw-wallet',
      slug: 'wallet',
      title: 'Wallet Connections',
      description: 'Connect crypto wallets via WalletConnect.',
      commands: ['wallet connect', 'wallet balance', 'wallet sessions', 'wallet chains'],
      steps: [
        { instruction: 'Connect a wallet: `wallet connect`', command: 'wallet connect', expectedOutput: 'WalletConnect QR/URI for scanning' },
        { instruction: 'Check balances: `wallet balance`', command: 'wallet balance', expectedOutput: 'Token balances across chains' },
        { instruction: 'View sessions: `wallet sessions` or `wallet list`' },
        { instruction: 'Supported chains: `wallet chains`', command: 'wallet chains', expectedOutput: 'Ethereum, Polygon, Solana, and more' },
      ],
      quiz: [
        { question: 'Which protocol connects wallets to Miau Finance?', options: ['WalletConnect', 'MetaMask SDK', 'Coinbase SDK', 'RainbowKit'], correctIndex: 0, explanation: 'Miau Finance uses WalletConnect for wallet integration.' },
      ],
    },
    {
      id: 'dw-protocols',
      slug: 'protocols',
      title: 'DeFi Protocols',
      description: 'Explore lending, DEX, and yield protocols.',
      commands: ['defi protocols'],
      steps: [
        { instruction: 'List protocols: `defi protocols`', command: 'defi protocols', expectedOutput: 'Uniswap, Aave, Curve, Lido, MakerDAO status' },
        { instruction: 'Shows TVL, APY, and key metrics for each protocol.' },
        { instruction: 'DEX volume, lending rates, and staking yields at a glance.' },
      ],
      quiz: [
        { question: 'What information does `defi protocols` show?', options: ['TVL, APY, and protocol metrics', 'Only token prices', 'Wallet balances', 'NFT listings'], correctIndex: 0, explanation: '`defi protocols` displays Total Value Locked, APY rates, and other DeFi metrics.' },
      ],
    },
    {
      id: 'dw-nft',
      slug: 'nft',
      title: 'NFT Portfolio',
      description: 'Track your NFT collection.',
      commands: ['wallet balance'],
      steps: [
        { instruction: 'Your wallet balance view includes NFT holdings when connected.' },
        { instruction: 'Track NFT floor prices, collection stats, and portfolio value.' },
        { instruction: 'Multi-chain support: Ethereum, Solana NFTs tracked.' },
      ],
      quiz: [
        { question: 'Where can you see your NFTs in Miau Finance?', options: ['In the wallet balance view', 'A separate NFT command', 'There is no NFT tracking', 'Only in the marketplace'], correctIndex: 0, explanation: 'NFT holdings are shown within the wallet balance view when a wallet is connected.' },
      ],
    },
  ],
}
