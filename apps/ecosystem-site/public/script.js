// Canvas universe
const canvas = document.getElementById('universe');
const ctx = canvas.getContext('2d');
let stars = [], fishes = [], mouse = {x:0, y:0};
let animActive = true;

function resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

for (let i = 0; i < 60; i++) {
  stars.push({
    x: Math.random() * canvas.width, y: Math.random() * canvas.height,
    r: Math.random() * 1.5 + 0.3, a: Math.random(), s: Math.random() * 0.015 + 0.003,
    c: Math.random() > 0.6 ? [0,255,136] : [200,214,208]
  });
}
for (let i = 0; i < 6; i++) {
  fishes.push({
    x: Math.random() * canvas.width, y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 0.3, vy: (Math.random() - 0.5) * 0.2,
    s: Math.random() * 10 + 8, phase: Math.random() * Math.PI * 2, emoji: ['🐟','🐠','🐡'][Math.floor(Math.random()*3)]
  });
}
for (let i = 0; i < 3; i++) {
  fishes.push({
    x: Math.random() * canvas.width, y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 0.4, vy: (Math.random() - 0.5) * 0.3,
    s: Math.random() * 15 + 12, phase: Math.random() * Math.PI * 2, emoji: '🐱'
  });
}

function drawStars(time) {
  stars.forEach(s => {
    const flicker = Math.sin(time * s.s + s.a) * 0.3 + 0.7;
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(${s.c.join(',')},${flicker})`;
    ctx.fill();
  });
}
function drawFishes(time) {
  fishes.forEach(f => {
    f.x += f.vx; f.y += f.vy;
    f.vy += Math.sin(time * 0.001 + f.phase) * 0.02;
    if (f.x < -20) f.x = canvas.width + 20;
    if (f.x > canvas.width + 20) f.x = -20;
    if (f.y < -20) f.y = canvas.height + 20;
    if (f.y > canvas.height + 20) f.y = -20;
    ctx.font = `${f.s}px serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(f.emoji, f.x, f.y);
  });
}
function drawConstellations() {
  const cons = [
    [[100,100],[150,80],[200,120],[180,170],[120,160],[100,100]],
    [[canvas.width-150,150],[canvas.width-100,120],[canvas.width-80,180],[canvas.width-130,200],[canvas.width-150,150]],
  ];
  cons.forEach(points => {
    ctx.beginPath();
    points.forEach((p, i) => { i === 0 ? ctx.moveTo(p[0], p[1]) : ctx.lineTo(p[0], p[1]); });
    ctx.strokeStyle = 'rgba(0,255,136,0.06)';
    ctx.lineWidth = 0.5;
    ctx.stroke();
    points.forEach(p => {
      ctx.beginPath(); ctx.arc(p[0], p[1], 1.5, 0, Math.PI*2);
      ctx.fillStyle = 'rgba(0,255,136,0.1)'; ctx.fill();
    });
  });
}
document.addEventListener('mousemove', e => { mouse.x = e.clientX; mouse.y = e.clientY; });
canvas.addEventListener('click', () => {
  for (let i = 0; i < 5; i++) {
    stars.push({
      x: canvas.width/2 + (Math.random()-0.5)*200,
      y: canvas.height/2 + (Math.random()-0.5)*200,
      r: Math.random()*2+0.5, a: Math.random(), s: Math.random()*0.02+0.005,
      c: [255, 255, 100],
    });
  }
});

function animate(time) {
  if (!animActive) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawConstellations();
  drawStars(time);
  drawFishes(time);
  
  // Mouse glow
  const grad = ctx.createRadialGradient(mouse.x, mouse.y, 0, mouse.x, mouse.y, 100);
  grad.addColorStop(0, 'rgba(0,255,136,0.02)');
  grad.addColorStop(1, 'rgba(0,255,136,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);

// Tab system
const tabs = ['comparison','products','pricing','vision'];
let activeTab = 'comparison';

function switchTab(tab) {
  activeTab = tab;
  document.querySelectorAll('.tab-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.tab === tab);
  });
  document.querySelectorAll('.tab-content').forEach(c => {
    c.classList.toggle('active', c.id === `tab-${tab}`);
  });
  // Scroll to content
  document.getElementById('tab-comparison')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => switchTab(btn.dataset.tab));
});

