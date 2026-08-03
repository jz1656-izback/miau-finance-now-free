import type { Course } from '../lib/types'

export const gettingStarted: Course = {
  id: 'getting-started',
  slug: 'getting-started',
  title: 'Getting Started',
  description: 'Master the basics — login, explore the terminal, and make the cat proud.',
  category: 'Platform',
  difficulty: 'beginner',
  icon: '🐱',
  lessonCount: 5,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'gs-welcome',
      slug: 'welcome',
      title: 'Welcome to Miau Finance',
      description: 'Your first steps in the terminal.',
      commands: ['help', 'clear'],
      steps: [
        { instruction: 'Type `help` to see all available commands.', command: 'help', expectedOutput: 'HELP — all commands listed' },
        { instruction: 'Type `next` to continue.', hint: 'You can also type help anytime to see all commands' },
        { instruction: 'Type `clear` to wipe the screen and start fresh.', command: 'clear', expectedOutput: 'Screen cleared, ready for input' },
      ],
      quiz: [
        { question: 'Which command shows all available commands?', options: ['help', 'list', 'show', 'commands'], correctIndex: 0, explanation: '`help` displays the full command reference.' },
      ],
    },
    {
      id: 'gs-login',
      slug: 'login',
      title: 'Authentication',
      description: 'Log in, log out, and check who you are.',
      commands: ['login', 'logout', 'whoami'],
      steps: [
        { instruction: 'Log in with `login <username>`, then type your password at the masked prompt (it is never echoed).', command: 'login <username>', expectedOutput: 'Authenticated as <username>' },
        { instruction: 'Verify your identity with `whoami`.', command: 'whoami', expectedOutput: 'Your username and role displayed' },
        { instruction: 'Log out with `logout`.', command: 'logout', expectedOutput: 'Logged out' },
      ],
      quiz: [
        { question: 'How do you check who you are logged in as?', options: ['whoami', 'login status', 'user', 'identity'], correctIndex: 0, explanation: '`whoami` shows your current user identity.' },
      ],
    },
    {
      id: 'gs-themes',
      slug: 'themes',
      title: 'Themes & Personalization',
      description: 'Switch terminal themes and customize your experience.',
      commands: ['theme'],
      steps: [
        { instruction: 'List available themes: `theme list`', command: 'theme list', expectedOutput: 'Available themes displayed' },
        { instruction: 'Switch to a dark theme: `theme dark`', command: 'theme dark', expectedOutput: 'Theme changed' },
        { instruction: 'Try other themes: `theme retro`, `theme miau`', command: 'theme miau', expectedOutput: 'Classic miau green theme' },
      ],
      quiz: [
        { question: 'Which command changes the terminal appearance?', options: ['theme', 'style', 'color', 'mode'], correctIndex: 0, explanation: '`theme [name]` switches between themes.' },
      ],
    },
    {
      id: 'gs-cat',
      slug: 'cat-fun',
      title: 'Cat Commands & Fun',
      description: 'The cat is your companion. Pet it, get jokes, and collect cats.',
      commands: ['cat', 'miau', 'joke', 'cats', 'panic', 'sudo'],
      steps: [
        { instruction: 'Pet the cat: `cat`', command: 'cat', expectedOutput: 'Cat ASCII art appears' },
        { instruction: 'Get a cat fact: `cats`', command: 'cats', expectedOutput: 'Random cat fact displayed' },
        { instruction: 'Get a joke: `joke`', command: 'joke', expectedOutput: 'A cat-themed finance joke' },
        { instruction: 'Try the boss key: `panic` — hides everything!', command: 'panic', expectedOutput: 'Screen goes blank' },
      ],
      quiz: [
        { question: 'What does the `panic` command do?', options: ['Hides the terminal (boss key)', 'Deletes your data', 'Logs you out', 'Nothing'], correctIndex: 0, explanation: '`panic` is the boss key — instantly hides the terminal.' },
      ],
    },
    {
      id: 'gs-navigation',
      slug: 'navigation',
      title: 'Terminal Navigation',
      description: 'Move around the terminal like a pro.',
      commands: ['exit', 'back', 'clear'],
      steps: [
        { instruction: 'Exit split mode or go back: `exit` or `back`', command: 'exit', expectedOutput: 'Returns to main view' },
        { instruction: 'Use Ctrl+R to search your command history.' },
        { instruction: 'Clear screen anytime: `clear`', command: 'clear', expectedOutput: 'Clean slate' },
      ],
      quiz: [
        { question: 'What key combination searches command history?', options: ['Ctrl+R', 'Ctrl+F', 'Ctrl+S', 'Ctrl+H'], correctIndex: 0, explanation: 'Ctrl+R opens the history search.' },
      ],
    },
  ],
}
