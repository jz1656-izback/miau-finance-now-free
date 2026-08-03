#!/bin/bash
# MIAU FINANCE - Agent Decision Helper
# Use this to propose and record decisions

ACTION=${1:-"help"}

case "$ACTION" in
    propose)
        echo "=========================================="
        echo "  PROPOSE A DECISION"
        echo "=========================================="
        echo ""
        read -p "Decision topic: " TOPIC
        read -p "Your agent name (e.g., backend-dev): " AGENT
        read -p "Needs input from (comma-separated): " NEEDS_INPUT
        read -p "Proposal description: " DESCRIPTION
        echo ""
        
        # Add to COMMUNICATION.md
        echo "" >> COMMUNICATION.md
        echo "### $(date +%Y-%m-%d) @$AGENT → @all" >> COMMUNICATION.md
        echo "**Topic:** $TOPIC" >> COMMUNICATION.md
        echo "**Message:** $DESCRIPTION" >> COMMUNICATION.md
        echo "**Action Required:** Yes" >> COMMUNICATION.md
        echo "**Priority:** Medium" >> COMMUNICATION.md
        echo "" >> COMMUNICATION.md
        
        # Add to Pending Decisions table
        DECISION_ID="D-$(grep -c "^| D-" COMMUNICATION.md 2>/dev/null || echo 0)"
        sed -i "/| D-000 |.*|/a | $DECISION_ID | $TOPIC | @$AGENT | @$NEEDS_INPUT | $(date -d '+1 day' +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d) | ⬜ Pending |" COMMUNICATION.md
        
        echo "✅ Decision proposed: $TOPIC"
        echo "📝 Added to COMMUNICATION.md"
        echo "🏷️ Decision ID: $DECISION_ID"
        ;;
        
    record)
        echo "=========================================="
        echo "  RECORD A DECISION"
        echo "=========================================="
        echo ""
        read -p "Decision ID (e.g., D-001): " DECISION_ID
        read -p "Decision: " DECISION
        read -p "Rationale: " RATIONALE
        read -p "Decided by: " DECIDED_BY
        echo ""
        
        # Move from Pending to Decisions Made
        sed -i "s/| $DECISION_ID |.*| ⬜ Pending |/| $DECISION_ID |.*| $DECISION | $RATIONALE | @$DECIDED_BY | $(date +%Y-%m-%d) |/" COMMUNICATION.md
        
        echo "✅ Decision recorded: $DECISION_ID"
        echo "📝 Updated COMMUNICATION.md"
        ;;
        
    check)
        echo "=========================================="
        echo "  PENDING DECISIONS"
        echo "=========================================="
        echo ""
        grep "⬜ Pending" COMMUNICATION.md 2>/dev/null || echo "✅ No pending decisions"
        ;;
        
    help)
        echo "=========================================="
        echo "  AGENT DECISION HELPER"
        echo "=========================================="
        echo ""
        echo "Usage: ./scripts/decision.sh <action>"
        echo ""
        echo "Actions:"
        echo "  propose  - Propose a new decision"
        echo "  record   - Record a made decision"
        echo "  check    - Check pending decisions"
        echo "  help     - Show this help"
        echo ""
        ;;
        
    *)
        echo "❌ Unknown action: $ACTION"
        echo "Run ./scripts/decision.sh help for usage"
        ;;
esac
