```
  ╱|、
 (˚ˎ 。7
  |、˜〵
  じしˍ,)ノ
```

# 🐋 CatPod — Single Binary, Zero Dependencies

## The 5MB Runtime That Runs Everything

CatPod is the MiauOS service runtime — a single, statically compiled binary that replaces the traditional stack of Python runtime + web server + application code + dependencies. It is the culmination of the Cat Core philosophy.

### Architecture

CatPod is written in Go (chosen for its single-binary output and excellent concurrency model) and includes:

- **HTTP/2 router** — Fast, zero-allocation routing with path parameters, query parsing, and middleware chaining
- **Postgres wire protocol client** — Native Postgres implementation, no libpq needed
- **Redis RESP client** — Native Redis protocol for caching and pub/sub
- **TLS 1.3 stack** — Built-in crypto, no OpenSSL dependency
- **JSON/MessagePack serializer** — Zero-copy serialization for high-performance APIs
- **WebSocket server** — RFC 6455 compliant with per-frame compression
- **gRPC server** — For inter-service communication
- **Prometheus metrics exporter** — `/metrics` endpoint with standard formats
- **Structured logger** — JSON output to stdout, configurable levels
- **Health check endpoints** — `/health`, `/ready`, `/live` for orchestration

### Performance Characteristics

| Metric | CatPod | Typical Python |
|--------|--------|----------------|
| Binary size | 4.2MB | 150MB+ (with venv) |
| Startup time | 8ms | 2-5 seconds |
| Memory (idle) | 4MB | 50-100MB |
| Requests/sec | 45,000 | 5,000-10,000 |
| P99 latency | 2ms | 15-50ms |

### Deployment Model

CatPod runs as a systemd service on the host OS:

```
/usr/bin/catpod serve \
  --config /etc/catpod/config.toml \
  --listen :8080 \
  --db postgres://miau@localhost/miau \
  --redis localhost:6379
```

It can also run in Docker (image size: 6MB):

```
FROM scratch
COPY catpod /catpod
COPY config.toml /etc/catpod/config.toml
EXPOSE 8080
ENTRYPOINT ["/catpod", "serve"]
```

Or on Kubernetes as a sidecar:

```yaml
containers:
- name: catpod
  image: miau/catpod:latest
  args: ["serve", "--listen", ":8080"]
  resources:
    requests:
      memory: "8Mi"
      cpu: "10m"
```

### The Plugin System

CatPod supports plugins via WASM (WebAssembly). Plugins are compiled to `.wasm` files and loaded at startup:

- **Sandboxed** — WASM modules cannot access the filesystem or network without explicit capability grants
- **Hot-reloadable** — Changed plugin files are detected and reloaded without restarting CatPod
- **Language-agnostic** — Write plugins in Go, Rust, C, or any language that compiles to WASM
- **Scoped permissions** — Each plugin declares required capabilities (db read, http fetch, etc.)

### Zero-Down boot Deploys

CatPod supports graceful restarts:
1. New binary is downloaded to `/tmp/catpod-new`
2. CatPod forks a new process with the new binary
3. Old process drains connections (30s timeout)
4. New process takes over
5. Old process exits

Zero dropped connections. Zero downtime. Zero cat complaints.

### Why CatPod?

Every time you write `apt-get install python3-pip && pip install -r requirements.txt`, a kitten loses its whiskers. CatPod eliminates that cruelty. One binary. One command. One purring service.

```
  ╱|、
 (˚ˎ 。7    "Small binary. Big purr."
  |、˜〵
  じしˍ,)ノ
```
