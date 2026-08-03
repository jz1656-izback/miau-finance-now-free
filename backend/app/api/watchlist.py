from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database import get_db
from app.middleware.auth import get_current_user

router = APIRouter()


@router.get("")
async def list_watchlists(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = user.get("sub", "default")
    result = await db.execute(
        text("""
            SELECT w.id, w.name, w.created_at,
                   COUNT(wi.id) AS item_count
            FROM watchlists w
            LEFT JOIN watchlist_items wi ON wi.watchlist_id = w.id
            WHERE w.user_id = :user_id
            GROUP BY w.id, w.name, w.created_at
            ORDER BY w.created_at DESC
        """),
        {"user_id": user_id},
    )
    rows = result.fetchall()
    return {
        "watchlists": [
            {
                "id": str(r[0]),
                "name": r[1],
                "created_at": r[2].isoformat() if r[2] else None,
                "item_count": r[3],
            }
            for r in rows
        ]
    }


@router.post("")
async def create_watchlist(
    name: str = Query("Default", min_length=1, max_length=100, pattern=r"^[\w\s\-]{1,100}$"),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = user.get("sub", "default")
    result = await db.execute(
        text("INSERT INTO watchlists (user_id, name) VALUES (:user_id, :name) RETURNING id, name"),
        {"user_id": user_id, "name": name},
    )
    row = result.fetchone()
    await db.commit()
    return {"id": str(row[0]), "name": row[1]}


@router.get("/items")
async def list_watchlist_items(
    watchlist_id: Optional[str] = Query(None),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = user.get("sub", "default")
    if watchlist_id:
        result = await db.execute(
            text("""
                SELECT wi.id, wi.ticker, wi.added_at, wi.notes
                FROM watchlist_items wi
                JOIN watchlists w ON w.id = wi.watchlist_id
                WHERE wi.watchlist_id = :wid AND w.user_id = :user_id
                ORDER BY wi.added_at DESC
            """),
            {"wid": watchlist_id, "user_id": user_id},
        )
    else:
        result = await db.execute(
            text("""
                SELECT wi.id, wi.ticker, wi.added_at, wi.notes
                FROM watchlist_items wi
                JOIN watchlists w ON w.id = wi.watchlist_id
                WHERE w.user_id = :user_id
                ORDER BY wi.added_at DESC
            """),
            {"user_id": user_id},
        )
    rows = result.fetchall()
    return {
        "items": [
            {
                "id": str(r[0]),
                "ticker": r[1],
                "added_at": r[2].isoformat() if r[2] else None,
                "notes": r[3] or "",
            }
            for r in rows
        ]
    }


@router.post("/items")
async def add_watchlist_item(
    ticker: str = Query(..., min_length=1, max_length=10, pattern=r"^[A-Za-z0-9.]{1,10}$"),
    notes: str = Query("", max_length=500),
    watchlist_id: Optional[str] = Query(None),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = user.get("sub", "default")
    ticker = ticker.upper()

    # Get or create default watchlist
    if not watchlist_id:
        wl_result = await db.execute(
            text("SELECT id FROM watchlists WHERE user_id = :user_id ORDER BY created_at ASC LIMIT 1"),
            {"user_id": user_id},
        )
        wl_row = wl_result.fetchone()
        if wl_row:
            watchlist_id = str(wl_row[0])
        else:
            wl_result = await db.execute(
                text("INSERT INTO watchlists (user_id) VALUES (:user_id) RETURNING id"),
                {"user_id": user_id},
            )
            watchlist_id = str(wl_result.fetchone()[0])
            await db.commit()

    # Check if already exists
    existing = await db.execute(
        text("SELECT id FROM watchlist_items WHERE watchlist_id = :wid AND ticker = :ticker"),
        {"wid": watchlist_id, "ticker": ticker},
    )
    if existing.fetchone():
        raise HTTPException(status_code=409, detail=f"{ticker} already in watchlist")

    result = await db.execute(
        text("""
            INSERT INTO watchlist_items (watchlist_id, ticker, notes)
            VALUES (:wid, :ticker, :notes)
            RETURNING id, ticker, added_at
        """),
        {"wid": watchlist_id, "ticker": ticker, "notes": notes},
    )
    row = result.fetchone()
    await db.commit()
    return {
        "id": str(row[0]),
        "ticker": row[1],
        "added_at": row[2].isoformat() if row[2] else None,
        "message": f"Added {ticker} to watchlist",
    }


@router.delete("/items/{item_id}")
async def remove_watchlist_item(
    item_id: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = user.get("sub", "default")
    result = await db.execute(
        text("""
            DELETE FROM watchlist_items wi
            USING watchlists w
            WHERE wi.id = :item_id
              AND wi.watchlist_id = w.id
              AND w.user_id = :user_id
            RETURNING wi.ticker
        """),
        {"item_id": item_id, "user_id": user_id},
    )
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.commit()
    return {"message": f"Removed {row[0]} from watchlist"}


@router.delete("/items")
async def remove_watchlist_item_by_ticker(
    ticker: str = Query(..., min_length=1, max_length=10, pattern=r"^[A-Za-z0-9.]{1,10}$"),
    watchlist_id: Optional[str] = Query(None),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = user.get("sub", "default")
    ticker = ticker.upper()

    if watchlist_id:
        result = await db.execute(
            text("""
                DELETE FROM watchlist_items wi
                USING watchlists w
                WHERE wi.ticker = :ticker
                  AND wi.watchlist_id = :wid
                  AND wi.watchlist_id = w.id
                  AND w.user_id = :user_id
                RETURNING wi.ticker
            """),
            {"ticker": ticker, "wid": watchlist_id, "user_id": user_id},
        )
    else:
        result = await db.execute(
            text("""
                DELETE FROM watchlist_items wi
                USING watchlists w
                WHERE wi.ticker = :ticker
                  AND wi.watchlist_id = w.id
                  AND w.user_id = :user_id
                RETURNING wi.ticker
            """),
            {"ticker": ticker, "user_id": user_id},
        )
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"{ticker} not found in watchlist")
    await db.commit()
    return {"message": f"Removed {row[0]} from watchlist"}
