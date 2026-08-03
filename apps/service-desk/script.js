const API = 'http://localhost:8000/api/v1/service-desk';
const AUTH_API = 'http://localhost:8000/api/v1/auth';
let tickets = [];
let pollTimer = null;
let soundEnabled = localStorage.getItem('miauSound') !== 'off';
let statusTimer = null;
let offlineMode = false;
let authToken = localStorage.getItem('miau_token') || null;
let authUser = localStorage.getItem('miau_user') || null;

const FIREFIGHTERS = [
  { emoji: '👨‍🚒', color: '#ff4444', name: 'Captain Ember', rank: '🔥 Fire Chief', role: 'Emergency Response & Portfolio Rescue', status: 'on-duty', age: '8 (has fought 1,247 portfolio fires and 3 actual fires)', hobby: 'Polishing the fire truck, napping at the station, sliding down the pole even when not on a call', motto: '"Where there is smoke, there is fire. Where there is fire, there is a cat with a hose."', bio: 'Captain Ember has been with the Miau Fire Brigade since the Great Portfolio Meltdown of 2024. She has personally rescued over 12,000 portfolios from certain doom. Her response time is legendary — 0.8 purrs (about 16 seconds). She can extinguish a margin call before the human has finished panicking. She leads a team of 4 elite firefighter cats and is respected across the entire cat empire. Her helmet has 47 badges of honor, most of them for "Excellence in Napping While On Call."' },
  { emoji: '🚒', color: '#ff8800', name: 'Lieutenant Spark', rank: '🔥 First Responder', role: 'Urgent Tickets & Critical Systems', status: 'on-duty', age: '6 (has never lost a ticket, has lost 3 mice)', hobby: 'Sliding down the fire pole, checking all smoke detectors, practicing rescue techniques on stuffed animals', motto: '"I arrive before the fire knows it is on fire. That is the Spark guarantee."', bio: 'Lieutenant Spark is the fastest responder in the brigade. He can triage a ticket, diagnose the issue, and deploy a fix before the ticket submitter has finished typing. He is known for his signature move: the "Spark Slide" — arriving on scene with such velocity that the fire is intimidated into extinguishing itself. He has a 100% ticket resolution rate and a 0% tolerance for slow load times. His only weakness: catnip. He cannot resist catnip.' },
  { emoji: '🐱', color: '#00aaff', name: 'Firefighter Whiskers', rank: '🧯 Tech Support', role: 'Bug Fixes & Technical Rescue', status: 'on-duty', age: '5 (has fixed more bugs than the entire internet has lines of code)', hobby: 'Reading Stack Overflow, refactoring legacy code, writing automated test cases with his paws', motto: '"It is not a bug. It is an undocumented feature. I will fix it anyway."', bio: 'Firefighter Whiskers is the technical backbone of the brigade. While the others fight portfolio fires, Whiskers fights actual code fires. He has personally debugged issues in 47 different programming languages, including ones that do not exist yet. He can reproduce a race condition in his sleep. He dreams in stack traces. His toolkit includes: a fire extinguisher (for overheating servers), a laptop (for hotfixes), and a laser pointer (for debugging cat issues specifically). He once fixed a production outage by walking across the keyboard. It worked.' },
  { emoji: '🐈', color: '#44cc88', name: 'Cadet Puddles', rank: '🪣 Junior Support', role: 'General Inquiries & Ticket Triage', status: 'on-duty', age: '2 (still learning but very enthusiastic)', hobby: 'Organizing tickets by color, practicing professional meowing, asking Captain Ember for performance reviews', motto: '"I may be small, but my purr of reassurance can calm any panicked human."', bio: 'Cadet Puddles is the newest member of the Miau Fire Brigade, but what she lacks in experience she makes up for in enthusiasm. She handles all general inquiries, routes tickets to the right firefighters, and provides emotional support to panicked users. She has a remarkable ability to purr at frequencies that calm human anxiety. She is currently studying for her "Senior Firefighter" certification, which requires passing a 3-part exam: "Portfolio Fire Theory," "Advanced Cat Rescue Techniques," and "Nap Strategy & Optimization." She scored 100% on Nap Strategy.' },
  { emoji: '☎️', color: '#aa66ff', name: 'Dispatcher Meow', rank: '📟 Ticket Triage', role: 'Routing, Prioritization & Cat Coordination', status: 'nap', age: '7 (has routed 50,000+ tickets without losing a single one)', hobby: 'Organizing spreadsheets by priority, color-coding the ticket board, napping with one eye open', motto: '"The ticket comes in, the cat goes out. I make sure the right cat goes out. It is simple. It is beautiful. It is nap time."', bio: 'Dispatcher Meow is the central nervous system of the Miau Fire Brigade. Every ticket, every emergency, every "my portfolio is on fire" panic — it all passes through Dispatcher Meow. He has an uncanny ability to assess ticket priority within seconds of reading the title. He has never misrouted a ticket. He has never lost a submission. He has, however, taken 47 "strategic naps" during his shift — but here is the thing: tickets always get routed perfectly even while he is asleep. Nobody knows how. Some say he has a sixth sense. Others say he just trained the system well. He says nothing. He is napping.' },
];

const CAT_REACTIONS = ['😸', '😹', '😻', '🙀', '😼', '😺', '😽', '😾', '🐱', '🐈'];

function catAvatar(id) {
  if (!id) return '🐱';
  const hash = Array.from(id).reduce((a, c) => a + c.charCodeAt(0), 0);
  return CAT_REACTIONS[Math.abs(hash) % CAT_REACTIONS.length];
}

