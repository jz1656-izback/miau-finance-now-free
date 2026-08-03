```
  ╱|、
 (˚ˎ 。7
  |、˜〵
  じしˍ,)ノ
```

# 🗄️ CatDB — File-Based Database, No PostgreSQL Required

## The Anti-Database

CatDB is a radical reimagining of data persistence. Instead of running a heavyweight PostgreSQL server with connection pools, replication slots, and WAL files, CatDB stores data in structured files on the filesystem. It is not a database in the traditional sense — it is a file-based data access pattern.

### The Philosophy

PostgreSQL is excellent for relational, transactional data with complex queries. But much of Miau Finance's data is not relational. User preferences, session tokens, cached market data, configuration — these are key-value stores at heart. Forcing them into SQL tables is like forcing a cat to wear a collar with a bell. Cruel and unnecessary.

### What CatDB Stores

- **User preferences** — JSON files keyed by user ID
- **Session data** — Encrypted session files with TTL
- **Configuration** — TO ML files that are reloaded on change
- **Cache** — File-based LRU cache with disk budget
- **Audit logs** — Append-only log files with rotation
- **Feature flags** — TOML files that enable/disable features without deploy

### The File Format

User preferences file (`/var/lib/catdb/users/abc123.json`):

```json
{
  "id": "abc123",
  "theme": "crt-green",
  "default_portfolio": "main",
  "currency": "EUR",
  "notifications": { "email": true, "push": false },
  "cat_name": "Whiskers",
  "tuna_balance": 420
}
```

Session file (`/var/lib/catdb/sessions/tok_xyz`):

```
miau:tok_xyz
user_id:abc123
expires:2026-06-22T14:00:00Z
created:2026-05-22T14:00:00Z
```

### Performance Characteristics

| Operation | CatDB (file) | Redis | PostgreSQL |
|-----------|-------------|-------|------------|
| Read (1KB) | 0.05ms | 0.1ms | 0.5ms |
| Write (1KB) | 0.1ms | 0.1ms | 1ms |
| Scan 1000 keys | 2ms | 0.5ms | 5ms |
| Memory (10K keys) | 50MB | 100MB+ | 200MB+ |
| Startup time | 0ms | 500ms | 5s |

### When to Use PostgreSQL

CatDB is not a replacement for PostgreSQL. It is a complement. Use PostgreSQL for:

- **Financial transactions** — Trades, orders, positions must be ACID-compliant
- **User accounts** — Authentication data needs referential integrity
- **Portfolio data** — Complex queries across multiple tables
- **Anything that needs to be consistent across multiple servers**

Use CatDB for:

- **Per-instance configuration**
- **Ephemeral session data**
- **Read-heavy caches**
- **Data that doesn't need cross-node consistency**

### The Hybrid Approach

Miau Finance uses both:

```
PostgreSQL ─── Relational data (accounts, trades, portfolios)
               │
CatDB ───────── Non-relational data (prefs, sessions, config, cache)
               │
Redis ───────── Distributed cache + pub/sub (rate limits, real-time)
```

Each tool for its purpose. Each cat for its nap spot.

### CatDB Operations

```bash
catdb get users/abc123              # Read a file
catdb set users/abc123 '{"theme":"dark"}'  # Write a file
catdb delete sessions/tok_xyz       # Delete a file
catdb list users/                   # List files in a directory
catdb watch config/                 # Watch for file changes
```

### The CatDB Daemon (Optional)

For cases where file I/O is too slow or you need atomic multi-file writes, CatDB can run as a daemon:

```
catdbd --root /var/lib/catdb --port 9797
```

This exposes a simple HTTP API:
- `GET /:namespace/:key` — Read
- `PUT /:namespace/:key` — Write
- `DELETE /:namespace/:key` — Delete
- `GET /:namespace/` — List

But the default is no daemon. Just files. Because cats prefer simplicity.

```
 /\_/\
( o.o )
 > ^ <    "PostgreSQL is for the humans.
           CatDB is for the cats."
```
