from pydantic import BaseModel
from typing import Optional
from app.models import UserRole


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.user


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None


class TeamCreate(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: str


class TeamResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    owner_id: str
    created_at: Optional[str] = None

    model_config = {"from_attributes": True}


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TeamMemberCreate(BaseModel):
    user_id: str
    role: str = "member"


class TeamMemberResponse(BaseModel):
    id: str
    team_id: str
    user_id: str
    role: str

    model_config = {"from_attributes": True}


class WorkspaceCreate(BaseModel):
    name: str
    team_id: str


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    team_id: str
    created_at: Optional[str] = None

    model_config = {"from_attributes": True}


class WorkspaceMemberCreate(BaseModel):
    user_id: str
    role: str = "member"


class WorkspaceMemberResponse(BaseModel):
    id: str
    workspace_id: str
    user_id: str
    role: str

    model_config = {"from_attributes": True}