const SERVICE_LABELS = {
  terminal: '🐱 Terminal', learning: '🎓 Education', corp: '🏢 Miau Corp',
  marketing: '📊 Marketing', 'service-desk': '🚒 Service Desk', galaxy: '🌌 Cat Galaxy',
  miaubook: '📝 MiauBook', admin: '🔧 Admin', logviewer: '📋 Log Viewer',
  api: '🔌 API', grafana: '📈 Grafana', homepage: '🏠 Homepage',
};
const CAT_PROVERBS = [
  '"A portfolio on fire is just a catnap away from being fine."',
  '"The cat who chases two mice catches none. Focus on one fire."',
  '"Every ticket is an opportunity to nap — I mean, learn."',
  '"The fire is not the problem. The problem is the lack of tuna."',
  '"A purring cat is a portfolio that is not on fire."',
  '"Cats have 9 lives. Your portfolio does not. Buy the dip."',
  '"The cat always lands on its feet. Your tickets will too."',
  '"Patience, young human. The cat is coming. The cat is always coming."',
  '"Tuna is not just a treat. Tuna is a solution to everything."',
  '"The firefighter and the cat are the same. Both arrive when least expected."',
  '"Do not panic. The cat has the hose. The cat has a plan."',
  '"Every fire starts small. So does every cat. Both grow fast."',
];

const SERVICE_STATUSES = [
  { name: '🐱 Terminal UI', port: 5173, status: 'online' },
  { name: '🎓 Education Platform', port: 5174, status: 'online' },
  { name: '🏢 Miau Corp', port: 5175, status: 'online' },
  { name: '📊 Marketing Dashboard', port: 5176, status: 'online' },
  { name: '🚒 Service Desk', port: 5180, status: 'online' },
  { name: '🔌 API Backend', port: 8000, status: 'online' },
  { name: '🗄️ PostgreSQL', port: 5432, status: 'online' },
  { name: '⚡ Redis Cache', port: 6379, status: 'online' },
  { name: '📈 Grafana', port: 3000, status: 'slow' },
  { name: '🌌 Cat Galaxy', port: 5181, status: 'online' },
];

// === Audio ===
let audioCtx = null;
function getAudio() {
  if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  return audioCtx;
}

function toggleSound() {
  soundEnabled = !soundEnabled;
  localStorage.setItem('miauSound', soundEnabled ? 'on' : 'off');
  document.getElementById('soundToggle').textContent = soundEnabled ? '🔊' : '🔇';
  if (soundEnabled) playMeow();
  showToast(soundEnabled ? '🔊 Cat sounds ON' : '🔇 Cat sounds OFF', 'info');
}

function playMeow() {
  if (!soundEnabled) return;
  try {
    const ctx = getAudio();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.type = 'sine';
    osc.frequency.setValueAtTime(600, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(400, ctx.currentTime + 0.15);
    gain.gain.setValueAtTime(0.1, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 0.3);
  } catch(e) { /* audio not available */ }
}

function playPurr() {
  if (!soundEnabled) return;
  try {
    const ctx = getAudio();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(80, ctx.currentTime);
    gain.gain.setValueAtTime(0.04, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.8);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 0.8);
  } catch(e) { /* audio not available */ }
}

function playAlarm() {
  if (!soundEnabled) return;
  try {
    const ctx = getAudio();
    [0, 0.15].forEach(delay => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.type = 'square';
      osc.frequency.setValueAtTime(880, ctx.currentTime + delay);
      gain.gain.setValueAtTime(0.05, ctx.currentTime + delay);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + delay + 0.12);
      osc.start(ctx.currentTime + delay);
      osc.stop(ctx.currentTime + delay + 0.12);
    });
  } catch(e) { /* audio not available */ }
}

// === Toast Notifications ===
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = message;
  container.appendChild(toast);
  setTimeout(() => { toast.classList.add('toast-out'); setTimeout(() => toast.remove(), 300); }, 4000);
}

// === Cat Reaction ===
function showCatReaction() {
  const el = document.getElementById('catReaction');
  const emoji = CAT_REACTIONS[Math.floor(Math.random() * CAT_REACTIONS.length)];
  el.textContent = emoji;
  el.classList.remove('cat-react-show');
  void el.offsetWidth;
  el.classList.add('cat-react-show');
  playMeow();
}

// === Emergency Siren ===
function emergencySiren() {
  playAlarm();
  document.body.classList.add('siren');
  setTimeout(() => document.body.classList.remove('siren'), 3000);
}

// === Dispatch Animation ===
function showDispatch(firefighter) {
  const overlay = document.getElementById('dispatchOverlay');
  const nameEl = document.getElementById('dispatchName');
  const bar = document.getElementById('dispatchBar');
  const statusEl = document.getElementById('dispatchStatus');
  nameEl.textContent = firefighter;
  bar.style.width = '0%';
  statusEl.textContent = '🚒 Dispatching firefighter...';
  overlay.classList.add('dispatch-open');
  let pct = 0;
  playAlarm();
  const interval = setInterval(() => {
    pct += Math.random() * 12 + 5;
    if (pct >= 100) { pct = 100; clearInterval(interval); }
    bar.style.width = pct + '%';
    if (pct < 30) statusEl.textContent = '🔥 Locating fire...';
    else if (pct < 60) statusEl.textContent = '🚒 Cat en route...';
    else if (pct < 90) statusEl.textContent = '🐱 Firefighter preparing hose...';
    else statusEl.textContent = '✅ Firefighter has arrived!';
  }, 150);
  setTimeout(() => {
    overlay.classList.remove('dispatch-open');
    playPurr();
    showCatReaction();
  }, 2500);
}

// === Local Storage Fallback (for when backend is sleeping) ===
function localTickets() {
  try { return JSON.parse(localStorage.getItem('sd_tickets') || '[]'); } catch { return []; }
}
function saveLocalTickets(t) {
  localStorage.setItem('sd_tickets', JSON.stringify(t));
}
function nextLocalId() {
  const last = localStorage.getItem('sd_next_id') || '100';
  const next = parseInt(last) + 1;
  localStorage.setItem('sd_next_id', String(next));
  return String(next);
}

