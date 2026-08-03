from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from typing import Optional
import bcrypt
from app.database import get_db
from app.middleware.auth import get_current_user

router = APIRouter()


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"


class UpdateUserRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None


def require_admin(user: dict):
    if user.get("role") not in ("admin",):
        raise HTTPException(403, "Admin access required")


def get_user_id(user: dict) -> str:
    return user.get("id", "")


@router.post("")
async def create_user(
    body: CreateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    require_admin(current_user)
    password_hash = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()
    user_id = uuid4()
    result = await db.execute(
        text("""
            INSERT INTO users (id, username, email, password_hash, role)
            VALUES (:id, :username, :email, :password_hash, :role)
            RETURNING id, username, email, role, created_at, updated_at
        """),
        {"id": user_id, "username": body.username, "email": body.email, "password_hash": password_hash, "role": body.role},
    )
    await db.commit()
    row = result.mappings().first()
    return dict(row)


@router.get("")
async def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    require_admin(current_user)
    offset = (page - 1) * per_page
    result = await db.execute(
        text("SELECT id, username, email, role, created_at, updated_at FROM users ORDER BY created_at DESC LIMIT :limit OFFSET :offset"),
        {"limit": per_page, "offset": offset},
    )
    rows = [dict(r) for r in result.mappings().all()]

    count_result = await db.execute(text("SELECT COUNT(*) FROM users"))
    total = count_result.scalar()

    return {"items": rows, "total": total, "page": page, "per_page": per_page}


@router.get("/{user_id}")
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(
        text("SELECT id, username, email, role, created_at, updated_at FROM users WHERE id = :id"),
        {"id": user_id},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(404, "User not found")
    return dict(row)


@router.put("/{user_id}")
async def update_user(
    user_id: UUID,
    body: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_identifier = get_user_id(current_user)
    if str(user_id) != user_identifier:
        require_admin(current_user)

    sets = []
    params: dict = {"id": user_id}
    if body.username is not None:
        sets.append("username = :username")
        params["username"] = body.username
    if body.email is not None:
        sets.append("email = :email")
        params["email"] = body.email
    if body.password is not None:
        sets.append("password_hash = :password_hash")
        params["password_hash"] = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()
    if body.role is not None:
        require_admin(current_user)
        sets.append("role = :role")
        params["role"] = body.role

    if not sets:
        raise HTTPException(400, "No fields to update")

    sets.append("updated_at = NOW()")
    set_clause = ", ".join(sets)

    result = await db.execute(
        text(f"UPDATE users SET {set_clause} WHERE id = :id RETURNING id, username, email, role, created_at, updated_at"),
        params,
    )
    await db.commit()
    row = result.mappings().first()
    if not row:
        raise HTTPException(404, "User not found")
    return dict(row)


@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    require_admin(current_user)
    result = await db.execute(
        text("DELETE FROM users WHERE id = :id RETURNING id"),
        {"id": user_id},
    )
    await db.commit()
    if not result.rowcount:
        raise HTTPException(404, "User not found")
    return {"message": "User deleted"}


@router.get("/{user_id}/followers")
async def get_followers(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(
        text("""
            SELECT u.id, u.username, f.created_at as followed_since
            FROM follows f
            JOIN users u ON u.id = f.follower_id
            WHERE f.followed_id = :uid
            ORDER BY f.created_at DESC
        """),
        {"uid": user_id},
    )
    return {"followers": [dict(r) for r in result.mappings().all()]}


@router.get("/{user_id}/following")
async def get_following(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(
        text("""
            SELECT u.id, u.username, f.created_at as followed_since
            FROM follows f
            JOIN users u ON u.id = f.followed_id
            WHERE f.follower_id = :uid
            ORDER BY f.created_at DESC
        """),
        {"uid": user_id},
    )
    return {"following": [dict(r) for r in result.mappings().all()]}
