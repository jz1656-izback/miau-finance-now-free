# 🐱 MIAU FINANCE — Broker Integration Guide

## Supported Brokers

| Broker | Paper Trading | Live Trading | Status |
|--------|--------------|--------------|--------|
| Alpaca | ✅ | ✅ | Full integration |
| Interactive Brokers | ❌ | ✅ | Via IB Gateway |
| DEGIRO | ❌ | ✅ | Read-only (regulatory) |
| Saxo Bank | ❌ | ✅ | Read-only |
| Rakuten Securities | ❌ | ✅ | Japan market |
| Zerodha | ❌ | ✅ | India market |

## Alpaca Setup (Recommended)

```bash
# 1. Sign up at https://alpaca.markets
# 2. Get API keys
# 3. Add to .env:
ALPACA_API_KEY=pk_...
ALPACA_SECRET_KEY=sk_...
ALPACA_PAPER=true  # true for paper trading
```

## Terminal Commands

```bash
broker list                  # List connected brokers
broker balance               # Check account balance
broker positions             # View open positions
broker submit <ticker> <qty> # Submit market order
broker connect <name>        # Connect a new broker
```

## Order Types

| Type | Supported | Description |
|------|-----------|-------------|
| Market | ✅ | Execute immediately at market price |
| Limit | ✅ | Execute at specified price or better |
| Stop | ✅ | Become market order when price hit |
| Stop-Limit | ✅ | Become limit order when price hit |
| Trailing Stop | ✅ | Dynamic stop that follows price |

## Risk Controls

- Maximum position size: 20% of portfolio
- Maximum leverage: 3x for stocks, 1x for crypto
- Daily loss limit: 10% (auto-stop)
- Cat override: VETO command can cancel any order

> *"The cat trades through Alpaca. The cat's trades always land on their feet." 🐱*
