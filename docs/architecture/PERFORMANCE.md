# 🐱 MIAU FINANCE — Performance Guide

## RAM Usage
| Service | Light Mode | Full Mode |
|---------|-----------|-----------|
| postgres | 31 MB | 31 MB |
| redis | 23 MB | 23 MB |
| backend | 25 MB | 25 MB |
| frontend | 25 MB | 25 MB |
| grafana | — | 3.93 GB |
| superset | — | 370 MB |
| prometheus | — | 170 MB |
| **Total** | **~104 MB** | **~4.7 GB** |

## Bundle Size (Frontend)
| Chunk | Raw | Gzip |
|-------|-----|------|
| index.js | 1.1 MB | 301 KB |
| charts.js | 537 KB | 156 KB |
| leaflet.js | 150 KB | 44 KB |
| globe.js | 48 KB | 16 KB |
| **Total** | **~1.8 MB** | **~517 KB** |

## Optimizations
- Lazy loading for globe/3D charts
- Code splitting (vendor, charts, globe)
- Redis caching (60-3600s TTL)
- Source maps removed in production
- Service worker for offline caching
- Database connection pooling
- Query timeouts at 30s

## Light Mode (Recommended)
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```
