from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class SocialActivity(Base):
    __tablename__ = 'social_activities'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    action_type = Column(String(64), nullable=False)
    resource_type = Column(String(64), nullable=False)
    resource_id = Column(String(255))
    details = Column(JSON, server_default=text("'{}'"))
    visibility = Column(String(32), server_default=text("'public'"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_social_user', 'user_id'),
        Index('idx_social_created', 'created_at'),
        Index('idx_social_action', 'action_type'),
    )


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id = Column(UUID(as_uuid=True), ForeignKey('social_activities.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('comments.id', ondelete='CASCADE'))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_comments_activity', 'activity_id'),
    )


class Follow(Base):
    __tablename__ = 'follows'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    follower_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    followed_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        UniqueConstraint('follower_id', 'followed_id', name='uq_follows_pair'),
        Index('idx_follow_follower', 'follower_id'),
        Index('idx_follow_followed', 'followed_id'),
    )
