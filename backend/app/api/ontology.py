from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from app.database import get_db
from app.services import ontology_service
from app.schemas.ontology import (
    OntologyType, OntologyTypeCreate,
    OntologyProperty, OntologyPropertyCreate,
    OntologyLink, OntologyLinkCreate,
    OntologyObject, OntologyObjectCreate, OntologyObjectUpdate,
    ObjectLink, ObjectLinkCreate,
)
from sqlalchemy import text

router = APIRouter()


@router.get("/types")
async def list_types(
    namespace: Optional[str] = Query(None, pattern=r"^[\w\-]{0,50}$", max_length=50),
    db: AsyncSession = Depends(get_db),
):
    return await ontology_service.get_types(db, namespace)


@router.get("/types/{type_id}")
async def get_type(type_id: UUID, db: AsyncSession = Depends(get_db)):
    t = await ontology_service.get_type(db, type_id)
    if not t:
        raise HTTPException(404, "Type not found")
    props = await ontology_service.get_properties(db, type_id)
    links = await ontology_service.get_links(db, type_id)
    return {**t, "properties": props, "links": links}


@router.get("/types/{type_id}/properties")
async def list_properties(type_id: UUID, db: AsyncSession = Depends(get_db)):
    return await ontology_service.get_properties(db, type_id)


@router.get("/links")
async def list_links(
    type_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
):
    return await ontology_service.get_links(db, type_id)


@router.get("/objects")
async def list_objects(
    type_id: Optional[UUID] = None,
    search: Optional[str] = Query(None, pattern=r"^[\w\s\-_.]{0,200}$", max_length=200),
    status: Optional[str] = Query(None, pattern=r"^[\w\-]{0,50}$", max_length=50),
    tags: Optional[str] = Query(None, pattern=r"^[\w\-,]{0,200}$", max_length=200),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    tag_list = tags.split(",") if tags else None
    return await ontology_service.get_objects(db, type_id, search, status, tag_list, limit, offset)


@router.get("/objects/{object_id}")
async def get_object(object_id: UUID, db: AsyncSession = Depends(get_db)):
    obj = await ontology_service.get_object(db, object_id)
    if not obj:
        raise HTTPException(404, "Object not found")
    links = await ontology_service.get_object_links(db, object_id)
    return {**obj, "links": links}


@router.get("/objects/{object_id}/links")
async def get_object_links(object_id: UUID, db: AsyncSession = Depends(get_db)):
    return await ontology_service.get_object_links(db, object_id)


@router.post("/objects")
async def create_object(data: OntologyObjectCreate, db: AsyncSession = Depends(get_db)):
    obj = await ontology_service.create_object(
        db, data.type_id, data.display_name, data.properties,
        data.description or "", data.status, data.tags, data.created_by,
    )
    return obj


@router.put("/objects/{object_id}")
async def update_object(object_id: UUID, data: OntologyObjectUpdate, db: AsyncSession = Depends(get_db)):
    obj = await ontology_service.update_object(
        db, object_id, data.model_dump(exclude_none=True),
    )
    if not obj:
        raise HTTPException(404, "Object not found")
    return obj


@router.post("/links")
async def create_link(data: ObjectLinkCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            INSERT INTO ontology_object_links (link_id, source_object_id, target_object_id, properties)
            VALUES (:link_id, :source_id, :target_id, :properties)
            RETURNING *
        """),
        {
            "link_id": data.link_id,
            "source_id": data.source_object_id,
            "target_id": data.target_object_id,
            "properties": data.properties,
        },
    )
    await db.commit()
    row = result.mappings().first()
    return dict(row)
