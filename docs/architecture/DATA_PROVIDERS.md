# 🐱 MIAU FINANCE — Data Providers

## 50+ Sources · One Unified Pattern

### Free (No Key Required)
| Provider | Data | Limit |
|----------|------|-------|
| Yahoo Finance | Stocks, crypto, forex | 30/min |
| FRED | Treasury, GDP, CPI | 120/min |
| CoinGecko | Crypto prices | 50/min |
| DeFiLlama | DeFi TVL, yields | Unlimited |
| Frankfurter | Forex (200+ pairs) | Unlimited |
| OpenSky | Flight tracking | 400/day |
| SecuritiesDB | Fama-French factors | Unlimited |

### API Key Required (Free Tiers Available)
| Provider | Data | Key |
|----------|------|-----|
| Finnhub | Equity, news, fundamentals | ✅ |
| Alpha Vantage | Technicals, forex | ✅ |
| EIA | Energy data | ✅ |
| IMF | Global economics | ✅ |
| BLS | Employment, CPI | ✅ |

### Provider Pattern
```python
from app.services.data.base import DataSource

class MyProvider(DataSource):
    @property
    def name(self) -> str: return "myprovider"
    @property
    def requires_key(self) -> bool: return False
    @property
    def rate_limit_per_minute(self) -> int: return 60
```

### Fallback Chain
```
Yahoo → Finnhub → Alpha Vantage → (error)
```

### Health Dashboard
```
GET /api/v1/datasources
```
