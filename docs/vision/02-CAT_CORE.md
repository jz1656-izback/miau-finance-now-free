```
  ╱|、
 (˚ˎ 。7
  |、˜〵
  じしˍ,)ノ
```

# 🐱 Cat Core — Minimal Architecture

## Dependency Elimination Crusade

The modern software stack is a monument to excess. Node_modules weighs more than a cat. Python environments require 47 packages to print "Hello World." Docker images are 2GB for a simple API server.

Cat Core is a radical rejection of this bloat.

### The 10 Commandments of Cat Core

**1. Thou shalt not npm install**
The Miau Finance backend runs on Python/FastAPI because Python is installed on every server. The frontend is vanilla React with minimal dependencies. Every third-party package must justify its existence in writing to the Cat Council.

**2. Zero runtime dependencies for production**
The ideal MiauOS deployment is a single 5MB static binary. No Python runtime. No Node.js. No JVM. A Go or Rust binary that bundles everything it needs. The Postgres client is compiled in. The HTTP router is compiled in. Even the template renderer is compiled in.

**3. Database is files**
CatDB replaces PostgreSQL for non-relational data. User preferences, session data, and configuration are stored in structured files on disk. No connection pool. No migration scripts. No ORM. Just files. Cats understand files. Cats do not understand B-tree indexes.

**4. Configuration is environment variables**
There is no config.json. There is no config.yaml. There is no config.toml. Configuration is done through environment variables with sensible defaults. If you need to change a setting, you change an env var and restart. Simple. Cat-approved.

**5. Logging is stdout**
The application logs to stdout in structured JSON format. The infrastructure (systemd, Docker, K8s) captures stdout and routes it appropriately. No log4j. No winston. No rotating file handlers in application code. The app logs. The platform routes.

**6. Caching is Redis (or memory)**
Redis is acceptable for distributed caching. For single-instance deployments, an in-memory LRU cache suffices. No memcached. No Varnish. No CDN for API responses. Keep it simple or keep it catted.

**7. Queues are optional**
For the vast majority of operations, synchronous request-response is fine. Async queues (Celery, RabbitMQ, Kafka) are added only when latency requirements demand it — and only after proving the synchronous path is insufficient.

**8. Monitoring is Prometheus + Grafana**
Metrics are exposed on a `/metrics` endpoint in Prometheus format. Grafana dashboards visualize them. No Datadog. No New Relic. No APM agents. Open standards. Closed bloat.

**9. Tests are pytest and vitest**
There are exactly two test frameworks in Miau Finance: pytest for Python and vitest for TypeScript. No jest. No mocha. No nose. No unittest. Two frameworks. One standard. Infinite coverage.

**10. Documentation is markdown**
All documentation is markdown, stored in the repo, rendered by the viewer of your choice. No Confluence. No Notion. No ReadTheDocs. If it's not in the repo, it doesn't exist.

### The Dependency Audit

Every quarter, the Cat Council audits the dependency tree:

- **Red dependencies** — Must be eliminated. These are large frameworks pulled in for minor convenience (looking at you, lodash).
- **Yellow dependencies** — Must be justified. These are medium-impact libraries that need quarterly re-approval.
- **Green dependencies** — Approved. These are essential libraries with no reasonable replacement (FastAPI, React, psycopg2).

The goal: zero red dependencies by end of year. Yellow dependencies reduced by 50%.

### The Binary Size Budget

| Component | Budget | Current |
|-----------|--------|---------|
| CatPod binary | 5MB | 4.2MB |
| Init container | 2MB | 1.8MB |
| Sidecar proxy | 3MB | N/A (not needed yet) |
| CLI tools | 1MB | 0.6MB |

Every megabyte counts. Every kilobyte is accounted for. The binary is stripped, compressed, and optimized. Cat Core does not waste bytes.

### Why Bother?

Smaller binaries mean faster deployments. Fewer dependencies mean fewer CVEs. Simpler architecture means fewer bugs. Cat Core is not minimalism for its own sake — it's minimalism for reliability, security, and performance.

The cat does not carry unnecessary weight. Neither should your software.

```
 /\_/\
( o.o )
 > ^ <    "Dependencies are for dogs."
```
