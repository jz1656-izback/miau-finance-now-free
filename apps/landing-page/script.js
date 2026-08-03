const canvas = document.getElementById('stars');
const ctx = canvas.getContext('2d');
let w, h, stars = [];

function resize() {
  w = canvas.width = window.innerWidth;
  h = canvas.height = window.innerHeight;
}

function initStars(count) {
  stars = [];
  for (let i = 0; i < count; i++) {
    stars.push({
      x: Math.random() * w, y: Math.random() * h,
      r: Math.random() * 1.5 + 0.3,
      a: Math.random() * 0.8 + 0.2,
      s: Math.random() * 0.3 + 0.05,
      phase: Math.random() * Math.PI * 2
    });
  }
}

function drawStars(time) {
  ctx.clearRect(0, 0, w, h);
  for (const star of stars) {
    const alpha = star.a * (0.6 + 0.4 * Math.sin(time * star.s + star.phase));
    ctx.beginPath();
    ctx.arc(star.x, star.y, star.r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(0, 255, 65, ${alpha})`;
    ctx.fill();
  }
}

function animate(time) {
  drawStars(time * 0.001);
  requestAnimationFrame(animate);
}

resize();
initStars(120);
animate(0);

window.addEventListener('resize', () => { resize(); initStars(120); });

const tagline = document.getElementById('tagline');
const text = "Where cats trade stocks. Portfolios purr with delight.";
let idx = 0;

function typeWriter() {
  if (idx < text.length) {
    tagline.textContent += text[idx];
    idx++;
    setTimeout(typeWriter, 35 + Math.random() * 30);
  }
}
setTimeout(typeWriter, 500);

const cmdEl = document.getElementById('cmd');
const commands = [
  'cat ./products --all', './miau --launch', 'ls -la services/',
  'docker ps --format "miau"', 'npm run deploy:galaxy', 'ssh miau@terminal',
  'cat ./VERSION', './run --all-services'
];

function typeCommand(el, text, cb) {
  let i = 0;
  el.textContent = '';
  function type() {
    if (i < text.length) {
      el.textContent += text[i];
      i++;
      setTimeout(type, 25 + Math.random() * 40);
    } else if (cb) setTimeout(cb, 1500);
  }
  type();
}

function cycleCommands() {
  const cmd = commands[Math.floor(Math.random() * commands.length)];
  typeCommand(cmdEl, cmd, () => setTimeout(cycleCommands, 2000));
}
setTimeout(cycleCommands, 3000);

const uptimeEl = document.getElementById('uptime');
const startTime = Date.now();
function updateUptime() {
  const elapsed = Math.floor((Date.now() - startTime) / 1000);
  uptimeEl.textContent = `UPTIME: ${Math.floor(elapsed/86400)}d ${Math.floor((elapsed%86400)/3600)}h ${Math.floor((elapsed%3600)/60)}m`;
}
setInterval(updateUptime, 10000);
updateUptime();
