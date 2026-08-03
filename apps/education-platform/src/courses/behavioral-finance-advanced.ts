import type { Course } from '../lib/types'

export const behavioralFinanceAdvanced: Course = {
  id: 'behavioral-finance-advanced',
  slug: 'behavioral-finance-advanced',
  title: 'Behavioral Finance — Advanced',
  description: 'Neurofinance, decision science, institutional biases, and debiasing strategies — the cat analyzes your brain.',
  category: 'Psychology',
  difficulty: 'advanced',
  icon: '🧠',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'neurofinance',
      slug: 'neurofinance-brain',
      title: 'Neurofinance: The Brain on Markets',
      description: 'How brain structure affects financial decisions.',
      commands: ['neurofinance', 'neurofinance --scan'],
      steps: [
        { instruction: 'Run a neurofinance analysis of a trading decision: `neurofinance --scan --decision "buy TSLA at ATH"`', command: 'neurofinance --scan --decision "buy TSLA at ATH"', expectedOutput: 'Brain scan analysis: Amygdala activation: HIGH (fear of missing out). Nucleus accumbens: HIGH (reward anticipation). Prefrontal cortex: LOW (rational analysis). Risk rating: FOOM (Fear Of Missing Out)' },
        { instruction: 'The amygdala processes fear, the nucleus accumbens processes reward — trading activates both.' },
        { instruction: 'The cat\'s brain scan shows a highly developed "tuna cortex" that activates during market hours.' },
        { instruction: 'Test your own biases: `neurofinance --test --bias "confirmation"`', command: 'neurofinance --test --bias "confirmation"', expectedOutput: 'Confirmation bias test: You were shown 10 data points. You focused on 8 that confirmed your existing view. Missed 2 contradictory signals. Score: Strong confirmation bias. Recommendation: Seek disconfirming evidence' },
      ],
      quiz: [
        { question: 'What part of the brain is most associated with fear-based trading decisions?', options: ['The amygdala — it processes fear and triggers fight-or-flight responses during market volatility', 'The hippocampus — it stores long-term memories', 'The cerebellum — it controls motor function', 'The brainstem — it regulates basic life functions'], correctIndex: 0, explanation: 'The amygdala is the brain fear center. During market crashes or high volatility, amygdala activation can trigger panic selling or irrational risk aversion, overriding rational prefrontal cortex analysis.' },
      ],
    },
    {
      id: 'institutional-biases',
      slug: 'institutional-behavioral-biases',
      title: 'Institutional & Professional Biases',
      description: 'How even professional investors fall prey to biases.',
      commands: ['bias institutional', 'bias institutional --analysis'],
      steps: [
        { instruction: 'Analyze institutional bias patterns: `bias institutional --analysis --fund "Large Cap Growth Fund" --period 5yr`', command: 'bias institutional --analysis --fund "Large Cap Growth Fund" --period 5yr', expectedOutput: 'Institutional bias analysis: Herding bias (80% correlation with peer funds), Home bias (92% US equities), Window dressing (Dec: sold losers, bought winners), Status quo bias (portfolio turnover 15% vs benchmark 30%)' },
        { instruction: 'Institutional biases: herding (following peers), home bias (overweighting domestic), window dressing (cosmetic portfolio changes).' },
        { instruction: 'The cat\'s fund has a "cat bias" — it overweights cat-related equities.' },
        { instruction: 'Check herding behavior in a sector: `bias institutional --herding --sector tech --period q3`', command: 'bias institutional --herding --sector tech --period q3', expectedOutput: 'Tech sector herding Q3: 12 of 15 top funds increased AI exposure simultaneously. Crowded trade alert. Historical similar crowding preceded 80% corrections in 70% of cases' },
      ],
      quiz: [
        { question: 'What is "window dressing" in institutional investing?', options: ['Selling poorly performing stocks and buying recent winners before quarter-end reporting to make the portfolio look better', 'Cleaning up office windows during earnings season', 'Presenting portfolio returns in a visually appealing format', 'Redecorating the trading floor'], correctIndex: 0, explanation: 'Window dressing is when fund managers sell losing positions and buy recent winners before reporting periods to present a portfolio that appears more strategically sound than their actual process.' },
      ],
    },
    {
      id: 'decision-science',
      slug: 'decision-science-trading',
      title: 'Decision Science & Trading Psychology',
      description: 'Systematic frameworks for better financial decisions.',
      commands: ['decisionscience', 'decisionscience --framework'],
      steps: [
        { instruction: 'Apply a decision framework to a trade: `decisionscience --framework "premortem" --decision "short TSLA before earnings"`', command: 'decisionscience --framework "premortem" --decision "short TSLA before earnings"', expectedOutput: 'Premortem: Assume the trade lost 50%. Reasons? 1) Earnings beat (40%), 2) Elon tweet (30%), 3) Short squeeze (20%), 4) Model error (10%). Mitigation: Tighter stop, smaller position' },
        { instruction: 'Premortem: imagine the decision failed and work backward to identify risks.' },
        { instruction: 'The cat does a premortem before every tuna purchase: "What if the fish market crashes?"' },
        { instruction: 'Run a decision journal entry: `decisionscience --journal --entry "Buy AAPL" --conviction 7 --risk 2%`', command: 'decisionscience --journal --entry "Buy AAPL" --conviction 7 --risk 2%', expectedOutput: 'Journal entry logged: Buy AAPL. Conviction 7/10. Risk 2%. Rationale: Strong earnings, reasonable valuation. Emotional state: Calm. Bias check: Recency (AAPL went up yesterday)' },
      ],
      quiz: [
        { question: 'What is a "premortem" in decision science?', options: ['Imagining a future failure and working backward to identify what could go wrong — a proactive risk identification tool', 'An analysis conducted after a failure to understand what happened', 'A medical examination before surgery', 'A trading strategy based on death cross patterns'], correctIndex: 0, explanation: 'A premortem is a proactive decision tool where you imagine your decision has failed spectacularly and work backward to identify possible causes, helping surface risks you might otherwise overlook.' },
      ],
    },
    {
      id: 'debiasing',
      slug: 'debiasing-strategies',
      title: 'Debiasing Strategies & Systems',
      description: 'Practical techniques to reduce bias in trading.',
      commands: ['debias', 'debias --checklist'],
      steps: [
        { instruction: 'Generate a pre-trade debiasing checklist: `debias --checklist --type "earnings trade"`', command: 'debias --checklist --type "earnings trade"', expectedOutput: 'Earnings trade checklist: [ ] Checked opposite view? [ ] Reviewed base rates? [ ] Set exit before entry? [ ] Position size calibrated to max loss? [ ] Peer consensus noted but discounted?' },
        { instruction: 'Debiasing techniques: slow down, use checklists, seek contrary evidence, track decisions in a journal.' },
        { instruction: 'The cat has a debiasing checklist for every trade. It is taped to the cat tree.' },
        { instruction: 'Run a post-trade debrief: `debias --debrief --trade-id "AAPL-2025-11-15"`', command: 'debias --debrief --trade-id "AAPL-2025-11-15"', expectedOutput: 'Trade debrief: AAPL buy 11/15. Outcome: +5%. Biases detected: Confirmation bias (ignored bearish signals), Overconfidence (too large position). Improvement: Use pre-mortem before entry. Score: 6/10' },
      ],
      quiz: [
        { question: 'What is the most effective single debiasing technique for traders?', options: ['Maintaining a decision journal and conducting structured pre-trade reviews with explicit contrary evidence seeking', 'Meditation', 'Following your gut feeling', 'Copying successful traders'], correctIndex: 0, explanation: 'Research shows that structured pre-trade reviews combined with decision journals significantly reduce behavioral biases. Forcing yourself to articulate why you might be wrong (seeking contrary evidence) is particularly effective.' },
      ],
    },
  ],
}
