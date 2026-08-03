import { useState, useMemo } from 'react'
import { Award, Star, Trophy, Zap, TrendingUp, Users, Eye } from 'lucide-react'
import {
  getAllAchievements,
  getUnlockedAchievements,
  getTotalPoints,
  getRank,
  getProgress,
  type Achievement,
} from '../lib/achievements'

const RARITY_COLORS: Record<Achievement['rarity'], string> = {
  common: 'border-slate-500 text-slate-300',
  rare: 'border-blue-500 text-blue-300',
  epic: 'border-purple-500 text-purple-300',
  legendary: 'border-amber-500 text-amber-300',
  mythic: 'border-pink-500 text-pink-300',
}

const RARITY_BG: Record<Achievement['rarity'], string> = {
  common: 'bg-slate-800',
  rare: 'bg-blue-900/30',
  epic: 'bg-purple-900/30',
  legendary: 'bg-amber-900/30',
  mythic: 'bg-pink-900/30',
}

const RARITY_LABEL: Record<Achievement['rarity'], string> = {
  common: 'Common',
  rare: 'Rare',
  epic: 'Epic',
  legendary: 'Legendary',
  mythic: 'Mythic',
}

const CATEGORY_ICONS: Record<Achievement['category'], React.ReactNode> = {
  trading: <TrendingUp size={14} />,
  portfolio: <Star size={14} />,
  analytics: <Zap size={14} />,
  community: <Users size={14} />,
  secret: <Eye size={14} />,
}

const CATEGORY_LABELS: Record<Achievement['category'], string> = {
  trading: 'Trading',
  portfolio: 'Portfolio',
  analytics: 'Analytics',
  community: 'Community',
  secret: 'Secret',
}

type FilterCategory = Achievement['category'] | 'all'

export default function CatAchievements() {
  const [filter, setFilter] = useState<FilterCategory>('all')
  const [showAll, setShowAll] = useState(false)

  const unlocked = useMemo(() => getUnlockedAchievements(), [])
  const all = useMemo(() => getAllAchievements(), [])
  const points = useMemo(() => getTotalPoints(), [])
  const rank = useMemo(() => getRank(), [])

  const unlockedIds = new Set(unlocked.map((a) => a.id))
  const filtered = filter === 'all'
    ? all
    : all.filter((a) => a.category === filter)

  const displayed = showAll ? filtered : filtered.filter((a) => unlockedIds.has(a.id))

  return (
    <div className="bg-gradient-to-br from-slate-900 to-slate-950 rounded-lg p-6 border border-slate-700 shadow-lg">
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Award size={24} className="text-amber-400" />
            CAT ACHIEVEMENTS
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            {rank.emoji} {rank.title} — {points} pts
          </p>
        </div>
        <div className="text-right">
          <div className="text-3xl">{rank.emoji}</div>
          <div className="text-xs text-slate-500 mt-1">
            {unlocked.length}/{all.length} unlocked
          </div>
        </div>
      </div>

      {/* Progress bar */}
      <div className="mb-4 bg-slate-800 rounded h-2 overflow-hidden">
        <div
          className="bg-gradient-to-r from-amber-500 to-pink-500 h-full transition-all duration-500"
          style={{ width: `${(unlocked.length / all.length) * 100}%` }}
        />
      </div>

      {/* Category filter */}
      <div className="flex flex-wrap gap-1.5 mb-4">
        {(['all', 'trading', 'portfolio', 'analytics', 'community', 'secret'] as FilterCategory[]).map((cat) => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            className={`px-2.5 py-1 rounded text-xs font-medium transition ${
              filter === cat
                ? 'bg-amber-600/30 text-amber-300 border border-amber-500/50'
                : 'bg-slate-800 text-slate-400 border border-slate-700 hover:border-slate-500'
            }`}
          >
            {cat === 'all'
              ? 'All'
              : (
                <span className="flex items-center gap-1">
                  {CATEGORY_ICONS[cat]}
                  {CATEGORY_LABELS[cat]}
                </span>
              )}
          </button>
        ))}
      </div>

      {/* Toggle show all */}
      <div className="flex items-center justify-between mb-4">
        <span className="text-xs text-slate-500">
          {filter === 'all' ? 'All categories' : CATEGORY_LABELS[filter]}
        </span>
        <button
          onClick={() => setShowAll(!showAll)}
          className="text-xs text-amber-400 hover:text-amber-300 transition"
        >
          {showAll ? 'Show unlocked only' : `Show all (${filtered.length})`}
        </button>
      </div>

      {/* Achievement list */}
      <div className="space-y-2 max-h-80 overflow-y-auto">
        {displayed.length === 0 && (
          <div className="text-center text-sm text-slate-500 py-6">
            No achievements yet. Start trading to unlock them! 🐱
          </div>
        )}
        {displayed.map((ach) => {
          const isUnlocked = unlockedIds.has(ach.id)
          const progress = getProgress(ach.id)
          const unlockDate = isUnlocked
            ? unlocked.find((u) => u.id === ach.id)?.unlockedAt
            : null

          return (
            <div
              key={ach.id}
              className={`rounded-lg p-3 border transition-all ${
                isUnlocked
                  ? `${RARITY_COLORS[ach.rarity]} border-opacity-50 ${RARITY_BG[ach.rarity]}`
                  : 'bg-slate-800/50 border-slate-700 opacity-60'
              }`}
            >
              <div className="flex items-start gap-3">
                {/* Icon */}
                <div className={`text-2xl ${isUnlocked ? '' : 'grayscale'}`}>
                  {ach.icon}
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className={`text-sm font-bold ${isUnlocked ? 'text-slate-100' : 'text-slate-400'}`}>
                      {ach.title}
                    </span>
                    <span className={`text-[10px] px-1.5 py-0.5 rounded uppercase font-bold ${
                      isUnlocked ? `${RARITY_COLORS[ach.rarity]} border` : 'bg-slate-700 text-slate-500'
                    }`}>
                      {RARITY_LABEL[ach.rarity]}
                    </span>
                    {isUnlocked && (
                      <Trophy size={12} className="text-amber-400" />
                    )}
                  </div>
                  <p className="text-xs text-slate-500 mt-0.5">{ach.description}</p>

                  {/* Progress bar for locked */}
                  {!isUnlocked && (
                    <div className="mt-2">
                      <div className="bg-slate-700 rounded h-1.5 overflow-hidden">
                        <div
                          className="bg-slate-500 h-full transition-all duration-500"
                          style={{ width: `${Math.min(100, Math.round(progress))}%` }}
                        />
                      </div>
                      <span className="text-[10px] text-slate-600 mt-0.5">
                        {Math.round(progress)}%
                      </span>
                    </div>
                  )}

                  {/* Unlock date */}
                  {isUnlocked && unlockDate && (
                    <div className="text-[10px] text-slate-500 mt-1">
                      Unlocked {new Date(unlockDate).toLocaleDateString()}
                    </div>
                  )}
                </div>

                {/* Points */}
                <div className={`text-xs font-mono ${isUnlocked ? 'text-amber-400' : 'text-slate-600'}`}>
                  +{ach.points}
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
