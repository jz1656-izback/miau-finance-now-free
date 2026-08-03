import type { Course } from '../lib/types'

export const gitForFinance: Course = {
  id: 'git-finance',
  slug: 'git-for-finance',
  title: 'Git for Finance',
  description: 'Version control, branching, and collaboration for quant teams — the cat tracks every code change like a hawk.',
  category: 'Tools & Workflow',
  difficulty: 'beginner',
  icon: '🔀',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'git-basics',
      slug: 'git-basics-finance',
      title: 'Git Basics for Quants',
      description: 'Init, add, commit, status.',
      commands: ['git', 'git init'],
      steps: [
        { instruction: 'Initialize a repository: `git init quant-strategies`', command: 'git init quant-strategies', expectedOutput: 'Initialized empty Git repository in quant-strategies/.git/' },
        { instruction: 'Git tracks every change so you can revert if your strategy blows up.' },
        { instruction: 'The cat commits every time it catches a mouse — atomic commits only.' },
      ],
      quiz: [
        { question: 'Why use version control for quant research?', options: ['Track changes, collaborate, and revert mistakes', 'Store large datasets efficiently', 'Deploy strategies automatically', 'Encrypt trading algorithms'], correctIndex: 0, explanation: 'Git provides a complete history of changes, enabling collaboration and safe experimentation through branching.' },
      ],
    },
    {
      id: 'git-branching',
      slug: 'branching-strategies',
      title: 'Branching Strategies',
      description: 'Feature branches, main branch protection.',
      commands: ['branch', 'branch create'],
      steps: [
        { instruction: 'Create a feature branch: `branch create --name momentum-strategy-v2`', command: 'branch create --name momentum-strategy-v2', expectedOutput: 'Switched to new branch momentum-strategy-v2' },
        { instruction: 'Keep main branch deployable — experiment in feature branches.' },
        { instruction: 'The cat\'s branches are named tuna-experiment and nap-refactor.' },
      ],
      quiz: [
        { question: 'What is the purpose of feature branches?', options: ['Isolate development work without affecting the main codebase', 'Store completed features permanently', 'Track production releases', 'Run automated tests'], correctIndex: 0, explanation: 'Feature branches let you develop and test changes in isolation before merging into the main branch.' },
      ],
    },
    {
      id: 'git-commits',
      slug: 'writing-good-commits',
      title: 'Writing Good Commits',
      description: 'Atomic commits and meaningful messages.',
      commands: ['commit', 'commit amend'],
      steps: [
        { instruction: 'Make an atomic commit: `commit --message "feat: add volatility surface calculation"`', command: 'commit --message "feat: add volatility surface calculation"', expectedOutput: '[main abc1234] feat: add volatility surface calculation' },
        { instruction: 'Write descriptive commit messages — future you will thank present you.' },
        { instruction: 'The cat uses emoji commits: 🐟 for features, 🐛 for bug fixes.' },
      ],
      quiz: [
        { question: 'What makes a good commit message?', options: ['Clear subject line with context and scope', 'One-word descriptions like "fix"', 'Just the ticket number', 'Default commit message is fine'], correctIndex: 0, explanation: 'Good commit messages have a concise subject line with scope and provide context about what and why the change was made.' },
      ],
    },
    {
      id: 'git-collab',
      slug: 'collaboration-merge-conflicts',
      title: 'Collaboration & Merge Conflicts',
      description: 'Pull requests, code review, resolving conflicts.',
      commands: ['merge', 'merge resolve'],
      steps: [
        { instruction: 'Merge a feature branch: `merge --from momentum-strategy-v2 --into main`', command: 'merge --from momentum-strategy-v2 --into main', expectedOutput: 'Merge successful: momentum-strategy-v2 into main (3 commits)' },
        { instruction: 'Resolve merge conflicts by editing the conflicted files and committing.' },
        { instruction: 'The cat resolves merge conflicts by napping on the keyboard until they disappear.' },
      ],
      quiz: [
        { question: 'What causes a merge conflict?', options: ['Two branches modified the same part of the same file', 'One branch deleted a file', 'The remote repository is down', 'The repository is corrupted'], correctIndex: 0, explanation: 'Merge conflicts occur when different branches have competing changes to the same line or section of a file.' },
      ],
    },
  ],
}
