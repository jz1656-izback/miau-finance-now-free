import { useState, useEffect } from 'react'
const CATS = ['🐱','😺','😸','😻','😽']

export default function CatProgress({ courseId, totalLessons }: { courseId: string; totalLessons: number }) {
  const [completed, setCompleted] = useState<number>(() => {
    try { return JSON.parse(localStorage.getItem('course_progress_' + courseId) || '0') } catch { return 0 }
  })
  const pct = totalLessons > 0 ? Math.round((completed / totalLessons) * 100) : 0

  useEffect(() => {
    localStorage.setItem('course_progress_' + courseId, String(completed))
  }, [completed, courseId])

  return (
    <div style={{marginBottom:12}}>
      <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:4}}>
        <div style={{display:'flex',gap:2}}>
          {[0,1,2,3,4].map(i => (
            <span key={i} style={{fontSize:10,opacity:i*20<=pct?1:0.3,transition:'all 0.3s'}}>
              {pct >= (i+1)*20 ? CATS[i] : '🐾'}
            </span>
          ))}
        </div>
        <span style={{fontSize:9,color:'#8899b0'}}>{pct}% · {completed}/{totalLessons} lessons</span>
      </div>
      <div style={{height:4,background:'rgba(42,42,64,0.4)',borderRadius:2,overflow:'hidden'}}>
        <div style={{height:'100%',width:`${pct}%`,background:'linear-gradient(90deg,#00e676,#a855f7)',borderRadius:2,transition:'width 0.5s ease'}} />
      </div>
    </div>
  )
}