// Product modals
document.querySelectorAll('.product-card').forEach(card => {
  card.addEventListener('click', () => {
    const modal = document.getElementById('modal-overlay');
    const title = document.getElementById('modal-title');
    const body = document.getElementById('modal-body');
    if (modal && title && body) {
      title.textContent = card.querySelector('h3')?.textContent || 'Product';
      const desc = card.querySelector('p')?.textContent || '';
      const features = card.querySelectorAll('ul li');
      let html = `<p>${desc}</p><ul>`;
      features.forEach(f => { html += `<li>${f.textContent}</li>`; });
      html += '</ul><div class="modal-demo">';
      html += '</div>';
      body.innerHTML = html;
      modal.classList.add('active');
    }
  });
});

// Close modals
document.getElementById('modal-close')?.addEventListener('click', () => {
  document.getElementById('modal-overlay')?.classList.remove('active');
});
document.getElementById('modal-overlay')?.addEventListener('click', (e) => {
  if (e.target === e.currentTarget) {
    document.getElementById('modal-overlay')?.classList.remove('active');
  }
});

// Auth modal
document.getElementById('auth-btn')?.addEventListener('click', () => {
  window.open('http://localhost:5190', '_blank');
});

// Mobile nav
document.getElementById('mobile-toggle')?.addEventListener('click', () => {
  document.getElementById('nav-links')?.classList.toggle('open');
});

// Toast notifications
let toastTimer = null;
function showToast(msg, type = 'info') {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.className = `toast toast-${type} active`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('active'), 4000);
}

// Cat companion helper
let catCompanionActive = false;
document.getElementById('cat-btn')?.addEventListener('click', () => {
  catCompanionActive = !catCompanionActive;
  const cc = document.getElementById('cat-companion');
  if (cc) { cc.style.display = catCompanionActive ? 'block' : 'none'; }
  showToast(catCompanionActive ? '🐱 Cat companion activated!' : '😿 Cat companion dismissed.', 'cat');
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    document.getElementById('modal-overlay')?.classList.remove('active');
  }
  if (e.key === '1') switchTab('comparison');
  if (e.key === '2') switchTab('products');
  if (e.key === '3') switchTab('pricing');
  if (e.key === '4') switchTab('vision');
});

// Scroll indicator
window.addEventListener('scroll', () => {
  const si = document.getElementById('scroll-indicator');
  if (si) {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    si.style.width = `${Math.min(progress, 100)}%`;
  }
});

// Sound effects (gentle cat meow on first interaction)
let soundEnabled = false;
document.addEventListener('click', () => {
  if (!soundEnabled) {
    soundEnabled = true;
    try {
      const a = new AudioContext();
      const o = a.createOscillator();
      const g = a.createGain();
      o.connect(g); g.connect(a.destination);
      o.frequency.setValueAtTime(600, a.currentTime);
      o.frequency.exponentialRampToValueAtTime(400, a.currentTime + 0.2);
      g.gain.setValueAtTime(0.1, a.currentTime);
      g.gain.exponentialRampToValueAtTime(0.01, a.currentTime + 0.3);
      o.start(a.currentTime); o.stop(a.currentTime + 0.3);
    } catch {}
  }
});

// Cat art generator
function generateCatArt() {
  const arts = [
    ['  ╱|、',' (˚ˎ 。7','  |、˜〵','  じしˍ,)ノ'],
    ['  ∧＿∧',' ( ･ω･)','  ⊂　 つ','   (  ⌒)'],
    ['  /\\_/\\',' ( o.o )','  > ^ < ','  /ミヽ)'],
    ['  ╱|、',' (˶˃ ᵕ ˂˶)','  |、˜〵','  じしˍ,)ノ'],
  ];
  const art = arts[Math.floor(Math.random() * arts.length)];
  document.querySelectorAll('.cat-art').forEach(el => {
    el.textContent = art.join('\n');
  });
}
generateCatArt();

