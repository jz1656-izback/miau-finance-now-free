from pydantic import BaseModel, field_validator
from typing import Optional, Any
from uuid import UUID
from datetime import datetime
from app.schemas.validators import safe_string_validator


class OntologyTypeCreate(BaseModel):
    name: str
    display_name: str
    description: Optional[str] = None
    namespace: str = "default"
    icon: str = "database"
    color: str = "#6366f1"
    config: dict = {}
    is_abstract: bool = False

    _validate_name = field_validator("name")(safe_string_validator)
    _validate_display_name = field_validator("display_name")(safe_string_validator)
    _validate_description = field_validator("description")(safe_string_validator)
    _validate_namespace = field_validator("namespace")(safe_string_validator)


class OntologyType(OntologyTypeCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OntologyPropertyCreate(BaseModel):
    type_id: UUID
    name: str
    display_name: str
    description: Optional[str] = None
    data_type: str = "string"
    is_required: bool = False
    is_unique: bool = False
    is_searchable: bool = False
    is_faceted: bool = False
    default_value: Optional[str] = None
    validation_rules: dict = {}
    ui_config: dict = {}
    sort_order: int = 0

    _validate_name = field_validator("name")(safe_string_validator)
    _validate_display_name = field_validator("display_name")(safe_string_validator)
    _validate_description = field_validator("description")(safe_string_validator)


class OntologyProperty(OntologyPropertyCreate):
    id: UUID

    class Config:
        from_attributes = True


class OntologyLinkCreate(BaseModel):
    name: str
    display_name: str
    description: Optional[str] = None
    source_type_id: UUID
    target_type_id: UUID
    link_type: str = "many_to_many"
    reverse_name: Optional[str] = None
    cardinality: str = "ONE_TO_MANY"

    _validate_name = field_validator("name")(safe_string_validator)
    _validate_display_name = field_validator("display_name")(safe_string_validator)
    _validate_description = field_validator("description")(safe_string_validator)


class OntologyLink(OntologyLinkCreate):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class OntologyObjectCreate(BaseModel):
    type_id: UUID
    display_name: str
    description: Optional[str] = None
    properties: dict = {}
    status: str = "active"
    tags: list[str] = []
    created_by: Optional[str] = None

    _validate_display_name = field_validator("display_name")(safe_string_validator)
    _validate_description = field_validator("description")(safe_string_validator)
    _validate_created_by = field_validator("created_by")(safe_string_validator)


class OntologyObjectUpdate(BaseModel):
    display_name: Optional[str] = None
    description: Optional[str] = None
    properties: Optional[dict] = None
    status: Optional[str] = None
    tags: Optional[list[str]] = None

    _validate_display_name = field_validator("display_name")(safe_string_validator)
    _validate_description = field_validator("description")(safe_string_validator)


class OntologyObject(OntologyObjectCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ObjectLinkCreate(BaseModel):
    link_id: UUID
    source_object_id: UUID
    target_object_id: UUID
    properties: dict = {}


class ObjectLink(BaseModel):
    id: UUID
    link_id: UUID
    source_object_id: UUID
    target_object_id: UUID
    properties: dict
    created_at: datetime
    link: Optional[OntologyLink] = None
    source_object: Optional[OntologyObject] = None
    target_object: Optional[OntologyObject] = None

    class Config:
        from_attributes = True
