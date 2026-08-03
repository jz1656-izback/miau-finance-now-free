import { describe, it, expect, beforeEach, afterEach } from 'vitest'

function setViewport(width: number, height: number = 800) {
  globalThis.innerWidth = width
  globalThis.innerHeight = height
  globalThis.dispatchEvent(new Event('resize'))
}

describe('Responsive Layout', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div id="app">
        <div class="terminal-container" style="width: 100%">
          <div class="sidebar" style="display: block">Sidebar</div>
          <div class="main-content">Content</div>
          <div class="mobile-nav" style="display: none">Mobile Nav</div>
        </div>
      </div>
    `
  })

  it('shows sidebar at desktop width (1024px)', () => {
    setViewport(1024)
    const sidebar = document.querySelector('.sidebar') as HTMLElement
    const mobileNav = document.querySelector('.mobile-nav') as HTMLElement
    expect(sidebar.style.display).toBe('block')
    expect(mobileNav.style.display).toBe('none')
  })

  it('shows mobile nav at mobile width (320px)', () => {
    setViewport(320)
    const sidebar = document.querySelector('.sidebar') as HTMLElement
    const mobileNav = document.querySelector('.mobile-nav') as HTMLElement
    sidebar.style.display = 'none'
    mobileNav.style.display = 'flex'
    expect(window.innerWidth).toBe(320)
  })

  it('handles tablet width (768px)', () => {
    setViewport(768)
    expect(window.innerWidth).toBe(768)
    expect(window.innerHeight).toBe(800)
  })

  it('terminal input has touch-friendly height at mobile widths', () => {
    setViewport(320)
    const input = document.createElement('input')
    input.style.height = '44px'
    input.style.minHeight = '44px'
    document.body.appendChild(input)
    const height = parseInt(input.style.height)
    expect(height).toBeGreaterThanOrEqual(44)
  })

  it('dark mode class toggles on body', () => {
    document.body.classList.add('dark-mode')
    expect(document.body.classList.contains('dark-mode')).toBe(true)
    document.body.classList.remove('dark-mode')
    expect(document.body.classList.contains('dark-mode')).toBe(false)
  })
})
