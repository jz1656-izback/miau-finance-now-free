from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"
    readonly = "readonly"

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole, name='user_role', create_constraint=False), nullable=False, server_default=text("'user'"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    teams_owned = relationship('Team', foreign_keys='Team.owner_id', back_populates='owner')
    team_memberships = relationship('TeamMember', back_populates='user')
    workspace_memberships = relationship('WorkspaceMember', back_populates='user')

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'role': self.role.value if self.role else 'user',
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None,
        }

class Team(Base):
    __tablename__ = 'teams'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    owner = relationship('User', foreign_keys=[owner_id])
    members = relationship('TeamMember', back_populates='team', cascade='all, delete-orphan')
    workspaces = relationship('Workspace', back_populates='team', cascade='all, delete-orphan')

class TeamMember(Base):
    __tablename__ = 'team_members'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role = Column(String(32), nullable=False, server_default=text("'member'"))

    team = relationship('Team', back_populates='members')
    user = relationship('User')

    __table_args__ = (
        UniqueConstraint('team_id', 'user_id', name='uq_team_members_team_user'),
    )

class Workspace(Base):
    __tablename__ = 'workspaces'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    team = relationship('Team', back_populates='workspaces')
    members = relationship('WorkspaceMember', back_populates='workspace', cascade='all, delete-orphan')

class ActivityLog(Base):
    __tablename__ = 'activity_logs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'), nullable=True)
    action = Column(String(64), nullable=False)
    resource_type = Column(String(64), nullable=False)
    resource_id = Column(String(255), nullable=True)
    details = Column(JSON, server_default=text("'{}'"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_activity_user', 'user_id'),
        Index('idx_activity_workspace', 'workspace_id'),
        Index('idx_activity_created', 'created_at'),
    )

class PortfolioShare(Base):
    __tablename__ = 'portfolio_shares'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolios.id', ondelete='CASCADE'), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    shared_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        UniqueConstraint('portfolio_id', 'workspace_id', name='uq_portfolio_shares'),
    )

class WorkspaceMember(Base):
    __tablename__ = 'workspace_members'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role = Column(String(32), nullable=False, server_default=text("'member'"))

    workspace = relationship('Workspace', back_populates='members')
    user = relationship('User')

    __table_args__ = (
        UniqueConstraint('workspace_id', 'user_id', name='uq_workspace_members_workspace_user'),
    )
