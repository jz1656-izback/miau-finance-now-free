import { useState } from 'react'
import type { Course } from '../lib/types'
import { COURSES } from '../courses'

interface Props {
  onSelectCourse: (course: Course) => void
  userTier: string
  onUpgrade: () => void
}

const FREE_COURSES = ['getting-started', 'market-data-basics', 'paper-trading']

const CAT_DIFFICULTY: Record<string, string> = {
  beginner: '😸', intermediate: '😺', advanced: '😼',
}

function difficultyColor(d: string) {
  if (d === 'beginner') return 'text-miau-green border-miau-green/30 bg-miau-green/5'
  if (d === 'intermediate') return 'text-miau-amber border-miau-amber/30 bg-miau-amber/5'
  return 'text-miau-red border-miau-red/30 bg-miau-red/5'
}

const DIFFICULTIES = ['All', 'Beginner', 'Intermediate', 'Advanced'] as const

export function CourseBrowser({ onSelectCourse, userTier, onUpgrade }: Props) {
  const [search, setSearch] = useState('')
  const [difficultyFilter, setDifficultyFilter] = useState<string>('All')

  const isPremium = (id: string) => !FREE_COURSES.includes(id)
  const isLocked = (id: string) => userTier === 'free' && isPremium(id)

  const totalCommands = COURSES.reduce((sum, c) => sum + c.lessons.reduce((s, l) => s + l.commands.length, 0), 0)

  const filteredCourses = COURSES.filter((course) => {
    const matchesSearch = search === '' ||
      course.title.toLowerCase().includes(search.toLowerCase()) ||
      course.description.toLowerCase().includes(search.toLowerCase())
    const matchesDifficulty = difficultyFilter === 'All' ||
      course.difficulty.toLowerCase() === difficultyFilter.toLowerCase()
    return matchesSearch && matchesDifficulty
  })

  return (
    <div className="p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-2xl">📚</span>
          <div>
            <h1 className="text-lg font-bold text-miau-green text-glow-green">Course Catalog</h1>
            <p className="text-sm text-miau-text-dim">Interactive tutorials for every Miau Finance command.</p>
          </div>
        </div>
        <div className="flex gap-4 mt-3 text-xs text-miau-text-dim">
          <span>{filteredCourses.length} / {COURSES.length} courses shown</span>
          <span>·</span>
          <span>{COURSES.reduce((s, c) => s + c.lessons.length, 0)} lessons</span>
          <span>·</span>
          <span>{totalCommands} commands covered</span>
        </div>
        {userTier === 'free' && (
          <div className="mt-3 p-3 bg-miau-amber/5 border border-miau-amber/20 rounded text-xs text-miau-text-dim">
            <span className="text-miau-amber font-bold">Free tier:</span> {FREE_COURSES.length} courses + 🟢 live API access.{' '}
            <button onClick={onUpgrade} className="text-miau-green hover:underline font-mono">
              Upgrade to Pro → unlock all courses
            </button>
          </div>
        )}
      </div>

      {/* Search & Filters */}
      <div className="mb-4 space-y-3">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search courses by title or description..."
          className="w-full px-3 py-2 bg-miau-surface border border-miau-border/50 rounded text-xs text-miau-text font-mono placeholder:text-miau-text-dim/30 outline-none focus:border-miau-green/50 transition-colors"
        />
        <div className="flex items-center gap-2">
          {DIFFICULTIES.map((d) => (
            <button
              key={d}
              onClick={() => setDifficultyFilter(d)}
              className={`px-3 py-1 text-xs font-mono rounded border transition-colors ${
                difficultyFilter === d
                  ? d === 'All' ? 'bg-miau-green/10 border-miau-green/30 text-miau-green'
                    : d === 'Beginner' ? 'bg-miau-green/10 border-miau-green/30 text-miau-green'
                    : d === 'Intermediate' ? 'bg-miau-amber/10 border-miau-amber/30 text-miau-amber'
                    : 'bg-miau-red/10 border-miau-red/30 text-miau-red'
                  : 'border-miau-border/30 text-miau-text-dim hover:text-miau-text hover:border-miau-border'
              }`}
            >
              {d}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
        {filteredCourses.map((course) => {
          const locked = isLocked(course.id)
          const premium = isPremium(course.id)

          return (
            <button
              key={course.id}
              onClick={() => onSelectCourse(course)}
              className={`text-left p-4 bg-miau-surface border rounded transition-all group ${
                locked
                  ? 'border-miau-border/10 opacity-50 cursor-pointer'
                  : 'border-miau-border/30 hover:border-miau-green/50 hover:bg-miau-green/[0.02]'
              }`}
            >
              <div className="flex items-start justify-between mb-2">
                <span className="text-2xl">{course.icon}</span>
                <div className="flex items-center gap-1.5">
                  {premium && <span className={`text-[10px] px-1.5 py-0.5 rounded border font-mono ${locked ? 'border-miau-amber/30 text-miau-amber/60' : 'border-miau-amber/40 text-miau-amber'}`}>PRO</span>}
                  <span className={`text-[10px] px-1.5 py-0.5 rounded border font-mono ${difficultyColor(course.difficulty)}`}>
                    {CAT_DIFFICULTY[course.difficulty] || '😺'} {course.difficulty}
                  </span>
                </div>
              </div>
              <h3 className={`text-sm font-bold mb-1 transition-colors ${locked ? 'text-miau-text-dim' : 'text-miau-text group-hover:text-miau-green'}`}>
                {locked && '🔒 '}{course.title}
              </h3>
              <p className="text-xs text-miau-text-dim mb-3 line-clamp-2">{course.description}</p>
              <div className="flex items-center gap-3 text-[10px] text-miau-text-dim font-mono">
                <span>{course.lessons.length} lessons</span>
                <span>·</span>
                <span>{course.lessons.reduce((s, l) => s + l.commands.length, 0)} commands</span>
                <span>·</span>
                <span>~{course.estimatedMinutes}min</span>
              </div>
            </button>
          )
        })}
      </div>
      {filteredCourses.length === 0 && (
        <div className="text-center py-12 text-sm text-miau-text-dim">
          No courses match your search/filter criteria.
        </div>
      )}
    </div>
  )
}
