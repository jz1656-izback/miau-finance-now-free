# 🐱 Miau CeoScratchSheet — Unified Ecosystem Dashboard

A single-page CEO dashboard showing everything in the Miau ecosystem at a glance.
One screen. All the cats. All the metrics.

## Quick Start

```bash
python3 -m http.server 5182 --directory apps/ceo-dashboard/
# Open: http://localhost:5182
```

## What it shows

| Section | Content |
|---------|---------|
| **Service Status** | Live ping of all 10 Miau apps (green/red indicators) |
| **Recent Tickets** | Latest 8 from Service Desk, with category emoji and status |
| **Cat Corner** | Cat of the day — random power cat with role, quote, tuna stats |
| **Quick Actions** | Links to all Miau apps — one click to any tool |
| **Live Activity** | Simulated activity feed showing ecosystem events |
| **Stats Bar** | Services online, open tickets, active fires, firefighters, tuna reserves |

## Header

- Logo + title with gradient
- Live fire count, active cats on duty, session uptime
- Logged-in user (from Pawdenity) or login link

## Auto-refresh

- Services: checks every 30s
- Tickets: fetches every 30s
- Activity feed: new event every 12s
- Clock: updates every second

## Cat of the Day

Randomly selected from 7 power cats, changes daily (persisted in localStorage).
Includes: Captain Ember, Lieutenant Spark, Firefighter Whiskers, Cadet Puddles,
Dispatcher Meow, Prof. Dr. Tuna, CatGPT.

## Integration

Add this to any app's header to link back:
```html
<a href="http://localhost:5182" style="color:rgba(0,255,136,0.3)">📊 CeoScratchSheet</a>
```
