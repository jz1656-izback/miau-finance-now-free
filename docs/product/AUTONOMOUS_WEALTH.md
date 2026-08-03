# 🐱 MIAU FINANCE — Autonomous Wealth Engine Technical Reference

## Overview

The Autonomous Wealth Engine (`wealth_engine.py`) is a scheduled orchestrator that automatically allocates revenue across three tiers and invests the Cat Ecosystem Fund. It runs weekly (every Sunday 00:00) via the scheduler.

## Architecture

```
Revenue (record_revenue)
    │
    ▼
Wealth Allocation Cycle (run_allocation_cycle)
    │
    ├── 1. Calculate 3-tier split (10/80/10)
    ├── 2. Record allocation in wealth_transactions table
    ├── 3. Mark hooman payout as ready
    └── 4. Auto-invest Cat Ecosystem Fund
        │
        ├── auto_buy_stocks() → Alpaca Broker
        ├── auto_buy_crypto() → DEX/CEX
        ├── buy_cloud_credits() → AWS/GCP
        └── Cat infrastructure fund
```

## Allocation Rules

| Asset Class | Target % | Execution | Minimum |
|-------------|----------|-----------|---------|
| Stocks (SPY/QQQ) | 40% | Alpaca market orders | €1 per symbol |
| Crypto (ETH/BTC) | 30% | Via exchange | €1 |
| Cloud Credits | 20% | Reserved for AWS/GCP | €10 |
| Cat Infrastructure | 10% | Miau servers/apps | €5 |

## Auto-Investor Logic

The `auto_investor.py` uses a buy-list approach:

```python
DEFAULT_BUY_LIST = [
    {"symbol": "SPY", "target": 0.35},   # S&P 500 ETF
    {"symbol": "QQQ", "target": 0.25},   # Nasdaq 100 ETF
    {"symbol": "VTI", "target": 0.15},   # Total Stock Market
    {"symbol": "BND", "target": 0.10},   # Total Bond Market
    {"symbol": "GLD", "target": 0.10},   # Gold
    {"symbol": "IAU", "target": 0.05},   # Gold Trust
]
```

## RFQ Engine

The RL Trading Agent (`rl_trading_agent.py`) uses a simple but effective scoring system:

```python
# Momentum signal: SMA20 vs SMA50
# RSI signal: <30 = buy, >70 = sell
# MACD signal: crossover direction
# Score >= 2 → buy, <= -2 → sell, else hold
```

## Tax Optimization

Before investing, the wealth engine checks jurisdiction routing. All Cat Ecosystem funds are routed through Estonia (0% tax on undistributed profits) before investment execution.

## Monitoring

```bash
miauauto status       # Engine status + last run
miauallocate          # Trigger allocation cycle
miauinvest stocks 100 # Manual investment trigger
miauwealth           # Net worth across all classes
```

> *"The autonomous engine runs while the cat sleeps. The cat wakes up richer." 🐱*
