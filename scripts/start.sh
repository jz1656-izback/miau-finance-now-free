#!/bin/bash
# Miau Finance — Start all services
# Kill any existing processes on common ports first, then start clean.

set -e

PORTS=(5173 3001 5181)
SERVICES=(
  "Frontend:5173:frontend:npx vite --host 0.0.0.0"
  "Homepage:3001:miau-homepage:npx next dev -p 3001"
  "CatGalaxy:5181:cat-galaxy:npx vite --host 0.0.0.0 --port 5181"
)

echo "🐱 Miau Finance — Starting services..."
echo ""

for entry in "${SERVICES[@]}"; do
  NAME="${entry%%:*}"
  REST="${entry#*:}"
  PORT="${REST%%:*}"
  REST="${REST#*:}"
  DIR="${REST%%:*}"
  CMD="${REST#*:}"

  # Kill any existing process on this port using fuser (more thorough than lsof)
  if fuser -k "$PORT/tcp" 2>/dev/null; then
    echo "  Killed old $NAME process on port $PORT"
    sleep 1
  fi

  # Check directory exists
  FULL_DIR="/home/jevgeniz/Projekte/$DIR"
  if [ ! -d "$FULL_DIR" ]; then
    FULL_DIR="/home/jevgeniz/Projekte/miau-finance/$DIR"
  fi

  if [ -d "$FULL_DIR" ]; then
    cd "$FULL_DIR"
    nohup $CMD > /dev/null 2>&1 &
    echo "  ✅ $NAME started on port $PORT"
  else
    echo "  ⚠️  $NAME: directory $FULL_DIR not found"
  fi
done

echo ""
echo "🐱 All services started. Open http://localhost:5173"
