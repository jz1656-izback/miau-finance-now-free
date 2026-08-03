from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class AuditLog(Base):
    __tablename__ = 'audit_log'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_id = Column(UUID(as_uuid=True), ForeignKey('ontology_objects.id', ondelete='CASCADE'), nullable=False)
    action = Column(String(32), nullable=False)
    user_id = Column(String(255))
    changes = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))


class DataLineage(Base):
    __tablename__ = 'data_lineage'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_system = Column(String(128), nullable=False)
    source_id = Column(String(255), nullable=False)
    target_table = Column(String(128), nullable=False)
    target_id = Column(UUID(as_uuid=True), nullable=False)
    operation = Column(String(32), nullable=False)
    metadata_ = Column('metadata', JSON, server_default=text("'{}'"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
