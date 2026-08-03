from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class OntologyType(Base):
    __tablename__ = 'ontology_types'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    display_name = Column(String(255), nullable=False)
    description = Column(Text)
    namespace = Column(String(255), server_default=text("'default'"))
    icon = Column(String(64), server_default=text("'database'"))
    color = Column(String(7), server_default=text("'#6366f1'"))
    config = Column(JSON, server_default=text("'{}'"))
    is_abstract = Column(Boolean, server_default=text('FALSE'))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    properties = relationship('OntologyProperty', back_populates='type_', cascade='all, delete-orphan')
    objects = relationship('OntologyObject', back_populates='type_', cascade='all, delete-orphan')


class OntologyProperty(Base):
    __tablename__ = 'ontology_properties'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_id = Column(UUID(as_uuid=True), ForeignKey('ontology_types.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=False)
    description = Column(Text)
    data_type = Column(String(64), nullable=False)
    is_required = Column(Boolean, server_default=text('FALSE'))
    is_unique = Column(Boolean, server_default=text('FALSE'))
    is_searchable = Column(Boolean, server_default=text('FALSE'))
    is_faceted = Column(Boolean, server_default=text('FALSE'))
    default_value = Column(Text)
    validation_rules = Column(JSON, server_default=text("'{}'"))
    ui_config = Column(JSON, server_default=text("'{}'"))
    sort_order = Column(Integer, server_default=text('0'))

    type_ = relationship('OntologyType', back_populates='properties')

    __table_args__ = (
        UniqueConstraint('type_id', 'name', name='uq_ontology_properties_type_name'),
    )


class OntologyLink(Base):
    __tablename__ = 'ontology_links'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    display_name = Column(String(255), nullable=False)
    description = Column(Text)
    source_type_id = Column(UUID(as_uuid=True), ForeignKey('ontology_types.id', ondelete='CASCADE'), nullable=False)
    target_type_id = Column(UUID(as_uuid=True), ForeignKey('ontology_types.id', ondelete='CASCADE'), nullable=False)
    link_type = Column(String(64), server_default=text("'many_to_many'"))
    reverse_name = Column(String(255))
    cardinality = Column(String(32), server_default=text("'ONE_TO_MANY'"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    source_type = relationship('OntologyType', foreign_keys=[source_type_id])
    target_type = relationship('OntologyType', foreign_keys=[target_type_id])


class OntologyObject(Base):
    __tablename__ = 'ontology_objects'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_id = Column(UUID(as_uuid=True), ForeignKey('ontology_types.id', ondelete='CASCADE'), nullable=False)
    display_name = Column(String(500), nullable=False)
    description = Column(Text)
    properties = Column(JSON, server_default=text("'{}'"))
    status = Column(String(64), server_default=text("'active'"))
    tags = Column(ARRAY(String), server_default=text("'{}'"))
    created_by = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    type_ = relationship('OntologyType', back_populates='objects')

    __table_args__ = (
        Index('idx_ontology_objects_type', 'type_id'),
        Index('idx_ontology_objects_status', 'status'),
    )


class OntologyObjectLink(Base):
    __tablename__ = 'ontology_object_links'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    link_id = Column(UUID(as_uuid=True), ForeignKey('ontology_links.id', ondelete='CASCADE'), nullable=False)
    source_object_id = Column(UUID(as_uuid=True), ForeignKey('ontology_objects.id', ondelete='CASCADE'), nullable=False)
    target_object_id = Column(UUID(as_uuid=True), ForeignKey('ontology_objects.id', ondelete='CASCADE'), nullable=False)
    properties = Column(JSON, server_default=text("'{}'"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        UniqueConstraint('link_id', 'source_object_id', 'target_object_id', name='uq_object_links'),
        Index('idx_object_links_source', 'source_object_id'),
        Index('idx_object_links_target', 'target_object_id'),
    )
