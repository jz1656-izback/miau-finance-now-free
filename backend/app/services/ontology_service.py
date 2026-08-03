from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
import logging

logger = logging.getLogger(__name__)


async def get_types(db: AsyncSession, namespace: Optional[str] = None):
    if namespace:
        result = await db.execute(
            text("SELECT * FROM ontology_types WHERE namespace = :ns ORDER BY display_name"),
            {"ns": namespace},
        )
    else:
        result = await db.execute(
            text("SELECT * FROM ontology_types ORDER BY display_name")
        )
    rows = result.mappings().all()
    return [dict(row) for row in rows]


async def get_type(db: AsyncSession, type_id: UUID):
    result = await db.execute(
        text("SELECT * FROM ontology_types WHERE id = :id"), {"id": type_id}
    )
    row = result.mappings().first()
    return dict(row) if row else None


async def get_properties(db: AsyncSession, type_id: UUID):
    result = await db.execute(
        text("SELECT * FROM ontology_properties WHERE type_id = :tid ORDER BY sort_order"),
        {"tid": type_id},
    )
    return [dict(row) for row in result.mappings().all()]


async def get_links(db: AsyncSession, type_id: Optional[UUID] = None):
    if type_id:
        result = await db.execute(
            text("""
                SELECT l.*, st.display_name as source_type_name, tt.display_name as target_type_name
                FROM ontology_links l
                JOIN ontology_types st ON l.source_type_id = st.id
                JOIN ontology_types tt ON l.target_type_id = tt.id
                WHERE l.source_type_id = :tid OR l.target_type_id = :tid
                ORDER BY l.display_name
            """),
            {"tid": type_id},
        )
    else:
        result = await db.execute(
            text("""
                SELECT l.*, st.display_name as source_type_name, tt.display_name as target_type_name
                FROM ontology_links l
                JOIN ontology_types st ON l.source_type_id = st.id
                JOIN ontology_types tt ON l.target_type_id = tt.id
                ORDER BY l.display_name
            """),
        )
    return [dict(row) for row in result.mappings().all()]


async def get_objects(
    db: AsyncSession,
    type_id: Optional[UUID] = None,
    search: Optional[str] = None,
    status: Optional[str] = None,
    tags: Optional[list[str]] = None,
    limit: int = 100,
    offset: int = 0,
):
    conditions = []
    params = {"limit": limit, "offset": offset}

    if type_id:
        conditions.append("o.type_id = :type_id")
        params["type_id"] = type_id
    if status:
        conditions.append("o.status = :status")
        params["status"] = status
    if search:
        conditions.append("o.display_name ILIKE :search")
        params["search"] = f"%{search}%"
    if tags:
        conditions.append("o.tags && :tags")
        params["tags"] = tags

    where = " AND ".join(conditions) if conditions else "TRUE"

    query = text(f"""
        SELECT o.*, t.display_name as type_name, t.icon as type_icon, t.color as type_color
        FROM ontology_objects o
        JOIN ontology_types t ON o.type_id = t.id
        WHERE {where}
        ORDER BY o.updated_at DESC
        LIMIT :limit OFFSET :offset
    """)

    result = await db.execute(query, params)
    return [dict(row) for row in result.mappings().all()]


async def get_object(db: AsyncSession, object_id: UUID):
    result = await db.execute(
        text("""
            SELECT o.*, t.display_name as type_name, t.icon as type_icon, t.color as type_color
            FROM ontology_objects o
            JOIN ontology_types t ON o.type_id = t.id
            WHERE o.id = :id
        """),
        {"id": object_id},
    )
    row = result.mappings().first()
    return dict(row) if row else None


async def get_object_links(db: AsyncSession, object_id: UUID):
    result = await db.execute(
        text("""
            SELECT ol.*, l.name as link_name, l.display_name as link_display_name,
                   l.reverse_name, l.cardinality,
                   src.display_name as source_name, src.type_id as source_type_id,
                   tgt.display_name as target_name, tgt.type_id as target_type_id,
                   st.display_name as source_type_name,
                   tt.display_name as target_type_name
            FROM ontology_object_links ol
            JOIN ontology_links l ON ol.link_id = l.id
            JOIN ontology_objects src ON ol.source_object_id = src.id
            JOIN ontology_objects tgt ON ol.target_object_id = tgt.id
            JOIN ontology_types st ON src.type_id = st.id
            JOIN ontology_types tt ON tgt.type_id = tt.id
            WHERE ol.source_object_id = :oid OR ol.target_object_id = :oid
            ORDER BY l.display_name
        """),
        {"oid": object_id},
    )
    return [dict(row) for row in result.mappings().all()]


async def search_objects(
    db: AsyncSession,
    query_str: str,
    type_filter: Optional[str] = None,
    limit: int = 50,
):
    params = {"query": f"%{query_str}%", "limit": limit}
    type_join = ""
    if type_filter:
        params["type_filter"] = type_filter
        type_join = "AND t.name = :type_filter"

    result = await db.execute(
        text(f"""
            SELECT o.id, o.display_name, o.description,
                   t.name as type_name, t.display_name as type_display_name,
                   t.icon as type_icon, t.color as type_color,
                   ts_rank(to_tsvector('simple', o.display_name), plainto_tsquery('simple', :query_str)) as rank
            FROM ontology_objects o
            JOIN ontology_types t ON o.type_id = t.id
            WHERE (o.display_name ILIKE :query OR o.description ILIKE :query OR o.properties::text ILIKE :query)
            {type_join}
            ORDER BY rank DESC, o.display_name ASC
            LIMIT :limit
        """),
        {"query_str": query_str, **params},
    )
    return [dict(row) for row in result.mappings().all()]


async def create_object(db: AsyncSession, type_id: UUID, display_name: str, properties: dict,
                        description: str = "", status: str = "active", tags: list = None,
                        created_by: str = None):
    result = await db.execute(
        text("""
            INSERT INTO ontology_objects (type_id, display_name, description, properties, status, tags, created_by)
            VALUES (:type_id, :display_name, :description, :properties, :status, :tags, :created_by)
            RETURNING *
        """),
        {
            "type_id": type_id,
            "display_name": display_name,
            "description": description,
            "properties": properties,
            "status": status,
            "tags": tags or [],
            "created_by": created_by,
        },
    )
    await db.commit()
    row = result.mappings().first()
    return dict(row) if row else None


async def update_object(db: AsyncSession, object_id: UUID, updates: dict):
    # Whitelist allowed fields for update
    ALLOWED_FIELDS = {"display_name", "description", "properties", "status", "tags"}
    
    sets = []
    params = {"id": object_id}
    for key, val in updates.items():
        if key in ALLOWED_FIELDS and val is not None:
            sets.append(f"{key} = :{key}")
            params[key] = val
        elif key not in ALLOWED_FIELDS:
            logger.warning(f"Ignored unauthorized update field: {key}")

    if not sets:
        return await get_object(db, object_id)

    sets.append("updated_at = NOW()")
    result = await db.execute(
        text(f"UPDATE ontology_objects SET {', '.join(sets)} WHERE id = :id RETURNING *"),
        params,
    )
    await db.commit()
    row = result.mappings().first()
    return dict(row) if row else None