const SAMPLE_TICKETS = [
  { id: '1', category: 'fire', priority: 'critical', title: 'My portfolio dropped 40% in 5 minutes', author: 'Panicked Human', service: 'terminal', status: 'open', assigned_to: 'Captain Ember', pokes: 2, created_at: new Date(Date.now() - 120000).toISOString() },
  { id: '2', category: 'bug', priority: 'medium', title: 'Terminal shows wrong cat emoji for Tesla', author: 'Cat Lover', service: 'terminal', status: 'open', assigned_to: 'Firefighter Whiskers', pokes: 0, created_at: new Date(Date.now() - 900000).toISOString() },
  { id: '3', category: 'question', priority: 'low', title: 'How do I calculate VaR with catnip?', author: 'Curious Trader', service: 'learning', status: 'open', assigned_to: 'Cadet Puddles', pokes: 1, created_at: new Date(Date.now() - 3600000).toISOString() },
  { id: '4', category: 'feature', priority: 'medium', title: 'Add "cat --laser" command', author: 'Feature Request Cat', service: 'terminal', status: 'progress', assigned_to: 'Lieutenant Spark', pokes: 5, created_at: new Date(Date.now() - 10800000).toISOString() },
  { id: '5', category: 'fire', priority: 'critical', title: 'Production server is on fire (literally)', author: 'DevOps Engineer', service: 'api', status: 'progress', assigned_to: 'Captain Ember', pokes: 8, created_at: new Date(Date.now() - 300000).toISOString() },
  { id: '6', category: 'bug', priority: 'high', title: 'Login form rejects valid passwords with cat emojis', author: '😺 User', service: 'corp', status: 'progress', assigned_to: 'Firefighter Whiskers', pokes: 3, created_at: new Date(Date.now() - 7200000).toISOString() },
  { id: '7', category: 'question', priority: 'low', title: 'What is the tuna-to-portfolio ratio?', author: 'Strategy Analyst', status: 'resolved', assigned_to: 'Dispatcher Meow', pokes: 0, created_at: new Date(Date.now() - 86400000).toISOString() },
  { id: '8', category: 'feature', priority: 'low', title: 'Implement "cat --dance" with disco ball', author: 'Party Cat', service: 'galaxy', status: 'resolved', assigned_to: 'Lieutenant Spark', pokes: 12, created_at: new Date(Date.now() - 259200000).toISOString() },
];

function initLocalStore() {
  if (localTickets().length === 0) {
    saveLocalTickets(SAMPLE_TICKETS);
  }
}

// === API with offline fallback ===
async function apiFetch(path, options = {}) {
  if (offlineMode) return localApiFetch(path, options);
  const url = path.startsWith('http') ? path : API + path;
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (authToken) headers['Authorization'] = `Bearer ${authToken}`;
  try {
    const resp = await fetch(url, { ...options, headers, signal: AbortSignal.timeout(3000) });
    if (!resp.ok) { const err = await resp.text(); throw new Error(err || `HTTP ${resp.status}`); }
    const data = await resp.json();
    return data;
  } catch (e) {
    if (e.name === 'TimeoutError' || e.message.includes('Failed to fetch') || e.message.includes('NetworkError') || e.message.includes('fetch')) {
      console.warn('🐱 Backend unreachable, switching to offline mode');
      offlineMode = true;
      document.getElementById('offlineBadge')?.classList.add('show');
  updateAuthUI();
  initLocalStore();
  checkTokenRelay(); // pick up token from another app
      showToast('🐱 Backend is napping — using local storage mode', 'info');
      return localApiFetch(path, options);
    }
    throw e;
  }
}

