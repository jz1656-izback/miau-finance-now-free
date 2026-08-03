import csv
import io
import json
import logging
from datetime import timezone, date, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.middleware.rbac import get_current_user_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/audit", tags=["Audit"])


def require_admin(user: dict):
    if user.get("role") not in ("admin",):
        raise HTTPException(403, "Admin access required")


def _serialize(val):
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    return val


@router.get("/logs")
async def list_audit_logs(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    action: Optional[str] = None,
    user_id: Optional[str] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    require_admin(user)
    conditions = []
    params: dict = {"limit": limit, "offset": offset}
    if action:
        conditions.append("action = :action")
        params["action"] = action
    if user_id:
        conditions.append("user_id = :uid")
        params["uid"] = user_id
    if from_date:
        conditions.append("created_at >= :from_date")
        params["from_date"] = from_date
    if to_date:
        conditions.append("created_at <= :to_date")
        params["to_date"] = to_date
    where = ""
    if conditions:
        where = "WHERE " + " AND ".join(conditions)

    result = await db.execute(
        text(f"""
            SELECT id, object_id, action, user_id, changes, created_at
            FROM audit_log
            {where}
            ORDER BY created_at DESC
            LIMIT :limit OFFSET :offset
        """),
        params,
    )
    rows = []
    for row in result.mappings().all():
        d = dict(row)
        d["id"] = str(d["id"])
        d["object_id"] = str(d["object_id"])
        rows.append(d)
    return rows


@router.get("/export")
async def export_audit_logs(
    format: str = Query("json", pattern="^(csv|json)$"),
    action: Optional[str] = None,
    user_id: Optional[str] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    require_admin(user)
    conditions = []
    params: dict = {}
    if action:
        conditions.append("action = :action")
        params["action"] = action
    if user_id:
        conditions.append("user_id = :uid")
        params["uid"] = user_id
    if from_date:
        conditions.append("created_at >= :from_date")
        params["from_date"] = from_date
    if to_date:
        conditions.append("created_at <= :to_date")
        params["to_date"] = to_date
    where = ""
    if conditions:
        where = "WHERE " + " AND ".join(conditions)

    result = await db.execute(
        text(f"""
            SELECT id, object_id, action, user_id, changes, created_at
            FROM audit_log
            {where}
            ORDER BY created_at DESC
            LIMIT 10000
        """),
        params,
    )
    rows = [dict(r) for r in result.mappings().all()]

    if format == "csv":
        return _export_csv(rows)
    return _export_json(rows)


def _export_csv(rows: list[dict]) -> StreamingResponse:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "object_id", "action", "user_id", "changes", "created_at"])
    for r in rows:
        writer.writerow([
            r.get("id", ""),
            r.get("object_id", ""),
            r.get("action", ""),
            r.get("user_id", ""),
            json.dumps(r.get("changes", {}), default=str),
            _serialize(r.get("created_at", "")),
        ])
    buf.seek(0)
    now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="audit_log_export_{now}.csv"',
        },
    )


def _export_json(rows: list[dict]) -> StreamingResponse:
    now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    data = []
    for r in rows:
        data.append({
            "id": str(r.get("id", "")),
            "object_id": str(r.get("object_id", "")),
            "action": r.get("action", ""),
            "user_id": r.get("user_id", ""),
            "changes": r.get("changes", {}),
            "created_at": _serialize(r.get("created_at", "")),
        })
    return StreamingResponse(
        iter([json.dumps(data, indent=2, default=str)]),
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="audit_log_export_{now}.json"',
        },
    )
