```
  ╱|、
 (˚ˎ 。7
  |、˜〵
  じしˍ,)ノ
```

# 🌉 Translation Layer — CatProtocol to REST Bridge

## The Universal Adapter

The Translation Layer is the component that converts between CatProtocol (the terminal-native binary protocol) and standard REST/HTTP APIs. It allows any HTTP client to communicate with the Miau Finance ecosystem without understanding CatProtocol, while also allowing the terminal to access standard REST APIs through CatProtocol framing.

### The Problem

The terminal speaks CatProtocol — a compact, streaming binary protocol optimized for low-latency financial data. REST APIs speak HTTP/JSON — a verbose, stateless, text-based protocol optimized for developer ergonomics. These two worlds need to communicate.

### Architecture

```
Terminal ──CatProtocol──→ Translation Layer ──HTTP/JSON──→ Backend API
                                 │
                                 └──CatProtocol──→ Other CatPod services
```

The Translation Layer sits between the terminal and the backend services. It:

1. **Decodes** incoming CatProtocol frames to JSON
2. **Routes** the JSON payload to the appropriate REST endpoint
3. **Encodes** the REST response back to CatProtocol
4. **Streams** responses for real-time data (ticker prices, trade updates)

### CatProtocol Frame Format

```
┌─────────┬─────────┬──────────┬──────────┬──────────────┐
│ Version │  Type   │  Flags   │  Length  │   Payload    │
│ (2B)    │  (2B)   │  (2B)    │  (4B)    │   (N B)      │
└─────────┴─────────┴──────────┴──────────┴──────────────┘
```

- **Version** — Protocol version (currently 0x0001)
- **Type** — Message type (request, response, stream, error, heartbeat)
- **Flags** — Metadata flags (compressed, encrypted, streaming, more)
- **Length** — Payload length in bytes (max: 16MB)
- **Payload** — Compressed JSON or binary data

### REST Translation Table

| CatProtocol Type | REST Method | Endpoint Pattern |
|-----------------|-------------|------------------|
| `request` | GET/POST | `/api/v1/miaucat/:path` |
| `stream_sub` | GET | `/api/v1/miaucat/stream/:topic` |
| `stream_unsub` | DELETE | `/api/v1/miaucat/stream/:topic` |
| `ping` | GET | `/api/v1/miaucat/ping` |
| `auth` | POST | `/api/v1/miaucat/auth` |

### Streaming

For real-time data, the Translation Layer supports Server-Sent Events (SSE):

```
GET /api/v1/miaucat/stream/prices

→ data: {"ticker":"AAPL","price":187.42,"change":0.82}
→ data: {"ticker":"GOOGL","price":141.30,"change":-0.31}
```

The terminal subscribes to a stream once and receives continuous updates. No polling. No WebSocket reconnection logic. Just data flowing like a cat's purr.

### The Bridge Mode

The Translation Layer can also operate in "bridge mode," where it forwards REST API calls to CatProtocol services:

```bash
# Standard HTTP request translated to CatProtocol
curl http://localhost:8080/api/v1/risk/AAPL \
  -H "X-Protocol: catprotocol"

# The Translation Layer converts this to a CatProtocol request,
# sends it to the CatPod risk service, and returns the response
```

### Performance

| Metric | Raw REST | Via Translation Layer | Overhead |
|--------|----------|----------------------|----------|
| Latency (p50) | 5ms | 5.5ms | 0.5ms |
| Latency (p99) | 50ms | 52ms | 2ms |
| Throughput | 10K req/s | 9.5K req/s | 5% |
| Bandwidth (payload) | 1.2KB | 0.3KB | -75% |

The bandwidth savings from CatProtocol's compact binary format offset the minimal latency overhead. For high-volume data streams, the Translation Layer reduces network costs by up to 75%.

### Why Not Just Use REST?

Because REST is verbose. A typical JSON ticker response is 200+ bytes. The same data in CatProtocol is 40 bytes. When you're streaming 10,000 tickers per second, that difference matters.

Because REST is stateless. CatProtocol supports streaming subscriptions, acknowledgments, and backpressure natively.

Because REST is not a cat protocol. CatProtocol is.

```
  ╱|、
 (˚ˎ 。7    "Bridging worlds. One meow at a time."
  |、˜〵
  じしˍ,)ノ
```
