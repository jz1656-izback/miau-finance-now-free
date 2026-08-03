"""Network governance API — proposals, voting, delegation, treasury."""

import logging
import uuid
from datetime import timezone, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from app.middleware.auth import get_current_user
from app.services.network.token_distribution import get_governance_power

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/network/governance", tags=["Network Governance"])

_proposals: dict[str, dict] = {}
_votes: dict[str, list[dict]] = {}


async def create_proposal(title: str, description: str, proposer: str, voting_days: int = 7) -> dict:
    pid = str(uuid.uuid4())[:8]
    _proposals[pid] = {
        "id": pid, "title": title, "description": description, "proposer": proposer, "status": "active",
        "voting_ends": datetime.now(timezone.utc).isoformat(), "voting_days": voting_days, "created_at": datetime.now(timezone.utc).isoformat(),
        "for_votes": 0, "against_votes": 0, "abstain_votes": 0, "total_power": 0,
    }
    _votes[pid] = []
    return _proposals[pid]


async def vote_on_proposal(proposal_id: str, voter: str, vote: str, power: float) -> dict:
    if proposal_id not in _proposals:
        return {"error": "Proposal not found"}
    if vote not in ("for", "against", "abstain"):
        return {"error": "Vote must be 'for', 'against', or 'abstain'"}
    _votes[proposal_id].append({"voter": voter, "vote": vote, "power": power, "timestamp": datetime.now(timezone.utc).isoformat()})
    if vote == "for":
        _proposals[proposal_id]["for_votes"] += power
    elif vote == "against":
        _proposals[proposal_id]["against_votes"] += power
    else:
        _proposals[proposal_id]["abstain_votes"] += power
    _proposals[proposal_id]["total_power"] += power

    total = _proposals[proposal_id]["for_votes"] + _proposals[proposal_id]["against_votes"]
    if total > 0 and _proposals[proposal_id]["for_votes"] / total > 0.5:
        _proposals[proposal_id]["status"] = "passed"

    return {"proposal_id": proposal_id, "vote": vote, "power": power, "new_status": _proposals[proposal_id]["status"]}


@router.post("/proposals")
async def api_create_proposal(title: str, description: str, user=Depends(get_current_user)):
    return await create_proposal(title, description, user.get("sub", "anonymous"))


@router.get("/proposals")
async def api_list_proposals():
    return list(_proposals.values())


@router.get("/proposals/{proposal_id}")
async def api_get_proposal(proposal_id: str):
    p = _proposals.get(proposal_id)
    if not p:
        raise HTTPException(404, "Proposal not found")
    return p


@router.post("/proposals/{proposal_id}/vote")
async def api_vote(proposal_id: str, vote: str = Query(..., pattern="^(for|against|abstain)$"), user=Depends(get_current_user)):
    power = await get_governance_power(user.get("sub", "anonymous"))
    if power <= 0:
        raise HTTPException(400, "No governance power — stake MIAU tokens to vote")
    return await vote_on_proposal(proposal_id, user.get("sub", "anonymous"), vote, power)
