from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ShareCreate(BaseModel):
    portfolio_id: str
    is_public: bool = True
    expires_at: Optional[datetime] = None


class ShareResponse(BaseModel):
    id: str
    portfolio_id: str
    share_token: str
    is_public: bool
    share_url: str
    expires_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


class ActivityCreate(BaseModel):
    action_type: str
    resource_type: str
    resource_id: Optional[str] = None
    details: Optional[dict] = None
    visibility: str = "public"


class ActivityResponse(BaseModel):
    id: str
    user_id: str
    username: Optional[str] = None
    action_type: str
    resource_type: str
    resource_id: Optional[str] = None
    details: Optional[dict] = None
    message: Optional[str] = None
    comment_count: int = 0
    created_at: Optional[str] = None


class CommentCreate(BaseModel):
    text: str
    parent_id: Optional[str] = None


class CommentResponse(BaseModel):
    id: str
    activity_id: str
    user_id: str
    username: Optional[str] = None
    text: str
    parent_id: Optional[str] = None
    created_at: Optional[str] = None


class FollowResponse(BaseModel):
    follower_id: str
    followed_id: str
    created_at: Optional[str] = None
