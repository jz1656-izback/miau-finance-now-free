# 🐱 MIAU FINANCE — Quant Engine Reference

## Mathematical Foundations

### 1. Technical Indicators

**SMA** (Simple Moving Average)
```
SMA(n) = (1/n) × Σ(P_i) for i = 1 to n
```

**EMA** (Exponential Moving Average)
```
EMA(n) = P_t × (2/(n+1)) + EMA_(t-1) × (1 - 2/(n+1))
```

**MACD**
```
MACD = EMA(12) - EMA(26)
Signal = EMA(9) of MACD
Histogram = MACD - Signal
```

**RSI** (Relative Strength Index)
```
RSI = 100 - 100/(1 + RS)
RS = AverageGain(14) / AverageLoss(14)
```

**Bollinger Bands**
```
Middle = SMA(20)
Upper = SMA(20) + 2 × σ(20)
Lower = SMA(20) - 2 × σ(20)
```

### 2. Econometrics

**OLS Regression**
```
Y = β0 + β1X + ε
β1 = Cov(X,Y) / Var(X)
```

**Granger Causality**
F-test on restricted vs unrestricted VAR models. Null hypothesis: X does not Granger-cause Y.

**Cointegration (Engle-Granger)**
1. Regress Y on X: Y = α + βX + ε
2. Test ε for unit root (ADF test)
3. If ε is stationary, Y and X are cointegrated

**CAPM**
```
E(Ri) = Rf + βi × (E(Rm) - Rf)
βi = Cov(Ri, Rm) / Var(Rm)
Sharpe = (E(Ri) - Rf) / σi
Treynor = (E(Ri) - Rf) / βi
```

### 3. Risk Metrics

**Value at Risk (Historical)**
```
VaR(95%) = Percentile(returns, 5%)
```

**CVaR**
```
CVaR = Mean of returns below VaR threshold
```

**Maximum Drawdown**
```
MDD = (Trough Value - Peak Value) / Peak Value
```

**Calmar Ratio**
```
Calmar = Annual Return / |Maximum Drawdown|
```

### 4. Portfolio Optimization

**Markowitz Mean-Variance**
```
Minimize: σ²(p) = w'Σw
Subject to: w'μ = μ_target, w'1 = 1
```

### 5. Reinforcement Learning (RL Trader)

The RL agent uses a simple scoring system based on momentum, mean reversion, and trend signals. It is implemented as a PPO-based agent in `rl_trading_agent.py`.

```
Score = MomentumSignal + RSISignal + MACDSignal
Decision:
  Score >= 2  → BUY
  Score <= -2 → SELL
  Otherwise   → HOLD
```

> *"The math is sound. The cat is confident. The trades are profitable." 🐱*
