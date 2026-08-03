import type { Course } from '../lib/types'

export const brokersApis: Course = {
  id: 'brokers-apis',
  slug: 'brokers-apis',
  title: 'Brokers & API Keys',
  description: 'Connect to real brokers and manage your API credentials.',
  category: 'Trading',
  difficulty: 'advanced',
  icon: '🔌',
  lessonCount: 3,
  estimatedMinutes: 15,
  lessons: [
    {
      id: 'ba-brokers',
      slug: 'brokers',
      title: 'Broker Connections',
      description: 'Connect to Alpaca, IB, and other brokers.',
      commands: ['broker list', 'broker connect', 'broker balance', 'broker positions', 'broker submit'],
      steps: [
        { instruction: 'List connected brokers: `broker list`', command: 'broker list', expectedOutput: 'Active broker connections' },
        { instruction: 'Connect a broker: `broker connect alpaca`', command: 'broker connect alpaca', expectedOutput: 'Broker connection established' },
        { instruction: 'Check balance: `broker balance alpaca`', command: 'broker balance', expectedOutput: 'Account balance and buying power' },
        { instruction: 'View positions: `broker positions`' },
        { instruction: 'Submit an order: `broker submit alpaca AAPL buy 10`' },
      ],
      quiz: [
        { question: 'Which command creates a broker connection?', options: ['broker connect', 'broker list', 'connect', 'login broker'], correctIndex: 0, explanation: '`broker connect <name>` establishes a broker connection.' },
      ],
    },
    {
      id: 'ba-apikeys',
      slug: 'apikeys',
      title: 'API Key Management',
      description: 'Create, list, and revoke API keys for programmatic access.',
      commands: ['apikey create', 'apikey list', 'apikey revoke'],
      steps: [
        { instruction: 'Create an API key: `apikey create my-app`', command: 'apikey create trading-bot', expectedOutput: 'API key created with permissions' },
        { instruction: 'List keys: `apikey list`', command: 'apikey list', expectedOutput: 'All your API keys with status' },
        { instruction: 'Revoke a key: `apikey revoke <id>`', command: 'apikey revoke 1', expectedOutput: 'Key revoked' },
      ],
      quiz: [
        { question: 'What does `apikey revoke` do?', options: ['Disables an API key', 'Creates a new key', 'Lists keys', 'Changes key permissions'], correctIndex: 0, explanation: '`apikey revoke <id>` permanently disables an API key.' },
      ],
    },
    {
      id: 'ba-billing',
      slug: 'billing',
      title: 'Billing & Subscriptions',
      description: 'View pricing plans and manage your subscription.',
      commands: ['billing', 'pricing', 'subscribe'],
      steps: [
        { instruction: 'View pricing: `billing` or `pricing`', command: 'pricing', expectedOutput: 'Free, Pro, and Enterprise plans displayed' },
        { instruction: 'Manage subscription: `billing portal` or `subscribe`', command: 'subscribe', expectedOutput: 'Subscription management info' },
      ],
      quiz: [
        { question: 'How many subscription tiers are there?', options: ['3 (Free, Pro, Enterprise)', '2', '5', '1'], correctIndex: 0, explanation: 'Miau Finance offers Free, Pro, and Enterprise tiers.' },
      ],
    },
  ],
}
