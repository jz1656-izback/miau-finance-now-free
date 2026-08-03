#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}╔══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║        Miau Finance — Test Runner           ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════╝${NC}"
echo

# ── Backend tests ──────────────────────────────────────────────
echo -e "${CYAN}━━━ Running Backend Tests (pytest) ─────────────────${NC}"
if [ -d "$SCRIPT_DIR/backend/.venv" ]; then
    PYTHON="$SCRIPT_DIR/backend/.venv/bin/python"
    PIP="$SCRIPT_DIR/backend/.venv/bin/pip"
else
    PYTHON="python3"
    PIP="pip3"
fi

# Install test deps if needed
"$PIP" install -q pytest pytest-asyncio pytest-httpx httpx 2>/dev/null || true

cd "$SCRIPT_DIR/backend"
if "$PYTHON" -m pytest tests/ \
    --tb=short \
    --no-header \
    -q \
    -x \
    2>&1; then
    echo -e "${GREEN}✓ Backend tests passed${NC}"
    BACKEND_EXIT=0
else
    echo -e "${RED}✗ Backend tests failed${NC}"
    BACKEND_EXIT=1
fi

echo

# ── Frontend tests ─────────────────────────────────────────────
echo -e "${CYAN}━━━ Running Frontend Tests (vitest) ─────────────────${NC}"

if [ -d "$SCRIPT_DIR/frontend/node_modules/.bin" ]; then
    VITEST="$SCRIPT_DIR/frontend/node_modules/.bin/vitest"
elif command -v npx &>/dev/null; then
    VITEST="npx vitest"
else
    VITEST="./node_modules/.bin/vitest"
fi

cd "$SCRIPT_DIR/frontend"
if $VITEST run \
    --reporter=verbose \
    2>&1; then
    echo -e "${GREEN}✓ Frontend tests passed${NC}"
    FRONTEND_EXIT=0
else
    echo -e "${RED}✗ Frontend tests failed${NC}"
    FRONTEND_EXIT=1
fi

echo

# ── Summary ────────────────────────────────────────────────────
echo -e "${CYAN}━━━ Summary ─────────────────────────────────────────${NC}"
if [ "$BACKEND_EXIT" -eq 0 ] && [ "$FRONTEND_EXIT" -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed.${NC}"
    echo "  Backend:  $([ "$BACKEND_EXIT" -eq 0 ] && echo 'PASS' || echo 'FAIL')"
    echo "  Frontend: $([ "$FRONTEND_EXIT" -eq 0 ] && echo 'PASS' || echo 'FAIL')"
    exit 1
fi
