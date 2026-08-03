# 🐾 V69 "The Great Delittering" — Repo Restructure

```
   ╱|、
  (˚ˎ 。7     "The litterbox was full. 114 markdown files, 9,426 lines of robot barks,
   |、˜〵      "old release notes, duplicate API refs, test artifacts everywhere."
   じしˍ,)ノ    "V69 cleaned it. The cat can breathe again."
```

## What moved

| From root | To | Contents |
|-----------|-----|----------|
| `education-platform/`, `ecosystem-site/`, `marketing-dashboard/` | `services/` | Standalone web apps |
| `cube/`, `superset/` | `services/` | Analytics services |
| `grafana/`, `prometheus/`, `postgres/`, `plugins/` | `services/` | Config & dashboards |
| `V3_BOARD.md`–`V11_BOARD.md`, `V8_VISION.md` | `boards/` | All sprint/vision boards |
| `AGENTS.md`, `AGENT_LOG.md`, `BARK.md`, `CATNIP_VISIONS.md` | `agents/` | Agent coordination files |
| `.opencode/` | `agents/.opencode/` | Agent configs |
| `V1_RELEASE.md`–`V6_MIAUGLOBE.md` | `docs/archive/` | Historical release notes |
| `CAREERS.md` | `docs/` | Creator profile |
| `V3_AGENT_HANDBOOK.md` | `docs/archive/` | Archived agent docs |
| `MIAUPAPERS.md` | `docs/` | 111 cat finance whitepapers |

## What was deleted

| File | Reason |
|------|--------|
| `docs/API_REFERENCE.md` | Described a different API (`/equity/price/`) — superseded by `docs/API.md` |
| `docs/TROUBLESHOOTING_QUICK.md` | Content merged into `docs/TROUBLESHOOTING.md` |
| `frontend/test-results/` | Auto-generated Playwright artifacts (3 failed test screenshots) |

## What was trimmed

| File | Before | After | Removed |
|------|--------|-------|---------|
| `agents/AGENT_LOG.md` | 9,426 lines | 600 lines | 8,836 lines of BARK robot restart logs |

## What was updated

| File | Change |
|------|--------|
| `docker-compose.yml` | All volume mount paths updated from `./dir/` → `./services/dir/` |
| `docker-compose.dev.yml` | Same path updates |
| `docker-compose.prod.yml` | Same path updates |

## Docker service names unchanged

Only volume paths changed. Docker service names (`education-platform`, `ecosystem-site`, `marketing-dashboard`, `postgres`, `grafana`, `prometheus`, etc.) remain the same — they are referenced by name across compose files and health checks.

## Git history preserved

All moves used `git mv` which preserves file history. `git log --follow <file>` works on all relocated files.

## Why

114 markdown files at root + 9,426 lines of auto-generated BARK logs + stale API docs + test artifacts = noise. The repo was hard to navigate. V69 organizes it so the next sprint starts from a clean structure.
