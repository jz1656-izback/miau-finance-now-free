# Miau Finance — AGI Governance Framework

**Phase:** 27 (v2.0.0)  
**Last Updated:** May 2026

---

## 1. Principles

| Principle | Description |
|-----------|-------------|
| **Transparency** | All AGI decisions must be explainable in natural language |
| **Alignment** | AGI goals must match user-defined financial objectives |
| **Safety** | Hard guardrails prevent catastrophic portfolio actions |
| **Oversight** | Human-in-the-loop for decisions above configurable thresholds |
| **Accountability** | Every autonomous action is logged, auditable, and reversible |
| **Privacy** | AGI never shares user data or strategies across instances |

---

## 2. Safety Architecture

### 2.1 Hard Guardrails (Cannot Be Overridden)

| Guardrail | Trigger | Action |
|-----------|---------|--------|
| Maximum position size | >20% of portfolio | Block order |
| Maximum daily loss | >5% portfolio value | Halt all trading |
| Leverage limit | >2x for non-margin accounts | Reject margin orders |
| Short-sale prohibition | Account without margin | Block short |
| Unregistered security | Not in allowed asset list | Block trade |

### 2.2 Soft Guardrails (Configurable)

| Guardrail | Default | Description |
|-----------|---------|-------------|
| Sector concentration | 30% | Max allocation to any sector |
| Single security limit | 10% | Max allocation to one security |
| Daily trade count | 20 | Max trades per day |
| Monthly turnover | 200% | Max portfolio turnover per month |
| Drawdown limit | 15% | Max drawdown before rebalancing |

### 2.3 Kill Switch

The kill switch (`frontend/src/components/agi/KillSwitch.tsx`) provides:

- **Manual stop**: Instant halt of all AGI trading
- **Circuit breaker**: Automatic halt if P&L exceeds thresholds
- **Graceful shutdown**: Complete pending trades, then disable AGI
- **Emergency liquidate**: Sell all positions to cash (configurable)

Accessible via terminal: `agi kill --reason "manual override"`

---

## 3. AGI Autonomy Tiers

| Tier | Level | Description | Human Oversight |
|------|-------|-------------|-----------------|
| 0 | None | AGI disabled | Full manual |
| 1 | Advisory | AGI suggests, human executes | All actions |
| 2 | Semi-autonomous | AGI executes within guardrails | Exception review |
| 3 | Autonomous | Full AGI control | Quarterly review |
| 4 | Singularity | Recursive self-improvement | Kill switch only |

Default tier: **2 (Semi-autonomous)**. Tier can be changed via `agi tier <n>`.

---

## 4. Explainability

All AGI decisions include a natural language explanation:

```
miau@finance:~$ agi explain last-trade
🧠 AGI Decision Explanation
══════════════════════════════════════════════
  Action: BUY 100 shares of AAPL @ $186.90
  Reason: Detected bullish flag pattern on 4h chart
          + positive earnings surprise + RSI oversold

  Confidence: 78%
  Alternatives considered:
    - MSFT (lower confidence - 62%)
    - None (no other signals detected)

  Risk assessment:
    - Stop-loss set at -3% ($181.30)
    - Position size within 5% limit
    - Correlation to existing positions: 0.12
```

## 5. AGI Safety Committee

| Role | Responsibility |
|------|---------------|
| AGI Safety Officer | Hard guardrail violations review |
| Ethics Board | Whitepaper compliance, bias audit |
| User Advocate | Tier override requests |
| Technical Lead | Kill switch testing, incident response |

---

## 6. Incident Response

See [INCIDENT_RESPONSE.md](../INCIDENT_RESPONSE.md) for AGI-specific escalation procedures.

| Severity | AGI Behavior | Action |
|----------|-------------|--------|
| SEV-1 | Unauthorized trade execution | Kill switch → manual review → code freeze |
| SEV-2 | Guardrail bypass attempt | Downgrade tier → log analysis → patch |
| SEV-3 | Unexplained strategy change | Advisory mode → investigation → revert |
| SEV-4 | Suboptimal allocation | Tier review → parameter tuning |

---

## 7. Compliance & Auditing

- All AGI decisions are logged to the audit system with `user_id`, `tier`, `confidence`, and `reason`
- Monthly AGI performance reports compare autonomous vs. benchmark returns
- Quarterly AGI safety audit by security-dev
- Annual third-party AGI ethics review
