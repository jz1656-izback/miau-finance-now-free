# 🚒 Miau Fire Brigade — Service Desk

The Miau Fire Brigade is the help desk and ticketing system for the Miau ecosystem.
Users report issues ("fires"), get assigned to cat firefighters, and track resolution.

## Terminal Commands

The `ticket` command works from the Terminal UI (port 5173):

| Command | Description |
|---------|-------------|
| `ticket list` | Show all your tickets |
| `ticket create --fire "..."` | Report a fire/emergency |
| `ticket create --bug "..."` | Report a bug |
| `ticket create --feature "..."` | Request a feature |
| `ticket poke <id>` | Poke a ticket to get attention |

Requires login (`login pawdmin miau2026`) before use.

## Emergency Siren

When a critical/fire ticket is submitted, the page flashes red and plays an alarm sound.
The cat companion bounces frantically for 3 seconds.

## Cat Avatar

Every ticket gets a deterministic cat emoji generated from its UUID.
The same ticket always shows the same cat — your ticket has its own face.

## Grafana Dashboard

A pre-built Grafana dashboard (`infra/grafana/dashboards/miau-fire-brigade.json`) tracks:
- Open vs resolved tickets over time
- Tickets by category (pie chart)
- Firefighter workload (bar gauge)
- Average response time in purrs
- Total pokes

## Sounds

| Sound | Trigger |
|-------|---------|
| Meow | Ticket submit, poke, reaction |
| Purr | Ticket resolved, tuna button |
| Alarm | Emergency siren (critical fire) |
| Hiss | Ticket deleted |
| Yawn | 2 minutes of inactivity |