// === Local Storage API (mirrors the backend API) ===
function localApiFetch(path, options) {
  const tickets = localTickets();
  const match = path.match(/^\/tickets\/([^/]+)(\/(\w+))?$/);
  const id = match ? match[1] : null;
  const action = match ? match[3] : null;
  const body = options.body ? JSON.parse(options.body) : {};

  // GET /tickets
  if (path === '/tickets' && (!options.method || options.method === 'GET')) {
    return tickets.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }

  // POST /tickets
  if (path === '/tickets' && options.method === 'POST') {
    const t = {
      id: nextLocalId(),
      category: body.category || 'question',
      priority: body.priority || 'medium',
      title: body.title,
      description: body.description || null,
      author: body.author || 'Anonymous Cat',
      service: body.service || null,
      status: 'open',
      assigned_to: FIREFIGHTERS[Math.floor(Math.random() * FIREFIGHTERS.length)].name,
      pokes: 0,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    tickets.unshift(t);
    saveLocalTickets(tickets);
    return t;
  }

  // PATCH /tickets/{id}
  if (id && options.method === 'PATCH') {
    const idx = tickets.findIndex(t => t.id === id);
    if (idx === -1) throw new Error('Ticket not found');
    if (body.status) tickets[idx].status = body.status;
    if (body.assigned_to) tickets[idx].assigned_to = body.assigned_to;
    tickets[idx].updated_at = new Date().toISOString();
    saveLocalTickets(tickets);
    return tickets[idx];
  }

  // POST /tickets/{id}/poke
  if (id && action === 'poke' && options.method === 'POST') {
    const idx = tickets.findIndex(t => t.id === id);
    if (idx === -1) throw new Error('Ticket not found');
    tickets[idx].pokes = (tickets[idx].pokes || 0) + 1;
    tickets[idx].updated_at = new Date().toISOString();
    saveLocalTickets(tickets);
    return tickets[idx];
  }

  // DELETE /tickets/{id}
  if (id && !action && options.method === 'DELETE') {
    const idx = tickets.findIndex(t => t.id === id);
    if (idx === -1) throw new Error('Ticket not found');
    tickets.splice(idx, 1);
    saveLocalTickets(tickets);
    return { message: 'Ticket extinguished' };
  }

  // GET /tickets/{id}
  if (id && !action && (!options.method || options.method === 'GET')) {
    const t = tickets.find(t => t.id === id);
    if (!t) throw new Error('Ticket not found');
    return t;
  }

  throw new Error('Unknown local API path: ' + path);
}

async function loadTickets() {
  const board = document.getElementById('ticketBoard');
  try {
    const data = await apiFetch('/tickets');
    tickets = data;
    renderTickets(tickets);
    updateFireCount();
  } catch (e) {
    if (tickets.length === 0) {
      board.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:60px;color:rgba(200,214,208,0.2)">
        <div style="font-size:60px;margin-bottom:16px">😿</div>
        <div style="font-size:18px;margin-bottom:8px;color:rgba(200,214,208,0.3)">${e.message}</div>
        <div style="font-size:13px;color:rgba(200,214,208,0.15)">Start the backend, then refresh. The cat is waiting.</div>
      </div>`;
    }
  }
}

// === Render Tickets ===
function renderTickets(tickets, filter = 'all') {
  const filtered = filter === 'all' ? tickets : tickets.filter(t => t.category === filter);
  ['open', 'progress', 'resolved'].forEach(status => {
    const col = document.querySelector(`.ticket-list[data-status="${status}"]`);
    const items = filtered.filter(t => t.status === status);
    col.innerHTML = items.length
      ? items.map(t => renderTicketCard(t)).join('')
      : '<div class="ticket-empty">🐱 No tickets here. The cat is pleased.</div>';
  });
  setupDragDrop();
  updateCatCounter();
}

function renderTicketCard(t) {
  const labels = { fire: '🔥 Fire', bug: '🐛 Bug', feature: '💡 Feature', question: '❓ Question' };
  const prioIcons = { critical: '🔴', high: '🟠', medium: '🟡', low: '🟢' };
  const svc = t.service ? SERVICE_LABELS[t.service] || t.service : null;
  return `<div class="ticket-card" data-ticket-id="${t.id}" onclick="openTicket('${t.id}')">
    <div class="ticket-cat"><span class="cat-badge ${t.category}">${catAvatar(t.id)} ${labels[t.category] || '❓'}</span> ${svc ? `<span style="font-size:10px;color:rgba(200,214,208,0.3);font-family:monospace">${svc}</span>` : ''}</div>
    <div class="ticket-title">${t.title}</div>
    <div class="ticket-meta">🐾 ${t.author || 'Anonymous'} · ${timeAgo(t.created_at)} · 👨‍🚒 ${t.assigned_to || 'Unassigned'}</div>
  </div>`;
}

// === Submit Ticket ===
async function submitTicket() {
  const category = document.getElementById('ticketCategory').value;
  const priority = document.getElementById('ticketPriority').value;
  const title = document.getElementById('ticketTitle').value.trim();
  const desc = document.getElementById('ticketDesc').value.trim();
  const author = document.getElementById('ticketAuthor').value.trim() || 'Anonymous Cat';
  const service = document.getElementById('ticketService').value || null;
  if (!title) { showToast('🐱 The cat needs a title! What is on fire?', 'error'); return; }
  const btn = document.querySelector('.btn-submit');
  btn.disabled = true;
  btn.innerHTML = '🐱 Dispatching cat...';
  try {
    const ticket = await apiFetch('/tickets', {
      method: 'POST',
      body: JSON.stringify({ category, priority, title, description: desc, author, service }),
    });
    showToast(`🚒 <strong>${ticket.assigned_to}</strong> is on the way! Ticket #${ticket.id.slice(0,8)}`, 'success');
    showDispatch(ticket.assigned_to);
    if (ticket.priority === 'critical' || ticket.category === 'fire') emergencySiren();
    document.getElementById('ticketTitle').value = '';
    document.getElementById('ticketDesc').value = '';
    await loadTickets();
    switchTab('board');
  } catch (e) {
    showToast(`😿 ${e.message}`, 'error');
  }
  btn.disabled = false;
  btn.innerHTML = '🐱 Send Cat to Rescue';
}

// === Ticket Modal ===
async function openTicket(id) {
  let t = tickets.find(x => x.id === id);
  if (!t) {
    try { t = await apiFetch(`/tickets/${id}`); } catch(e) { showToast('😿 Ticket not found', 'error'); return; }
  }
  const labels = { fire: '🔥 Fire', bug: '🐛 Bug', feature: '💡 Feature', question: '❓ Question' };
  const statusLabels = { open: '🚒 To The Rescue', progress: '👨‍🚒 On It!', resolved: '✅ Extinguished' };
  const colors = { open: '#ff8800', progress: '#00aaff', resolved: '#00ff88' };
  const content = document.getElementById('ticketContent');
  content.innerHTML = `
    <button class="modal-back" onclick="closeTicket()">← Back to Board</button>
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px">
      <div style="background:${colors[t.status]}10;border:2px solid ${colors[t.status]}30;border-radius:16px;width:60px;height:60px;display:flex;align-items:center;justify-content:center;font-size:28px">${labels[t.category]?.split(' ')[0] || '❓'}</div>
      <div>
        <div class="modal-badge" style="border-color:${colors[t.status]}30;color:${colors[t.status]}">${statusLabels[t.status]}</div>
        <h1 style="font-size:22px;margin:8px 0 0;color:#fff">${t.title}</h1>
      </div>
    </div>
    <div class="modal-meta" style="display:flex;gap:16px;flex-wrap:wrap">
      <span>🐾 ${t.author || 'Anonymous'}</span>
      <span>🕐 ${timeAgo(t.created_at)}</span>
      <span>⚡ ${t.priority}</span>
      ${t.service ? `<span>🌐 ${SERVICE_LABELS[t.service] || t.service}</span>` : ''}
      <span>👨‍🚒 ${t.assigned_to || 'Unassigned'}</span>
      <span>👆 Poked ${t.pokes || 0} times</span>
    </div>
    <div class="modal-body">
      <p>${t.description || 'No additional details provided. The cat is investigating.'}</p>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:16px">
        <button class="btn btn-secondary" style="padding:10px 18px;font-size:12px" onclick="changeTicketStatus('${t.id}','${t.status === 'open' ? 'progress' : t.status === 'progress' ? 'resolved' : 'open'}')">
          ${t.status === 'open' ? '🚒 Start Rescue' : t.status === 'progress' ? '✅ Mark Resolved' : '🔄 Reopen'}
        </button>
        <button class="btn btn-secondary" style="padding:10px 18px;font-size:12px" onclick="pokeTicket('${t.id}')">
          👆 Poke the Cat
        </button>
        <button class="btn btn-secondary" style="padding:10px 18px;font-size:12px;color:#ff4444" onclick="deleteTicket('${t.id}')">
          🗑️ Extinguish Ticket
        </button>
      </div>
      <div class="reaction-bar">
        <button class="reaction-btn" onclick="reactToTicket('${t.id}','🐟')">🐟</button>
        <button class="reaction-btn" onclick="reactToTicket('${t.id}','😹')">😹</button>
        <button class="reaction-btn" onclick="reactToTicket('${t.id}','🙀')">🙀</button>
        <button class="reaction-btn" onclick="reactToTicket('${t.id}','🔥')">🔥</button>
        <span style="font-size:11px;color:rgba(200,214,208,0.2);margin-left:8px;align-self:center">React with your cat feelings</span>
      </div>
    </div>`;
  document.getElementById('ticketModal').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeTicket() {
  document.getElementById('ticketModal').classList.remove('open');
  document.body.style.overflow = '';
}

async function changeTicketStatus(id, newStatus) {
  try {
    await apiFetch(`/tickets/${id}`, { method: 'PATCH', body: JSON.stringify({ status: newStatus }) });
    const labels = { progress: '🚒 On it!', resolved: '✅ Extinguished!', open: '🔄 Reopened!' };
    showToast(`${labels[newStatus] || '✅ Updated!'}`, 'success');
    if (newStatus === 'resolved') playPurr();
    closeTicket();
    await loadTickets();
  } catch (e) { showToast(`😿 ${e.message}`, 'error'); }
}

async function pokeTicket(id) {
  try {
    const t = await apiFetch(`/tickets/${id}/poke`, { method: 'POST' });
    showToast(`👆 Poked! The cat has been poked ${t.pokes} times now.`, 'info');
    playMeow();
    showCatReaction();
    closeTicket();
    await loadTickets();
  } catch (e) { showToast(`😿 ${e.message}`, 'error'); }
}

async function deleteTicket(id) {
  if (!confirm('🔥 Are you sure you want to extinguish this ticket? The cat will be sad.')) return;
  playHiss();
  try {
    await apiFetch(`/tickets/${id}`, { method: 'DELETE' });
    showToast('🗑️ Ticket extinguished. The cat nods approvingly.', 'success');
    closeTicket();
    await loadTickets();
  } catch (e) { showToast(`😿 ${e.message}`, 'error'); }
}

async function reactToTicket(id, emoji) {
  showToast(`${emoji} You reacted with ${emoji}! The cat noticed.`, 'info');
  playMeow();
  showCatReaction();
}

// === Tabs ===
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    switchTab(link.dataset.tab);
  });
});

