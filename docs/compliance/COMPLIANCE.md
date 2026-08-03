# 🐱 MIAU FINANCE — Compliance & Legal

## Regulatory Status

Miau Finance is a **financial analytics platform**, not a regulated financial institution. We provide data, analysis, and tools. We do not provide financial advice, execute trades on your behalf without instruction, or hold customer funds.

| Area | Status | Notes |
|------|--------|-------|
| BaFin (German Regulator) | Not required | No banking, no FFA, no investment advice |
| MiFID II | Not applicable | Terminal is a data tool, not a trading venue |
| GDPR | ✅ Compliant | Data processed in EU, no unnecessary collection |
| PSD2 | Not applicable | We don't process payments directly (Stripe does) |
| AML/KYC | Partial | Required for Stripe, not required for terminal access |
| AI Act (EU) | Low risk | AI provides analysis, not automated decisions |
| SFDR | Data only | ESG data provided for user's own reporting |

## GDPR Compliance

```
Data collected:
  - Email address (for Stripe billing)
  - Portfolio holdings (stored locally in DB)
  - Usage analytics (anonymized)

Data NOT collected:
  - Real names (optional)
  - Bank details (Stripe handles this)
  - Government IDs
  - Biometric data

Data storage:
  - PostgreSQL (self-hosted in EU)
  - Redis cache (ephemeral)
  - No third-party data sharing

User rights:
  - Download your data: /api/v1/users/export
  - Delete your account: /api/v1/users/delete
  - Object to processing: email ziebartjevgeni@googlemail.com
```

## Legal Disclaimers

> **Not Financial Advice.** The cat is not a licensed financial advisor. Miau Finance provides tools for analysis, not recommendations. Always consult a qualified professional.

> **No Guarantee.** Tuna prices may fluctuate. The cat is not responsible for trading losses. The cat is especially not responsible for losses caused by ignoring the cat's advice.

> **Tax Compliance.** The user is responsible for their own tax reporting. Miau Finance's jurisdiction routing is a technical feature, not tax advice. Consult a tax professional.

> **Open Source Disclaimer.** While the source code is visible on GitHub, Miau Finance is proprietary (All Rights Reserved). No license is granted for commercial use without explicit agreement.

## Contact for Legal Matters

```
Jevgeni Ziebart
ziebartjevgeni@googlemail.com
Zypressenweg 21, 53340 Meckenheim, Germany
```

> *"The cat has layers of compliance. Like onions. Or lasagna." 🐱*
