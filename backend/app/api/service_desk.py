"""Miau Fire Brigade — Service Desk API"""
import uuid
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, func
from app.database import get_db
from app.middleware.auth import get_current_user
from app.schemas.service_desk import TicketCreate, TicketUpdate, TicketResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Service Desk"])

FIREFIGHTERS = ["Captain Ember", "Lieutenant Spark", "Firefighter Whiskers", "Cadet Puddles", "Dispatcher Meow"]

# In-memory token relay for cross-origin SSO
# 🔒 SECURITY (V7-001/C2): relay now requires authentication to write AND read,
# is bound to the authenticated user, expires after BROADCAST_TOKEN_TTL_SECONDS,
# and GET consumes it (one-time read) to prevent token theft/replay.
_token_relay: dict = {"token": None, "user": None, "timestamp": None}
BROADCAST_TOKEN_TTL_SECONDS = 30


class TokenRelayBody(BaseModel):
    token: str
    user: str


@router.post("/api/v1/auth/broadcast-token")
async def broadcast_token(
    body: TokenRelayBody,
    user: dict = Depends(get_current_user),
):
    # Only allow relaying a token for the authenticated user themselves.
    if body.user != user.get("sub"):
        raise HTTPException(status_code=403, detail="Cannot relay a token for another user")
    _token_relay["token"] = body.token
    _token_relay["user"] = body.user
    _token_relay["timestamp"] = datetime.now(timezone.utc).isoformat()
    return {"ok": True}


@router.get("/api/v1/auth/broadcast-token")
async def get_broadcast_token(
    user: dict = Depends(get_current_user),
):
    ts = _token_relay.get("timestamp")
    if ts:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(ts)).total_seconds()
        if age > BROADCAST_TOKEN_TTL_SECONDS:
            _token_relay.clear()
    # Only the user who set the token may read it; read is one-time.
    if _token_relay.get("user") != user.get("sub") or not _token_relay.get("token"):
        return {"token": None, "user": None, "timestamp": None}
    relay = dict(_token_relay)
    _token_relay.clear()
    return relay


def _pick_firefighter() -> str:
    import random
    return random.choice(FIREFIGHTERS)


def _row_to_ticket(row) -> dict:
    return {
        "id": str(row["id"]),
        "category": row["category"],
        "priority": row["priority"],
        "title": row["title"],
        "description": row.get("description"),
        "author": row.get("author"),
        "service": row.get("service"),
        "status": row["status"],
        "assigned_to": row.get("assigned_to"),
        "pokes": row.get("pokes", 0),
        "created_at": row["created_at"].isoformat() if row.get("created_at") else None,
        "updated_at": row["updated_at"].isoformat() if row.get("updated_at") else None,
    }


@router.get("/api/v1/service-desk/tickets")
async def list_tickets(
    status: str = Query(None, description="Filter by status: open, progress, resolved"),
    category: str = Query(None, description="Filter by category: fire, bug, feature, question"),
    db: AsyncSession = Depends(get_db),
):
    conditions = ["1=1"]
    params = {}
    if status:
        conditions.append("status = :status")
        params["status"] = status
    if category:
        conditions.append("category = :category")
        params["category"] = category
    where = " AND ".join(conditions)
    query = text(f"SELECT * FROM service_desk_tickets WHERE {where} ORDER BY created_at DESC")
    result = await db.execute(query, params)
    rows = result.mappings().all()
    return [_row_to_ticket(r) for r in rows]


@router.post("/api/v1/service-desk/tickets", status_code=201)
async def create_ticket(
    body: TicketCreate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    user_id = user.get("sub") if user else None
    ticket_id = uuid.uuid4()
    assigned = _pick_firefighter()
    now = datetime.now(timezone.utc)
    query = text("""
        INSERT INTO service_desk_tickets (id, user_id, category, priority, title, description, author, service, status, assigned_to, pokes, created_at, updated_at)
        VALUES (:id, :user_id, :category, :priority, :title, :description, :author, :service, 'open', :assigned_to, 0, :now, :now)
        RETURNING *
    """)
    result = await db.execute(query, {
        "id": ticket_id, "user_id": user_id, "category": body.category,
        "priority": body.priority, "title": body.title, "description": body.description,
        "author": body.author, "service": body.service, "assigned_to": assigned, "now": now,
    })
    await db.commit()
    row = result.mappings().first()
    return _row_to_ticket(row)


@router.get("/api/v1/service-desk/tickets/{ticket_id}")
async def get_ticket(
    ticket_id: str,
    db: AsyncSession = Depends(get_db),
):
    try:
        tid = uuid.UUID(ticket_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ticket ID")
    query = text("SELECT * FROM service_desk_tickets WHERE id = :id")
    result = await db.execute(query, {"id": tid})
    row = result.mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return _row_to_ticket(row)


@router.patch("/api/v1/service-desk/tickets/{ticket_id}")
async def update_ticket(
    ticket_id: str,
    body: TicketUpdate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    try:
        tid = uuid.UUID(ticket_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ticket ID")
    updates = []
    params = {"id": tid}
    if body.status is not None:
        updates.append("status = :status")
        params["status"] = body.status
    if body.assigned_to is not None:
        updates.append("assigned_to = :assigned_to")
        params["assigned_to"] = body.assigned_to
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    updates.append("updated_at = :now")
    params["now"] = datetime.now(timezone.utc)
    set_clause = ", ".join(updates)
    query = text(f"UPDATE service_desk_tickets SET {set_clause} WHERE id = :id RETURNING *")
    result = await db.execute(query, params)
    await db.commit()
    row = result.mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return _row_to_ticket(row)


@router.post("/api/v1/service-desk/tickets/{ticket_id}/poke")
async def poke_ticket(
    ticket_id: str,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    try:
        tid = uuid.UUID(ticket_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ticket ID")
    query = text("UPDATE service_desk_tickets SET pokes = pokes + 1, updated_at = :now WHERE id = :id RETURNING *")
    result = await db.execute(query, {"id": tid, "now": datetime.now(timezone.utc)})
    await db.commit()
    row = result.mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return _row_to_ticket(row)


@router.delete("/api/v1/service-desk/tickets/{ticket_id}")
async def delete_ticket(
    ticket_id: str,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    try:
        tid = uuid.UUID(ticket_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ticket ID")
    query = text("DELETE FROM service_desk_tickets WHERE id = :id RETURNING id")
    result = await db.execute(query, {"id": tid})
    await db.commit()
    row = result.mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket extinguished", "id": ticket_id}
