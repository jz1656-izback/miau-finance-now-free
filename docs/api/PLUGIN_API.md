# Miau Finance — Plugin API Guide

> Extend Miau Finance with custom plugins.
> Plugins run in a sandboxed environment with scoped API permissions.
> Build once. Share with the community. Earn tuna.

---

## Plugin Architecture

```
Plugin
├── plugin.yaml         # Metadata + permissions
├── __init__.py         # Entry point with hook handlers
├── requirements.txt    # Python dependencies (optional)
└── README.md           # User-facing documentation
```

## Quick Start: Hello World Plugin

```bash
mkdir my-plugin && cd my-plugin
```

### `plugin.yaml`
```yaml
name: my-plugin
version: 1.0.0
author: "Your Name"
description: "Does something useful (probably involving cats)"
hooks:
  - on_market_data
  - on_order
permissions:
  - market:read
```

### `__init__.py`
```python
from miau.plugin import PluginBase, hook

class MyPlugin(PluginBase):
    @hook("on_market_data")
    def augment_market_data(self, ticker: str, data: dict) -> dict:
        data["miau_rating"] = "🐱" if float(data.get("price", 0)) > 100 else "😿"
        return data

    @hook("on_order")
    def validate_order(self, order: dict) -> dict:
        if order["quantity"] > 1000:
            order["warning"] = "That's a lot of shares. The cat is watching."
        return order
```

### `requirements.txt`
```
miau-sdk>=1.0
```

## Install the Plugin

```bash
# From a local directory
plugin install ./my-plugin

# From the marketplace
plugin install my-plugin

# Verify it's active
plugin list
```

## Hook Points

| Hook | Purpose | Input | Output |
|------|---------|-------|--------|
| `on_market_data` | Augment market data before display | `(ticker, data)` | `data` (dict) |
| `on_order` | Validate/modify orders | `(order)` | `order` (dict) |
| `on_alert` | Custom alert handling | `(alert)` | `alert` (dict) |
| `on_analysis` | Augment AI analysis results | `(analysis)` | `analysis` (dict) |
| `on_trade_fill` | React to filled trades | `(trade)` | None |
| `on_portfolio_change` | React to portfolio updates | `(portfolio)` | None |

Each hook receives the relevant data and can return:
- **Modified data** — Augment the response (e.g., add custom fields)
- **Same data** — Pass through unchanged
- **Raise `PluginBlocked`** — Block the action and show reason

## Permissions

Plugins declare required permissions in `plugin.yaml`:

| Permission | Access |
|------------|--------|
| `market:read` | Read market data |
| `market:write` | Place orders via hooks |
| `portfolio:read` | Read portfolio data |
| `portfolio:write` | Modify portfolios |
| `analytics:read` | Read analytics data |
| `social:read` | Read social feed |
| `network:tcp` | Make outbound TCP connections |
| `network:http` | Make HTTP requests |

Permissions are shown to users during install:

```
Installing plugin "my-plugin"...
This plugin requests:
  ✓ market:read  — Read market data
  ✓ network:http — Make HTTP requests to external APIs

Allow these permissions? [y/N] y
Installed.
```

## Sandbox

Plugins run in a sandboxed environment:

| Constraint | Limit |
|------------|-------|
| Execution time | 5 seconds per hook |
| Memory | 50 MB |
| CPU | 25% of 1 core |
| API calls | 10 per hook execution |
| File system | Read-only `/tmp/plugin/` |
| Network | Whitelist only (declared in permissions) |

## Example: Custom Alert Handler

```python
from miau.plugin import PluginBase, hook
import requests

class AlertHandlerPlugin(PluginBase):
    @hook("on_alert")
    def send_webhook(self, alert: dict) -> dict:
        if alert["severity"] == "critical":
            requests.post(
                "https://hooks.slack.com/services/YOUR/WEBHOOK",
                json={"text": f"🔴 {alert['title']}: {alert['message']}"},
            )
        return alert
```

## Example: Custom Strategy Plugin

```python
from miau.plugin import PluginBase, hook

class MeanReversionStrategy(PluginBase):
    @hook("on_analysis")
    def generate_signal(self, analysis: dict) -> dict:
        price = analysis.get("current_price", 0)
        sma = analysis.get("sma_20", 0)
        if sma > 0 and price < sma * 0.95:
            analysis["signal"] = "BUY"
            analysis["confidence"] = 0.7
            analysis["reason"] = f"Price ${price} is 5% below SMA-20 (${sma:.2f})"
        return analysis
```

## Testing Plugins

```bash
# Run plugin in isolation
plugin test ./my-plugin --hook on_market_data --input '{"ticker":"AAPL"}'

# Debug plugin output
plugin debug ./my-plugin --hook on_order

# Check plugin logs
plugin logs my-plugin
```

## Publishing to the Marketplace

1. Create your plugin directory with `plugin.yaml`, `__init__.py`, `README.md`
2. Test locally with `plugin test ./my-plugin`
3. Submit via the [Plugin Marketplace](https://miau.finance/plugins/submit)

### Marketplace Guidelines

- Plungins must have a `plugin.yaml` with valid schema
- Unused permissions will be rejected during review
- Plugins that break the platform will be removed 🐱✂️
- The cat judges your code quality. The cat is a harsh critic.

---

## Plugin API Reference

| Method | Description |
|--------|-------------|
| `plugin install <path or name>` | Install a plugin |
| `plugin list` | List installed plugins |
| `plugin remove <name>` | Remove a plugin |
| `plugin info <name>` | Show plugin details |
| `plugin enable <name>` | Enable an installed plugin |
| `plugin disable <name>` | Disable without removing |
| `plugin test <path> --hook <h>` | Test a hook |
| `plugin logs <name>` | Show plugin logs |

---

*The cat watched you write this plugin. The cat approves.*
*If the cat did not approve, the cat would have walked across your keyboard.*
