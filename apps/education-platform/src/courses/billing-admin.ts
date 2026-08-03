import type { Course } from '../lib/types'

export const billingAdmin: Course = {
  id: 'billing-admin',
  slug: 'billing-admin',
  title: 'Billing & Administration',
  description: 'Manage subscriptions, API keys, and monitor system health.',
  category: 'Admin',
  difficulty: 'beginner',
  icon: '⚙️',
  lessonCount: 3,
  estimatedMinutes: 15,
  lessons: [
    {
      id: 'ba-billing',
      slug: 'billing',
      title: 'Subscriptions & Billing',
      description: 'Upgrade, manage, or cancel your plan.',
      commands: ['billing', 'pricing', 'subscribe'],
      steps: [
        { instruction: 'View plans: `billing` or `pricing`', command: 'pricing', expectedOutput: 'Free, Pro ($116/mo), Enterprise (custom)' },
        { instruction: 'Manage subscription: `billing portal` or `subscribe`' },
        { instruction: 'Pro tier includes: AI advisor, strategy backtesting, paper trading, and more.' },
      ],
      quiz: [
        { question: 'What does the Pro tier cost per month?', options: ['$116', '$10', '$99', '$49'], correctIndex: 0, explanation: 'Pro tier is $116/month with advanced features like AI advisor and backtesting.' },
      ],
    },
    {
      id: 'ba-apikeys',
      slug: 'apikeys',
      title: 'API Key Administration',
      description: 'Create scoped API keys for programmatic access.',
      commands: ['apikey create', 'apikey list', 'apikey revoke'],
      steps: [
        { instruction: 'Create: `apikey create my-bot`', command: 'apikey create trading-bot', expectedOutput: 'Key + permissions created' },
        { instruction: 'List: `apikey list`', command: 'apikey list', expectedOutput: 'All keys with scope and status' },
        { instruction: 'Revoke: `apikey revoke <id>`', command: 'apikey revoke 1', expectedOutput: 'Key disabled' },
      ],
      quiz: [
        { question: 'What can API keys be used for?', options: ['Programmatic access to Miau Finance APIs', 'Only login', 'Only reading prices', 'Nothing yet'], correctIndex: 0, explanation: 'API keys provide programmatic access to Miau Finance APIs with scoped permissions.' },
      ],
    },
    {
      id: 'ba-system',
      slug: 'system',
      title: 'System Monitoring',
      description: 'Check platform health and performance.',
      commands: ['summary', 'ping', 'scorecard'],
      steps: [
        { instruction: 'Platform status: `summary` or `ping`', command: 'summary', expectedOutput: 'API health, uptime, user count' },
        { instruction: 'Performance scorecard: `scorecard`', command: 'scorecard', expectedOutput: 'System performance metrics and cat productivity score' },
      ],
      quiz: [
        { question: 'What does `summary` display?', options: ['Platform health and stats', 'Your portfolio summary', 'Market summary', 'News summary'], correctIndex: 0, explanation: '`summary` shows platform health, uptime, and usage statistics.' },
      ],
    },
  ],
}
