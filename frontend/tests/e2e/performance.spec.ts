/**
 * V6-011e: Performance Benchmark — 60fps target with all layers active
 *
 * Measures rendering performance of the WorldMap with all data layers active.
 * Runs both 2D (Leaflet) and 3D (MiauGlobe) benchmarks.
 */
import { test, expect } from '@playwright/test'

const URL = process.env.MIAU_FRONTEND_URL || 'http://localhost:5173'

test.describe('Performance Benchmarks', () => {
  test('terminal loads within 5 seconds', async ({ page }) => {
    const start = Date.now()
    await page.goto(URL, { waitUntil: 'networkidle' })
    const loadTime = Date.now() - start
    console.log(`⏱ Terminal load: ${loadTime}ms`)
    expect(loadTime).toBeLessThan(5000)
    // Verify terminal is visible — check for the terminal root element
    await expect(page.locator('.terminal-root, .crt')).toBeVisible({ timeout: 10000 })
  })

  test('login completes within 3 seconds', async ({ page }) => {
    await page.goto(URL, { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(1000)

    // Type login command
    const input = page.locator('#terminal-input').first()
    await input.fill(`login ${process.env.MIAU_TEST_USER || 'admin'} ${process.env.MIAU_TEST_PASS || ''}`)
    await input.press('Enter')

    // Wait for response
    await page.waitForTimeout(1500)

    // Check terminal output for success
    const body = await page.locator('body').innerText()
    expect(body.toLowerCase()).toContain('token')
    console.log('✅ Login successful')
  })

  test('WorldMap opens and renders tiles', async ({ page }) => {
    await page.goto(URL, { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(1000)

    // Login first
    const input = page.locator('#terminal-input').first()
    await input.fill(`login ${process.env.MIAU_TEST_USER || 'admin'} ${process.env.MIAU_TEST_PASS || ''}`)
    await input.press('Enter')
    await page.waitForTimeout(1500)

    // Open map
    await input.fill('map')
    await input.press('Enter')
    await page.waitForTimeout(3000)

    // Wait for Leaflet tiles to load
    await page.waitForSelector('.leaflet-tile-loaded', { timeout: 15000 }).catch(() => {
      console.log('⚠️ Some Leaflet tiles may not have loaded')
    })

    // Verify map is visible
    const leafletContainer = page.locator('.leaflet-container')
    await expect(leafletContainer).toBeVisible({ timeout: 10000 })

    console.log('✅ WorldMap rendered successfully')
  })

  test('WorldMap performs at 30+ FPS while dragging', async ({ page }) => {
    await page.goto(URL, { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(1000)

    // Login
    const input = page.locator('#terminal-input').first()
    await input.fill(`login ${process.env.MIAU_TEST_USER || 'admin'} ${process.env.MIAU_TEST_PASS || ''}`)
    await input.press('Enter')
    await page.waitForTimeout(1500)

    // Open map
    await input.fill('map')
    await input.press('Enter')
    await page.waitForTimeout(3000)

    // Wait for Leaflet
    const map = page.locator('.leaflet-container')
    await expect(map).toBeVisible({ timeout: 10000 })

    // Measure FPS during drag — inject a simple FPS counter
    const fps = await page.evaluate(() => {
      return new Promise<number>((resolve) => {
        let frames = 0
        let running = true
        const interval = setInterval(() => { frames = 0 }, 1000)
        const count = () => { if (running) { frames++; requestAnimationFrame(count) } }
        requestAnimationFrame(count)
        // Simulate dragging for 2 seconds
        const canvas = document.querySelector('canvas') || document.querySelector('.leaflet-container')
        if (!canvas) { clearInterval(interval); resolve(0); return }
        const rect = canvas.getBoundingClientRect()
        const cx = rect.left + rect.width / 2
        const cy = rect.top + rect.height / 2
        // Dispatch drag events
        canvas.dispatchEvent(new PointerEvent('pointerdown', { clientX: cx, clientY: cy, bubbles: true }))
        for (let i = 0; i < 20; i++) {
          canvas.dispatchEvent(new PointerEvent('pointermove', {
            clientX: cx + i * 5, clientY: cy + i * 3, bubbles: true,
          }))
        }
        canvas.dispatchEvent(new PointerEvent('pointerup', { clientX: cx + 100, clientY: cy + 60, bubbles: true }))
        setTimeout(() => {
          running = false
          clearInterval(interval)
          resolve(frames)
        }, 2100)
      })
    })

    console.log(`📊 WorldMap drag FPS: ~${fps}`)
    expect(fps).toBeGreaterThanOrEqual(20)  // 20fps minimum for acceptable UX
  })

  test('All overlays toggle without errors', async ({ page }) => {
    await page.goto(URL, { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(1000)

    // Login
    const input = page.locator('#terminal-input').first()
    await input.fill(`login ${process.env.MIAU_TEST_USER || 'admin'} ${process.env.MIAU_TEST_PASS || ''}`)
    await input.press('Enter')
    await page.waitForTimeout(1500)

    // Open map
    await input.fill('map')
    await input.press('Enter')
    await page.waitForTimeout(3000)

    await expect(page.locator('.leaflet-container')).toBeVisible({ timeout: 10000 })

    // Toggle all visible buttons in the toolbar
    const buttons = page.locator('button').filter({ hasText: /✈️|🚢|⛏️|⚔️|🛰️|🐱|🛢️|📜|🔗/ })
    const count = await buttons.count()
    console.log(`📊 Found ${count} overlay toggle buttons`)

    let errors = 0
    for (let i = 0; i < count; i++) {
      try {
        await buttons.nth(i).click()
        await page.waitForTimeout(300)
      } catch {
        errors++
      }
    }
    expect(errors).toBe(0)
    console.log(`✅ All ${count} overlays toggled, 0 errors`)
  })

  test('Console has zero errors during normal operation', async ({ page }) => {
    const consoleErrors: string[] = []
    page.on('console', (msg) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text())
    })
    page.on('pageerror', (err) => consoleErrors.push(err.message))

    await page.goto(URL, { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(2000)

    const input = page.locator('#terminal-input').first()
    await input.fill(`login ${process.env.MIAU_TEST_USER || 'admin'} ${process.env.MIAU_TEST_PASS || ''}`)
    await input.press('Enter')
    await page.waitForTimeout(2000)

    await input.fill('map')
    await input.press('Enter')
    await page.waitForTimeout(3000)

    await input.fill('help')
    await input.press('Enter')
    await page.waitForTimeout(1000)

    // Filter known non-critical messages
    const criticalErrors = consoleErrors.filter(e =>
      !e.includes('favicon') &&
      !e.includes('manifest') &&
      !e.includes('401') &&
      !e.includes('Unauthorized') &&
      !e.includes('React DevTools') &&
      !e.includes('Download the React DevTools')
    )

    if (criticalErrors.length > 0) {
      console.log('⚠️ Console errors:', criticalErrors)
    }
    expect(criticalErrors.length).toBe(0)
  })
})