function switchTab(tab) {
  document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelector(`.nav-link[data-tab="${tab}"]`)?.classList.add('active');
  document.getElementById(`tab-${tab}`)?.classList.add('active');
  if (tab === 'board') loadTickets();
  if (tab === 'fighters') renderFighters();
  if (tab === 'status') renderStatus();
}

// === Filter Buttons ===
document.querySelectorAll('.btn-filter').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.btn-filter').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderTickets(tickets, btn.dataset.filter);
  });
});

// === Render Fighters ===
function renderFighters() {
  const grid = document.getElementById('fightersGrid');
  grid.innerHTML = FIREFIGHTERS.map((f, i) => `
    <div class="fighter-card fade-up" onclick="openFighter(${i})" style="animation-delay:${i * 0.1}s">
      <span class="f-emoji">${f.emoji}</span>
      <div class="f-rank">${f.rank}</div>
      <div class="f-name">${f.name}</div>
      <div class="f-role">${f.role}</div>
      <div class="f-status ${f.status}">${f.status === 'on-duty' ? '🟢 On Duty' : '💤 Strategic Nap'}</div>
    </div>
  `).join('');
}

function hissFighter(name) {
  const today = new Date().toISOString().slice(0,10);
  const key = `hiss_${name.replace(/\s/g,'_')}_${today}`;
  const count = parseInt(localStorage.getItem(key) || '0') + 1;
  localStorage.setItem(key, String(count));
  const el = document.getElementById(`hissCount_${name.replace(/\s/g,'_')}`);
  if (el) el.textContent = `😾 Hissed ${count} time${count > 1 ? 's' : ''} today`;
  const modal = document.getElementById('fighterModal');
  coinBurst(modal.querySelector('.modal-content'));
  playHiss();
  showToast(`😾 You hissed at ${name}! The cat is offended.`, 'info');
}

