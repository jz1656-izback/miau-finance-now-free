import type { Course } from '../lib/types'

export const platformFeatures: Course = {
  id: 'platform-features',
  slug: 'platform-features',
  title: 'Platform Features',
  description: 'Map, Catberg, themes, journaling, and hidden gems.',
  category: 'Platform',
  difficulty: 'beginner',
  icon: '🎮',
  lessonCount: 5,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'pf-map',
      slug: 'map',
      title: 'World Map & Globe',
      description: 'Live trading desk with a 3D globe.',
      commands: ['map', 'heatmap', 'split'],
      steps: [
        { instruction: 'Toggle the globe: `map`', command: 'map', expectedOutput: '3D globe overlay with country heatmap' },
        { instruction: 'Sector heatmap: `heatmap`', command: 'heatmap', expectedOutput: 'Sector correlation heatmap displayed' },
        { instruction: 'Split terminal: `split`', command: 'split', expectedOutput: 'Split-screen view activated' },
        { instruction: 'The globe shows: catboats on trade routes, smart money jets, ISS, and rocket launches.' },
      ],
      quiz: [
        { question: 'What does the `map` command show?', options: ['3D globe with live market data', 'A static image', 'Your portfolio map', 'A road map'], correctIndex: 0, explanation: '`map` toggles an interactive 3D globe with live market data, trade routes, and space events.' },
      ],
    },
    {
      id: 'pf-catberg',
      slug: 'catberg',
      title: 'Catberg Bloomberg Terminal',
      description: '41 Bloomberg-style function codes with cat commentary.',
      commands: ['catberg'],
      steps: [
        { instruction: 'Open Catberg: `catberg WEI`', command: 'catberg WEI', expectedOutput: 'World Equity Index view, Bloomberg-style' },
        { instruction: 'Try popular functions: `catberg N` (news), `catberg DES` (description), `catberg GPO` (graphical overview).' },
        { instruction: 'Every panel includes cat commentary — "The Cat, CFA" provides market wisdom.' },
        { instruction: 'F1-F6 function keys, real-time ticker bar, and 7% cat walk interruptions.' },
      ],
      quiz: [
        { question: 'What is Catberg?', options: ['Bloomberg terminal emulation', 'A cat game', 'A mountain', 'A trading bot'], correctIndex: 0, explanation: 'Catberg emulates a Bloomberg terminal with 41 function codes and cat-themed commentary.' },
      ],
    },
    {
      id: 'pf-chaos',
      slug: 'chaos',
      title: 'Easter Eggs',
      description: 'Discover hidden features and fun modes.',
      commands: ['chaos', 'hack', 'sudo', 'miau', 'cats', 'joke'],
      steps: [
        { instruction: 'Toggle CHAOS MODE: `chaos`', command: 'chaos', expectedOutput: 'Random cat interventions in your terminal' },
        { instruction: 'Simulate a hack: `hack`', command: 'hack', expectedOutput: 'Cyber attack simulation with cat defense' },
        { instruction: 'Pretend root: `sudo rm -rf /` (safe, it is just for fun)', command: 'sudo whoami', expectedOutput: 'Cat pretends to be root' },
        { instruction: 'Display MiauPapers: `miaupapers` or `papers`' },
      ],
      quiz: [
        { question: 'What does CHAOS MODE do?', options: ['Random cat interventions in commands', 'Deletes your data', 'Crashes the terminal', 'Changes the language'], correctIndex: 0, explanation: 'CHAOS MODE adds random cat commentary and effects to your terminal session.' },
      ],
    },
    {
      id: 'pf-journal',
      slug: 'journal',
      title: 'Trading Journal',
      description: 'Log your trades and track your learning.',
      commands: ['journal add', 'journal list', 'journal clear'],
      steps: [
        { instruction: 'Add an entry: `journal add bought AAPL at 180, good earnings report`', command: 'journal add bought TSLA at 250', expectedOutput: 'Entry saved' },
        { instruction: 'Review entries: `journal list`', command: 'journal list', expectedOutput: 'Your journal entries with timestamps' },
        { instruction: 'Clear journal: `journal clear`' },
      ],
      quiz: [
        { question: 'What is the trading journal for?', options: ['Logging trades and thoughts', 'Automatic trading', 'Publishing research', 'Nothing'], correctIndex: 0, explanation: 'The trading journal lets you log trades with notes for later review and learning.' },
      ],
    },
    {
      id: 'pf-achievements',
      slug: 'achievements',
      title: 'Achievements & Progress',
      description: 'Earn badges, track progress, and climb the leaderboard.',
      commands: ['achievements', 'leaderboard', 'scorecard'],
      steps: [
        { instruction: 'View achievements: `achievements`', command: 'achievements', expectedOutput: 'Your earned badges and unlock progress' },
        { instruction: 'Leaderboard: `leaderboard` — see how you rank against other traders.' },
        { instruction: 'Scorecard: `scorecard` — your overall platform activity and Miau Score.' },
      ],
      quiz: [
        { question: 'What is the Miau Score?', options: ['Sharpe ratio × ESG × diversification', 'Number of cat commands used', 'Portfolio value', 'Trading frequency'], correctIndex: 0, explanation: 'Miau Score = Sharpe × ESG × Diversification — a holistic performance metric.' },
      ],
    },
  ],
}
