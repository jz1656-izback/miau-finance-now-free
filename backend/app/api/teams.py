from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from app.database import get_db
from app.middleware.auth import get_current_user

router = APIRouter()


async def get_current_user_db(
    db: AsyncSession = Depends(get_db),
    token_user: dict = Depends(get_current_user),
) -> dict:
    username = token_user.get("sub")
    result = await db.execute(
        text("SELECT id, username, email, role FROM users WHERE username = :username"),
        {"username": username},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(401, "User not found")
    return dict(row)


def require_owner_or_admin(user: dict, owner_id: str):
    if user.get("role") != "admin" and str(user.get("id")) != str(owner_id):
        raise HTTPException(403, "Owner or admin access required")


def require_admin(user: dict):
    if user.get("role") != "admin":
        raise HTTPException(403, "Admin access required")


@router.post("")
async def create_team(
    name: str,
    description: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            INSERT INTO teams (id, name, description, owner_id)
            VALUES (gen_random_uuid(), :name, :description, :owner_id)
            RETURNING id, name, description, owner_id, created_at
        """),
        {"name": name, "description": description, "owner_id": current_user["id"]},
    )
    await db.commit()
    row = result.mappings().first()
    return dict(row)


@router.get("")
async def list_teams(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    offset = (page - 1) * per_page
    result = await db.execute(
        text("""
            SELECT t.id, t.name, t.description, t.owner_id, t.created_at
            FROM teams t
            LEFT JOIN team_members tm ON tm.team_id = t.id
            WHERE t.owner_id = :user_id OR tm.user_id = :user_id2
            GROUP BY t.id
            ORDER BY t.created_at DESC
            LIMIT :limit OFFSET :offset
        """),
        {"user_id": current_user["id"], "user_id2": current_user["id"], "limit": per_page, "offset": offset},
    )
    rows = [dict(r) for r in result.mappings().all()]

    count_result = await db.execute(
        text("""
            SELECT COUNT(DISTINCT t.id)
            FROM teams t
            LEFT JOIN team_members tm ON tm.team_id = t.id
            WHERE t.owner_id = :user_id OR tm.user_id = :user_id2
        """),
        {"user_id": current_user["id"], "user_id2": current_user["id"]},
    )
    total = count_result.scalar()

    return {"items": rows, "total": total, "page": page, "per_page": per_page}


@router.get("/{team_id}")
async def get_team(
    team_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            SELECT t.*, u.username as owner_username
            FROM teams t
            JOIN users u ON u.id = t.owner_id
            WHERE t.id = :id
        """),
        {"id": team_id},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(404, "Team not found")

    members = await db.execute(
        text("""
            SELECT tm.id, tm.user_id, tm.role, u.username
            FROM team_members tm
            JOIN users u ON u.id = tm.user_id
            WHERE tm.team_id = :team_id
        """),
        {"team_id": team_id},
    )

    return {
        **dict(row),
        "members": [dict(r) for r in members.mappings().all()],
    }


@router.put("/{team_id}")
async def update_team(
    team_id: UUID,
    name: Optional[str] = None,
    description: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    team = await db.execute(
        text("SELECT owner_id FROM teams WHERE id = :id"),
        {"id": team_id},
    )
    team_row = team.mappings().first()
    if not team_row:
        raise HTTPException(404, "Team not found")

    require_owner_or_admin(current_user, team_row["owner_id"])

    sets = []
    params: dict = {"id": team_id}
    if name is not None:
        sets.append("name = :name")
        params["name"] = name
    if description is not None:
        sets.append("description = :description")
        params["description"] = description

    if not sets:
        raise HTTPException(400, "No fields to update")

    result = await db.execute(
        text(f"UPDATE teams SET {', '.join(sets)} WHERE id = :id RETURNING id, name, description, owner_id, created_at"),
        params,
    )
    await db.commit()
    return dict(result.mappings().first())


@router.delete("/{team_id}")
async def delete_team(
    team_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    team = await db.execute(
        text("SELECT owner_id FROM teams WHERE id = :id"),
        {"id": team_id},
    )
    team_row = team.mappings().first()
    if not team_row:
        raise HTTPException(404, "Team not found")

    if str(team_row["owner_id"]) != str(current_user["id"]):
        require_admin(current_user)

    await db.execute(
        text("DELETE FROM teams WHERE id = :id"),
        {"id": team_id},
    )
    await db.commit()
    return {"message": "Team deleted"}


@router.post("/{team_id}/members")
async def add_team_member(
    team_id: UUID,
    user_id: str,
    role: str = "member",
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    team = await db.execute(
        text("SELECT owner_id FROM teams WHERE id = :id"),
        {"id": team_id},
    )
    team_row = team.mappings().first()
    if not team_row:
        raise HTTPException(404, "Team not found")

    require_owner_or_admin(current_user, team_row["owner_id"])

    result = await db.execute(
        text("""
            INSERT INTO team_members (id, team_id, user_id, role)
            VALUES (gen_random_uuid(), :team_id, :user_id, :role)
            RETURNING id, team_id, user_id, role
        """),
        {"team_id": team_id, "user_id": user_id, "role": role},
    )
    await db.commit()
    return dict(result.mappings().first())


@router.delete("/{team_id}/members/{member_user_id}")
async def remove_team_member(
    team_id: UUID,
    member_user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    team = await db.execute(
        text("SELECT owner_id FROM teams WHERE id = :id"),
        {"id": team_id},
    )
    team_row = team.mappings().first()
    if not team_row:
        raise HTTPException(404, "Team not found")

    require_owner_or_admin(current_user, team_row["owner_id"])

    result = await db.execute(
        text("DELETE FROM team_members WHERE team_id = :team_id AND user_id = :user_id RETURNING id"),
        {"team_id": team_id, "user_id": member_user_id},
    )
    await db.commit()
    if not result.rowcount:
        raise HTTPException(404, "Member not found")
    return {"message": "Member removed"}