function coinBurst(target) {
  const coins = ['💰','🪙','💎','💵','🐟'];
  const rect = (target || document.body).getBoundingClientRect();
  for (let i = 0; i < 5; i++) {
    const c = document.createElement('span');
    c.className = 'coin-burst';
    c.textContent = coins[Math.floor(Math.random() * coins.length)];
    c.style.left = (rect.left + Math.random() * (rect.width || 200)) + 'px';
    c.style.top = (rect.top + Math.random() * (rect.height || 200)) + 'px';
    document.body.appendChild(c);
    setTimeout(() => c.remove(), 800);
  }
}

function openFighter(index) {
  const f = FIREFIGHTERS[index];
  const modal = document.getElementById('fighterModal');
  const content = document.getElementById('fighterContent');
  content.innerHTML = `
    <button class="modal-back" onclick="closeFighter()">← Back to Firefighters</button>
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px">
      <div style="font-size:72px;background:${f.color}10;border:2px solid ${f.color}30;border-radius:20px;width:100px;height:100px;display:flex;align-items:center;justify-content:center">${f.emoji}</div>
      <div>
        <div class="modal-badge" style="border-color:${f.color}30;color:${f.color};margin-bottom:8px">${f.rank}</div>
        <h1 style="font-size:28px;margin:0;color:#fff">${f.name}</h1>
        <div style="color:${f.color};font-size:15px;font-weight:500;margin-top:4px">${f.role}</div>
      </div>
    </div>
    <div class="modal-meta" style="margin-bottom:24px;padding-bottom:20px">Age: ${f.age} · Status: ${f.status === 'on-duty' ? '🟢 On Duty' : '💤 Napping (but still reachable)'}</div>
    <div class="modal-body">
      <p>${f.bio}</p>
      <h2>🔥 Life Philosophy</h2>
      <div class="equation">"${f.motto}"</div>
      <h2>😴 When Not Fighting Fires</h2>
      <p>${f.hobby}</p>
      <div style="margin-top:16px">
        <button class="hiss-btn" onclick="hissFighter('${f.name}')">😾 Hiss at ${f.name}</button>
        <span class="hiss-count" id="hissCount_${f.name.replace(/\s/g,'_')}"></span>
      </div>
    </div>`;
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeFighter() {
  document.getElementById('fighterModal').classList.remove('open');
  document.body.style.overflow = '';
}

// === FAQ ===
function toggleFaq(el) {
  el.parentElement.classList.toggle('open');
}

// === Cross-Origin Token Sync ===
const ALL_PORTS = [5173, 5174, 5175, 5176, 5178, 5179, 5180, 5181, 8080];

async function broadcastTokenToAll() {
  if (!authToken || !authUser) return;
  // Tell the backend relay
  try { await fetch(`${AUTH_API}/broadcast-token`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({token: authToken, user: authUser}) }); } catch(e) {}
  // Try to set token on all known apps via their auth endpoints
  for (const port of ALL_PORTS) {
    if (port === 5180) continue; // skip self
    try {
      await fetch(`http://localhost:${port}/auth-set-token`, {
        method: 'POST', mode: 'no-cors',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({token: authToken, user: authUser}),
      });
    } catch(e) { /* cross-origin, may fail silently */ }
  }
}

async function checkTokenRelay() {
  if (authToken) return; // already have one
  try {
    const r = await fetch(`${AUTH_API}/broadcast-token`);
    if (!r.ok) return;
    const d = await r.json();
    if (d.token && d.timestamp) {
      const age = (Date.now() - new Date(d.timestamp).getTime()) / 1000;
      if (age < 30) { // token broadcast within last 30 seconds
        authToken = d.token;
        authUser = d.user;
        localStorage.setItem('miau_token', authToken);
        localStorage.setItem('miau_user', authUser);
        updateAuthUI();
        offlineMode = false;
        document.getElementById('offlineBadge')?.classList.remove('show');
        showToast(`🐱 Synced login as ${authUser} from another app!`, 'success');
        await loadTickets();
      }
    }
  } catch(e) {}
}

// === Cat of the Day ===
const COT_DIV = document.getElementById('catOfTheDay');
if (COT_DIV) {
  const today = new Date().toDateString();
  const saved = localStorage.getItem('miau_cotd');
  let cotd;
  if (saved && saved.startsWith(today)) {
    cotd = JSON.parse(saved.slice(today.length));
  } else {
    const cats = FIREFIGHTERS.concat([
      { emoji: '🐟', name: 'Prof. Dr. Tuna', quote: '"Tuna is the answer. What was the question?"', role: 'ESG & Sustainable Finance' },
      { emoji: '🤖', name: 'CatGPT', quote: '"I do not need feelings. I have backtests."', role: 'Chief AI Officer' },
    ]);
    cotd = cats[Math.floor(Math.random() * cats.length)];
    localStorage.setItem('miau_cotd', today + JSON.stringify(cotd));
  }
  COT_DIV.innerHTML = `<span style="font-size:24px">${cotd.emoji}</span> <span style="font-size:11px;color:rgba(200,214,208,0.3)">${cotd.name} — ${cotd.role}<br><span style="font-size:10px;color:rgba(200,214,208,0.15);font-style:italic">${cotd.quote || cotd.motto || ''}</span></span>`;
}

// === More Cat Sounds ===
function playHiss() {
  if (!soundEnabled) return;
  try { const ctx = getAudio(); const o = ctx.createOscillator(); const g = ctx.createGain(); o.connect(g); g.connect(ctx.destination); o.type = 'sawtooth'; o.frequency.setValueAtTime(2000, ctx.currentTime); o.frequency.exponentialRampToValueAtTime(500, ctx.currentTime + 0.2); g.gain.setValueAtTime(0.03, ctx.currentTime); g.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.25); o.start(ctx.currentTime); o.stop(ctx.currentTime + 0.25); } catch(e) {}
}

