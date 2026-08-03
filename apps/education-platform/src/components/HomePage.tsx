import type { User } from '../App'
import { COURSES } from '../courses'
import { CERTIFICATIONS, LEARNING_PATHS } from '../courses/certifications'

interface Props {
  onBrowse: () => void
  onGetStarted: () => void
  onCertifications: () => void
  user: User | null
}

export function HomePage({ onBrowse, onGetStarted, onCertifications, user }: Props) {
  const totalLessons = COURSES.reduce((s, c) => s + c.lessons.length, 0)
  const totalCommands = COURSES.reduce((s, c) => s + c.lessons.reduce((a, l) => a + l.commands.length, 0), 0)

  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden border-b border-miau-border">
        <div className="absolute inset-0 opacity-5 pointer-events-none" style={{
          backgroundImage: 'radial-gradient(circle at 50% 30%, #00ff88 0%, transparent 60%)',
        }} />
        <div className="max-w-4xl mx-auto px-6 py-20 text-center relative z-10">
          <div className="text-4xl mb-4">🐱📈</div>
          <h1 className="text-3xl md:text-5xl font-bold text-miau-green text-glow-green mb-4 font-mono">
            The Cat, CFA
          </h1>
          <p className="text-lg md:text-xl text-miau-text mb-3 font-mono">
            Master finance through the terminal.
          </p>
          <p className="text-sm text-miau-text-dim max-w-2xl mx-auto mb-8">
            Interactive courses teaching investing, trading, risk management, DeFi, and quantitative finance — 
            all through the same commands used by professional traders. No videos. No fluff. Just the terminal.
          </p>
          <div className="flex items-center justify-center gap-3 flex-wrap">
            <button
              onClick={user ? onBrowse : onGetStarted}
              className="px-6 py-3 bg-miau-green text-miau-bg rounded font-bold font-mono text-sm hover:bg-miau-green/90 transition-colors"
            >
              {user ? 'Browse Courses' : 'Start Learning Free'}
            </button>
            <button
              onClick={onBrowse}
              className="px-6 py-3 border border-miau-border text-miau-text-dim rounded font-mono text-sm hover:text-miau-text hover:border-miau-text/30 transition-colors"
            >
              View All Courses
            </button>
          </div>
          <div className="mt-8 flex items-center justify-center gap-6 text-xs text-miau-text-dim font-mono">
            <span>{COURSES.length} courses</span>
            <span>·</span>
            <span>{totalLessons} lessons</span>
            <span>·</span>
            <span>{totalCommands} commands covered</span>
            <span>·</span>
            <span>{CERTIFICATIONS.length} certifications</span>
            <span>·</span>
            <span>{LEARNING_PATHS.length} career tracks</span>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="border-b border-miau-border py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-center text-sm font-bold text-miau-text-dim mb-10 uppercase tracking-widest">Why The Cat, CFA?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { icon: '⌨️', title: 'Terminal-First', desc: 'Learn finance the way professionals work — through command-line interaction. Every course teaches real commands you can use immediately in Miau Finance or any trading platform.' },
              { icon: '🧠', title: 'Interactive Practice', desc: 'Each lesson includes a live terminal simulator. Type real commands, see real outputs. No passive watching — you learn by doing, not by watching videos.' },
              { icon: '📊', title: 'Real Market Data', desc: 'Courses use live market data where applicable. Learn to analyze real stocks, real crypto, real portfolios — not made-up textbook examples.' },
              { icon: '🏆', title: 'Earn Certificates', desc: 'Complete courses and earn verifiable certificates. Share them on LinkedIn, add them to your resume, or frame them for your cat.' },
              { icon: '🐱', title: 'Cat-Powered Learning', desc: 'Every course is infused with cat humor, cat facts, and cat commentary. Because finance is serious, but learning shouldn\'t be boring.' },
              { icon: '🌍', title: 'Learn Anywhere', desc: 'Download courses and learn offline. Progress syncs when you\'re back online. On a plane? In a coffee shop? The cat has you covered.' },
            ].map((f) => (
              <div key={f.title} className="p-5 bg-miau-surface border border-miau-border/30 rounded hover:border-miau-green/30 transition-colors">
                <div className="text-2xl mb-3">{f.icon}</div>
                <h3 className="text-sm font-bold text-miau-text mb-2">{f.title}</h3>
                <p className="text-xs text-miau-text-dim leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing — 🐱 MIAU IS FREE! */}
      <section className="border-b border-miau-border py-16 px-6" id="pricing">
        <div className="max-w-5xl mx-auto">
          {/* Crying cat banner */}
          <div className="text-center mb-8 p-6 rounded-lg" style={{background:'rgba(255,102,136,0.04)',border:'2px solid rgba(255,102,136,0.15)'}}>
            <pre className="text-2xl leading-relaxed font-mono" style={{color:'#ff6688'}}>
{`   /\_/\
 ( o.o )  😿
   =^=   "miau is free..."
    /_||_\\`}
            </pre>
            <p className="text-sm font-bold mt-2" style={{color:'#ff6688'}}>NO MORE PRICING! 🥳</p>
            <p className="text-xs mt-1" style={{color:'rgba(200,214,208,0.6)'}}>
              No pawborghinis. No weird billionaires eating kittens. Just cats and charts. 🐱📊
            </p>
            <p className="text-xs font-bold mt-2" style={{color:'#00ff88'}}>Miau Finance is now FREE and OPEN SOURCE!</p>
            <p className="text-xs mt-2" style={{color:'rgba(200,214,208,0.3)',textDecoration:'line-through',textDecorationColor:'#ff3344'}}>
              Free €0 · Pro €10/mo · Tiny Catfunds €19/mo · Enterprise €99/mo
            </p>
          </div>

          {/* Pricing cards — CROSSED OUT */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 opacity-30 grayscale">
            {[
              {name:'Free', price:'€0', period:'', features:['Basic terminal commands','30 req/min rate limit','5 data providers','0 barks'], cta:'Start Free'},
              {name:'Pro', price:'€10', period:'/user/mo', features:['300 req/min','25 data providers','AI advisor & 3D charts','Priority support','7-day trial'], cta:'Upgrade'},
              {name:'Tiny Catfunds', price:'€19', period:'/user/mo', features:['1k req/min','All providers','Team workspaces','3 barks/year','Extra barks: €9,999'], cta:'Go Catfund'},
              {name:'Enterprise', price:'€99', period:'/user/mo', features:['10k req/min','All features','15 barks/year','On-premise','SSO & 99.9% SLA'], cta:'Contact Us'},
            ].map((plan) => (
              <div key={plan.name} className="p-5 rounded border border-miau-border/30 bg-miau-surface relative">
                <span className="absolute -top-2 -right-2 text-xl" style={{color:'#ff3344',textShadow:'0 0 8px rgba(255,51,68,0.5)'}}>✕</span>
                <h3 className="text-sm font-bold text-miau-text mb-1 line-through" style={{textDecorationColor:'#ff3344'}}>{plan.name}</h3>
                <div className="mb-2">
                  <span className="text-3xl font-bold text-miau-green line-through" style={{textDecorationColor:'#ff3344'}}>{plan.price}</span>
                  <span className="text-xs text-miau-text-dim">{plan.period}</span>
                </div>
                <ul className="space-y-1.5 mb-5 flex-1">
                  {plan.features.map((f) => (
                    <li key={f} className="flex items-start gap-2 text-xs text-miau-text-dim line-through" style={{textDecorationColor:'#ff3344'}}>
                      <span className="text-miau-green mt-0.5">✓</span>
                      {f}
                    </li>
                  ))}
                </ul>
                <button className="w-full py-2.5 rounded font-mono text-sm font-bold border border-miau-border text-miau-text-dim line-through" style={{textDecorationColor:'#ff3344',cursor:'not-allowed'}}>
                  {plan.cta}
                </button>
                <p className="text-[10px] text-center mt-2" style={{color:'#00ff88'}}>← FREE NOW! 🎉</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Course Preview */}
      <section className="border-b border-miau-border py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-center text-sm font-bold text-miau-text-dim mb-10 uppercase tracking-widest">Course Catalog</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {COURSES.map((c) => (
              <div key={c.id} className="p-4 bg-miau-surface border border-miau-border/20 rounded hover:border-miau-green/30 transition-colors cursor-pointer" onClick={onBrowse}>
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xl">{c.icon}</span>
                  <div>
                    <h4 className="text-xs font-bold text-miau-text">{c.title}</h4>
                    <p className="text-[10px] text-miau-text-dim">{c.lessons.length} lessons · ~{c.estimatedMinutes}min</p>
                  </div>
                </div>
                <p className="text-[10px] text-miau-text-dim/70 line-clamp-2">{c.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Certifications */}
      <section className="border-b border-miau-border py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-sm font-bold text-miau-text-dim uppercase tracking-widest">Earn Your Stripes</h2>
              <p className="text-xs text-miau-text-dim mt-1">{CERTIFICATIONS.length} professional certifications</p>
            </div>
            <button onClick={onCertifications} className="text-xs text-miau-green hover:underline font-mono">
              View All →
            </button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {CERTIFICATIONS.map((cert) => (
              <div key={cert.id} onClick={onCertifications} className="p-4 bg-miau-surface border border-miau-border/20 rounded hover:border-miau-green/30 transition-colors cursor-pointer group">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xl">{cert.icon}</span>
                  <div>
                    <h4 className="text-xs font-bold text-miau-text group-hover:text-miau-green transition-colors">{cert.title}</h4>
                    <span className="text-[10px] text-miau-text-dim">{cert.courseIds.length} courses · ~{cert.estimatedHours}h</span>
                  </div>
                </div>
                <p className="text-[10px] text-miau-text-dim/70 line-clamp-2">{cert.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Career Tracks */}
      <section className="border-b border-miau-border py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-sm font-bold text-miau-text-dim uppercase tracking-widest">Career Tracks</h2>
              <p className="text-xs text-miau-text-dim mt-1">Structured learning paths for every role</p>
            </div>
            <button onClick={onCertifications} className="text-xs text-miau-green hover:underline font-mono">
              View All →
            </button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {LEARNING_PATHS.map((path) => (
              <div key={path.id} onClick={onCertifications} className="p-4 bg-miau-surface border border-miau-border/20 rounded hover:border-miau-green/30 transition-colors cursor-pointer group">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xl">{path.icon}</span>
                  <div>
                    <h4 className="text-xs font-bold text-miau-text group-hover:text-miau-green transition-colors">{path.title}</h4>
                    <p className="text-[10px] text-miau-text-dim">🎯 {path.role}</p>
                  </div>
                </div>
                <p className="text-[10px] text-miau-text-dim/70 line-clamp-2 mb-2">{path.description}</p>
                <div className="flex items-center gap-2 text-[10px] text-miau-text-dim font-mono">
                  <span>{path.stages.length} stages</span>
                  <span>·</span>
                  <span>~{path.estimatedHours}h total</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-sm font-bold text-miau-text-dim mb-8 uppercase tracking-widest">What Students Say</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-left">
            {[
              { quote: 'I passed the CFA Level 1 after working through the Investment Banking course. The DCF practice terminal was a game changer.', name: 'Meowgan S.', role: 'CFA Candidate' },
              { quote: 'Finally, a finance course that doesn\'t make me fall asleep. The cat jokes keep me going through options Greeks at 2 AM.', name: 'Purrcy W.', role: 'Day Trader' },
              { quote: 'I learned more about DeFi in one afternoon than I did in six months of YouTube videos. The wallet simulator is amazing.', name: 'Feline D.', role: 'DeFi Developer' },
              { quote: 'My cat sits on my keyboard while I study. The platform taught me keyboard shortcuts I didn\'t know existed. Now we both trade.', name: 'Tabby K.', role: 'Retail Investor' },
            ].map((t) => (
              <div key={t.name} className="p-4 bg-miau-surface border border-miau-border/20 rounded">
                <p className="text-xs text-miau-text leading-relaxed mb-3 italic">"{t.quote}"</p>
                <div>
                  <p className="text-xs font-bold text-miau-green">{t.name}</p>
                  <p className="text-[10px] text-miau-text-dim">{t.role}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-12 px-6 bg-miau-green/[0.03] border-t border-miau-border">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-lg font-bold text-miau-green mb-3 font-mono">Ready to earn your CFA?</h2>
          <p className="text-sm text-miau-text-dim mb-6">Cat Financial Analyst. The only certification that comes with tuna.</p>
          <button
            onClick={onGetStarted}
            className="px-8 py-3 bg-miau-green text-miau-bg rounded font-bold font-mono text-sm hover:bg-miau-green/90 transition-colors"
          >
            Start Learning Free
          </button>
        </div>
      </section>
    </div>
  )
}
