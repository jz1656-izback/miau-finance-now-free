# 🚒 Miau Fire Brigade — Service Desk

The Miau Fire Brigade is a help desk and support ticketing system
where users report issues ("fires"), track their tickets, and get rescued by cat firefighters.

## Features

- **Ticket Board** — Kanban-style columns: To The Rescue (open) → On It! (progress) → Extinguished (resolved)
- **Submit Ticket** — Report a fire, bug, feature request, or question
- **Affected Service** — Specify which Miau app has the problem
- **Cat Firefighters** — 5 support cats with bios and personalities
- **Drag & Drop** — Move tickets between columns to update status
- **Poke the Cat** — 👆 Poke a ticket to get attention
- **Emoji Reactions** — 🐟 😹 🙀 🔥 react to tickets
- **FAQ / Knowledge Base** — Searchable common questions
- **System Status** — Live ping of all Miau services
- **Cat Sounds** — Meow, purr, and alarm effects (toggleable)
- **Cat Companion** — A cat follows your cursor 🐱
- **Tuna Button** — Random tuna facts
- **Offline Mode** — Works with localStorage when backend is down

## Quick Start

```bash
# Start the frontend:
python3 -m http.server 5180 --directory apps/service-desk/

# Open: http://localhost:5180
```

## Features

- **Ticket Board** — Kanban-style columns: To The Rescue (open) → On It! (progress) → Extinguished (resolved)
- **Submit Ticket** — Report a fire, bug, feature request, or question
- **Affected Service** — Specify which Miau app has the problem
- **Cat Firefighters** — 5 support cats with bios and personalities
- **Drag & Drop** — Move tickets between columns to update status
- **Poke the Cat** — 👆 Poke a ticket to get attention
- **Emoji Reactions** — 🐟 😹 🙀 🔥 react to tickets
- **FAQ / Knowledge Base** — Searchable common questions
- **System Status** — Live ping of all Miau services
- **Cat Sounds** — Meow, purr, alarm, hiss, yawn effects (toggleable with 🔊/🔇)
- **Cat Companion** — A cat follows your cursor 🐱
- **Tuna Button** — Random tuna facts
- **Emergency Siren** — Page flashes red + alarm when a critical fire ticket is submitted
- **Cat Avatar** — Every ticket gets a deterministic cat emoji based on its ID
- **Cat of the Day** — Random firefighter cat shown in the footer, changes daily
- **Idle Yawn** — Cat yawns after 2 minutes of inactivity
- **Offline Mode** — Works with localStorage when backend is down

## Terminal Integration

You can interact with the Service Desk directly from the terminal (port 5173):

```
login pawdmin miau2026         # Login first
ticket list                     # View all tickets
ticket create --fire "API down" # Report a fire
ticket create --bug "Cat emoji broken"  # Report a bug
ticket poke <id>                # Poke a ticket
```

## How to Use

1. **Report a fire** — Click "New Ticket" or "🚨 Report an Emergency"
2. **Select category** — Fire (urgent), Bug, Feature, Question
3. **Pick affected service** — Which Miau app is burning?
4. **Submit** — A cat firefighter is dispatched with animation
5. **Track** — Watch your ticket move through the board
6. **Interact** — Poke the cat, react with emojis, drag between columns

## API (Backend)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/v1/service-desk/tickets` | List tickets (filters: `?status=`, `?category=`) |
| `POST` | `/api/v1/service-desk/tickets` | Create ticket |
| `GET` | `/api/v1/service-desk/tickets/{id}` | Get single ticket |
| `PATCH` | `/api/v1/service-desk/tickets/{id}` | Update status |
| `POST` | `/api/v1/service-desk/tickets/{id}/poke` | Poke the cat 👆 |
| `DELETE` | `/api/v1/service-desk/tickets/{id}` | Delete ticket |

## Cat Firefighters

| Name | Role | Emoji |
|------|------|-------|
| Captain Ember | Fire Chief / Emergency Response | 👨‍🚒 |
| Lieutenant Spark | First Responder / Urgent Tickets | 🚒 |
| Firefighter Whiskers | Tech Support / Bug Fixes | 🐱 |
| Cadet Puddles | Junior Support / Ticket Triage | 🐈 |
| Dispatcher Meow | Ticket Routing / Coordination | ☎️ |

## Offline Mode

If the backend is unreachable, the Service Desk automatically switches to localStorage mode.
Sample tickets are loaded and all features work with local storage persistence.
An orange "Offline Mode" badge appears in the corner.
