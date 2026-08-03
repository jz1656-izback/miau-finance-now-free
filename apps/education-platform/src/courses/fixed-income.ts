import type { Course } from '../lib/types'

export const fixedIncome: Course = {
  id: 'fixed-income',
  slug: 'fixed-income',
  title: 'Fixed Income & Bonds',
  description: 'Bond pricing, duration, convexity, and yield curves — the cat collects coupons.',
  category: 'Fixed Income',
  difficulty: 'intermediate',
  icon: '📜',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'fi-bonds',
      slug: 'bond-basics',
      title: 'Bond Basics',
      description: 'Understand what bonds are and how they work.',
      commands: ['bonds', 'bonds list'],
      steps: [
        { instruction: 'List available bonds: `bonds list`', command: 'bonds list', expectedOutput: 'Table of bonds with issuer, coupon, maturity, and yield' },
        { instruction: 'A bond is a loan — you lend money to the issuer in exchange for periodic interest payments.' },
        { instruction: 'Key terms: face value (par), coupon rate, maturity date, and yield to maturity.' },
      ],
      quiz: [
        { question: 'What is a bond\'s coupon rate?', options: ['The interest rate the bond pays', 'The bond\'s market price', 'The bond\'s credit rating', 'The bond\'s maturity date'], correctIndex: 0, explanation: 'The coupon rate is the annual interest rate the bond issuer pays to bondholders.' },
      ],
    },
    {
      id: 'fi-pricing',
      slug: 'bond-pricing',
      title: 'Bond Pricing',
      description: 'Learn how bonds are priced in the market.',
      commands: ['bond', 'bond price'],
      steps: [
        { instruction: 'Price a bond: `bond price --face 1000 --coupon 5 --yield 4 --years 10`', command: 'bond price --face 1000 --coupon 5 --yield 4 --years 10', expectedOutput: 'Bond price of $1,081.11 (trading at a premium)' },
        { instruction: 'Bonds trade at a premium when coupon rate > market yield, and at a discount when coupon < yield.' },
        { instruction: 'Bond prices and yields move inversely — when yields go up, prices go down.' },
      ],
      quiz: [
        { question: 'What happens to bond prices when market yields rise?', options: ['Bond prices fall', 'Bond prices rise', 'Bond prices stay the same', 'Bond prices double'], correctIndex: 0, explanation: 'Bond prices and yields have an inverse relationship — when yields rise, existing bond prices fall.' },
      ],
    },
    {
      id: 'fi-duration',
      slug: 'duration-convexity',
      title: 'Duration & Convexity',
      description: 'Measure bond price sensitivity to interest rate changes.',
      commands: ['duration', 'duration calc'],
      steps: [
        { instruction: 'Calculate duration: `duration calc --coupon 5 --yield 4 --years 10`', command: 'duration calc --coupon 5 --yield 4 --years 10', expectedOutput: 'Macaulay duration of 8.2 years, modified duration of 7.9' },
        { instruction: 'Duration measures how much a bond\'s price changes per 1% change in yield.' },
        { instruction: 'Convexity accounts for the fact that duration changes as yields change — more accurate for large moves.' },
      ],
      quiz: [
        { question: 'If a bond has a modified duration of 5, what happens when yields rise by 1%?', options: ['Price falls by ~5%', 'Price rises by ~5%', 'Price falls by ~1%', 'Price stays the same'], correctIndex: 0, explanation: 'Modified duration of 5 means the bond price changes by approximately 5% for each 1% change in yield.' },
      ],
    },
    {
      id: 'fi-yield-curve',
      slug: 'yield-curves',
      title: 'Yield Curves',
      description: 'Interpret the bond market\'s economic outlook.',
      commands: ['yield', 'yield curve'],
      steps: [
        { instruction: 'View the yield curve: `yield curve`', command: 'yield curve', expectedOutput: 'Current yield curve plot with historical comparison' },
        { instruction: 'A normal (upward-sloping) yield curve means long-term rates are higher than short-term.' },
        { instruction: 'An inverted yield curve (short-term > long-term) often predicts a recession.' },
      ],
      quiz: [
        { question: 'What does an inverted yield curve typically predict?', options: ['A recession', 'Economic expansion', 'Low inflation', 'Stock market boom'], correctIndex: 0, explanation: 'An inverted yield curve has been a reliable predictor of recessions, as short-term rates exceed long-term rates.' },
      ],
    },
  ],
}
