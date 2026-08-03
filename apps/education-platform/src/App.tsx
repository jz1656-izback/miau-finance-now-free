import { useState, useEffect } from 'react'
import EduBackground from './components/EduBackground'
import { CourseBrowser } from './components/CourseBrowser'
import { LessonViewer } from './components/LessonViewer'
import { TerminalSimulator } from './components/TerminalSimulator'
import { QuizPanel } from './components/QuizPanel'
import { HomePage } from './components/HomePage'
import { AuthModal } from './components/AuthModal'
import { CertificationBrowser } from './components/CertificationBrowser'
import { COURSES } from './courses'
import type { Course, Lesson } from './lib/types'
import { CERTIFICATIONS, LEARNING_PATHS } from './courses/certifications'

type View = 'home' | 'browser' | 'lesson' | 'simulator' | 'quiz' | 'certifications'
type Tier = 'free' | 'pro' | 'enterprise'

export interface User {
  username: string
  email: string
  tier: Tier
}

const FREE_COURSES = ['getting-started', 'market-data-basics', 'paper-trading', 'miau-shell-maniac']

function isPremium(courseId: string): boolean {
  return !FREE_COURSES.includes(courseId)
}

export default function App() {
  const [view, setView] = useState<View>('home')
  const [activeCourse, setActiveCourse] = useState<Course | null>(null)
  const [activeLesson, setActiveLesson] = useState<Lesson | null>(null)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false)
  const [practiceCommand, setPracticeCommand] = useState('')
  const [user, setUser] = useState<User | null>(null)
  const [showAuth, setShowAuth] = useState(false)
  const [continueCourse, setContinueCourse] = useState<Course | null>(null)
  const [continueLesson, setContinueLesson] = useState<Lesson | null>(null)

  useEffect(() => {
    const lastCourseId = localStorage.getItem('lastCourseId')
    const lastLessonId = localStorage.getItem('lastLessonId')
    if (lastCourseId && lastLessonId) {
      const course = COURSES.find((c) => c.id === lastCourseId)
      if (course) {
        const lesson = course.lessons.find((l) => l.id === lastLessonId)
        if (lesson) {
          setContinueCourse(course)
          setContinueLesson(lesson)
        }
      }
    }
  }, [])

  const saveLastLesson = (course: Course, lesson: Lesson) => {
    localStorage.setItem('lastCourseId', course.id)
    localStorage.setItem('lastLessonId', lesson.id)
    setContinueCourse(course)
    setContinueLesson(lesson)
  }

  const selectCourse = (course: Course) => {
    if (user && isPremium(course.id) && user.tier === 'free') {
      setShowAuth(true)
      return
    }
    setActiveCourse(course)
    const firstLesson = course.lessons[0]
    setActiveLesson(firstLesson)
    setView('lesson')
    setPracticeCommand(firstLesson.commands[0] || '')
    saveLastLesson(course, firstLesson)
    setMobileSidebarOpen(false)
  }

  const selectLesson = (l: Lesson) => {
    setActiveLesson(l)
    setView('lesson')
    setPracticeCommand(l.commands[0] || '')
    if (activeCourse) saveLastLesson(activeCourse, l)
    setMobileSidebarOpen(false)
  }

  const enrolledCount = user ? 3 : 0

  return (
    <div className="min-h-screen bg-miau-bg flex flex-col" style={{position:'relative'}}>
      <EduBackground />
      {/* Header */}
      <header className="flex items-center justify-between px-4 py-2.5 border-b border-miau-border shrink-0 bg-miau-surface/50">
        <div className="flex items-center gap-3">
          <button onClick={() => { setView('home'); setActiveCourse(null); setActiveLesson(null) }} className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <span className="text-xl">🐱</span>
            <span className="text-miau-green text-glow-green font-bold text-sm hidden sm:inline">MIAU FINANCE</span>
            <span className="text-miau-text-dim text-xs hidden sm:inline">Education</span>
          </button>
        </div>
        <div className="flex items-center gap-3">
          <a href="http://localhost:5175" target="_blank" className="text-[10px] text-miau-text-dim hover:text-miau-green font-mono transition-colors">Ecosystem</a>
          <a href="http://localhost:5173" target="_blank" className="text-[10px] text-miau-text-dim hover:text-miau-green font-mono transition-colors">Terminal</a>
          {activeCourse && (view === 'lesson' || view === 'simulator' || view === 'quiz') && (
            <button
              onClick={() => setMobileSidebarOpen(!mobileSidebarOpen)}
              className="md:hidden text-miau-text-dim hover:text-miau-green text-xs font-mono transition-colors"
            >
              {mobileSidebarOpen ? '✕' : '☰'}
            </button>
          )}
          {view !== 'home' && (
            <>
              <button onClick={() => { setView('browser'); setActiveCourse(null); setActiveLesson(null) }} className="text-xs text-miau-text-dim hover:text-miau-green font-mono transition-colors">
                Courses
              </button>
              <button onClick={() => { setView('certifications'); setActiveCourse(null); setActiveLesson(null) }} className="text-xs text-miau-text-dim hover:text-miau-green font-mono transition-colors">
                Certifications
              </button>
            </>
          )}
          {activeCourse && view === 'lesson' && (
            <button onClick={() => { setView('simulator'); setPracticeCommand(activeLesson?.commands[0] || '') }} className="text-xs text-miau-text-dim hover:text-miau-green font-mono transition-colors">
              Practice
            </button>
          )}
          {activeLesson && view !== 'quiz' && (
            <button onClick={() => setView('quiz')} className="text-xs text-miau-text-dim hover:text-miau-amber font-mono transition-colors">
              Quiz
            </button>
          )}
          {user ? (
            <div className="flex items-center gap-2">
              {user.tier === 'pro' && <span className="text-[10px] px-1.5 py-0.5 rounded border border-miau-amber/50 text-miau-amber font-mono">PRO</span>}
              {user.tier === 'free' && <span className="text-[10px] px-1.5 py-0.5 rounded border border-miau-border/50 text-miau-text-dim font-mono">FREE</span>}
              <span className="text-xs text-miau-text-dim font-mono">{user.username}</span>
              <button onClick={() => setUser(null)} className="text-xs text-miau-text-dim/50 hover:text-miau-red font-mono transition-colors">logout</button>
            </div>
          ) : (
            <button onClick={() => setShowAuth(true)} className="px-3 py-1 text-xs text-miau-green border border-miau-green/30 rounded hover:bg-miau-green/10 font-mono transition-colors">
              Sign In
            </button>
          )}
        </div>
      </header>

      {/* Main */}
      <main className="flex-1 flex flex-col">
        {view === 'home' && (
          <div className="relative">
            {continueCourse && continueLesson && (
              <div className="max-w-4xl mx-auto pt-4 px-6">
                <button
                  onClick={() => { setActiveCourse(continueCourse); setActiveLesson(continueLesson); setPracticeCommand(continueLesson.commands[0] || ''); setView('lesson') }}
                  className="w-full p-3 bg-miau-amber/10 border border-miau-amber/30 rounded flex items-center gap-3 hover:bg-miau-amber/20 transition-colors group"
                >
                  <span className="text-lg">📖</span>
                  <div className="text-left flex-1">
                    <p className="text-xs text-miau-amber font-mono font-bold">CONTINUE LEARNING</p>
                    <p className="text-sm text-miau-text group-hover:text-miau-green transition-colors">{continueCourse.icon} {continueCourse.title} — {continueLesson.title}</p>
                  </div>
                  <span className="text-miau-text-dim text-xs font-mono">Resume →</span>
                </button>
              </div>
            )}
            <HomePage
              onBrowse={() => setView('browser')}
              onGetStarted={() => setShowAuth(true)}
              onCertifications={() => setView('certifications')}
              user={user}
            />
          </div>
        )}
        {view === 'browser' && (
          <CourseBrowser
            onSelectCourse={selectCourse}
            userTier={user?.tier || 'free'}
            onUpgrade={() => setShowAuth(true)}
          />
        )}
        {view === 'certifications' && <CertificationBrowser />}
        {(view === 'lesson' || view === 'simulator' || view === 'quiz') && activeLesson && (
          <div className="flex flex-1 overflow-hidden">
            {(sidebarOpen || mobileSidebarOpen) && activeCourse && (
              <aside className="w-56 border-r border-miau-border overflow-y-auto shrink-0 bg-miau-surface/30 md:relative absolute left-0 top-0 bottom-0 z-40">
                <div className="p-3 border-b border-miau-border text-xs font-bold text-miau-green">
                  {activeCourse.icon} {activeCourse.title}
                </div>
                {activeCourse.lessons.map((l, i) => (
                  <button
                    key={l.id}
                    onClick={() => selectLesson(l)}
                    className={`w-full text-left px-3 py-2 text-xs border-b border-miau-border/20 transition-colors ${
                      activeLesson?.id === l.id
                        ? 'bg-miau-border/40 text-miau-green'
                        : 'text-miau-text-dim hover:text-miau-text hover:bg-miau-border/10'
                    }`}
                  >
                    <span className="text-miau-text-dim/50 mr-1">{i + 1}.</span>
                    {l.title}
                  </button>
                ))}
              </aside>
            )}
            <div className="flex-1 overflow-y-auto">
              {view === 'lesson' && (
                <LessonViewer
                  lesson={activeLesson}
                  onPractice={(cmd) => { setPracticeCommand(cmd); setView('simulator') }}
                  onQuiz={() => setView('quiz')}
                  onNext={() => {
                    if (activeCourse) {
                      const idx = activeCourse.lessons.findIndex((l) => l.id === activeLesson.id)
                      if (idx < activeCourse.lessons.length - 1) {
                        const nextLesson = activeCourse.lessons[idx + 1]
                        setActiveLesson(nextLesson)
                        setPracticeCommand(nextLesson.commands[0] || '')
                        saveLastLesson(activeCourse, nextLesson)
                      }
                    }
                  }}
                />
              )}
              {view === 'simulator' && (
                <TerminalSimulator
                  initialCommand={practiceCommand}
                  lesson={activeLesson}
                  onBack={() => setView('lesson')}
                />
              )}
              {view === 'quiz' && (
                <QuizPanel
                  lesson={activeLesson}
                  onBack={() => setView('lesson')}
                />
              )}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="flex items-center justify-between px-4 py-1.5 border-t border-miau-border text-xs text-miau-text-dim shrink-0">
        <span>{COURSES.length}+ courses · {COURSES.reduce((s, c) => s + c.lessons.length, 0)}+ lessons · {CERTIFICATIONS.length} certifications · {LEARNING_PATHS.length} career tracks · Interactive terminal</span>
        <span className="flex items-center gap-3">
          <a href="http://localhost:5175" target="_blank" className="text-miau-text-dim/50 hover:text-miau-green transition-colors">Miau Corp</a>
          <span className="text-miau-green/60">Miau Finance Education v3.0</span>
        </span>
      </footer>

      {showAuth && <AuthModal onClose={() => setShowAuth(false)} onLogin={(u) => { setUser(u); setShowAuth(false) }} />}
    </div>
  )
}