function playYawn() {
  if (!soundEnabled) return;
  try { const ctx = getAudio(); const o = ctx.createOscillator(); const g = ctx.createGain(); o.connect(g); g.connect(ctx.destination); o.type = 'sine'; o.frequency.setValueAtTime(300, ctx.currentTime); o.frequency.exponentialRampToValueAtTime(150, ctx.currentTime + 0.6); g.gain.setValueAtTime(0.04, ctx.currentTime); g.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.7); o.start(ctx.currentTime); o.stop(ctx.currentTime + 0.7); } catch(e) {}
}

// Hiss on ticket delete — handled inside deleteTicket()
// Yawn on idle detection
let lastActivity = Date.now();
document.addEventListener('mousemove', () => { lastActivity = Date.now(); });
setInterval(() => {
  if (Date.now() - lastActivity > 120000 && soundEnabled) playYawn();
}, 60000);

// === Init ===
function updateAuthUI() {
  const btn = document.getElementById('authBtn');
  const userEl = document.getElementById('authUser');
  if (offlineMode) {
    btn.innerHTML = '🔑 Demo (offline)';
    btn.onclick = () => showToast('🐱 Running in offline demo mode — no login needed', 'info');
    btn.style.color = '#ffcc00';
    userEl.textContent = '🐱 Demo Cat';
    userEl.style.display = 'inline';
    return;
  }
  if (authToken && authUser) {
    btn.innerHTML = '🚪 Logout';
    btn.onclick = logout;
    btn.style.color = '#ff6644';
    userEl.textContent = `🐱 ${authUser}`;
    userEl.style.display = 'inline';
  } else {
    btn.innerHTML = '🔑 Login';
    btn.onclick = () => document.getElementById('loginModal').classList.add('open');
    userEl.textContent = '';
    userEl.style.display = 'none';
  }
}

async function login() {
  const username = document.getElementById('loginUser').value.trim();
  const password = document.getElementById('loginPass').value;
  if (!username || !password) { showToast('🐱 Username and password required', 'error'); return; }
  const btn = document.querySelector('.login-btn');
  btn.disabled = true; btn.innerHTML = '🐱 Logging in...';
  try {
    const data = await apiFetch(`${AUTH_API}/token`, {
      method: 'POST', body: JSON.stringify({ username, password }),
    });
    authToken = data.access_token;
    authUser = username;
    localStorage.setItem('miau_token', authToken);
    localStorage.setItem('miau_user', authUser);
    document.getElementById('loginModal').classList.remove('open');
    document.getElementById('loginUser').value = '';
    document.getElementById('loginPass').value = '';
    showToast(`🐱 Welcome, ${username}!`, 'success');
    updateAuthUI();
    offlineMode = false;
    document.getElementById('offlineBadge')?.classList.remove('show');
    broadcastTokenToAll();
    await loadTickets();
  } catch (e) {
    showToast(`😿 Login failed: ${e.message}`, 'error');
  }
  btn.disabled = false; btn.innerHTML = '🐱 Login';
}

async function register() {
  const username = document.getElementById('regUser').value.trim();
  const password = document.getElementById('regPass').value;
  const email = document.getElementById('regEmail').value.trim();
  if (!username || !password || !email) { showToast('🐱 All fields required', 'error'); return; }
  const btn = document.querySelector('.register-btn');
  btn.disabled = true; btn.innerHTML = '🐱 Registering...';
  try {
    await apiFetch(`${AUTH_API}/register`, {
      method: 'POST', body: JSON.stringify({ username, password, email }),
    });
    showToast(`🐱 Registered! Logging in as ${username}...`, 'success');
    document.getElementById('regUser').value = '';
    document.getElementById('regPass').value = '';
    document.getElementById('regEmail').value = '';
    document.getElementById('registerModal').classList.remove('open');
    // Auto-login after register
    document.getElementById('loginUser').value = username;
    document.getElementById('loginPass').value = password;
    login();
  } catch (e) {
    showToast(`😿 Registration failed: ${e.message}`, 'error');
  }
  btn.disabled = false; btn.innerHTML = '🐱 Register';
}

function logout() {
  authToken = null;
  authUser = null;
  localStorage.removeItem('miau_token');
  localStorage.removeItem('miau_user');
  showToast('🐱 Logged out. The cat will miss you.', 'info');
  updateAuthUI();
}

function showRegister() {
  document.getElementById('loginModal').classList.remove('open');
  document.getElementById('registerModal').classList.add('open');
}

function showLoginFromRegister() {
  document.getElementById('registerModal').classList.remove('open');
  document.getElementById('loginModal').classList.add('open');
}

function updateCatCounter() {
  const active = tickets.filter(t => t.status !== 'resolved').length;
  const el = document.getElementById('catCounter');
  if (el) el.textContent = active;
}

function updateFireCount() {
  const count = tickets.filter(t => t.category === 'fire' && t.status !== 'resolved').length;
  document.getElementById('fireCount').textContent = count;
}

// === Polling ===
function startPolling() {
  if (pollTimer) clearInterval(pollTimer);
  pollTimer = setInterval(loadTickets, 15000);
}

// === Drag & Drop Tickets ===
function setupDragDrop() {
  document.querySelectorAll('.ticket-card').forEach(card => {
    card.setAttribute('draggable', 'true');
    card.addEventListener('dragstart', e => {
      e.dataTransfer.setData('text/plain', card.dataset.ticketId);
      card.classList.add('dragging');
    });
    card.addEventListener('dragend', () => card.classList.remove('dragging'));
  });
  document.querySelectorAll('.ticket-list').forEach(col => {
    col.addEventListener('dragover', e => { e.preventDefault(); col.classList.add('drag-over'); });
    col.addEventListener('dragleave', () => col.classList.remove('drag-over'));
    col.addEventListener('drop', async e => {
      e.preventDefault();
      col.classList.remove('drag-over');
      const id = e.dataTransfer.getData('text/plain');
      if (!id) return;
      const statusMap = { 'open': 'open', 'progress': 'progress', 'resolved': 'resolved' };
      const newStatus = statusMap[col.dataset.status];
      if (!newStatus) return;
      const t = tickets.find(x => x.id === id);
      if (!t || t.status === newStatus) return;
      try {
        await apiFetch(`/tickets/${id}`, { method: 'PATCH', body: JSON.stringify({ status: newStatus }) });
        const msgs = { progress: '🚒 Moved to On It!', resolved: '✅ Extinguished!', open: '🔄 Reopened!' };
        showToast(msgs[newStatus] || '✅ Moved!', 'success');
        if (newStatus === 'resolved') playPurr();
        await loadTickets();
      } catch (e) { showToast(`😿 ${e.message}`, 'error'); }
    });
  });
}

