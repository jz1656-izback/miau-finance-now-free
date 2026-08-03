# 🐱 MIAU FINANCE — Architecture Decision Records (ADR)

## ADR-001: Terminal-First UI

**Status:** Accepted
**Context:** Users need fast access to financial data without loading heavy web UIs.
**Decision:** Built a terminal-style interface with CRT effects. All data accessible via text commands.
**Consequences:** Learning curve for new users, but extremely fast for power users.

## ADR-002: Single Command File (commands.ts)

**Status:** Accepted
**Context:** 160+ commands needed a dispatch mechanism.
**Decision:** Single 5800-line switch statement file.
**Consequences:** Simple, no routing overhead. File is large but maintainable.

## ADR-003: DataSource Provider Pattern

**Status:** Accepted
**Context:** 50+ external APIs with different auth, rate limits, and response formats.
**Decision:** Abstract DataSource base class with registry auto-discovery.
**Consequences:** Adding a new provider = 1 file + 1 registration line. Fallback chains automatic.

## ADR-004: 3-Tier Revenue Model

**Status:** Accepted
**Context:** Needed to split revenue fairly between ops, hooman, and cat ecosystem.
**Decision:** 10% ops / 80% hooman / 10% cat ecosystem. Cat takes rounding remainder.
**Consequences:** Simple, transparent, cat-friendly. Cat always wins.

## ADR-005: Multi-Jurisdiction Payment Routing

**Status:** Accepted
**Context:** Tax authorities can freeze accounts. Cats need SEK-proof infrastructure.
**Decision:** Payment router with 10 jurisdictions. Cat Bank with 5 blockchains.
**Consequences:** Technically legal tax optimization. SEK can't freeze all accounts simultaneously.

## ADR-006: No React Router

**Status:** Accepted
**Context:** Terminal app doesn't need traditional routing.
**Decision:** State-based rendering. URL path checked on mount for redirects.
**Consequences:** Simpler code, but direct URL linking limited.

## ADR-007: Docker Compose for Dev

**Status:** Accepted
**Context:** Need reproducible development environment.
**Decision:** Docker Compose with 4 services (postgres, redis, backend, frontend).
**Consequences:** ~200 MB RAM. Same environment everywhere.

## ADR-008: Cat Currency = Tuna

**Status:** Accepted
**Context:** Needed a unit of account for gamification.
**Decision:** Tuna (🐟) is the universal currency. 1 tuna = 1 task completed.
**Consequences:** Infinite tuna glitch discovered. Not patched. Tuna is forever.

## ADR-009: SEK-Proof Architecture

**Status:** Accepted
**Context:** Tax authorities may attempt to seize assets.
**Decision:** Multi-jurisdiction routing, crypto treasury, no single point of failure.
**Consequences:** 0.03€ overpayment found by SEK. Cat moved remaining €99.97. SEK cries.

> *"The cat makes decisions. The cat documents decisions. The cat is never wrong." 🐱*
