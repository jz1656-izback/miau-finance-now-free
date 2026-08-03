"""Dashboard API — aggregated market overview, portfolio summary, quick stats."""
import logging
from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard")
async def get_dashboard(user: dict = Depends(get_current_user)):
    """Aggregated dashboard data for the terminal dashboard command."""
    from app.services.data.providers.registry import get_provider

    indices = ["^GSPC", "^IXIC", "^DJI", "^FTSE", "^N225", "^HSI", "DAX"]
    provider = get_provider("market")
    quotes = {}

    for sym in indices:
        try:
            q = await provider.get_quote(sym) if hasattr(provider, "get_quote") else None
            if q:
                quotes[sym] = {
                    "price": q.get("price"),
                    "change_pct": q.get("change_pct"),
                    "name": q.get("name", sym),
                }
            else:
                quotes[sym] = {"price": None, "change_pct": None, "name": sym}
        except Exception:
            quotes[sym] = {"price": None, "change_pct": None, "name": sym}

    return {
        "indices": quotes,
        "user_id": user.get("sub"),
    }