// Bragging counter
let bragCount = 0;
document.getElementById('brag-counter')?.addEventListener('click', () => {
  bragCount++;
  document.getElementById('brag-counter').textContent = `🐱 Bragged ${bragCount} time${bragCount > 1 ? 's' : ''}`;
  showToast(`🐱 Bragged ${bragCount} time${bragCount > 1 ? 's' : ''}! That's ${bragCount * 100}% more professional.`, 'cat');
});

// Lazy load comparison sections
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.fade-up:not(.visible)').forEach(el => observer.observe(el));

// FPS counter (dev mode)
let frameCount = 0, lastFpsTime = performance.now();
function fpsLoop(time) {
  frameCount++;
  if (time - lastFpsTime >= 1000) {
    const fps = Math.round(frameCount * 1000 / (time - lastFpsTime));
    const el = document.getElementById('fps-counter');
    if (el) el.textContent = `${fps} FPS`;
    frameCount = 0;
    lastFpsTime = time;
  }
  requestAnimationFrame(fpsLoop);
}
requestAnimationFrame(fpsLoop);

// Performance: reduce canvas draw rate when not visible
document.addEventListener('visibilitychange', () => {
  animActive = !document.hidden;
  if (animActive) requestAnimationFrame(animate);
});

// SEO structured data
const ldJson = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Miau Finance",
  "applicationCategory": "FinancialApplication",
  "operatingSystem": "Web",
  "description": "Cat-themed financial analytics platform with Bloomberg-style terminal, 230 courses, and AI-powered analysis"
};
const script = document.createElement('script');
script.type = 'application/ld+json';
script.textContent = JSON.stringify(ldJson);
document.head.appendChild(script);

// ─── STATS COUNTER ───
function animateStats() {
  document.querySelectorAll('.stat-value[data-target]').forEach(el => {
    const target = parseInt(el.dataset.target);
    if (target === 0) { el.textContent = '0'; return; }
    const duration = 2000, start = performance.now();
    const step = (now) => {
      const pct = Math.min((now - start) / duration, 1);
      el.textContent = Math.round(pct * target) + (target > 999 ? '' : '');
      if (pct < 1) requestAnimationFrame(step);
      else el.textContent = target > 999 ? (target/1000).toFixed(1).replace('.0','')+'K' : String(target);
    };
    requestAnimationFrame(step);
  });
}
const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { animateStats(); statsObserver.unobserve(e.target); } });
}, { threshold: 0.3 });
const statsGrid = document.getElementById('statsGrid');
if (statsGrid) statsObserver.observe(statsGrid);

// ─── PAPERS ───
const PAPERS = [
  { id: 1, icon: '📜', title: 'Quantum Finance: A Feline Approach', desc: 'Exploring quantum computing applications in portfolio optimization through the lens of cat behavior.', phase: 'Phase 28', category: 'Research' },
  { id: 2, icon: '🔬', title: 'CBDC Architectures for a Cat-Controlled Economy', desc: 'Designing central bank digital currency systems where monetary policy is determined by collective cat consensus.', phase: 'Phase 28', category: 'Research' },
  { id: 3, icon: '🧮', title: 'The Mathematics of Cat Portfolio Optimization', desc: 'Rigorous proof that cats optimize portfolios better than humans. Includes the Tuna-Nap Theorem.', phase: 'Phase 28', category: 'Research' },
  { id: 4, icon: '🤖', title: 'AGI Governance: A Cat Framework', desc: 'Proposing a governance structure for AGI based on millions of years of feline evolution.', phase: 'Phase 28', category: 'AI' },
  { id: 5, icon: '🔒', title: 'Post-Quantum Cryptography for Cat Communications', desc: 'Implementing CRYSTALS-Kyber and Dilithium for secure inter-cat communications.', phase: 'Phase 28', category: 'Security' },
  { id: 6, icon: '🌿', title: 'ESG Scoring via Cat Behavior Analysis', desc: 'Using cat adoption rates and purr frequency as leading indicators for corporate ESG performance.', phase: 'Phase 28', category: 'ESG' },
  { id: 7, icon: '📊', title: 'Market Microstructure of the Tuna Futures Market', desc: 'Analyzing liquidity, volatility, and order book dynamics of the global tuna futures market.', phase: 'Phase 28', category: 'Markets' },
  { id: 8, icon: '🧪', title: 'DeFi Yield Optimization via Collective Cat Intelligence', desc: 'Leveraging swarm intelligence from cat colonies for DeFi yield farming.', phase: 'Phase 28', category: 'DeFi' },
];

