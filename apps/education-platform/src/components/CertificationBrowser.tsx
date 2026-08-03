import { useState } from 'react'
import type { Certification, LearningPath } from '../lib/types'
import { CERTIFICATIONS, LEARNING_PATHS } from '../courses/certifications'
import { COURSES } from '../courses'

type Tab = 'certifications' | 'paths'

export function CertificationBrowser() {
  const [tab, setTab] = useState<Tab>('certifications')
  const [expandedCert, setExpandedCert] = useState<string | null>(null)
  const [expandedPath, setExpandedPath] = useState<string | null>(null)

  const courseCount = COURSES.length
  const totalLessons = COURSES.reduce((s, c) => s + c.lessons.length, 0)

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-2xl">🏆</span>
          <div>
            <h1 className="text-lg font-bold text-miau-green text-glow-green">Certifications & Career Tracks</h1>
            <p className="text-sm text-miau-text-dim">Earn verifiable credentials and follow structured career paths.</p>
          </div>
        </div>
        <div className="flex gap-4 mt-3 text-xs text-miau-text-dim">
          <span>{CERTIFICATIONS.length} certifications</span>
          <span>·</span>
          <span>{LEARNING_PATHS.length} career tracks</span>
          <span>·</span>
          <span>{courseCount} courses</span>
          <span>·</span>
          <span>{totalLessons} lessons</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 bg-miau-surface border border-miau-border/30 rounded-lg p-1 w-fit">
        <button
          onClick={() => setTab('certifications')}
          className={`px-4 py-2 text-xs font-mono rounded-md transition-colors ${
            tab === 'certifications' ? 'bg-miau-green/20 text-miau-green' : 'text-miau-text-dim hover:text-miau-text'
          }`}
        >
          Certifications
        </button>
        <button
          onClick={() => setTab('paths')}
          className={`px-4 py-2 text-xs font-mono rounded-md transition-colors ${
            tab === 'paths' ? 'bg-miau-green/20 text-miau-green' : 'text-miau-text-dim hover:text-miau-text'
          }`}
        >
          Career Tracks
        </button>
      </div>

      {tab === 'certifications' && (
        <div className="space-y-4">
          {CERTIFICATIONS.map((cert) => {
            const isExpanded = expandedCert === cert.id
            const certCourses = COURSES.filter((c) => cert.courseIds.includes(c.id))

            return (
              <div
                key={cert.id}
                className="bg-miau-surface border border-miau-border/30 rounded-lg overflow-hidden hover:border-miau-border/60 transition-colors"
              >
                <button
                  onClick={() => setExpandedCert(isExpanded ? null : cert.id)}
                  className="w-full text-left p-5 flex items-start gap-4"
                >
                  <div
                    className="w-12 h-12 rounded-lg flex items-center justify-center text-xl shrink-0"
                    style={{ backgroundColor: `${cert.color}15`, border: `1px solid ${cert.color}30` }}
                  >
                    {cert.icon}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="text-sm font-bold text-miau-text">{cert.title}</h3>
                      <span
                        className="text-[10px] px-1.5 py-0.5 rounded font-mono font-bold"
                        style={{ backgroundColor: `${cert.color}20`, color: cert.color, border: `1px solid ${cert.color}30` }}
                      >
                        {cert.badge}
                      </span>
                    </div>
                    <p className="text-xs text-miau-text-dim mb-2">{cert.description}</p>
                    <div className="flex items-center gap-3 text-[10px] text-miau-text-dim font-mono">
                      <span>{cert.courseIds.length} courses · ~{cert.estimatedHours}h</span>
                      <span>·</span>
                      <span className={cert.difficulty === 'beginner' ? 'text-miau-green' : cert.difficulty === 'intermediate' ? 'text-miau-amber' : 'text-miau-red'}>
                        {cert.difficulty}
                      </span>
                    </div>
                  </div>
                  <div className={`text-miau-text-dim transition-transform ${isExpanded ? 'rotate-180' : ''}`}>
                    ▼
                  </div>
                </button>

                {isExpanded && (
                  <div className="px-5 pb-5 border-t border-miau-border/20 pt-4">
                    <div className="mb-3">
                      <h4 className="text-[10px] text-miau-text-dim font-mono uppercase mb-2">Skills You Will Gain</h4>
                      <div className="flex flex-wrap gap-1.5">
                        {cert.skills.map((skill) => (
                          <span
                            key={skill}
                            className="text-[10px] px-2 py-0.5 rounded font-mono"
                            style={{ backgroundColor: `${cert.color}10`, color: cert.color, border: `1px solid ${cert.color}20` }}
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h4 className="text-[10px] text-miau-text-dim font-mono uppercase mb-2">Required Courses</h4>
                      <div className="space-y-1">
                        {certCourses.map((course) => (
                          <div key={course.id} className="flex items-center gap-2 text-xs text-miau-text-dim">
                            <span>{course.icon}</span>
                            <span className="text-miau-text">{course.title}</span>
                            <span className="text-[10px] text-miau-text-dim/50">
                              ({course.lessons.length} lessons · ~{course.estimatedMinutes}min)
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}

      {tab === 'paths' && (
        <div className="space-y-6">
          {LEARNING_PATHS.map((path) => {
            const isExpanded = expandedPath === path.id

            return (
              <div
                key={path.id}
                className="bg-miau-surface border border-miau-border/30 rounded-lg overflow-hidden hover:border-miau-border/60 transition-colors"
              >
                <button
                  onClick={() => setExpandedPath(isExpanded ? null : path.id)}
                  className="w-full text-left p-5 flex items-start gap-4"
                >
                  <div
                    className="w-12 h-12 rounded-lg flex items-center justify-center text-xl shrink-0"
                    style={{ backgroundColor: `${path.color}15`, border: `1px solid ${path.color}30` }}
                  >
                    {path.icon}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="text-sm font-bold text-miau-text">{path.title}</h3>
                    </div>
                    <p className="text-xs text-miau-text-dim mb-1">{path.description}</p>
                    <div className="flex items-center gap-3 text-[10px] text-miau-text-dim font-mono">
                      <span>🎯 {path.role}</span>
                      <span>·</span>
                      <span>{path.stages.length} stages · ~{path.estimatedHours}h</span>
                    </div>
                  </div>
                  <div className={`text-miau-text-dim transition-transform ${isExpanded ? 'rotate-180' : ''}`}>
                    ▼
                  </div>
                </button>

                {isExpanded && (
                  <div className="px-5 pb-5 border-t border-miau-border/20 pt-4">
                    <div className="relative">
                      {path.stages.map((stage, i) => {
                        const stageCourses = COURSES.filter((c) => stage.courseIds.includes(c.id))

                        return (
                          <div key={stage.title} className="flex gap-4 pb-6 last:pb-0">
                            {/* Timeline */}
                            <div className="flex flex-col items-center shrink-0">
                              <div
                                className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold font-mono"
                                style={{ backgroundColor: `${path.color}20`, color: path.color, border: `2px solid ${path.color}` }}
                              >
                                {i + 1}
                              </div>
                              {i < path.stages.length - 1 && (
                                <div className="w-px flex-1 mt-1" style={{ backgroundColor: `${path.color}20` }} />
                              )}
                            </div>
                            {/* Content */}
                            <div className="flex-1 min-w-0">
                              <h4 className="text-sm font-bold text-miau-text mb-0.5">{stage.title}</h4>
                              <p className="text-xs text-miau-text-dim mb-2">{stage.description}</p>
                              <div className="space-y-1">
                                {stageCourses.map((course) => (
                                  <div key={course.id} className="flex items-center gap-2 text-xs text-miau-text-dim">
                                    <span>{course.icon}</span>
                                    <span className="text-miau-text">{course.title}</span>
                                    <span className="text-[10px] text-miau-text-dim/50">
                                      ({course.lessons.length} lessons)
                                    </span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
