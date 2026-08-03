import type { Course } from '../lib/types'

export const socialFeatures: Course = {
  id: 'social-features',
  slug: 'social-features',
  title: 'Social Trading',
  description: 'Share portfolios, follow traders, and compete on leaderboards.',
  category: 'Social',
  difficulty: 'beginner',
  icon: '👥',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'sf-share',
      slug: 'share',
      title: 'Sharing Portfolios',
      description: 'Share your portfolio publicly with a link.',
      commands: ['share'],
      steps: [
        { instruction: 'Share a portfolio: `share 1`', command: 'share 1', expectedOutput: 'Public share link generated' },
        { instruction: 'The link can be viewed by anyone — no login required.' },
        { instruction: 'Great for showing off your returns or getting feedback.' },
      ],
      quiz: [
        { question: 'Who can view a shared portfolio link?', options: ['Anyone with the link', 'Only logged-in users', 'Only followers', 'Only you'], correctIndex: 0, explanation: 'Shared portfolio links are public — anyone with the link can view them.' },
      ],
    },
    {
      id: 'sf-feed',
      slug: 'feed',
      title: 'Activity Feed',
      description: 'See what traders are doing.',
      commands: ['feed', 'comments'],
      steps: [
        { instruction: 'View social feed: `feed`', command: 'feed', expectedOutput: 'Recent trading activity from the community' },
        { instruction: 'Filter by type: `feed trades` or `feed achievements`' },
        { instruction: 'Comment on activity: `comments <activity_id>`', command: 'comments 1', expectedOutput: 'Comment thread displayed' },
      ],
      quiz: [
        { question: 'What does the `feed` command show?', options: ['Community trading activity', 'Your portfolio', 'Market data', 'News'], correctIndex: 0, explanation: '`feed` shows recent trading activity, shares, and achievements from the community.' },
      ],
    },
    {
      id: 'sf-profile',
      slug: 'profile',
      title: 'User Profiles',
      description: 'View profiles and follow other traders.',
      commands: ['profile', 'follow', 'unfollow'],
      steps: [
        { instruction: 'View a profile: `profile trader123`', command: 'profile admin', expectedOutput: 'User stats, badges, and recent activity' },
        { instruction: 'Follow a trader: `follow trader123`', command: 'follow admin', expectedOutput: 'Now following this user' },
        { instruction: 'Unfollow: `unfollow trader123`' },
      ],
      quiz: [
        { question: 'How do you follow another trader?', options: ['follow <username>', 'subscribe <username>', 'add friend <username>', 'track <username>'], correctIndex: 0, explanation: '`follow <username>` adds a trader to your following list.' },
      ],
    },
    {
      id: 'sf-leaderboard',
      slug: 'leaderboard',
      title: 'Leaderboard',
      description: 'Climb the ranks and earn badges.',
      commands: ['leaderboard', 'achievements', 'journal'],
      steps: [
        { instruction: 'View leaderboard: `leaderboard`', command: 'leaderboard', expectedOutput: 'Top traders by returns' },
        { instruction: 'Filter by metric: `leaderboard sharpe` or `leaderboard returns`' },
        { instruction: 'Check achievements: `achievements`', command: 'achievements', expectedOutput: 'Your earned badges and progress' },
        { instruction: 'Trading journal: `journal add` to log a trade', command: 'journal add bought AAPL at 180', expectedOutput: 'Entry added to journal' },
      ],
      quiz: [
        { question: 'What does `leaderboard` show?', options: ['Top traders ranked by performance', 'Stock market rankings', 'Sector performance', 'Your portfolio'], correctIndex: 0, explanation: '`leaderboard` ranks traders by various performance metrics.' },
      ],
    },
  ],
}
