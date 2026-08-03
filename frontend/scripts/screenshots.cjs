const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const PROJECT_ROOT = path.join(__dirname, '..', '..');
const SCREENSHOTS_DIR = path.join(PROJECT_ROOT, 'docs', 'screenshots');
const HOMEPAGE_PUBLIC = '/home/jevgeniz/Projekte/miau-homepage/public';

async function main() {
  fs.mkdirSync(SCREENSHOTS_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 2,
  });

  const page = await context.newPage();

  try {
    // 1. Education Platform
    console.log('📸 Education Platform...');
    await page.goto('http://localhost:5174', { timeout: 15000, waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'education-platform.png'), fullPage: true });
    console.log('   ✅ education-platform.png');

    // 2. Main Terminal
    console.log('📸 Main Terminal...');
    await page.goto('http://localhost:5173', { timeout: 15000, waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'terminal-landing.png') });
    console.log('   ✅ terminal-landing.png');

    // 3. Login + Map
    console.log('📸 Map...');
    await page.fill('#terminal-input', 'login ' + (process.env.MIAU_TEST_USER || 'admin') + ' ' + (process.env.MIAU_TEST_PASS || ''));
    await page.press('#terminal-input', 'Enter');
    await page.waitForTimeout(2000);
    await page.fill('#terminal-input', 'map');
    await page.press('#terminal-input', 'Enter');
    await page.waitForTimeout(3000);
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'world-map.png') });
    console.log('   ✅ world-map.png');

    // 4. Catberg
    console.log('📸 Catberg...');
    // Close map first via the portal Back button
    await page.waitForTimeout(1000);
    await page.evaluate(() => {
      // Click Back button in the portal toolbar
      const btns = document.querySelectorAll('button');
      for (const btn of btns) {
        if (btn.textContent?.includes('← Back')) { btn.click(); break; }
      }
    });
    await page.waitForTimeout(1000);
    await page.fill('#terminal-input', 'catberg wei');
    await page.press('#terminal-input', 'Enter');
    await page.waitForTimeout(3000);
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'catberg-terminal.png') });
    console.log('   ✅ catberg-terminal.png');

    // 5. Portfolio
    console.log('📸 Portfolio...');
    await page.evaluate(() => {
      const btns = document.querySelectorAll('button');
      for (const btn of btns) {
        if (btn.textContent?.includes('← Back')) { btn.click(); break; }
      }
    });
    await page.waitForTimeout(1000);
    await page.fill('#terminal-input', 'portfolios');
    await page.press('#terminal-input', 'Enter');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'portfolio-view.png') });
    console.log('   ✅ portfolio-view.png');

  } catch (err) {
    console.error('❌ Error:', err.message);
  }

  // 6. OG Image (separate page)
  try {
    console.log('📸 OG Image...');
    const ogPage = await context.newPage();
    await ogPage.setViewportSize({ width: 1200, height: 630 });
    await ogPage.setContent(`<!DOCTYPE html>
<html><head><style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: linear-gradient(135deg, #0a1a14 0%, #0d2418 30%, #001a0d 100%); font-family: monospace; width: 1200px; height: 630px; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.container { text-align: center; }
.cat { font-size: 72px; margin-bottom: 8px; }
h1 { color: #00ff88; font-size: 48px; text-shadow: 0 0 20px rgba(0,255,136,0.4); margin-bottom: 4px; }
h2 { color: #88ffbb; font-size: 24px; font-weight: normal; margin-bottom: 20px; }
.stats { display: flex; gap: 24px; justify-content: center; }
.stat { text-align: center; }
.stat-num { color: #00ff88; font-size: 28px; font-weight: bold; }
.stat-label { color: #557755; font-size: 12px; margin-top: 2px; }
.footer { color: #335533; font-size: 11px; margin-top: 24px; }
.glow { position: absolute; width: 400px; height: 400px; border-radius: 50%; filter: blur(80px); opacity: 0.1; pointer-events: none; }
.g1 { top: -100px; left: -100px; background: #00ff88; }
.g2 { bottom: -100px; right: -100px; background: #00ccff; }
</style></head><body>
<div class="glow g1"></div><div class="glow g2"></div>
<div class="container">
  <div class="cat">🐱</div>
  <h1>Miau Finance</h1>
  <h2>Autonomous Financial Intelligence</h2>
  <div class="stats">
    <div class="stat"><div class="stat-num">50</div><div class="stat-label">Markets</div></div>
    <div class="stat"><div class="stat-num">100+</div><div class="stat-label">Companies</div></div>
    <div class="stat"><div class="stat-num">20</div><div class="stat-label">Courses</div></div>
    <div class="stat"><div class="stat-num">39</div><div class="stat-label">Cats</div></div>
    <div class="stat"><div class="stat-num">10</div><div class="stat-label">Brokers</div></div>
  </div>
  <div class="footer">Terminal-first · AI-powered · Cat-approved</div>
</div>
</body></html>`);
    await ogPage.waitForTimeout(500);
    const ogPath = path.join(HOMEPAGE_PUBLIC, 'og-image.png');
    await ogPage.screenshot({ path: ogPath });
    // Copy to screenshots too
    await ogPage.screenshot({ path: path.join(SCREENSHOTS_DIR, 'og-image.png') });
    console.log('   ✅ og-image.png');
  } catch (err) {
    console.error('❌ OG Error:', err.message);
  }

  await browser.close();
  console.log('\n✅ All screenshots captured!');
}

main().catch(console.error);