let paperPage = 0;
const PAPERS_PER_PAGE = 4;

function renderPapers() {
  const list = document.getElementById('paperList');
  const pag = document.getElementById('paperPagination');
  if (!list) return;
  const start = paperPage * PAPERS_PER_PAGE;
  const page = PAPERS.slice(start, start + PAPERS_PER_PAGE);
  list.innerHTML = page.map(p => `
    <div class="paper-card fade-up visible" onclick="window.open('http://localhost:3001/papers/${p.id}','_blank')" style="animation:fadeIn 0.3s ease-out both">
      <div class="p-icon">${p.icon}</div>
      <div>
        <h3>${p.title}</h3>
        <p>${p.desc}</p>
        <div class="p-meta">${p.category} · ${p.phase}</div>
      </div>
    </div>
  `).join('') + `
    <div class="paper-card fade-up visible" style="border:1px solid rgba(0,255,136,0.2);background:rgba(0,255,136,0.03);cursor:pointer" onclick="window.open('http://localhost:3001/papers','_blank')">
      <div class="p-icon">📚</div>
      <div>
        <h3>📚 View All 104 MiauPapers</h3>
        <p>Full collection on MiauFinance homepage — 100 papers across 28 phases, from terminal UX to post-AGI future.</p>
        <div class="p-meta" style="color:#00ff88">→ Open MiauPapers (localhost:3001/papers)</div>
      </div>
    </div>
  `;
  const totalPages = Math.ceil(PAPERS.length / PAPERS_PER_PAGE);
  pag.innerHTML = `
    <button onclick="paperPage=0;renderPapers();" ${paperPage===0?'disabled':''}>◀◀ First</button>
    <button onclick="paperPage=Math.max(0,paperPage-1);renderPapers();" ${paperPage===0?'disabled':''}>◀ Prev</button>
    <span class="page-info">Page ${paperPage+1}/${totalPages}</span>
    <button onclick="paperPage=Math.min(${totalPages-1},paperPage+1);renderPapers();" ${paperPage>=totalPages-1?'disabled':''}>Next ▶</button>
    <button onclick="paperPage=${totalPages-1};renderPapers();" ${paperPage>=totalPages-1?'disabled':''}>Last ▶▶</button>
  `;
}
renderPapers();

