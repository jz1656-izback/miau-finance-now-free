export interface LessonStep {
  instruction: string
  command?: string
  expectedOutput?: string
  hint?: string
}

export interface QuizQuestion {
  question: string
  options: string[]
  correctIndex: number
  explanation: string
}

export interface Lesson {
  id: string
  slug: string
  title: string
  description: string
  commands: string[]
  steps: LessonStep[]
  quiz: QuizQuestion[]
}

export interface Course {
  id: string
  slug: string
  title: string
  description: string
  category: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  icon: string
  lessonCount: number
  estimatedMinutes: number
  lessons: Lesson[]
}

export interface Certification {
  id: string
  title: string
  description: string
  icon: string
  color: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  estimatedHours: number
  courseIds: string[]
  skills: string[]
  badge: string
}

export interface LearningPath {
  id: string
  title: string
  description: string
  icon: string
  color: string
  role: string
  estimatedHours: number
  stages: LearningStage[]
}

export interface LearningStage {
  title: string
  description: string
  courseIds: string[]
}

export type EducationShellTab = 'courses' | 'lesson' | 'practice' | 'quiz'
