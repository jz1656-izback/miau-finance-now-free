"""Plugin registry + marketplace API — list, install, remove, info."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.middleware.auth import get_current_user
from app.middleware.rbac import get_current_user_db
from app.services.plugin.loader import discover_plugins, get_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/plugins", tags=["Plugins"])


@router.get("")
async def list_plugins(
    user: dict = Depends(get_current_user),
):
    """List all available plugins (discovered + loaded)."""
    discovered = discover_plugins()
    manager = get_manager()
    loaded_names = {p["name"] for p in manager.loaded_plugins}

    plugins = []
    for meta in discovered:
        plugins.append({
            **meta,
            "loaded": meta.get("name", "") in loaded_names,
        })

    for p in manager.loaded_plugins:
        if not any(d.get("name") == p["name"] for d in discovered):
            plugins.append({**p, "loaded": True, "path": ""})

    return {"plugins": plugins, "count": len(plugins)}


@router.get("/{name}")
async def get_plugin_info(
    name: str,
    user: dict = Depends(get_current_user),
):
    """Get detailed info about a specific plugin."""
    manager = get_manager()
    for p in manager.loaded_plugins:
        if p["name"] == name:
            return {**p, "loaded": True, "hook_points": list(manager._hook_registry.keys()) if hasattr(manager, '_hook_registry') else []}

    discovered = discover_plugins()
    for meta in discovered:
        if meta.get("name") == name:
            return {**meta, "loaded": False}

    raise HTTPException(404, f"Plugin not found: {name}")


@router.post("/{name}/load")
async def load_plugin(
    name: str,
    user: dict = Depends(get_current_user_db),
):
    """Load and initialize a plugin."""
    if user.get("role") not in ("admin",):
        raise HTTPException(403, "Admin access required")

    manager = get_manager()
    try:
        result = await manager.load(name)
        return result
    except Exception as e:
        raise HTTPException(400, f"Failed to load plugin '{name}': {e}")


@router.post("/{name}/unload")
async def unload_plugin(
    name: str,
    user: dict = Depends(get_current_user_db),
):
    """Unload a plugin."""
    if user.get("role") not in ("admin",):
        raise HTTPException(403, "Admin access required")

    manager = get_manager()
    result = await manager.unload(name)
    return result


@router.get("/loaded")
async def list_loaded_plugins(
    user: dict = Depends(get_current_user),
):
    """List currently loaded plugins."""
    manager = get_manager()
    return {"loaded": manager.loaded_plugins, "count": len(manager.loaded_plugins)}
