"""Database-backed DAO governance — proposals, weighted voting, delegation, treasury."""
import logging
import uuid
from datetime import timezone, datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.middleware.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/governance", tags=["Governance"])


@router.post("/proposals")
async def create_proposal(
    title: str, description: str,
    voting_days: int = Query(7, ge=1, le=30),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Create a new governance proposal."""
    uid = user.get("sub", "anonymous")
    pid = str(uuid.uuid4())[:8]
    ends = datetime.now(timezone.utc) + timedelta(days=voting_days)
    await db.execute(text("""
        INSERT INTO governance_proposals (id, title, description, proposer_id, voting_ends_at)
        VALUES (:pid, :title, :desc, :uid, :ends)
    """), {"pid": pid, "title": title, "desc": description, "uid": uid, "ends": ends})
    await db.commit()
    return {"id": pid, "title": title, "status": "active", "voting_ends": ends.isoformat()}


@router.get("/proposals")
async def list_proposals(
    status: str = Query("active"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """List governance proposals with vote tallies."""
    where = "" if status == "all" else "WHERE gp.status = :status"
    rows = await db.execute(text(f"""
        SELECT gp.id, gp.title, gp.description, gp.proposer_id, gp.status,
               gp.voting_ends_at, gp.created_at,
               COALESCE(gv.for_votes, 0) AS for_votes,
               COALESCE(gv.against_votes, 0) AS against_votes,
               COALESCE(gv.abstain_votes, 0) AS abstain_votes,
               COALESCE(gv.total_power, 0) AS total_power
        FROM governance_proposals gp
        LEFT JOIN (
            SELECT proposal_id,
                   SUM(CASE WHEN vote = 'for' THEN power ELSE 0 END) AS for_votes,
                   SUM(CASE WHEN vote = 'against' THEN power ELSE 0 END) AS against_votes,
                   SUM(CASE WHEN vote = 'abstain' THEN power ELSE 0 END) AS abstain_votes,
                   SUM(power) AS total_power
            FROM governance_votes GROUP BY proposal_id
        ) gv ON gv.proposal_id = gp.id
        {where}
        ORDER BY gp.created_at DESC LIMIT :lim
    """), {"status": status, "lim": limit})
    return [dict(r._mapping) for r in rows]


@router.get("/proposals/{proposal_id}")
async def get_proposal(proposal_id: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    row = await db.execute(text("""
        SELECT * FROM governance_proposals WHERE id = :pid
    """), {"pid": proposal_id})
    proposal = dict(row.mappings().first() or {})
    if not proposal:
        raise HTTPException(404, "Proposal not found")
    votes = await db.execute(text("""
        SELECT voter_id, vote, power, timestamp FROM governance_votes WHERE proposal_id = :pid ORDER BY timestamp DESC
    """), {"pid": proposal_id})
    proposal["votes"] = [dict(r._mapping) for r in votes]
    return proposal


@router.post("/proposals/{proposal_id}/vote")
async def cast_vote(
    proposal_id: str, vote: str = Query(..., pattern="^(for|against|abstain)$"),
    power: float = Query(1.0, ge=0.1, le=1000),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Cast a weighted vote on a proposal."""
    uid = user.get("sub", "anonymous")
    await db.execute(text("""
        INSERT INTO governance_votes (proposal_id, voter_id, vote, power)
        VALUES (:pid, :uid, :vote, :power)
        ON CONFLICT ON CONSTRAINT uq_voter_proposal DO UPDATE SET vote = :vote2, power = :power2
    """), {"pid": proposal_id, "uid": uid, "vote": vote, "power": power, "vote2": vote, "power2": power})
    await db.commit()
    return {"proposal_id": proposal_id, "vote": vote, "power": power}


@router.post("/delegate")
async def delegate_vote(
    delegate_to: str,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Delegate voting power to another user."""
    uid = user.get("sub", "anonymous")
    await db.execute(text("""
        INSERT INTO governance_delegations (delegator_id, delegate_id)
        VALUES (:uid, :to)
        ON CONFLICT ON CONSTRAINT uq_delegation DO UPDATE SET delegate_id = :to2, updated_at = NOW()
    """), {"uid": uid, "to": delegate_to, "to2": delegate_to})
    await db.commit()
    return {"delegator": uid, "delegate": delegate_to}


@router.get("/delegations")
async def list_delegations(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    uid = user.get("sub", "anonymous")
    rows = await db.execute(text("""
        SELECT delegator_id, delegate_id, updated_at FROM governance_delegations WHERE delegator_id = :uid
    """), {"uid": uid})
    return [dict(r._mapping) for r in rows]


@router.get("/stats")
async def governance_stats(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    """Return governance dashboard stats."""
    proposals = await db.execute(text("SELECT status, COUNT(*) as cnt FROM governance_proposals GROUP BY status"))
    total_votes = await db.execute(text("SELECT COUNT(*) as cnt, COALESCE(SUM(power),0) as total_power FROM governance_votes"))
    delegations = await db.execute(text("SELECT COUNT(*) as cnt FROM governance_delegations"))
    return {
        "proposals": {r[0]: r[1] for r in proposals.fetchall()},
        "votes": dict(total_votes.mappings().first() or {"cnt": 0, "total_power": 0}),
        "delegations": delegations.scalar() or 0,
    }
