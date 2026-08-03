#!/bin/bash
# MIAU FINANCE - Agent Status Checker
# Run this script before starting work to get current status

echo "=========================================="
echo "  MIAU FINANCE - AGENT STATUS CHECK"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "AGENTS.md" ]; then
    echo "❌ Error: Not in miau-finance directory"
    exit 1
fi

echo "📁 Project: miau-finance"
echo "📅 Date: $(date +%Y-%m-%d)"
echo ""

# Check git status
echo "🔀 Git Status:"
cd /home/jevgeniz/Projekte/miau-finance
git status --short | head -10
echo ""

# Check current branch
echo "🌿 Current Branch: $(git branch --show-current)"
echo ""

# Check recent commits
echo "📝 Recent Commits:"
git log --oneline -5
echo ""

# Check Docker status
echo "🐳 Docker Containers:"
docker ps --format "table {{.Names}}\t{{.Status}}" 2>/dev/null | head -10
echo ""

# Check backend health
echo "🏥 Backend Health:"
curl -s http://localhost:8000/api/v1/health 2>/dev/null || echo "❌ Backend not running"
echo ""

# Check pending messages
echo "📨 Pending Messages (from COMMUNICATION.md):"
if grep -q "Action Required: Yes" COMMUNICATION.md 2>/dev/null; then
    grep -A 5 "Action Required: Yes" COMMUNICATION.md | head -20
else
    echo "✅ No pending messages"
fi
echo ""

# Check pending decisions
echo "🤔 Pending Decisions (from COMMUNICATION.md):"
if grep -q "⬜ Pending" COMMUNICATION.md 2>/dev/null; then
    grep "⬜ Pending" COMMUNICATION.md | head -5
else
    echo "✅ No pending decisions"
fi
echo ""

# Check agent tasks
echo "📋 Your Tasks (from AGENTS.md):"
echo "Check AGENTS.md for your assigned tasks"
echo ""

# Check conventions
echo "📖 Conventions:"
echo "Read CONVENTIONS.md before coding"
echo ""

# Check dependencies
echo "🔗 Dependencies (from COMMUNICATION.md):"
if grep -q "⬜ Pending" COMMUNICATION.md 2>/dev/null; then
    grep -B 2 "⬜ Pending" COMMUNICATION.md | grep -E "data-dev|backend-dev|infra-dev|security-dev" | head -5
else
    echo "✅ No pending dependencies"
fi
echo ""

echo "=========================================="
echo "  NEXT STEPS:"
echo "  1. Read COMMUNICATION.md for messages"
echo "  2. Read AGENTS.md for your tasks"
echo "  3. Read CONVENTIONS.md for standards"
echo "  4. Read AGENT_PROTOCOL.md for workflow"
echo "  5. Start working on your task"
echo "=========================================="
