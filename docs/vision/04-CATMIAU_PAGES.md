```
  ╱|、
 (˚ˎ 。7
  |、˜〵
  じしˍ,)ノ
```

# 📄 CatMiau Pages — Page-Based Development

## Not a Language. A Specification.

CatMiau Pages (`.miau` files) are not a programming language. They are a structured documentation format that describes every component, service, and app in the Miau Finance ecosystem. Think of them as the DNA of the system — each page encodes the essential information about a single unit of functionality.

### The Format

Every `.miau` file has exactly 7 lines:

```
Page: <Name>
Cat: <emoji>
Function: <one line>
Description: <paragraph>
API: <endpoint or "—">
Output: <what it shows>
Tuna: <number>
```

### Why 7 Lines?

Seven is a magic number. Seven days in a week. Seven wonders of the world. Seven lines of specification per page. Any more and the spec becomes unwieldy. Any less and you lose critical information. Seven is the cat's preferred number.

### The Fields Explained

**Page** — A human-readable name for the component. This is displayed in catalogs, menus, and search results. Keep it short but descriptive.

**Cat** — The emoji that represents this page's feline guardian. Every page has a cat. The cat's emoji is used in navigation, error messages, and the page favicon. Choose wisely.

**Function** — Exactly one line describing what this page does. If you cannot describe it in one line, the page is too complex. Split it into multiple pages.

**Description** — A paragraph (3-5 sentences) explaining the page in detail. What does it do? Who uses it? Why does it exist? This is the primary documentation for the page.

**API** — The REST endpoint(s) associated with this page, or "—" if it has no direct API (e.g., a frontend component). Multiple endpoints can be listed with `GET/POST/PUT/DELETE` prefixes.

**Output** — What the user sees when interacting with this page. Be specific about the data format, visualization type, and interactivity.

**Tuna** — The economic value of this page in the tuna economy. Higher values indicate more complex, more revenue-generating pages. The cat's food budget depends on this number.

### The Tuna Economy

Every page pays the cat. The Tuna value determines:

- **Developer priority** — Pages with higher Tuna values are developed first
- **Maintenance budget** — Higher Tuna pages get more engineering time
- **Cat food allocation** — Tuna is converted to actual cat food at the end of each sprint

Tuna values range from 1 (a simple health check) to 10 (the AI advisor or quantum finance engine). The total Tuna across all pages represents the net worth of the Miau Finance ecosystem.

### Page Discovery

`.miau` files are indexed by the Miau Page Engine:

```bash
miau list              # List all pages
miau search risk       # Search pages by keyword
miau cat 🛡️            # Find pages guarded by specific cat
miau tuna              # Show tuna economy dashboard
```

### The Page Lifecycle

1. **Draft** — Page spec is written but not implemented
2. **Active** — Page is implemented and deployed
3. **Deprecated** — Page is being phased out (Tuna = 0)
4. **Removed** — Page file is deleted after migration period

### Page Dependencies

Pages can reference other pages by name in their Description field. The page engine builds a dependency graph:

```
health.miau → api-gateway.miau → auth.miau → user-service.miau
```

This graph is used for deployment ordering, impact analysis, and cat food allocation.

### Not a Language

CatMiau Pages are not interpreted, compiled, or executed. They are documentation. They are specifications. They are the single source of truth for what the system contains. The implementation may be in Python, Go, or TypeScript, but the specification is always in `.miau`.

Because cats don't code. Cats specify. Humans implement.

```
 /\_/\
( o.o )
 > ^ <    "Spec first. Code second. Tuna always."
```
