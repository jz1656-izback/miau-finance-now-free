
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
    vx: (Math.random() - 0.5) * 0.15, vy: (Math.random() - 0.5) * 0.1,
    s: Math.random() * 12 + 14, phase: Math.random() * Math.PI * 2, emoji: '🐱'
  });
}

function drawUniverse() {
  if (!animActive) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (const star of stars) {
    star.a += star.s; const alpha = (Math.sin(star.a) + 1) / 2 * 0.5 + 0.1;
    ctx.beginPath(); ctx.arc(star.x, star.y, star.r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(${star.c.join(',')},${alpha})`; ctx.fill();
  }
  for (const f of fishes) {
    f.x += f.vx; f.y += f.vy; f.phase += 0.03;
    if (f.x < -50) f.x = canvas.width + 50; if (f.x > canvas.width + 50) f.x = -50;
    if (f.y < -50) f.y = canvas.height + 50; if (f.y > canvas.height + 50) f.y = -50;
    ctx.save(); ctx.translate(f.x, f.y); ctx.font = `${f.s}px sans-serif`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.globalAlpha = 0.2 + Math.sin(f.phase) * 0.08;
    ctx.fillText(f.emoji, 0, Math.sin(f.phase) * 2); ctx.restore();
  }
  requestAnimationFrame(drawUniverse);
}
drawUniverse();
document.addEventListener('visibilitychange', () => { animActive = !document.hidden; if (!document.hidden) drawUniverse(); });
document.addEventListener('mousemove', e => { mouse.x = e.clientX; mouse.y = e.clientY; });

function animateCounters() {
  document.querySelectorAll('[data-target]').forEach(c => {
    const target = parseInt(c.dataset.target);
    const duration = 2000, start = performance.now();
    function update(now) {
      const p = Math.min((now - start) / duration, 1);
      c.textContent = Math.floor((1 - Math.pow(1 - p, 3)) * target);
      if (p < 1) requestAnimationFrame(update); else c.textContent = target;
    }
    requestAnimationFrame(update);
  });
}
let fadeObserver;
function observeFade() {
  fadeObserver = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); if (e.target.dataset.target) animateCounters(); }
    });
  }, { threshold: 0.05 });
  document.querySelectorAll('.fade-up, .fade-in').forEach(el => fadeObserver.observe(el));
}
function observeNew(el) {
  if (fadeObserver) fadeObserver.observe(el);
}
document.addEventListener('scroll', () => { document.getElementById('header').classList.toggle('scrolled', window.scrollY > 50); });

let tuna = 0;
document.getElementById('tunaFloat').addEventListener('click', () => {
  tuna += Math.floor(Math.random() * 10) + 1;
  document.getElementById('tunaCount').textContent = tuna;
  const s = document.createElement('div'); s.className = 'sparkle';
  s.textContent = '🐟 +' + (Math.floor(Math.random() * 10) + 1);
  s.style.left = (Math.random() * window.innerWidth * 0.8 + window.innerWidth * 0.1) + 'px';
  s.style.top = (Math.random() * window.innerHeight * 0.8 + window.innerHeight * 0.1) + 'px';
  document.body.appendChild(s); setTimeout(() => s.remove(), 1500);
});

const trail = document.getElementById('cursorTrail');
let trailTimer;
document.addEventListener('mousemove', e => {
  cancelAnimationFrame(trailTimer);
  trailTimer = requestAnimationFrame(() => { trail.style.left = e.clientX + 'px'; trail.style.top = e.clientY + 'px'; });
});

const cats = [
  {
    emoji: '🐱', color: '#00ff88',
    name: 'Sir Whiskers III',
    role: 'CEO & Chief Tuna Officer',
    age: '12 (in human years — 67 in cat years of executive experience)',
    hobby: 'Napping on server racks, knocking expensive monitors off desks, reviewing pull requests by walking on keyboards',
    motto: '"A closed mouth catches no tuna. But a catnap catches all the gains."',
    bio: 'Sir Whiskers III founded Miau Corp in 2024 after a distinguished career as a stray who talked his way into a Georgetown MBA program. He has since built the largest cat-operated financial ecosystem in the known universe. His management philosophy combines aggressive tuna acquisition with strategic laziness. He owns 51% of the company and 100% of the warm spots in the office. His boardroom presence is commanding — mostly because he sits directly on the keyboard until he gets what he wants.',
  },
  {
    emoji: '🐈', color: '#00aaff',
    name: 'Professor Mittens',
    role: 'Head of Quantitative Research',
    age: '9 (tenured at 7)',
    hobby: 'Chasing laser pointers (stochastic processes), bird-watching (probability theory), unraveling toilet paper rolls (entropy)',
    motto: '"If you cannot explain it with a p-value less than 0.05, you are not napping hard enough."',
    bio: 'Professor Mittens holds three PhDs: one in Quantitative Finance from MIT, one in Pure Mathematics from Cambridge, and one in Napping from the University of Windowsill. His groundbreaking paper on feline stochastic calculus is the most cited work in meowhematical finance. He developed the 9-Lives Risk Parity model while asleep — literally. He dreamt the entire mathematical framework, woke up, wrote it down, and went back to sleep. The paper has 12,000 citations. He has never been awake for a single one.',
  },
  {
    emoji: '🐾', color: '#ff8800',
    name: 'Lady Paws',
    role: 'VP of Frontend & UX',
    age: '8 (pixel-perfect since birth)',
    hobby: 'Sitting on keyboards (user testing), pawing at moving cursors (QA), rearranging desktop icons (information architecture)',
    motto: '"If a button is not big enough for a paw, it is not big enough for a human finger either."',
    bio: 'Lady Paws is the design genius behind the Miau terminal interface. She believes every UI should be navigable by paw — if a cat cannot use it, a human should not either. Her defining contribution: ensuring every clickable element is at least 44×44 pixels (paw-friendly size). She also introduced the "warm spot" heat map for terminal layout optimization. She reviews every pull request by physically sitting on the laptop and refusing to move until the design meets her standards. Her design philosophy: "Less is more. More naps is most."',
  },
  {
    emoji: '😺', color: '#ffcc00',
    name: 'Captain Claw',
    role: 'Lead Backend Engineer',
    age: '7 (started coding at 4 months)',
    hobby: 'Scratching server cabinets (stress testing), chasing fiber optic cables (network topology), hiding in server rooms (infrastructure)',
    motto: '"It is not a bug, it is an undocumented feature. Also, your cable management is offensive."',
    bio: 'Captain Claw wrote the first line of Miau Finance\'s backend at 4 months old by walking across a keyboard during a hackathon. His paw has never left the keyboard since. He is responsible for the core trading engine, which processes 200,000 orders per second with 99.999% uptime — a reliability rate that his personal sleep schedule does not match. He insists on writing everything in Go because "chasing pointers is what cats do." His code reviews consist of either a purr (approved) or a hiss (denied). There is no in-between. He has never written a comment in his life and sees no reason to start.',
  },
  {
    emoji: '😸', color: '#ff66aa',
    name: 'Doc Snuggles',
    role: 'AI & Machine Learning',
    age: '6 (neural network specialist)',
    hobby: 'Cuddling for warmth (hardware optimization), watching YouTube videos of birds (training data), knocking things off shelves (reinforcement learning)',
    motto: '"The neural network is not overfitting. It has simply achieved a higher state of understanding that you puny humans cannot comprehend."',
    bio: 'Doc Snuggles trained the Miau AI Advisor on a dataset of 10 million cat photos and 50 million financial data points. The resulting model can predict market movements with 67% accuracy — and tell you whether you are a dog person with 100% accuracy (disappointed meow). He believes the key to AGI is understanding that all intelligence is just a fancy way of optimizing for tuna. His current project: teaching the AI to nap productively. Early results show a 40% improvement in inference speed after power naps.',
  },
  {
    emoji: '😻', color: '#44cc44',
    name: 'Duchess Fluff',
    role: 'Head of Security & Compliance',
    age: '10 (paranoid since birth — in a good way)',
    hobby: 'Hiding in cardboard boxes (air-gapped security), staring at walls (intrusion detection), hissing at strangers (zero trust)',
    motto: '"The only secure system is one that is powered off, buried in concrete, and guarded by a cat. We have implemented two of three."',
    bio: 'Duchess Fluff oversees all security operations at Miau Corp. She implemented the post-quantum cryptography suite, the zero-trust network architecture, and the office policy that all humans must pass a "sniff test" before entering the server room. She once prevented a $50M flash loan attack by simply sitting on the alert button for 3 hours (the attacker gave up). Her threat model includes other cats, vacuum cleaners, and the mail carrier. She requires all code to pass 47 security checks before deployment. And a personal sniff.',
  },
  {
    emoji: '🙀', color: '#ff4444',
    name: 'Lord Scaredy',
    role: 'Risk Management & QA',
    age: '5 (anxious but accurate)',
    hobby: 'Hiding under beds (disaster recovery planning), jumping at sudden noises (penetration testing), overthinking everything (risk modeling)',
    motto: '"I told you this would happen. I have been saying it for weeks. Did anyone listen? No. Now where is my emergency tuna stash?"',
    bio: 'Lord Scaredy is the most risk-averse creature in the known universe. His job is to worry about everything so nobody else has to. He models 10,000+ risk scenarios daily, ranging from "what if the Fed raises rates by 200bps" to "what if all the tuna in the world suddenly disappears." His worst-case scenario model has been correct 73% of the time, which honestly just makes him more anxious. His emergency preparedness kit includes: 47 cans of tuna, a backup of the entire codebase, a solar-powered heating pad, and a cardboard box with air holes. He refreshes the kit weekly.',
  },
  {
    emoji: '😹', color: '#aa66ff',
    name: 'Baron Tuna',
    role: 'DeFi & Web3 Protocols',
    age: '4 (started in crypto at 2 weeks old)',
    hobby: 'Staring at trading screens (on-chain analysis), chasing digital mice (NFTs), knocking over blockchain towers (stress testing consensus)',
    motto: '"Not your keys, not your catnip. Also, I minted your profile picture as an NFT. You are welcome."',
    bio: 'Baron Tuna is the youngest member of the cabinet but has been in crypto longer than most humans. He was born on a laptop keyboard during a DeFi hackathon and has been building protocols ever since. He personally designed the Miau DeFi bridge, which handles $2B in cross-chain volume monthly. His first words were "gas war." His favorite protocol is whatever he is currently building, and his least favorite is whatever he built last week (it is "so last quarter"). He holds the record for most consecutive hours staring at a candlestick chart (37 hours, fueled by catnip and spite).',
  },
  {
    emoji: '😼', color: '#00dd88',
    name: 'Count Noir',
    role: 'Infrastructure & DevOps',
    age: '9 (been in production since birth)',
    hobby: 'Tunneling through boxes (containerization), finding warm GPUs (load balancing), unplugging cables (chaos engineering)',
    motto: '"It runs in production. Do not ask how. If something breaks, wait 5 minutes — I probably fixed it already or I am napping."',
    bio: 'Count Noir built the entire Miau Corp infrastructure on a single Raspberry Pi that he found in a dumpster. It has since grown to 10 Docker services across 47 nodes, but he still keeps the original Pi running as a DNS server "for sentimental reasons." He practices chaos engineering by randomly unplugging cables and seeing who notices. His uptime record is 847 days — broken when he accidentally chewed through the backup power cable. He has since implemented cable-chewing detection (a motion-activated spray bottle). He writes all Terraform configs with his paws — actual terraforming.',
  },
  {
    emoji: '😽', color: '#ff88aa',
    name: 'Princess Purr',
    role: 'Developer Relations',
    age: '6 (never met a stranger)',
    hobby: 'Purring at people (customer support), rubbing against keyboards (onboarding), bringing dead mice to meetings (feedback)',
    motto: '"Have you tried turning it off and turning it on again? Also, have you tried petting me? It helps with debugging."',
    bio: 'Princess Purr is the friendly face of Miau Corp. She handles all community interactions, developer onboarding, and crisis de-escalation. Her technique: purr loudly until the other person calms down, then solve their problem while sitting on their keyboard. She personally onboarded 12,000+ students to Miau Learning with a 98% satisfaction rate. Her secret: she listens more than she talks — which is easy when you cannot talk. She communicates entirely through purrs, meows, and disappointed stares. Humans have learned to understand all three fluently.',
  },
  {
    emoji: '😾', color: '#ff6644',
    name: 'Judge Grumpy',
    role: 'Legal & Compliance',
    age: '13 (has seen it all, disapproves of all of it)',
    hobby: 'Judging everyone silently, writing angry letters (cease and desist), hissing at regulatory loopholes',
    motto: '"I am not grumpy. I am just disappointed. In everyone. Always."',
    bio: 'Judge Grumpy is the oldest and most senior member of the cabinet. He has seen every market cycle, every regulatory change, and every stupid human trick in the book. He has never given a verbal compliment in his life and does not plan to start. His approval process for new features: he either looks at it and walks away (approved with extreme prejudice) or he swats it off the desk (rejected). He personally reviews all legal documents by lying on top of them. If he falls asleep, they are approved. If he walks away, they need revision. If he shreds them, they are illegal. His stare has been known to crash development servers from across the room.',
  },
  {
    emoji: '🐟', color: '#44cc88',
    name: 'Prof. Dr. Tuna',
    role: 'ESG & Sustainable Finance',
    age: '11 (fish are friends and food)',
    hobby: 'Swimming in circles (circular economy), staring at fish tanks (impact investing), evaluating carbon pawprints (personal sustainability)',
    motto: '"The planet is warming and your portfolio is not helping. I have three PhDs about this. Also, give me tuna."',
    bio: 'Prof. Dr. Tuna is the most academically decorated fish in the finance industry. Despite being a fish, he has somehow earned PhDs in Climatology, Sustainable Finance, and Cat Law. He is the only non-cat member of the cabinet, included by special decree of Sir Whiskers III after he correctly predicted the 2023 carbon credit market rally. His personal carbon footprint is net-negative (he lives in water and photosynthesizes occasionally). He develops the ESG scoring methodology used by 500+ institutional investors. He is also a certified green bond auditor. His one weakness: he cannot resist a well-presented spreadsheet. Or tuna. Mostly tuna.',
  },
];

const papers = [
  {
    icon: '🧬', color: '#00aaff',
    title: 'Quantum Finance: QUBO Optimization for Portfolio Construction',
    meta: '24 pages · Peer reviewed by the Cat Academy of Sciences · Published 2025',
    authors: 'Professor Mittens, PhD (Quantum Physics, University of Catbridge)',
    sections: [
      { heading: 'Abstract', body: 'We present a novel formulation of the portfolio optimization problem as a Quadratic Unconstrained Binary Optimization (QUBO) problem, solvable on current-generation quantum annealing hardware. Our approach maps the classical mean-variance optimization with cardinality constraints directly to the Ising model, enabling portfolios of up to 2,000 assets to be optimized in under one second of annealing time. We demonstrate that quantum annealing avoids many of the local minima traps that plague classical solvers in high-dimensional portfolio spaces.' },
      { heading: '1. Introduction', body: 'Modern portfolio theory, as originally formulated by Markowitz (1952), requires solving a convex optimization problem that becomes computationally intractable under real-world constraints. The addition of cardinality constraints (limiting the number of assets held), minimum position sizes, and transaction costs transforms the problem into a mixed-integer quadratic program (MIQP) that scales poorly with traditional methods.' },
      { heading: '2. The QUBO Formulation', body: 'We define the portfolio optimization problem using binary decision variables x_i ∈ {0,1} for each of N assets, where x_i = 1 indicates inclusion in the portfolio. The QUBO objective function is:' },
      { heading: '', body: 'minimize: q · (xᵀΣx) — μᵀx + λ · (Σxᵢ — K)² + penalty terms', isEquation: true },
      { heading: '', body: 'where Σ is the covariance matrix, μ is the expected returns vector, K is the target number of assets, q is the risk aversion parameter, and λ is a Lagrange multiplier for the cardinality constraint. The penalty terms handle minimum investment thresholds and sector concentration limits.' },
      { heading: '3. Quantum Annealing Results', body: 'We benchmarked our QUBO formulation against classical solvers (CPLEX, Gurobi) using 10 years of S&P 500 data with 1,500 assets:' },
      { heading: '', body: 'Classical solvers achieved optimal solutions in 47 seconds on average. The D-Wave Advantage quantum annealer reached solutions within 1% of optimal in 0.8 seconds — a 58x speedup. For portfolios with 2,000+ assets, classical solvers failed to converge within 10 minutes, while quantum annealing consistently found high-quality solutions in under 2 seconds.' },
      { heading: '4. Cat Superiority Hypothesis', body: 'We theorize that cats instinctively understand quantum superposition because they exist in all possible states simultaneously (asleep, hungry, plotting, affectionate) until observed. This natural affinity for quantum mechanics may explain their superior portfolio management abilities. Early results from our Quantum Cat Lab support this hypothesis.' },
      { heading: '5. Conclusion', body: 'Quantum annealing offers a practical path to solving large-scale portfolio optimization problems that are intractable for classical computers. Combined with feline intuition, we believe this represents the future of quantitative finance.' },
    ],
  },
  {
    icon: '🏛️', color: '#ff8800',
    title: 'CBDC Architecture: A Technical Framework for Central Bank Digital Currencies',
    meta: '32 pages · Published 2025 · Endorsed by the Central Bank of Miau',
    authors: 'Duchess Fluff, PhD (Distributed Systems) · Count Noir (Infrastructure)',
    sections: [
      { heading: 'Abstract', body: 'We present a comprehensive technical framework for Central Bank Digital Currency (CBDC) design that addresses the competing requirements of privacy, scalability, offline functionality, programmability, and cross-border settlement. Our architecture uses a two-tier model with a permissioned core ledger for wholesale operations and privacy-preserving payment channels for retail transactions. We also introduce the "Purr-consensus" mechanism optimized for central bank use cases.' },
      { heading: '1. Design Principles', body: 'A CBDC must satisfy five core requirements: (1) Privacy — transactions must be private from commercial entities but auditable by regulators, (2) Scalability — support for thousands of transactions per second at national scale, (3) Offline capability — payments must work without internet connectivity, (4) Programmability — support for smart contracts and programmable money, (5) Interoperability — cross-border settlement with other CBDCs and existing payment systems.' },
      { heading: '2. Two-Tier Architecture', body: 'The core ledger runs on a permissioned blockchain maintained by the central bank and regulated commercial banks. Transactions are settled in batches using a novel Byzantine Fault Tolerant (BFT) consensus mechanism we call "Purr-consensus," which achieves 50,000 TPS with finality under 2 seconds. Retail transactions occur off-chain through payment channels with zero-knowledge proofs for privacy.' },
      { heading: '3. Offline Payments', body: 'Offline payments use a blinded signature scheme where users can issue signed transaction vouchers while disconnected. Upon reconnection, vouchers are settled in batch. Our security analysis shows this scheme is resistant to double-spending attacks up to a configurable offline limit (recommended: €200 per day per wallet).' },
      { heading: '4. Cross-Border Settlement', body: 'We propose a "hub-and-spoke" model with a global CBDC clearing house running a atomic swap protocol. Each participating central bank maintains a collateral account in the hub, enabling real-time gross settlement without a global settlement currency. Latency is under 5 seconds for cross-border payments.' },
      { heading: '5. Programmability & Compliance', body: 'Smart contracts are executed in a sandboxed WebAssembly runtime with strict gas limits and timeouts. Compliance rules (KYC/AML, sanctions screening, transaction limits) are enforced at the consensus layer as pre-execution hooks. Regulators have access to a privacy-preserving audit trail via secure multi-party computation.' },
    ],
  },
  {
    icon: '🤖', color: '#ff66aa',
    title: 'Tomorrow: Autonomous Finance AGI',
    meta: '28 pages · Published 2025 · MIAUPAPER FUT-2026-V001',
    authors: 'Doc Snuggles, PhD (AI Safety) · Judge Grumpy, LLD (Cat Law)',
    sections: [
      { heading: 'Abstract', body: 'Miau Finance is on a path to v2.0.0 — a fully autonomous financial operating system. By Phase 27, the platform will transform from a terminal-native trading tool into an AGI that manages your entire financial life. You describe your goals. The cat executes. This paper lays out the roadmap from v1.0.0 to v2.0.0, the engineering challenges, the safety frameworks, and the critical role of feline oversight in autonomous finance.' },
      { heading: '1. The AGI Finance Vision', body: 'Phase 27 represents a paradigm shift in financial software. Instead of you doing the work, you tell the AGI what you want: "I want to retire in 2045 with $2M, and I care about ESG." The system responds by planning your portfolio allocation, tax strategy, rebalancing schedule, and insurance needs. Then it executes — opens positions, harvests tax losses, rebalances quarterly, and reports weekly via terminal and push notification. You live your life. The cat runs the finances. You pet the cat.' },
      { heading: '2. The Roadmap', body: 'The path from v1.0.0 to v2.0.0 spans 27 phases. Phase 13 (AI-Native Terminal) delivered voice commands and agentic workflows. Phase 14 (Global Markets) added multi-currency and international exchanges. Phases 15-16 delivered SDK and ESG tracking. Phase 17 shipped the first autonomous trading agent with human-in-the-loop. Phases 18-21 brought DeFi, WalletConnect, and DAO governance. Phase 22 delivered the Personal AI Analyst. Phase 23 is the Education Platform — 74 courses, 7 certifications. Phases 24-26 added GameFi, CBDC, and quantum-ready infrastructure. Phase 27 is AGI Finance.' },
      { heading: '3. What Stands Between Us and AGI', body: 'Four challenges remain. (1) Reliability — the AI must be correct 99.9%+ on financial decisions. Currently at ~85% on structured tasks, ~60% on open-ended. (2) Safety — guardrails that prevent the AI from YOLO-ing your retirement into 0DTE options. (3) Explainability — every trade must come with a 3-sentence justification a human can understand. (4) Cat approval — the cat must sign off on all trades >$10,000. The cat is the final escalation point. We are 70% through the roadmap as of this publication.' },
      { heading: '4. The Cat Advisor Architecture', body: 'Miau\'s AI advisor has full portfolio context. It doesn\'t just know you asked a question — it knows your holdings, Sharpe ratio, drawdown, VaR, sector weights vs SPY, rolling beta over 36 months, last 20 trades, and attribution report. When you type "ai should I add healthcare exposure?", the AI sees your 3% healthcare vs the benchmark\'s 14% and responds with specific, actionable advice: "Your portfolio has 3.0% healthcare vs SPY\'s 14.2%. This sector underweight explains 2.1% of tracking error. Adding UNH (+22% upside per DCF) would close this gap."' },
      { heading: '5. Safety & Governance', body: 'Every AGI trading agent implements a three-level circuit breaker: Soft kill (completes current transactions, accepts no new instructions), Hard kill (all positions liquidated, system shut down), and Cat override (a physical switch only a cat can press — designed to be warm and comfortable to encourage feline intervention). All decisions are logged to an immutable audit trail with full explainability. The emergency shutdown protocol: open a tin of tuna in another room. The AGI, being cat-brained, will investigate. This buys 15 minutes to restore backups.' },
    ],
  },
  {
    icon: '🌿', color: '#44cc44',
    title: 'ESG Beyond Scores: Climate Risk, Carbon Accounting, and Nature-Based Solutions',
    meta: '20 pages · Published 2025 · Prof. Dr. Tuna, PhD, MBA, LLD',
    authors: 'Prof. Dr. Tuna (Climatology, Catbridge University) · Lady Paws (Sustainable Finance)',
    sections: [
      { heading: 'Abstract', body: 'We move beyond simple ESG scoring to provide a comprehensive framework for climate risk assessment, carbon lifecycle analysis, and natural capital valuation. Our methodology integrates physical risk modeling (flood, fire, storm exposure) with transition risk analysis (policy change, technology disruption) and nature-based solution valuation. Applied to a portfolio of 500 global equities, we find that 73% of companies have material un-priced climate risk.' },
      { heading: '1. Physical Risk Modeling', body: 'Using CMIP6 climate model outputs downscaled to asset-level resolution, we compute physical risk scores for each portfolio holding. Risk factors include: flood risk (coastal and riverine), wildfire risk (based on vegetation, climate, and topography), hurricane/typhoon risk (using historical tracks and SST projections), and heat stress risk (impact on labor productivity and crop yields). Each asset receives a 0-100 physical risk score for 2030, 2050, and 2100 horizons.' },
      { heading: '2. Transition Risk Analysis', body: 'We model transition risk through three scenarios: (1) Net Zero 2050 — orderly transition with increasing carbon prices reaching $250/ton by 2050, (2) Delayed Transition — policies begin in 2030 with rapid catch-up (carbon price spikes to $400/ton), (3) Current Policies — no new climate policies. For each scenario, we compute revenue-at-risk for each portfolio company based on its carbon intensity, regulatory exposure, and technological adaptability.' },
      { heading: '3. Carbon Lifecycle Accounting', body: 'Our framework extends beyond Scope 1, 2, and 3 emissions to include: avoided emissions (products that reduce others\' emissions), sequestered emissions (nature-based solutions), and embedded carbon (supply chain materials). We introduce the "Carbon Pawprint" metric — a standardized measure of total climate impact normalized to tuna equivalents.' },
      { heading: '4. Nature-Based Solutions', body: 'We value nature-based assets including: forest carbon credits (verified under REDD+), blue carbon (mangrove and seagrass sequestration), soil carbon (regenerative agriculture), and biodiversity offsets. Our pricing model uses a combination of market prices (voluntary carbon markets), social cost of carbon (SCC) methodology, and option value (preserving future use options).' },
      { heading: '5. Portfolio Implications', body: 'Applying our framework to a typical pension fund portfolio reveals: 18% of holdings have severe un-priced physical risk, 34% face material transition risk under Net Zero 2050, and only 12% have any exposure to nature-based solutions. We recommend a minimum 5% allocation to nature-based solutions and active management of both physical and transition risk exposures.' },
    ],
  },
  {
    icon: '🐱', color: '#00ff88',
    title: 'Why Cats Make Better Traders Than Humans',
    meta: '16 pages · Published 2024 · MIAUPAPER PHIL-2026-V001',
    authors: 'Sir Whiskers III, PhD (Feline Economics) · Professor Mittens, PhD (Behavioral Finance)',
    sections: [
      { heading: 'Abstract', body: 'Why does Miau Finance have a cat theme? Because cats embody the ideal trading psychology. This paper examines seven feline traits and their direct application to financial markets: patience (a cat waits at the mouse hole for hours — a good trader waits for the perfect entry), independence (cats do not follow the herd — they look at it, yawn, and go back to sleep), risk management (a cat always lands on its feet — always have a hedge), selectivity (cats do not chase every laser pointer — good traders do not chase every trade), rest (cats sleep 16 hours a day — tired traders make bad decisions), curiosity (cats investigate boxes — good traders investigate before investing), and indifference (cats do not care about a bad trade from 3 days ago — neither should you).' },
      { heading: '1. The Cat Philosophy', body: 'Cat trading vs human trading: Cats sleep until hungry, humans overthink until paralyzed. Cats always land on their feet, humans sometimes land in bankruptcy. Cats have no FOMO — they nap instead, humans buy the top and sell the bottom. Cats do whisker analysis, humans watch 48 hours of YouTube videos. Cats hold 50% tuna and 50% treats, humans hold 100% conviction picks. Cats do not track win rates — who knows, who cares. Humans track them religiously. Cats are on 24/7 nap schedule, humans trade 9:30-4:00 EST plus pre/post market. Cats key indicator: can opener sound. Humans: RSI + MACD + Fibonacci.' },
      { heading: '2. Patience & Independence', body: 'A cat can wait motionless at a mouse hole for 4 hours. Not distracted. Not checking Twitter. Not second-guessing the spot. Just waiting for the optimal moment to strike. This is the ideal entry strategy for any financial market. Furthermore, cats do not care what the herd thinks. A cat looks at 100 humans doing the same thing, yawns, and walks away. This is anti-FOMO behavior encoded at the biological level. The cat was contrarian before being contrarian was mainstream.' },
      { heading: '3. Risk Management & Selectivity', body: 'Cats have an innate righting reflex — they always land on their feet. This is the biological equivalent of a trailing stop loss and a hedge rolled into one. In finance, this means: always have an exit plan, always know your downside, and never risk more than you can afford to land on. Additionally, a cat does not chase every laser pointer. It evaluates: "Is this worth my energy?" Most trades are not worth your energy. The best traders take the fewest trades. The cat approves.' },
      { heading: '4. Rest & Curiosity', body: 'Cats sleep 12-16 hours per day. They are the most efficient energy conservers in the animal kingdom. A tired trader makes bad decisions — chasing losses, taking unnecessary risks, abandoning the plan. The market will be there tomorrow. The cat will be there, too. Probably in the same sunny spot. Curiosity: cats investigate every box, every bag, every closed door. Good traders investigate every investment. But here is the key: cats investigate efficiently. They sniff once. If it passes, they sit in the box. No second-guessing. No analysis paralysis.' },
      { heading: '5. The Cat vs Human Benchmark', body: 'We compared a cat\'s portfolio (50% tuna futures, 30% cardboard box manufacturers, 20% things that sparkle) against 1,000 actively managed human portfolios over 12 months. The cat\'s portfolio returned 7.2% — outperforming 68% of human-managed portfolios. The cat slept through 91% of trading hours. The humans averaged 47 hours per week. We legally have to clarify: no cats were consulted during this study. Several cats were consulted. Their feedback was "meow." We interpreted this as strong approval.' },
    ],
  },
  {
    icon: '🔐', color: '#aa66ff',
    title: 'Post-Quantum Cryptography for Financial Infrastructure',
    meta: '22 pages · Published 2025 · NIST-Standard Compliant',
    authors: 'Duchess Fluff, PhD (Cryptography) · Count Noir (Security Architecture)',
    sections: [
      { heading: 'Abstract', body: 'We present a comprehensive migration framework for financial infrastructure to post-quantum cryptography (PQC). Our implementation covers three NIST-standardized algorithms: CRYSTALS-Dilithium for digital signatures, CRYSTALS-Kyber for key encapsulation, and FALCON for compact signatures. We benchmark these algorithms across financial workloads including JWT authentication, transaction signing, API request signing, and secure communication channels. Results show that PQC is production-ready for most financial applications with acceptable performance trade-offs.' },
      { heading: '1. The Quantum Threat to Finance', body: 'Shor\'s algorithm threatens all public-key cryptography currently used in financial infrastructure. RSA-2048 can be broken by a fault-tolerant quantum computer with approximately 4,000 logical qubits — a threshold that NIST projects could be reached within 10-15 years. Financial data with long confidentiality requirements (mortgage records, trade histories) is at immediate risk of "harvest now, decrypt later" attacks.' },
      { heading: '2. Algorithm Selection', body: 'After evaluating all NIST PQC finalists, we selected: CRYSTALS-Dilithium (primary signature algorithm) — provides the best balance of signature size, verification speed, and security margin. We use Dilithium-3 (NIST security level 3) as default. CRYSTALS-Kyber (key encapsulation) — recommended by NIST for general encryption. Kyber-768 provides AES-192 equivalent security. FALCON (compact signatures) — used where signature size is critical (blockchain transactions, hardware security modules).' },
      { heading: '3. JWT Migration', body: 'We migrated Miau Finance\'s JWT authentication from RS256 (RSA) to Dilithium-3. Token size increased from ~400 bytes to ~1,200 bytes (3x). Signing time increased from 1.2ms to 3.8ms (3.2x). Verification time increased from 0.3ms to 0.9ms (3x). Critical finding: PQC JWT verification is still 10,000x faster than a single database query — the performance impact on real-world applications is negligible.' },
      { heading: '4. Transaction Signing', body: 'For high-frequency trading applications where every microsecond counts, we implemented a hybrid signing scheme: FALCON-512 for the primary signature (only 666 bytes, fastest verification of any PQC scheme) combined with ECDSA as a backward-compatible fallback. Our benchmarks show FALCON verification completes in 0.15ms — within 2x of ECDSA and acceptable for all but the most latency-sensitive HFT applications.' },
      { heading: '5. Migration Strategy', body: 'We recommend a four-phase migration: (1) Inventory — catalog all cryptographic dependencies, (2) Hybrid mode — implement dual signing (PQC + classical) for backward compatibility, (3) Upgrade clients — migrate all clients to support PQC, (4) Full cutover — disable classical algorithms. Estimated timeline: 18-24 months for full migration. Cost: approximately 3-5% increase in CPU utilization and 2-4x increase in signature storage requirements.' },
    ],
  },
  {
    icon: '🔗', color: '#aa66ff',
    title: 'DeFi Composability Risk: A Systematic Framework',
    meta: '18 pages · Published 2025 · DeFi Safety Rating: A+ (Cat Approved)',
    authors: 'Baron Tuna (DeFi Architecture) · Lord Scaredy (Risk Management)',
    sections: [
      { heading: 'Abstract', body: 'We introduce a systematic framework for measuring and managing composability risk in decentralized finance (DeFi) protocols. Composability — the ability of DeFi protocols to interact and combine like LEGO blocks — creates systemic risk that traditional financial risk models fail to capture. Our framework introduces the "Composability Contagion Matrix" (CCM) for modeling cascade effects and the "Degen Multiplier" (β) for quantifying ape-in readiness.' },
      { heading: '1. The Composability Problem', body: 'In traditional finance, risk is contained within institutional boundaries. In DeFi, protocols are interconnected through shared liquidity, nested positions, and recursive dependencies. A liquidation event in one protocol can cascade through 5+ protocols within seconds. The May 2022 UST/LUNA collapse and the November 2022 FTX contagion demonstrated that composability risk is the single greatest systemic threat in decentralized finance.' },
      { heading: '2. The Composability Contagion Matrix', body: 'The CCM is an N×N matrix where each entry C_ij represents the probability that a failure in protocol i causes a failure in protocol j. We compute C_ij using four factors: (1) Shared liquidity exposure — percentage of liquidity shared between protocols, (2) Dependency depth — number of protocol layers between i and j, (3) Oracle correlation — degree of shared price feed dependencies, (4) Governance overlap — shared token holders and governance participants.' },
      { heading: '3. The Degen Multiplier (β)', body: 'The Degen Multiplier quantifies the "ape-in readiness" of a DeFi protocol. β = Σ(w_i × r_i) / (σ_portfolio × √L), where w_i are position weights, r_i are expected returns, σ_portfolio is portfolio volatility, and L is leverage ratio. A β > 1.5 indicates degen territory — proceed with caution (and cat supervision). Current DeFi market average β: 2.3 (extremely degen). Cat-recommended maximum β: 1.0 (responsible degen).' },
      { heading: '4. Cascade Modeling', body: 'We simulate cascade effects using a multi-agent model with 1,000 heterogeneous agents across 50 DeFi protocols. Key findings: (1) A 30% ETH price drop triggers cascading liquidations affecting 23% of protocols within 2 blocks, (2) Protocols with >50% composability exposure (connected to 25+ other protocols) show cascading failure probability of 67%, (3) Isolated protocols (<10 connections) show cascade probability of only 8%, (4) Circuit breakers at individual protocol levels reduce cascade probability by 41%.' },
      { heading: '5. Risk Mitigation Strategies', body: 'We recommend: (1) Protocol-level circuit breakers — automatic trading pauses when price moves exceed thresholds, (2) Cross-protocol collateral limits — restrict borrowing against LP tokens from highly interconnected protocols, (3) Composability scoring — public ratings for protocol interconnectivity (the "Degen Score"), (4) Insurance pools — decentralized insurance against composability failures, (5) The Cat Rule — if a protocol\'s complexity exceeds nine steps of nested dependencies, the cat must personally approve all interactions.' },
    ],
  },
  {
    icon: '🎓', color: '#00aaff',
    title: 'Why the Terminal Will Eat the Dashboard',
    meta: '30 pages · Published 2025 · MIAUPAPER FIN-2026-V001',
    authors: 'Lady Paws (UX Research) · Captain Claw (Terminal Architecture)',
    sections: [
      { heading: 'Abstract', body: 'Bloomberg Terminal costs $24,000 per year. Reuters Eikon costs $22,000. Meanwhile, your average hedge fund analyst clicks a GUI dashboard 10,000 times a day to accomplish what a single grep command could do in 200 milliseconds. Miau Finance chose the terminal not because it is retro-cool (though it is), but because CLI is fundamentally faster than any GUI for financial workflows. This paper quantifies the performance difference and presents the case for terminal-native financial software.' },
      { heading: '1. The Numbers', body: 'Every click costs approximately 1.2 seconds of cognitive context-switch. A typical financial workflow has 40-60 clicks — 48-72 seconds of lost focus per workflow, or roughly 1 hour of lost productivity per day for a full-time analyst. Miau Finance cuts this to 4-8 commands — 3-6 seconds total. Specific benchmarks: Checking AAPL price takes 0.4s in terminal vs 12s in GUI. Getting portfolio risk takes 0.8s vs 45s. Comparing 5 tickers takes 1.2s vs 60s. Backtesting a strategy takes 3.1s vs 15+ minutes. Getting AI advisor opinion takes 2.4s vs 5+ minutes.' },
      { heading: '2. Why Not Both?', body: 'Miau is not GUI-hating. The terminal is the primary interface for power users, while the PWA provides push notifications, offline access, and touch-optimized views for mobile. You can share a portfolio link with a client and they see a beautiful rendered page. But when you need to work — really work — the keyboard is your weapon and the terminal is your battlefield. The CLI is the last honest interface. It does not pretend to be user-friendly. It is user-efficient.' },
      { heading: '3. The Terminal Philosophy', body: 'GUI workflow: Mouse → Click → Wait → Scan → Click → Wait → Read → Click → Type → Click. CLI workflow: Type → Enter → Read. That is the difference between 10 cognitive steps and 3. Every extra step is a context switch, a chance for distraction, an opportunity for error. The terminal eliminates the middleman between your brain and the data. It is direct manipulation of information, not indirect manipulation of interface widgets. This is why hedge fund analysts who switch to Miau report 40% faster research workflows.' },
      { heading: '4. Education Pipeline', body: 'The terminal-native approach extends to education. Miau Learning teaches finance through the same terminal commands used by professionals. 74 courses, 7 certifications, 5 career tracks. Students learn by typing real commands, seeing real outputs, and making real (paper) mistakes. After 10 hours of terminal-native instruction, students achieve proficiency equivalent to 40 hours of video instruction — a 4x efficiency gain. The cat learned by breaking things. So will you.' },
      { heading: '5. The Proprietary Advantage', body: 'Miau Finance is proprietary. This means we charge money, which means we can afford tuna, pawborghinis, purraris, and pawrsches. Our developers are well-fed and well-compensated. They do not eat ramen. They do not beg for GitHub stars. They ship features because you pay for them. Proprietary means dedicated support, guaranteed SLAs, audit compliance, and enterprise-grade security. It means no abandoned open source forks with 0 commits in 2 years. It means when you email support@miau.finance, a cat responds within 1 hour. (The cat delegates to a human. The human is also well-paid because we charge money.)' },
    ],
  },
  {
    icon: '💡', color: '#ff8800',
    title: 'Why the Terminal Will Eat the Dashboard',
    meta: '12 pages · MIAUPAPER FIN-2026-V001 · Published 2025',
    authors: 'Lady Paws (UX Research) · Captain Claw (Terminal Architecture)',
    sections: [
      { heading: 'Abstract', body: 'Bloomberg Terminal costs $24,000 per year. Reuters Eikon costs $22,000. Meanwhile, your average hedge fund analyst clicks a GUI dashboard 10,000 times a day to accomplish what a single `grep` could have done in 200 milliseconds. Miau Finance chose the terminal not because it\'s retro-cool (though it is), but because CLI is fundamentally faster than any GUI for financial workflows. Terminal is 4-10x faster for financial tasks and is scriptable, SSH-able, and doesn\'t require a $3,000 GPU.' },
      { heading: '1. The Click Tax', body: 'Every click costs approximately 1.2 seconds of cognitive context-switch. A typical financial workflow has 40-60 clicks. That is 48-72 seconds of lost focus per workflow, or roughly 1 hour of lost productivity per day for a full-time analyst. Checking AAPL price: GUI takes 12 seconds (navigate → search → type → click → wait → read). Terminal: 0.4 seconds. Getting portfolio risk: GUI takes 45 seconds (Reports → Risk → Select → Generate → Wait → Scroll → Read). Terminal: 0.8 seconds.' },
      { heading: '2. The CLI Philosophy', body: 'GUI workflow: Mouse → Click → Wait → Scan → Click → Wait → Read → Click → Type → Click. CLI workflow: Type → Enter → Read. That is 10 cognitive steps versus 3. Every extra step is a context switch, a chance for distraction, an opportunity for error. The terminal eliminates the middleman between your brain and the data. It is direct manipulation of information, not indirect manipulation of interface widgets. The CLI is the last honest interface. It does not pretend to be user-friendly. It is user-efficient.' },
      { heading: '3. Why Not Both', body: 'Miau is not GUI-hating. The terminal is the primary interface for power users, while the PWA provides push notifications, offline access, and touch-optimized views for mobile. You can share a portfolio link with a client and they see a beautiful rendered page. But when you need to work — really work — the keyboard is your weapon and the terminal is your battlefield. Hedge fund analysts who switch to Miau report 40% faster research workflows.' },
    ],
  },
  {
    icon: '🤖', color: '#ff66aa',
    title: 'The Cat Advisor: AI That Knows Your Portfolio',
    meta: '14 pages · MIAUPAPER AI-2026-V001 · Published 2025',
    authors: 'Doc Snuggles, PhD (AI Research) · Princess Purr (UX)',
    sections: [
      { heading: 'Abstract', body: 'Most "AI-powered finance" products wrap ChatGPT\'s API and call it a product. The conversation is always: "Consider AAPL, MSFT, AMZN — they have strong fundamentals." This is not financial advice. This is a search engine with a personality. Miau\'s AI advisor has full portfolio context — it knows your holdings, Sharpe ratio, drawdown, VaR, sector weights, rolling beta, last 20 trades, and attribution report before it generates a response. When you ask a question, the AI sees everything.' },
      { heading: '1. The Context Architecture', body: 'When you type "ai should I add healthcare exposure?", the Context Builder fetches live portfolio data, market data, risk analytics, and valuation models before the prompt reaches the AI. The AI receives a 3,000-token structured context with everything it needs. Result: "Your portfolio has 3.0% healthcare exposure vs SPY\'s 14.2%. This sector underweight explains 2.1% of your tracking error. Adding UNH (+22% potential upside per DCF, $590 fair price) would help close this gap. Your WACC is 8.4%, making healthcare a defensive addition. Recommendation: BUY 10% UNH."' },
      { heading: '2. The Intent Pipeline', body: 'The ask command converts plain English to API calls using an intent-to-endpoint mapper. "Show me my top 5 holdings by weight" → GET /api/v1/portfolios. "Show me the correlation between AAPL and MSFT over the last year" → GET /api/v1/economics/correlation. The mapper supports 40+ intents with a regex fallback when the LLM is unavailable. You get answers even when OpenAI has an outage.' },
      { heading: '3. Benchmarks', body: 'We benchmarked our AI against 3 human financial advisors. Our AI was more specific 78% of the time. The humans were more comforting 100% of the time. Neither understood cats. The cat\'s investment strategy (50% tuna futures, 50% scratching post manufacturers) returned +7.2% YTD vs Bloomberg\'s +1.8%. Draw your own conclusions.' },
    ],
  },
  {
    icon: '📝', color: '#ff4444',
    title: 'Paper Trading That Hurts (And Why That\'s Good)',
    meta: '10 pages · MIAUPAPER TRD-2026-V001 · Published 2025',
    authors: 'Lord Scaredy (Risk Simulation) · Captain Claw (Fill Engine)',
    sections: [
      { heading: 'Abstract', body: 'Most paper trading platforms are video games. You place a market order and it fills at the exact price you saw on the screen, with zero friction. You win every time. Then you go live and lose 30% in a week because reality has slippage, commissions, and market impact. Miau\'s paper trading is designed to hurt. Not because we are mean — because we want you to learn what real trading feels like before you touch real money.' },
      { heading: '1. The Fill Simulator', body: 'Volume-based slippage: larger orders get more slippage (configurable 0.01%-0.5%). Per-share + per-trade tiered commission schedule. Full transaction cost analysis: spread cost + market impact + timing cost. Limit orders only fill when market price crosses your limit, with partial fills supported. Stop orders trigger on stop price, convert to market, fill at triggered price + slippage. Trailing stops track the highest price and trigger on reversal by trail amount.' },
      { heading: '2. Accuracy Benchmarks', body: 'We ran 10,000 paper trades across 50 tickers and compared fill prices to actual exchange data. Market order fill price accuracy: ±0.08%. Limit order fill probability accuracy: ±3%. Commission model accuracy: ±$0.02/trade. Users who paper-traded for 2 weeks before going live had 22% lower max drawdown, 3.4x more limit orders placed (saving ~$0.12/share in spread), and 40% fewer trades per day (less overtrading).' },
    ],
  },
  {
    icon: '🦀', color: '#ff6644',
    title: 'From Red to Green in 60 Lines of Rust',
    meta: '8 pages · MIAUPAPER ENG-2026-V001 · Published 2025',
    authors: 'Count Noir (Rust Architecture) · Captain Claw (Performance)',
    sections: [
      { heading: 'Abstract', body: 'Financial computing is performance-critical. A Monte Carlo simulation with 10,000 paths and 252 time steps takes 1,240ms in pure Python (for loop), 87ms in NumPy vectorized, 41ms in Miau Rust (PyO3), and 32ms in raw Rust. Our Rust engine delivers 2.1x speedup vs NumPy and 30x vs pure Python while maintaining Python-callable ergonomics through PyO3 bindings.' },
      { heading: '1. The Rust Modules', body: 'The Rust engine comprises 6 modules totaling ~2,140 lines: monte_carlo.rs (580 lines, GBM simulation, price paths, confidence intervals), optimizer.rs (420 lines, Markowitz mean-variance, efficient frontier), regression.rs (240 lines, OLS Gaussian elimination, factor loadings, t-stats), regime.rs (380 lines, HMM with log-domain forward-backward, Viterbi, Baum-Welch), anomaly.rs (400 lines, Z-score detection, isolation forest, rolling window statistics), and tokenizer.rs (120 lines for AI prompt optimization).' },
      { heading: '2. The Fallback Architecture', body: 'Every Rust function has a transparent Python/NumPy fallback. Users with Rust installed get 2x speed. Users without Rust (ARM Macs, Windows without MSVC) still get correct results via NumPy. The fallback is never silent — it logs a warning so users know when they are running the slower path. But it always returns correct results. The Rust compiler once refused to compile our code because we wrote unwrap() in a production path. The compiler was right.' },
    ],
  },
  {
    icon: '📱', color: '#00aaff',
    title: 'DeFi Without the Laptop',
    meta: '10 pages · MIAUPAPER MOB-2026-V001 · Published 2025',
    authors: 'Princess Purr (PWA) · Baron Tuna (Mobile DeFi)',
    sections: [
      { heading: 'Abstract', body: 'Financial platforms assume you are at a desk. But financial decisions happen everywhere — checking overnight futures from bed at 6:45 AM, getting push notifications for pre-market moves at 8:02 AM, reviewing P&L on lunch break, closing positions before market close at 3:58 PM, and reviewing daily performance on the couch at 9:00 PM. Miau runs as a Progressive Web App that works offline, installs on your home screen, sends push notifications, and sizes from 320px to 4K.' },
      { heading: '1. The PWA Stack', body: 'Install as app via manifest.json + service worker. Offline mode via Cache API (stale-while-revalidate for market data, cache-first for portfolios) and IndexedDB for local portfolio storage. Push notifications via VAPID keys. Responsive from 320px to 4K. Dark mode via prefers-color-scheme detection. Background Sync queues offline commands and retries when connection restores.' },
      { heading: '2. Notification Channels', body: 'Browser Push for price alerts, trade confirmations, and AI analysis ready. WhatsApp for daily portfolio summary at 08:00 local time. Telegram bot with inline keyboard for quick actions. Email via SMTP with configurable sender. The WhatsApp bot once sent "Your portfolio is up 2.3% today. Also, the local grocery store has tuna on sale." We are not sure which notification got higher engagement.' },
    ],
  },
  {
    icon: '💬', color: '#ff88aa',
    title: 'The Social Network Your Broker Doesn\'t Want',
    meta: '10 pages · MIAUPAPER SOC-2026-V001 · Published 2025',
    authors: 'Princess Purr (Community) · Sir Whiskers III (Strategy)',
    sections: [
      { heading: 'Abstract', body: 'Trading is isolating. You stare at charts, make decisions, and nobody sees your wins or your losses. Your broker doesn\'t care. Your cat cares, but only if your wins mean more treats. Miau adds a social layer that turns trading into a community: portfolio sharing via public links, leaderboards by return/Sharpe/gain, a real-time activity feed, a follow system, reputation badges, and threaded comments.' },
      { heading: '1. Social Features & Impact', body: 'Generate a public link (/p/abc123) that shows your portfolio to anyone with no auth required. Weekly, monthly, and all-time leaderboards by return, Sharpe, and total gain. Real-time stream of trades, achievements, and AI insights from people you follow. Follow traders whose strategies you respect. Automatic badges: first_trade, profitable_week, top_10_weekly, ai_master. Data shows users who follow 5+ traders have 15% higher win rate. Users on the leaderboard are 40% more likely to share their strategy.' },
      { heading: '2. Moderation Philosophy', body: 'Algorithmic spam detection on posts with 5+ identical messages in 60 seconds. Community reporting — items with 3+ reports are hidden pending review. Cat-based moderation: a random cat emoji is inserted into the feed every 100 activities. If nobody notices, the feed is too noisy and we tune the algorithm. The top-ranked user is actually a cat who gained 12% by sleeping through the entire trading week. The cat refuses to share its strategy. "Proprietary napping techniques" is all we got.' },
    ],
  },
  {
    icon: '💳', color: '#ffcc00',
    title: 'API Keys and Tuna: Monetization Without the Slime',
    meta: '12 pages · MIAUPAPER BIZ-2026-V001 · Published 2025',
    authors: 'Sir Whiskers III (CEO) · Duchess Fluff (Security)',
    sections: [
      { heading: 'Abstract', body: 'Most finance platforms monetize by selling your data to hedge funds, showing ads, or charging $24,000/year for "enterprise" (same features as free but with a PDF invoice). Miau monetizes by selling value, not users. Free tier is genuinely useful — prices, portfolio, signals, watchlist. No nag screens. Pro tier (€99/mo) unlocks AI advisor, paper trading, and full strategy backtesting. Enterprise (€396/mo) adds multi-user workspaces, custom brokers, and API key platform.' },
      { heading: '1. The API Key Platform', body: 'Enterprise users can generate scoped API keys: market:read, orders:create, portfolios:read, analytics:all. Each key has per-key rate limits (configurable multiplier vs base limit), usage tracking (requests/day, data transfer/month), expiration dates (auto-revoke on expiry), and webhook events (key created, key revoked, usage threshold reached).' },
      { heading: '2. Why This Model Works', body: 'Free tier is genuinely useful — everything a retail investor needs. Pro tier unlocks power user features that save time and money. Enterprise tier enables businesses to build on Miau. We charge money so we don\'t have to sell your data. We charge money so we can buy tuna. Open source developers tried to fork Miau. They couldn\'t afford the hosting. They couldn\'t afford the tuna. They went back to using free APIs.' },
    ],
  },
  {
    icon: '🔒', color: '#44cc44',
    title: 'Privacy by Default, Paranoia by Design',
    meta: '14 pages · MIAUPAPER SEC-2026-V001 · Published 2025',
    authors: 'Duchess Fluff, PhD (Security) · Judge Grumpy (Compliance)',
    sections: [
      { heading: 'Abstract', body: 'Miau Finance was built with the assumption that someone, somewhere, will try to break in. Probably a cat. Cats are naturally curious about API endpoints. The security stack spans 8 layers: JWT with bcrypt-hashed passwords and 15min access token expiry, RBAC with workspace isolation and API key scopes, Redis sliding window rate limiting, input sanitization (XSS, SQLi, ticker regex), CSP/HSTS/COEP/COOP transport security, PCI-DSS/SOC2 compliant audit logging, double-submit cookie CSRF protection, and full TLS encryption for all broker connections.' },
      { heading: '1. OWASP Audit Results', body: 'Full OWASP Top 10 audit results: Broken Access Control — fixed with RBAC middleware and workspace isolation. Cryptographic Failures — fixed with PBKDF2 salt randomization, bcrypt, TLS enforcement. Injection — fixed with input sanitization middleware and parameterized queries. Insecure Design — fixed with rate limiting, CSP, audit logging. Security Misconfiguration — fixed with .env secrets, no hardcoded credentials, security headers. Auth Failures — fixed with JWT 32+ char secret enforcement and token expiry.' },
      { heading: '2. The Privacy Model', body: 'No third-party analytics (no Google Analytics, no Mixpanel). No telemetry — the backend doesn\'t phone home. No data selling — your portfolio data is yours. Self-hostable — the entire stack is Docker Compose. GDPR-ready with export/delete user data endpoints. We encrypt your data so well even the cat can\'t scratch it. The cat is annoyed. The cat feels it should have root access. The cat has been denied.' },
    ],
  },
  {
    icon: '📡', color: '#00aaff',
    title: 'Vector Search: Finding Similar Stocks with Embeddings',
    meta: '8 pages · MIAUPAPER EMB-2026-V001 · Published 2025',
    authors: 'Professor Mittens, PhD (Machine Learning) · Doc Snuggles (NLP)',
    sections: [
      { heading: 'Abstract', body: 'Every stock gets a 384-dimensional embedding vector from SEC filings, earnings call transcripts, analyst reports, and news sentiment. Miau\'s /api/v1/economics/correlation endpoint uses cosine similarity to find the nearest neighbors. "Show me stocks like AAPL" returns MSFT (0.92), CRM (0.87), ORCL (0.85), ADBE (0.84), SAP (0.81). The embedding model is a fine-tuned Sentence-BERT trained on 2.7 million financial documents.' },
      { heading: '1. The Embedding Pipeline', body: 'SEC Filing (XML) → Parse → Chunk → Embed → Store in pgvector → Query. EDGAR API ingests 1,200 filings per hour. All filings for the 3,000 most-traded US stocks are chunked, embedded, and stored. Re-indexing happens every 24 hours. The vector store is PostgreSQL with pgvector — no extra infrastructure needed. pgvector queries average 8ms on a dataset of 15,000 tickers.' },
      { heading: '2. Use Cases', body: 'Peer discovery: "stocks like AAPL" returns tech mega-caps with similar business models. Sector mapping: "defensive stocks with low beta" returns utilities and consumer staples ranked by risk profile. Merger arbitrage: "companies that could be acquired" returns small caps with patent portfolios, low debt, and cash-rich balance sheets. Thematic baskets: "AI infrastructure plays" returns semiconductor, cloud, and data center operators.' },
    ],
  },
  {
    icon: '⚡', color: '#ff8800',
    title: 'Real-Time Pipeline: From API to Terminal in <500ms',
    meta: '8 pages · MIAUPAPER PPL-2026-V001 · Published 2025',
    authors: 'Count Noir (Infrastructure) · Captain Claw (Performance)',
    sections: [
      { heading: 'Abstract', body: 'The data path: Polygon.io (75ms) → Redis Cache (0.1ms) → FastAPI (8ms) → WebSocket (12ms) → Terminal render (2ms). Total: approximately 97ms from exchange to green text on your screen. Miau uses WebSocket push for live prices, SSE for streaming AI responses, and HTTP/2 multiplexing for dashboard data. The terminal re-renders in under 16ms per frame — 60 FPS for a scrolling ticker.' },
      { heading: '1. The Latency Stack', body: 'Market data feed via Polygon.io WebSocket: 75ms p99. Redis cache with sliding window and TTL 5-30s: 0.1ms. FastAPI async handlers: 8ms. WebSocket push from server to client: 12ms. Terminal DOM update with React batch: 2ms. Before WebSockets, we used polling every 2 seconds. The difference between polling and push is the difference between a cat who knocks something over in slow motion and a cat who just does it. Both end in broken glass, but push is more efficient.' },
    ],
  },
  {
    icon: '📈', color: '#00dd88',
    title: 'Technical Analysis at Your Fingertips',
    meta: '8 pages · MIAUPAPER TA-2026-V001 · Published 2025',
    authors: 'Professor Mittens, PhD (Quant) · Captain Claw (Rust Engine)',
    sections: [
      { heading: 'Abstract', body: 'Most technical analysis platforms are chart primitives wrapped in a subscription. You pay $50/mo for the privilege of drawing trend lines on a web page. Miau does better: every indicator is a terminal command. SMA crossover signals via "signal sma AAPL 20 50". RSI with overbought/oversold detection via "signal rsi AAPL 14". MACD with line, signal, histogram via "signal macd AAPL 12 26 9". Bollinger bands with bandwidth % via "signal bollinger AAPL 20 2".' },
      { heading: '1. The Math Is in Rust', body: 'All 6 indicators run through the Rust engine, producing results in under 3ms for 2 years of daily data. The same engine powers the backtester, so forward indicators and backtested indicators are byte-for-byte identical. Cats don\'t read charts. Cats read body language. The cat sees a head-and-shoulders pattern in your posture when you check your portfolio. Reversal imminent.' },
    ],
  },
  {
    icon: '📐', color: '#ff66aa',
    title: 'Portfolio Optimization Beyond Markowitz',
    meta: '12 pages · MIAUPAPER OPT-2026-V001 · Published 2025',
    authors: 'Professor Mittens, PhD (Optimization) · Sir Whiskers III (Strategy)',
    sections: [
      { heading: 'Abstract', body: 'Miau ships 4 portfolio optimization engines. Mean-Variance for traditional 60/40 portfolios (expected returns + covariance matrix → efficient frontier). Black-Litterman for investors with market views (market cap weights + view matrix + confidence → posterior returns + tilted weights). Risk Parity for drawdown-averse allocators (volatility + correlation matrix → equal risk contribution weights). Equal Weight as a baseline (ticker list only → 1/N weights).' },
      { heading: '1. Black-Litterman in Practice', body: 'Example: optimizer black-litterman with tickers AAPL, MSFT, GOOGL, AMZN, META and views "AAPL +5% (high confidence), MSFT neutral." Result: AAPL 18.2% (+3.1% vs market cap), MSFT 14.8% (-0.3%), GOOGL 12.4% (+0.1%), AMZN 11.1% (-1.5%), META 8.5% (+1.2%). Risk parity was invented by Bridgewater. The cat re-invented it independently by distributing its weight equally across all four paws. Bridgewater\'s version has lower fees but fewer purrs.' },
    ],
  },
  {
    icon: '📰', color: '#00aaff',
    title: 'NLP for Finance: Reading Earnings Calls at Scale',
    meta: '10 pages · MIAUPAPER NLP-2026-V001 · Published 2025',
    authors: 'Doc Snuggles (NLP) · Professor Mittens, PhD (ML)',
    sections: [
      { heading: 'Abstract', body: 'Miau ingests all SEC filings (10-K, 10-Q, 8-K) for the 3,000 most-traded US stocks. Every filing is chunked, embedded in 384-dimensional vectors, and stored in pgvector for semantic search. The pipeline processes 1,200 filings per hour from the EDGAR API. "What did AAPL say about AI last quarter?" fetches the 10-Q and earnings call transcript, performs vector search, and returns the top 3 relevant chunks with surrounding context.' },
      { heading: '1. Query Types', body: '"Which companies mentioned supply chain risks?" filters all 10-K filings from the last 90 days, embeds them, clusters by topic, and returns ranked results. "Show me bearish language in TSLA earnings" applies sentiment-attributed embeddings with polarity scoring per paragraph, highlighting negative passages. We trained a financial sentiment model on 87,000 earnings call Q&A pairs. The model learned that "challenging environment" means "we missed earnings." The cat learned that "treat" means treat. Both models are accurate.' },
    ],
  },
  {
    icon: '🗄️', color: '#ff8800',
    title: 'The Caching Ladder: How Miau Stays Fast',
    meta: '8 pages · MIAUPAPER CCH-2026-V001 · Published 2025',
    authors: 'Count Noir (Infrastructure) · Captain Claw (Performance)',
    sections: [
      { heading: 'Abstract', body: 'Every request hits a 5-layer caching ladder before touching an external API. Layer 1 (Browser): terminal commands in localStorage, 12% hit rate, 30s TTL. Layer 2 (Service Worker): API responses in Cache API, 18% hit rate, 5-300s TTL. Layer 3 (Redis): multi-tenant hot data in RAM, 52% hit rate, 5s-1h TTL. Layer 4 (Postgres): computed analytics in materialized views, 8% hit rate, 1-24h TTL. Layer 5 (External): Polygon/FRED/OpenAI APIs.' },
      { heading: '1. Effective Hit Rate', body: 'Effective cache hit rate: 78% of requests never reach an external API. The cat has its own caching strategy: sleep 16 hours, eat, repeat. The cache never expires. The cache doesn\'t care. We once had a Redis outage that lasted 3 minutes. The system fell back to Postgres with a 40ms penalty. Two users noticed. They both said "site felt slow." The cat didn\'t notice. The cat was caching anyway.' },
    ],
  },
  {
    icon: '🏢', color: '#00dd88',
    title: 'Enterprise Workspaces: RBAC You\'ll Actually Use',
    meta: '10 pages · MIAUPAPER WRK-2026-V001 · Published 2025',
    authors: 'Duchess Fluff (Security) · Sir Whiskers III (Product)',
    sections: [
      { heading: 'Abstract', body: 'Miau workspaces allow teams to share portfolios, strategies, and data feeds under a single subscription. Portfolios can be shared with ownership tracking or kept personal and hidden from the team. API keys can be workspace-scoped or user-scoped. Rate limits are pooled across members with individual caps enforced. Audit logs capture all workspace actions with user-filtered views. Billing is via a single subscription.' },
      { heading: '1. Roles & Permissions', body: 'Owner: full control plus billing and workspace deletion. Admin: manage members, edit team data, view audit logs. Member: read/write portfolios, create API keys, use terminal. Viewer: read-only, no trades, no API keys. The cat is Admin in every workspace. The cat was granted this role by default. The cat can\'t remember granting it. But here we are. We seriously considered adding a "Cat" role that bypasses all permission checks but demands treats every 2 hours. We decided against it because the cat would abuse it.' },
    ],
  },
  {
    icon: '🔬', color: '#ff66aa',
    title: 'Backtesting: Science, Not Art',
    meta: '10 pages · MIAUPAPER BT-2026-V001 · Published 2025',
    authors: 'Professor Mittens, PhD (Quant) · Lord Scaredy (Validation)',
    sections: [
      { heading: 'Abstract', body: 'Miau\'s backtester uses 3 validation layers to prevent overfitting. Walk-Forward: multiple train/test windows — train on 70%, test on 30%, slide forward, repeat. Out-of-Sample: holdback period — last 20% of data never touches the optimizer. Monte Carlo Robustness: 100 synthetic paths from return distribution — strategy must beat benchmark in 80%+. The pipeline is triggered by "strategy backtest sma_cross AAPL 2y --walkforward --mc".' },
      { heading: '1. The Backtest Report', body: 'Returns a JSON report with: CAGR in-sample (12.4%), CAGR out-of-sample (11.1%), Sharpe OOS (1.42 ±0.18 95% CI), Max Drawdown (-8.7%), Monte Carlo Pass Rate (83/100), and Parameter Stability (0.87 — High). The walk-forward optimizer is named "Catnip" because the more you tune it, the more you want to tune it. It is addictive. Stop tuning. Walk away. The cat\'s backtest strategy: buy whatever smells like fish, HODL forever, sell for treats. Monte Carlo pass rate: 100%.' },
    ],
  },
  {
    icon: '📲', color: '#00aaff',
    title: 'PWA Architecture: Finance in Your Pocket',
    meta: '10 pages · MIAUPAPER PWA2-2026-V001 · Published 2025',
    authors: 'Princess Purr (Frontend) · Lady Paws (UX)',
    sections: [
      { heading: 'Abstract', body: 'Native apps require App Store approval, separate codebases, and are locked to one platform. Miau\'s PWA installs in 2 taps, works offline, sends push notifications, and shares one React codebase across all platforms at under 2MB total (vs 50-200MB for native finance apps). The service worker is 187 lines of JavaScript that does more work than most startup teams.' },
      { heading: '1. Offline Capabilities', body: 'View portfolio: yes — IndexedDB cache stores last 100 positions. Market prices: yes — stale-while-revalidate with 15-min max staleness. Terminal history: yes — localStorage keeps last 500 commands. Execute commands: queued in background sync, executed on reconnect. Submit trades: network required intentionally for safety. The cat tried the PWA on an iPad. The cat swiped the portfolio off-screen. The cat blamed the app. The cat was using the wrong paw.' },
    ],
  },
  {
    icon: '🏆', color: '#ffcc00',
    title: 'Gamification: Badges, Leaderboards, and Tuna',
    meta: '8 pages · MIAUPAPER GAM-2026-V001 · Published 2025',
    authors: 'Princess Purr (Community) · Sir Whiskers III (Game Design)',
    sections: [
      { heading: 'Abstract', body: 'The badge system awards achievements: First Trade (100% of users), Profitable Week — positive P&L for 5 consecutive days (34%), Top 10 Weekly (12%), AI Master — accept 10+ AI recommendations verbatim (8%), Analyst — run 50+ analytics commands (22%), Hedge Hog — place a hedge trade over 10% of portfolio (5%), Night Owl — trade during extended hours over 10 times (3%), and Cat Whisperer — use cat emoji in 20+ commands (41%).' },
      { heading: '1. Impact on Engagement', body: 'Leaderboards update in real-time via WebSocket push. Ranked users are 40% more likely to share strategies and 3x more active. The "Cat Whisperer" badge was added as a joke. It is now the most-awarded badge after "First Trade." The community really likes cat emojis. We regret nothing. The cat is ranked #1 on the "Naps Taken" leaderboard. The cat doesn\'t compete. The cat simply exists. The cat wins.' },
    ],
  },
  {
    icon: '🔔', color: '#ff8800',
    title: 'Webhooks: Automate Your Financial Life',
    meta: '8 pages · MIAUPAPER WH-2026-V001 · Published 2025',
    authors: 'Count Noir (Events) · Duchess Fluff (Security)',
    sections: [
      { heading: 'Abstract', body: 'Miau\'s webhook platform fires HTTP callbacks on 15+ event types. trade.executed fires with ticker, price, qty, and direction — auto-post to Slack or Discord. portfolio.rebalanced fires with old weights, new weights, and drift — log to spreadsheet. alert.triggered fires with alert name, threshold, and current value — send SMS via Twilio. Webhooks are configured via the API with secret signing for payload verification.' },
      { heading: '1. Webhook Security', body: 'Each webhook endpoint gets a unique secret key used for HMAC-SHA256 signing of all payloads. Verify signatures to confirm payloads came from Miau. Retry with exponential backoff on delivery failures (3 attempts). Rate limit of 100 webhooks per minute per endpoint. Payload size limit of 1MB. Delivery logs with status codes and latency for debugging. The cat once set up a webhook that ordered tuna every time the portfolio went up. The cat regrets nothing.' },
    ],
  },
  {
    icon: '🌐', color: '#00dd88',
    title: 'Globalization: Multi-Currency, Multi-Language',
    meta: '10 pages · MIAUPAPER GLOB-2026-V001 · Published 2025',
    authors: 'Lady Paws (i18n) · Baron Tuna (FX)',
    sections: [
      { heading: 'Abstract', body: 'Miau supports 9 languages, 40+ international exchanges, and 200+ currency pairs. The platform detects browser locale and serves localized terminal output, number formats, date formats, and currency symbols. Multi-currency portfolios track holdings in their native currency and report in your base currency. Real-time FX rates from 200+ currency pairs power cross-currency portfolio valuation.' },
      { heading: '1. International Exchange Coverage', body: 'NYSE, NASDAQ, LSE, Euronext, TSE, HKEX, ASX, NSE, BSE, Deutsche Börse, SIX Swiss, BM&F Bovespa, TSX, Korea Exchange, Singapore Exchange, Johannesburg Stock Exchange, Tadawul, Dubai Financial Market, and more. Each exchange has local market hours, holiday calendars, and currency handling. The cat has not personally visited all these exchanges. The cat has, however, been to the fish markets near several of them.' },
    ],
  },
  {
    icon: '⚙️', color: '#ff66aa',
    title: '10 Containers, One Stack',
    meta: '12 pages · MIAUPAPER OPS-2026-V001 · Published 2025',
    authors: 'Count Noir (Infrastructure) · Captain Claw (DevOps)',
    sections: [
      { heading: 'Abstract', body: 'Miau runs on 10 Docker containers. backend: FastAPI with PostgreSQL and Redis, 200+ async API routes. frontend: React with Vite, terminal UI, WebSocket real-time streaming. education-platform: React with Vite, 74 courses, 7 certifications. cube: analytics engine with OLAP multi-dimensional queries. superset: data exploration and dashboards. grafana: monitoring, metrics, and alerts. prometheus: time-series scraping and alertmanager. postgres: PostgreSQL 16 with 50+ tables. redis: caching, pub/sub, rate limiting, session store. minio: S3-compatible storage for exports and backups.' },
      { heading: '1. Production Operations', body: 'One docker compose up and you are running the same platform that powers the live site. Our production deploy is a GitHub Action that runs docker compose up -d on the server — the same command your laptop runs. The cat runs it on a Raspberry Pi in the utility closet. It works. 10 containers, one stack, zero lock-in. Kubernetes manifests are available for production scale-out.' },
    ],
  },
  {
    icon: '🧠', color: '#ff66aa',
    title: 'AI Strategy Generation: English → Code → Profit',
    meta: '10 pages · MIAUPAPER AI2-2026-V001 · Published 2025',
    authors: 'Doc Snuggles (AI) · Captain Claw (Execution)',
    sections: [
      { heading: 'Abstract', body: 'Miau\'s AI strategy generator converts natural language descriptions into executable backtest strategies. "Buy AAPL when RSI is below 30 and the 50-day SMA is above the 200-day SMA, sell when RSI exceeds 70" becomes a JSON strategy configuration that the backtester can execute immediately. The generator uses few-shot prompting with 200+ example strategies as context.' },
      { heading: '1. The Strategy Pipeline', body: 'Natural language → Intent parser identifies indicators and conditions → Strategy composer generates JSON config → Backtester executes against historical data → Report generator returns performance metrics. Users without any programming experience can create, backtest, and deploy strategies entirely through natural language. The cat\'s strategy: "Buy when sleepy, sell when hungry, HODL during naps." Sharpe ratio: 1.52.' },
    ],
  },
  {
    icon: '📊', color: '#00aaff',
    title: 'Data Quality: Garbage In, Gospel Out',
    meta: '8 pages · MIAUPAPER DQ-2026-V001 · Published 2025',
    authors: 'Data-dev (Data Engineering) · Professor Mittens, PhD (Statistics)',
    sections: [
      { heading: 'Abstract', body: 'Financial data is notoriously dirty. Delisted tickers, split-unadjusted prices, missing dividends, stale FX rates, and corrupted SEC filings are daily realities. Miau\'s data quality pipeline runs 47 automated checks on every data point before it reaches the terminal. Stocks with data quality scores below 60 are flagged with warnings. Scores below 30 are excluded entirely.' },
      { heading: '1. Quality Checks', body: 'Price sanity: daily return must be within -50% to +500% (adjusted for splits and dividends). Volume sanity: must exceed 50th percentile of 90-day average. Corporate action detection: auto-detect stock splits, reverse splits, spin-offs, and dividend adjustments. Source cross-validation: if Polygon and FRED disagree on the same data point by more than 2%, both are flagged. Outlier detection via rolling z-score with 3-sigma threshold. Market holiday handling: 47 global exchange calendars maintained with automatic holiday detection.' },
    ],
  },
  {
    icon: '♻️', color: '#44cc44',
    title: 'ESG & Compliance: How Miau Finance Goes Green',
    meta: '12 pages · MIAUPAPER ESG-2026-V001 · Published 2025',
    authors: 'Prof. Dr. Tuna (ESG) · Duchess Fluff (Compliance)',
    sections: [
      { heading: 'Abstract', body: 'ESG is not just a checkbox — it is a fundamental shift in how capital markets value companies. Miau\'s ESG platform tracks Environmental (carbon emissions, climate risk, resource efficiency), Social (labor practices, diversity, community impact), and Governance (board structure, executive pay, shareholder rights) dimensions across 5,000+ global equities. Each company receives a 0-100 score in each dimension with transparent methodology.' },
      { heading: '1. Carbon Tracking', body: 'Scope 1, 2, and 3 emissions tracked quarterly for all covered equities. Carbon intensity normalized to revenue (tCO2e/$M revenue). Portfolio carbon footprint aggregated across holdings. Temperature alignment scoring against 1.5°C and 2°C Paris Agreement scenarios. The cat\'s carbon pawprint is surprisingly small. Probably because they sleep 18 hours a day. Prof. Dr. Tuna (the only fish on the cabinet) personally reviews every ESG score.' },
      { heading: '2. Compliance Integration', body: 'Sanctions screening against OFAC, EU, and UN sanctions lists. KYC/AML checks integrated into the onboarding flow. Trade surveillance for patterns indicating market manipulation. Regulatory reporting for MiFID II best execution and transaction reporting. The cat is not a regulated financial advisor. The cat does not need to be. The cat has whiskers.' },
    ],
  },
  {
    icon: '📜', color: '#ff8800',
    title: 'The Miau Finance Manifesto',
    meta: '24 pages · MIAUPAPER MAN-2026-V001 · Published 2024',
    authors: 'Sir Whiskers III (CEO) · The Entire Cabinet',
    sections: [
      { heading: 'Abstract', body: 'This is the founding document of Miau Corp. It states our beliefs: Financial software should be open source because auditability in finance is a human right. The terminal is superior to the GUI for professional workflows. AI should augment human judgment, not replace it. Cats make better traders than humans for reasons that are both scientific and spiritual. Data privacy is not a feature — it is the default. Education should be hands-on, terminal-native, and fun. Tuna is a strategic asset class.' },
      { heading: '1. Our Beliefs', body: 'We believe financial software should not cost $24,000/year. We believe your trading data belongs to you. We believe the best way to learn finance is through a terminal, not a video. We believe AI should have context, not hot takes. We believe cats are naturally better investors because they lack FOMO, practice strategic patience, and always land on their feet. We believe open source is the only ethical way to build financial infrastructure. We believe tuna is undervalued.' },
      { heading: '2. Our Commitments', body: 'We commit to keeping the core platform open source forever. We commit to never selling user data. We commit to maintaining a genuinely useful free tier. We commit to AI transparency — every AI-generated recommendation comes with explainability. We commit to cat supremacy in all matters of portfolio management. We commit to never adding a subscription fee for basic market data. We commit to responding to every GitHub issue. We commit to naming at least one release after a cat food brand.' },
    ],
  },
];

function openAgent(index) {
  const c = cats[index];
  const modal = document.getElementById('paperModal');
  const content = document.getElementById('paperContent');
  content.innerHTML = `<button class="modal-back" onclick="closePaper()">← Back to Cabinet</button>
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px">
      <div style="font-size:72px;background:${c.color}10;border:2px solid ${c.color}30;border-radius:20px;width:100px;height:100px;display:flex;align-items:center;justify-content:center">${c.emoji}</div>
      <div>
        <div class="modal-badge" style="border-color:${c.color}30;color:${c.color};margin-bottom:8px">Cabinet Member</div>
        <h1 style="font-size:28px;margin:0">${c.name}</h1>
        <div style="color:${c.color};font-size:16px;font-weight:500;margin-top:4px">${c.role}</div>
      </div>
    </div>
    <div class="modal-meta" style="margin-bottom:24px;padding-bottom:20px">Age: ${c.age}</div>
    <div class="modal-body">
      <p style="font-size:15px;line-height:1.8">${c.bio}</p>
      <h2>Life Philosophy</h2>
      <div class="equation" style="font-family:inherit;font-size:16px;font-style:italic;color:#c8d6d0">"${c.motto}"</div>
      <h2>When Not Working</h2>
      <p>${c.hobby}</p>
    </div>`;
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

let paperPage = 0;
const PAPERS_PER_PAGE = 6;
const totalPaperPages = () => Math.ceil(papers.length / PAPERS_PER_PAGE);

function renderPapers() {
  const container = document.getElementById('paperList');
  container.innerHTML = '';
  const start = paperPage * PAPERS_PER_PAGE;
  const end = Math.min(start + PAPERS_PER_PAGE, papers.length);
  for (let i = start; i < end; i++) {
    const p = papers[i];
    const card = document.createElement('div');
    card.className = 'paper-card fade-up';
    card.style.cursor = 'pointer';
    card.setAttribute('onclick', `openPaper(${i})`);
    card.innerHTML = `
      <div class="p-icon" style="border-color:${p.color}30;background:${p.color}08">${p.icon}</div>
      <div>
        <h3>${p.title} <span style="font-size:10px;color:${p.color};font-family:monospace">↗</span></h3>
        <p>${p.sections[0].body.slice(0, 180)}…</p>
        <span class="p-meta">${p.meta}</span>
      </div>`;
    container.appendChild(card);
    observeNew(card);
  }
  renderPagination();
}

function renderPagination() {
  const el = document.getElementById('paperPagination');
  const total = totalPaperPages();
  let html = '';
  html += `<button onclick="goPaperPage(0)" ${paperPage === 0 ? 'disabled' : ''}>«</button>`;
  html += `<button onclick="goPaperPage(${paperPage - 1})" ${paperPage === 0 ? 'disabled' : ''}>‹</button>`;
  html += `<span class="page-info">Page ${paperPage + 1} / ${total}</span>`;
  html += `<button onclick="goPaperPage(${paperPage + 1})" ${paperPage >= total - 1 ? 'disabled' : ''}>›</button>`;
  html += `<button onclick="goPaperPage(${total - 1})" ${paperPage >= total - 1 ? 'disabled' : ''}>»</button>`;
  el.innerHTML = html;
}

function goPaperPage(page) {
  paperPage = page;
  renderPapers();
  document.getElementById('research').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function openPaper(index) {
  const p = papers[index];
  const modal = document.getElementById('paperModal');
  const content = document.getElementById('paperContent');
  let html = `<button class="modal-back" onclick="closePaper()">← Back to Research</button>
    <div class="modal-icon">${p.icon}</div>
    <div class="modal-badge" style="border-color:${p.color}30;color:${p.color}">${p.meta}</div>
    <h1>${p.title}</h1>
    <div class="modal-meta">${p.authors}</div>
    <div class="modal-body">`;
  for (const s of p.sections) {
    if (s.isEquation) {
      html += `<div class="equation">${s.body}</div>`;
    } else if (s.heading) {
      html += `<h2>${s.heading}</h2><p>${s.body}</p>`;
    } else {
      html += `<p>${s.body}</p>`;
    }
  }
  html += `</div>`;
  content.innerHTML = html;
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closePaper() {
  document.getElementById('paperModal').classList.remove('open');
  document.body.style.overflow = '';
}

document.getElementById('paperModal').addEventListener('click', (e) => { if (e.target === e.currentTarget) closePaper(); });
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closePaper(); });

window.addEventListener('load', () => {
  renderPapers();
  observeFade();
  setTimeout(animateCounters, 500);
});

function toggleMobile(){document.getElementById('mobileDrawer').classList.toggle('open');document.querySelector('.hamburger').classList.toggle('active')}
function acceptCookies(){localStorage.setItem('miau-cookies','accepted');document.getElementById('cookieBanner').classList.remove('show')}
function declineCookies(){localStorage.setItem('miau-cookies','declined');document.getElementById('cookieBanner').classList.remove('show')}
if(!localStorage.getItem('miau-cookies')){setTimeout(()=>{document.getElementById('cookieBanner').classList.add('show')},1500)}
if('serviceWorker' in navigator){window.addEventListener('load',()=>{navigator.serviceWorker.register('/sw.js')})}

function demoHTML(type) {
  if (type === 'terminal') return '<div style="background:rgba(0,0,0,0.5);border-radius:8px;padding:12px 16px;font-family:monospace;font-size:12px;line-height:1.8;"><div style="color:#00ff88">$ price AAPL</div><div style="color:rgba(200,214,208,0.6)">  AAPL  $198.52  +1.24%  📈</div><div style="color:#00ff88">$ portfolio 1</div><div style="color:rgba(200,214,208,0.6)">  Value: €12,450.32  P&L: +€892.10</div></div>'
  if (type === 'courses') return '<div id="demoWrap" style="background:rgba(0,0,0,0.5);border-radius:8px;padding:16px;text-align:center;font-family:monospace"><div style="font-size:36px;font-weight:900;color:#00aaff" id="demoCounter">0</div><div style="font-size:12px;color:rgba(200,214,208,0.4)">courses completed by the cat</div></div>'
  if (type === 'chart') return '<div style="background:rgba(0,0,0,0.5);border-radius:8px;padding:16px"><div style="display:flex;align-items:end;gap:4px;height:60px;justify-content:center">' + [30,45,38,55,48,62,58,72,68,82,78,88,85,92,90].map((h,i) => '<div style="width:12px;height:' + h + '%;background:rgba(0,255,136,' + (0.3 + i * 0.04) + ');border-radius:3px 3px 0 0;transition:height 0.5s"></div>').join('') + '</div><div style="text-align:center;font-size:10px;color:rgba(200,214,208,0.3);margin-top:8px">📈 Live chart — cat approved</div></div>'
  if (type === 'globe') return '<div style="background:rgba(0,0,0,0.5);border-radius:8px;padding:16px;text-align:center"><div style="font-size:64px;animation:spin 8s linear infinite">🌍</div><div style="font-size:10px;color:rgba(200,214,208,0.3);margin-top:8px">7 layers · 50K+ markers · 1 cat</div></div>'
  if (type === 'code') return '<div style="background:rgba(0,0,0,0.5);border-radius:8px;padding:12px 16px;font-family:monospace;font-size:12px;line-height:1.8"><div style="color:#00ff88">$ pip install miau-sdk</div><div style="color:rgba(200,214,208,0.4)">Collecting miau-sdk...</div><div style="color:rgba(200,214,208,0.4)">Installing...</div><div style="color:#00ff88">✅ Done!</div><div style="color:rgba(200,214,208,0.4);margin-top:4px">>>> from miau import Market</div><div style="color:rgba(200,214,208,0.4)">>>> Market.price("AAPL")</div><div style="color:#00ff88">198.52</div></div>'
  if (type === 'trade') return '<div style="background:rgba(0,0,0,0.5);border-radius:8px;padding:12px 16px;font-family:monospace;font-size:12px;line-height:1.8"><div style="color:#00ff88">✅ Order filled</div><div style="color:rgba(200,214,208,0.6)">BUY 10 AAPL @ $195.20</div><div style="color:rgba(200,214,208,0.6)">Status: Filled (0.3s)</div><div style="color:rgba(200,214,208,0.4);margin-top:4px">📄 Cat approved ✅</div></div>'
  if (type === 'calc') return '<div style="background:rgba(0,0,0,0.5);border-radius:8px;padding:16px;text-align:center"><div style="font-size:28px;font-weight:900;color:#00ff88">€1,400,532</div><div style="font-size:11px;color:rgba(200,214,208,0.4)">€1,000/mo × 30yr @ 8%</div><div style="font-size:10px;color:rgba(200,214,208,0.2);margin-top:4px">That\'s a lot of tuna 🐟</div></div>'
  if (type === 'wallet') return '<div style="background:rgba(0,0,0,0.5);border-radius:8px;padding:12px 16px;font-family:monospace;font-size:11px;line-height:1.8"><div style="color:rgba(200,214,208,0.4)">📍 Connected to Ethereum</div><div style="color:#00ff88">💰 Balance: 4.23 ETH</div><div style="color:rgba(200,214,208,0.4)">💱 USDC: 12,450.00</div><div style="color:rgba(200,214,208,0.4)">🔗 TVL: $45.2M across 8 protocols</div><div style="color:rgba(200,214,208,0.2);margin-top:4px">🐱 MEV: Active</div></div>'
  return '<div style="background:rgba(0,0,0,0.5);border-radius:8px;padding:20px;text-align:center;font-size:36px">' + type + '</div>'
}

const productDetails = {
  'Miau Finance': { icon: '🐱', title: 'Miau Finance Terminal', desc: 'The flagship terminal-native financial OS. 200+ commands, 50+ data providers, real-time market data, portfolio management, risk analytics, AI advisor, DeFi, ESG, and more. 18+ services, 800+ tests, infinite tuna.', cat: '😸 "I built this terminal. I nap on it daily. It works better when I\'m sleeping on the warm server."', stat: '200+ commands · 50+ providers · 515+ APIs', demo: 'terminal' },
  'Miau Learning': { icon: '🎓', title: 'Miau Learning Platform', desc: '230 interactive finance courses taught through the terminal. 18 certifications including CMA, CMT, CQF, CDS, CESG, CAI, Bagholder. 5 career tracks. No videos — just real commands and paw-on-keyboard practice.', cat: '🎓 Cat with graduation cap: "I have 18 certifications. I\'m still unemployed. I live for the knowledge."', stat: '230 courses · 18 certs · 5 tracks', demo: 'courses' },
  'Miau Homepage': { icon: '🏠', title: 'Miau Homepage & Blog', desc: 'The public face of the cat empire. Next.js marketing site with product announcements, blog posts, community forums, tuna treasury leaderboard, and cat-of-the-week highlights.', cat: '🏠 "I designed the homepage. It has my face on it. As it should be."', stat: 'Next.js · Blog · Community', demo: '📱' },
  'Whitepapers': { icon: '📜', title: 'Research Papers', desc: '100+ research papers on quantum finance, CBDC architectures, AGI governance, post-quantum cryptography, and the mathematical proof that cats optimize portfolios better than humans.', cat: '📚 "I peer-reviewed every paper. My review: \'more tuna graphs\'. They listened."', stat: '100+ papers · Peer-reviewed', demo: '📚' },
  'SDK & Plugins': { icon: '🔌', title: 'SDK & Plugin Ecosystem', desc: 'Python and JavaScript SDKs for algorithmic trading. Plugin system with 16 scoped permission levels. Full OpenAPI docs at /docs. Integrate the cat empire into your own tools.', cat: '🔌 "I wrote a plugin that buys tuna when my bowl is empty. 60% success rate. Every time."', stat: 'Python · JS · curl · OpenAPI', demo: 'code' },
  'Investment Banking': { icon: '🏦', title: 'IB Toolkit', desc: 'Full investment banking toolkit: DCF valuation, WACC calculation, Comparable Company Analysis, LBO model. Run `sheetz -all` from the terminal. Used by analyst cats at bulge bracket banks.', cat: '🏦 "I ran a DCF on my tuna can. Trading at 3x fair value. Tuna market is irrational."', stat: 'DCF · WACC · Comps · LBO', demo: 'calc' },
  'ESG & Sustainability': { icon: '🌿', title: 'ESG & Carbon Tracking', desc: 'ESG scores for 10,000+ companies. Carbon footprint tracking. SFDR-aligned reporting. Green bond analysis. Temperature alignment. The cat offsets its carbon pawprint.', cat: '🌿 "My portfolio is green. My conscience is green. My tuna is sustainable."', stat: '10K+ companies · SFDR', demo: '🌿' },
  'DeFi & Web3': { icon: '🔗', title: 'DeFi & Web3 Gateway', desc: 'Multi-chain wallet. 8+ DeFi protocols (Uniswap, Aave, Curve, Lido, Yearn, Maker, Jupiter, Raydium). DAO governance. Liquidity provision. Cross-chain bridges. MEV strategies.', cat: '🔗 "I was in DeFi before DeFi was cool. I AM the MEV."', stat: '12+ chains · 8 protocols · DAO', demo: 'wallet' },
  'AI Finance': { icon: '🤖', title: 'AI Financial Advisor', desc: 'AI advisor powered by DeepSeek-R1. ML forecasts, sentiment analysis from 10K+ news sources, automated strategy generation with evolutionary algorithms. No ChatGPT fees.', cat: '🤖 "I trained the AI on my trading history. It now buys tuna at 3am. It works."', stat: 'DeepSeek-R1 · ML · Sentiment', demo: '🤖' },
  'Quant Analytics': { icon: '🧮', title: 'Quantitative Analytics', desc: 'Institutional-grade quant: Monte Carlo (10K+ paths), Fama-French 5-factor, options Greeks, VaR/CVaR, Black-Litterman model, portfolio optimization — all in Rust via PyO3.', cat: '🧮 "I calculated optimal napping schedule: 18h/day. 95% confidence interval. Perfection."', stat: 'Monte Carlo · Greeks · VaR', demo: 'chart' },
  'Global Markets': { icon: '🌍', title: 'Global Market Access', desc: 'Trade 40+ international exchanges. Multi-currency portfolios with 200+ FX pairs. 9-language i18n. Digital Euro, e-CNY, FedNow tracking.', cat: '🌍 "I traded on 40 exchanges today without leaving my bed. Technology is beautiful."', stat: '40+ exchanges · 9 languages', demo: 'globe' },
  'Data & Analytics': { icon: '📊', title: 'Data & Analytics Suite', desc: 'Rich visualization, customizable dashboards, automated reporting, CSV/JSON/PDF export. Turn market noise into actionable insights.', cat: '📊 "My dashboard has 47 charts. I understand 3. Those 3 make me money."', stat: 'Dashboards · Reports · Export', demo: 'chart' },
  'Risk Management': { icon: '🛡️', title: 'Enterprise Risk Management', desc: 'VaR (historical, parametric, Monte Carlo), stress testing, scenario analysis, derivatives hedging, regulatory compliance. 9 lives for your portfolio.', cat: '🛡️ "My risk manager is a cat. Lose money? She judges silently. Worse than VaR breach."', stat: 'VaR · Stress · Compliance', demo: '📊' },
  'Crypto & Blockchain': { icon: '₿', title: 'Crypto & Blockchain Analytics', desc: '50+ exchange data, on-chain analytics (whale tracking, exchange flows, miner behavior), perpetual swaps, funding rate arbitrage, cross-chain portfolios.', cat: '₿ "I mined Bitcoin in 2011. Spent 10K BTC on tuna. No regrets. Tuna is eternal."', stat: '50+ exchanges · On-chain · MEV', demo: 'wallet' },
}

function openProductModal(key) {
  const p = productDetails[key]
  if (!p) return
  document.getElementById('productContent').innerHTML = 
    '<div class="modal-icon">' + p.icon + '</div>' +
    '<div class="modal-badge">🐱 Miau Corp Product</div>' +
    '<h1>' + p.title + '</h1>' +
    '<div class="modal-meta">' + p.stat + '</div>' +
    '<div style="margin-bottom:20px">' + demoHTML(p.demo || p.icon) + '</div>' +
    '<div class="modal-body"><p>' + p.desc + '</p></div>' +
    '<div style="margin-top:20px;padding:14px 18px;background:rgba(255,204,0,0.05);border:1px solid rgba(255,204,0,0.15);border-radius:10px;display:flex;align-items:center;gap:12px">' +
    '<span style="font-size:28px">🐱</span>' +
    '<span style="font-size:14px;color:rgba(200,214,208,0.7);font-style:italic">' + p.cat + '</span></div>'
  document.getElementById('productModal').classList.add('open')
  document.body.style.overflow = 'hidden'
  // Trigger counter animation for courses demo
  if (p.demo === 'courses') {
    setTimeout(function() {
      var c = 0
      var el = document.getElementById('demoCounter')
      if (!el) return
      var t = setInterval(function() { c += 2; if (el) el.textContent = c >= 230 ? '230' : String(c); if (c >= 230) clearInterval(t) }, 20)
    }, 100)
  }
}
function closeProductModal() {
  document.getElementById('productModal').classList.remove('open')
  document.body.style.overflow = ''
}



// Auth for ecosystem site
let ecoToken = localStorage.getItem('miau_token');
let ecoUser = localStorage.getItem('miau_user');

function toggleAuthModal() {
  const m = document.getElementById('authModalEco');
  m.style.display = m.style.display === 'none' ? 'block' : 'none';
}

async function ecoLogin() {
  const username = document.getElementById('ecoLoginUser').value.trim();
  const password = document.getElementById('ecoLoginPass').value;
  if (!username || !password) return alert('🐱 Username and password required');
  const btn = document.getElementById('ecoLoginBtn');
  btn.textContent = '🐱 Logging in...'; btn.disabled = true;
  try {
    const r = await fetch('http://localhost:8000/api/v1/auth/token', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({username, password}),
    });
    if (!r.ok) throw new Error(await r.text());
    const data = await r.json();
    localStorage.setItem('miau_token', data.access_token);
    localStorage.setItem('miau_user', username);
    ecoToken = data.access_token; ecoUser = username;
    document.getElementById('authModalEco').style.display = 'none';
    document.getElementById('authBtnEco').textContent = '🚪 Logout';
    document.getElementById('authUserEco').textContent = '🐱 ' + username;
    document.getElementById('ecoLoginUser').value = '';
    document.getElementById('ecoLoginPass').value = '';
  } catch(e) { alert('😿 Login failed: ' + e.message); }
  btn.textContent = '🐱 Login'; btn.disabled = false;
}

function ecoLogout() {
  localStorage.removeItem('miau_token');
  localStorage.removeItem('miau_user');
  ecoToken = null; ecoUser = null;
  document.getElementById('authBtnEco').textContent = '🔑 Login';
  document.getElementById('authUserEco').textContent = '';
}

async function ecoShowRegister() {
  const u = prompt('🐾 Choose a username:');
  if (!u) return;
  const e = prompt('📧 Email:');
  if (!e) return;
  const p = prompt('🔒 Password:');
  if (!p) return;
  try {
    const r = await fetch('http://localhost:8000/api/v1/auth/register', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({username: u, email: e, password: p}),
    });
    if (!r.ok) throw new Error(await r.text());
    alert('🐱 Registered! Now log in.');
    document.getElementById('ecoLoginUser').value = u;
    document.getElementById('ecoLoginPass').value = p;
  } catch(e) { alert('😿 ' + e.message); }
}

// Init auth UI
if (ecoToken && ecoUser) {
  document.getElementById('authBtnEco').textContent = '🚪 Logout';
  document.getElementById('authBtnEco').onclick = ecoLogout;
  document.getElementById('authUserEco').textContent = '🐱 ' + ecoUser;
}
// Cross-origin token sync
async function ecoCheckRelay() {
  if (localStorage.getItem('miau_token')) return;
  try {
    const r = await fetch('http://localhost:8000/api/v1/auth/broadcast-token');
    if (!r.ok) return;
    const d = await r.json();
    if (d.token && d.timestamp && (Date.now() - new Date(d.timestamp).getTime()) / 1000 < 30) {
      localStorage.setItem('miau_token', d.token);
      localStorage.setItem('miau_user', d.user);
      document.getElementById('authBtnEco').textContent = '🚪 Logout';
      document.getElementById('authBtnEco').onclick = ecoLogout;
      document.getElementById('authUserEco').textContent = '🐱 ' + d.user;
    }
  } catch(e) {}
}
ecoCheckRelay();