// === FAQ Search ===
function searchFaq(query) {
  const items = document.querySelectorAll('.faq-item');
  const q = query.toLowerCase().trim();
  items.forEach(item => {
    const text = item.textContent.toLowerCase();
    item.style.display = !q || text.includes(q) ? '' : 'none';
  });
}

// === Tuna Facts ===
const TUNA_FACTS = [
  'Tuna is the official currency of the Miau economy. 1 TUNA = 1 completed task.',
  'The Tuna-Bond Spread is +3.2% — tuna outperforms government bonds.',
  'Tuna inflation is stable at 2.1% (Cat Bureau of Statistics, Q1 2026).',
  'The Cat Happiness Function: CH = ∫(Tuna × Purrs × Humans) dt. As Tuna→∞, CH→∞.',
  'Purrs Per Tuna (PPT) is 4.7, according to a peer-reviewed cat survey.',
  'Prof. Dr. Tuna holds 3 PhDs and is the only fish on the cabinet. He is also a certified green bond auditor.',
  'Tuna futures are traded exclusively during catnap hours for optimal pricing.',
  'The Miau Fire Brigade\'s emergency services are paid entirely in tuna.',
  'A single tuna can can resolve 47% of all customer complaints (source: the cat told us).',
  'The International Cat Academy recommends a minimum daily intake of 2 tuna jokes per user.',
];

function showTuna() {
  showRandomTunaFact();
  document.getElementById('tunaModal').classList.add('open');
  document.body.style.overflow = 'hidden';
  playPurr();
}

function showRandomTunaFact() {
  const fact = TUNA_FACTS[Math.floor(Math.random() * TUNA_FACTS.length)];
  document.getElementById('tunaFact').textContent = fact;
}

function closeTuna() {
  document.getElementById('tunaModal').classList.remove('open');
  document.body.style.overflow = '';
}

// === Cat Companion (cursor follower) ===
document.addEventListener('mousemove', e => {
  const cat = document.getElementById('catCompanion');
  if (cat) {
    cat.style.left = (e.clientX + 20) + 'px';
    cat.style.top = (e.clientY - 10) + 'px';
  }
});

// === System Status with real checks ===
async function checkServiceStatus() {
  const grid = document.getElementById('statusGrid');
  if (!grid) return;
  const labels = { online: '🟢 Online', slow: '🟡 Slow', down: '🔴 Down', checking: '⏳ Checking...' };
  grid.innerHTML = SERVICE_STATUSES.map(s => `
    <div class="status-card fade-up">
      <div><div class="s-name">${s.name}</div><div class="s-port">Port ${s.port}</div></div>
      <div class="s-indicator checking">⏳ Checking...</div>
    </div>
  `).join('');
  for (let i = 0; i < SERVICE_STATUSES.length; i++) {
    const s = SERVICE_STATUSES[i];
    const cards = grid.querySelectorAll('.status-card');
    const indicator = cards[i]?.querySelector('.s-indicator');
    if (!indicator) continue;
    try {
      const resp = await fetch(`http://localhost:${s.port}`, { method: 'HEAD', mode: 'no-cors', signal: AbortSignal.timeout(3000) });
      indicator.className = 's-indicator online';
      indicator.textContent = '🟢 Online';
    } catch (e) {
      if (s.status === 'slow') {
        indicator.className = 's-indicator slow';
        indicator.textContent = '🟡 Slow';
      } else {
        indicator.className = 's-indicator down';
        indicator.textContent = '🔴 Down';
      }
    }
  }
}

function renderStatus() {
  checkServiceStatus();
  if (statusTimer) clearInterval(statusTimer);
  statusTimer = setInterval(checkServiceStatus, 30000);
}

// === Utility ===
function timeAgo(dateStr) {
  if (!dateStr) return 'unknown';
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'just now';
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

// === Modals: click overlay to close ===
document.querySelectorAll('.modal-overlay').forEach(m => {
  m.addEventListener('click', e => { if (e.target === m) { m.classList.remove('open'); document.body.style.overflow = ''; } });
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.open').forEach(m => { m.classList.remove('open'); document.body.style.overflow = ''; });
  }
});

// === Fade-up observer ===
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.style.opacity = '1'; entry.target.style.transform = 'translateY(0)'; }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.fade-up').forEach(el => {
  el.style.opacity = '0'; el.style.transform = 'translateY(30px)'; el.style.transition = 'all 0.8s ease'; observer.observe(el);
});

// === Set random cat proverb in footer ===
document.querySelectorAll('.cat-proverb').forEach(el => {
  el.textContent = CAT_PROVERBS[Math.floor(Math.random() * CAT_PROVERBS.length)];
});

// === Init ===
(async function init() {
  document.getElementById('soundToggle').textContent = soundEnabled ? '🔊' : '🔇';
  initLocalStore();
  // Try online first, will auto-fallback to offline if backend is down
  await loadTickets();
  startPolling();
  updateFireCount();
  updateCatCounter();
  setupDragDrop();
  playPurr();
})();