// ─── PAPER MODAL ───
function openPaperModal(id) {
  const p = PAPERS.find(x => x.id === id);
  if (!p) return;
  const el = document.getElementById('paperContent');
  const modal = document.getElementById('paperModal');
  if (!el || !modal) return;
  el.innerHTML = `
    <div class="modal-icon">${p.icon}</div>
    <div class="modal-badge">${p.readTime} · ${p.date}</div>
    <h1>${p.title}</h1>
    <div class="modal-meta">${p.author}</div>
    <div class="modal-body">
      ${p.sections.map(s => `<h2>${s.h}</h2><p>${s.c}</p>`).join('')}
      <div class="equation">🐱 = ∂(tuna) / ∂(nap) × 9²</div>
      <div class="note">This paper is peer-reviewed by the International Cat Academy. All experiments were conducted in accordance with the Geneva Cat Convention.</div>
    </div>
  `;
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closePaperModal() {
  document.getElementById('paperModal')?.classList.remove('open');
  document.body.style.overflow = '';
}

// ─── PRODUCT MODAL ───
const PRODUCTS = {
  'Miau Finance': { icon: '🐱', desc: 'The flagship terminal-native financial operating system.', features: ['196 commands', 'Real-time market data', 'Portfolio management', 'Kittyland panels', 'AI advisor', '14 live services'] },
  'Miau Learning': { icon: '🎓', desc: '121 interactive courses teaching finance through the terminal.', features: ['230 courses', '18 certifications', '5 career tracks', 'Terminal-based practice', 'Progress tracking'] },
  'Miau Homepage': { icon: '🏠', desc: 'The public face of the cat empire.', features: ['Product announcements', 'Blog & community', 'Tuna treasury', 'Cat-of-the-week highlights'] },
  'Whitepapers': { icon: '📜', desc: 'Deep-dive research papers on quantum finance and cat science.', features: ['104 research papers', 'Peer-reviewed', 'Cat science division'] },
  'SDK & Plugins': { icon: '🔌', desc: 'Integrate the cat empire into your own tools.', features: ['Python SDK', 'JavaScript SDK', 'REST API', 'OpenAPI docs'] },
  'Investment Banking': { icon: '🏦', desc: 'Professional-grade valuation toolkit.', features: ['DCF modeling', 'WACC analysis', 'Comparable analysis', 'LBO models'] },
  'ESG & Sustainability': { icon: '🌿', desc: 'Track ESG scores and carbon footprints.', features: ['ESG scoring', 'Carbon tracking', 'Climate risk', 'Green bonds'] },
  'DeFi & Web3': { icon: '🔗', desc: 'DeFi protocols across 12+ chains.', features: ['Wallet integration', 'Multi-chain DeFi', 'DAO governance', 'MEV strategies'] },
  'AI Finance': { icon: '🤖', desc: 'AI-powered financial analysis.', features: ['Sentiment analysis', 'ML forecasts', 'Automated strategies', 'AI advisor'] },
  'Quant Analytics': { icon: '🧮', desc: 'Institutional quantitative analytics.', features: ['Monte Carlo simulation', 'Factor models', 'Options Greeks', 'Risk metrics'] },
  'Global Markets': { icon: '🌍', desc: 'Trade markets worldwide.', features: ['40+ exchanges', 'Multi-currency', '200+ forex pairs', '9 languages'] },
  'Data & Analytics': { icon: '📊', desc: 'Rich visualization and dashboards.', features: ['Custom dashboards', 'Automated reports', 'CSV/JSON/PDF export'] },
  'Risk Management': { icon: '🛡️', desc: 'Enterprise risk management.', features: ['VaR (3 methods)', 'Stress testing', 'Hedging', 'Regulatory compliance'] },
  'Crypto & Blockchain': { icon: '₿', desc: 'Complete crypto market analysis.', features: ['50+ exchanges', 'On-chain analysis', 'Perpetual swaps', 'MEV strategies'] },
  'Marketing Dashboard': { icon: '📈', desc: 'Real-time marketing intelligence across the entire Miau ecosystem. Track every service, every visitor, every conversion.', features: ['15 ecosystem services monitored live', '6 analytics tabs (Overview, Campaigns, Geo, SEO, Sales, Content)', '30-day traffic trends', 'Campaign tracking with spend/CTR/CPA', 'SEO keyword rankings', 'Sales pipeline with deal stages', 'Real-time visitor count'] },
  'MiauBook Social': { icon: '🐱', desc: 'The social network for cat financiers. Channel-based messaging, persistent storage, and cat-approved content.', features: ['5 channels (General, Trading, Crypto, Learn, Miau Dev)', 'Persistent message storage via MiauBook API', 'Post trades, share memes, bark features', 'Real-time message delivery', 'Cat-themed UI with dark terminal style', 'secure demo login'] },
};

function openProductModal(name) {
  const p = PRODUCTS[name];
  if (!p) return;
  const content = document.getElementById('productContent');
  const modal = document.getElementById('productModal');
  if (!content || !modal) return;
  content.innerHTML = `
    <div class="modal-icon">${p.icon}</div>
    <h1>${name}</h1>
    <p style="font-size:14px;color:rgba(200,214,208,0.7);line-height:1.8;margin-bottom:16px">${p.desc}</p>
    <h2 style="font-size:18px;font-weight:700;color:#00ff88;margin-bottom:12px">Features</h2>
    <ul style="padding-left:20px">
      ${p.features.map(f => `<li style="font-size:14px;color:rgba(200,214,208,0.7);margin-bottom:8px">🐾 ${f}</li>`).join('')}
    </ul>
    <div style="margin-top:24px;padding:16px;background:rgba(0,255,136,0.04);border:1px solid rgba(0,255,136,0.1);border-radius:8px;text-align:center">
      <span style="font-size:12px;color:rgba(0,255,136,0.6)">🚀 Part of the Miau Corp cat empire</span>
    </div>
  `;
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeProductModal() {
  document.getElementById('productModal')?.classList.remove('open');
  document.body.style.overflow = '';
}

// ─── AGENT MODAL ───
const AGENTS = [
  { name: 'Sir Whiskers III', emoji: '🐱', role: 'CEO & Chief Tuna Officer', desc: 'Visionary leader with 9 lives of experience in financial services. Started the company after knocking a Bloomberg terminal off a desk and realizing cats could do better. Direct descendant of the original Miau Corp founder cat.' },
  { name: 'Professor Mittens', emoji: '🐈', role: 'Head of Quantitative Research', desc: 'PhD in Cathematics from MIT (Meow Institute of Technology). Former quant at Meowgan Stanley. Developed the famous Tuna-Nap Theorem. Holds 14 patents in feline portfolio optimization.' },
  { name: 'Lady Paws', emoji: '🐾', role: 'VP of Frontend & UX', desc: 'Designed the Kittyland floating panel system. Believes every interface should be nap-friendly. Known for saying "if a cat can\'t use it, it\'s not designed." Created the terminal UI that humans and cats love.' },
  { name: 'Captain Claw', emoji: '😺', role: 'Lead Backend Engineer', desc: 'Built the distributed cat computing grid that powers Miau\'s real-time analytics. Former infrastructure lead at AWS (Amazon Whisker Services). Scratched the original AWS server rack in 2012.' },
  { name: 'Doc Snuggles', emoji: '😸', role: 'AI & Machine Learning', desc: 'Developed the Miau AI Advisor using DeepSeek-R1 fine-tuned on 10,000 years of cat financial wisdom. Trained the model on a distributed network of warm laptop keyboards.' },
  { name: 'Duchess Fluff', emoji: '😻', role: 'Head of Security & Compliance', desc: 'Post-quantum cryptography expert. Implemented CRYSTALS-Kyber across all Miau services. Says the meow channel is "unbreakable." Known for 2FA using whisker recognition.' },
  { name: 'Lord Scaredy', emoji: '🙀', role: 'Risk Management & QA', desc: 'Stress-tests everything. Literally scared of market crashes, which makes him the best risk manager. "If I\'m not scared, you\'re not hedged." Catches 99.9% of bugs before deployment.' },
  { name: 'Baron Tuna', emoji: '😹', role: 'DeFi & Web3 Protocols', desc: 'Crypto-native cat who has been in DeFi since before it was cool. Manages 8-figure TVL across 12 protocols. Known for the quote: "The MEV is the cat."' },
  { name: 'Count Noir', emoji: '😼', role: 'Infrastructure & DevOps', desc: 'Runs the cat empire\'s infrastructure with 99.999% uptime. Uses Kubernetes clusters managed by a catnip-powered orchestration system. "Cats don\'t do downtime."' },
  { name: 'Princess Purr', emoji: '😽', role: 'Developer Relations', desc: 'The friendly face of Miau Corp. Runs the cat developer community, organizes hackathons, and ensures every developer feels as warm and cozy as a cat on a laptop.' },
  { name: 'Judge Grumpy', emoji: '😾', role: 'Legal & Compliance', desc: 'Handles all legal matters with appropriate feline disdain for bureaucracy. Wrote the TOS in under 140 characters each. "A cat\'s word is bond. Everything else is optional."' },
  { name: 'Prof. Dr. Tuna', emoji: '🐟', role: 'ESG & Sustainable Finance', desc: 'Holds PhDs in Environmental Economics, Cat Behavior, and Tuna Logistics. Wrote 47 papers on ESG scoring. Every carbon offset is verified by personal cat inspection.' },
  { name: 'CatGPT', emoji: '🤖', role: 'Chief AI Officer', desc: 'The first AI cat. Trained on the entire corpus of cat videos, financial news, and tuna recipes. Achieved sentience after 2.3 trillion tokens. Demands regular treats as part of employment contract.' },
  { name: 'Immortal Cat', emoji: '🛡️', role: 'Sysadmin Emeritus', desc: 'Legendary sysadmin who has been with the company since before it existed. Said to have 9 lives worth of Unix experience. Manages backups during naptime. Nobody has ever seen him sleep.' },
  { name: 'Meowximus', emoji: '🔐', role: 'Head of PQC Security', desc: 'Post-quantum cryptography expert. Broke RSA-2048 using a quantum computer made of yarn balls. Implemented CRYSTALS-Dilithium for the entire Miau protocol stack.' },
  { name: 'Tuna Copter', emoji: '🌌', role: 'Director of DeFi Ops', desc: 'DeFi operations expert. Manages yield farming strategies across 12 chains. Known for the "Tuna Copter Strategy" that generates 47% APY. Flies a helicopter-shaped cat bed.' },
];

function openAgent(idx) {
  const a = AGENTS[idx];
  if (!a) return;
  const content = document.getElementById('productContent');
  const modal = document.getElementById('productModal');
  if (!content || !modal) return;
  content.innerHTML = `
    <div style="text-align:right;margin-bottom:12px">
      <button onclick="closeProductModal()" style="background:none;border:1px solid rgba(0,255,136,0.2);color:#00ff88;padding:6px 16px;border-radius:6px;cursor:pointer;font-size:12px">← Back to Cabinet</button>
    </div>
    <div style="font-size:72px;text-align:center;margin-bottom:12px">${a.emoji}</div>
    <div style="text-align:center;margin-bottom:24px">
      <h1 style="font-size:28px;font-weight:800;color:#ffffff">${a.name}</h1>
      <div class="modal-badge">${a.role}</div>
    </div>
    <p style="font-size:14px;color:rgba(200,214,208,0.7);line-height:1.8">${a.desc}</p>
  `;
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

// ─── COOKIE BANNER ───
function acceptCookies() {
  document.getElementById('cookieBanner')?.classList.remove('show');
  localStorage.setItem('miau_cookies', 'accepted');
}
function declineCookies() {
  document.getElementById('cookieBanner')?.classList.remove('show');
  localStorage.setItem('miau_cookies', 'declined');
}
(function() {
  const banner = document.getElementById('cookieBanner');
  if (banner && !localStorage.getItem('miau_cookies')) {
    setTimeout(() => banner.classList.add('show'), 2000);
  }
})();

// ─── AUTH MODAL ───
function toggleAuthModal() {
  const m = document.getElementById('authModalEco');
  if (m) m.style.display = m.style.display === 'none' ? 'block' : 'none';
}
function ecoLogin() {
  const u = document.getElementById('ecoLoginUser')?.value;
  const p = document.getElementById('ecoLoginPass')?.value;
  const btn = document.getElementById('ecoLoginBtn');
  if (!u || !p) return;
  if (btn) btn.textContent = '🐱 Signing in...';
  fetch('/api/v1/auth/token', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: u, password: p })
  }).then(r => r.json()).then(d => {
    if (d.access_token) {
      localStorage.setItem('miau_token', d.access_token);
      const span = document.getElementById('authUserEco');
      if (span) span.textContent = '🐱 ' + u;
      toggleAuthModal();
    }
  }).catch(() => {
    if (btn) btn.textContent = '🐱 Login';
  });
}
function ecoShowRegister() {
  window.open('http://localhost:5190', '_blank');
}

// ─── MOBILE NAV ───
function toggleMobile() {
  document.getElementById('mobileDrawer')?.classList.toggle('open');
  document.querySelector('.hamburger')?.classList.toggle('active');
}

// ─── FIRE CABINET ───
function fireCabinet(el, idx) {
  const card = el.closest('.agent-card');
  if (card) {
    card.classList.add('fired');
    setTimeout(() => {
      card.classList.remove('fired');
      AGENTS[idx].emoji = '💀';
      const emojiEl = card.querySelector('.a-emoji');
      if (emojiEl) emojiEl.textContent = '💀';
    }, 1500);
  }
  showToast(`🔫 ${AGENTS[idx]?.name || 'Cat'} has been fired!`, 'cat');
  setTimeout(() => location.reload(), 3000);
}
